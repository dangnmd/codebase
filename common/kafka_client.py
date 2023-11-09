import pickle
import random
import signal
import time
from copy import deepcopy
import confluent_kafka
from kafka import KafkaProducer as PythonProducer, KafkaConsumer as PythonConsumer
from kafka.errors import FailedPayloadsError, KafkaUnavailableError, \
    UnknownError, LeaderNotAvailableError, UnknownTopicOrPartitionError, \
    NotLeaderForPartitionError
from common.enum_type import EnumBase
from common.jsonutils import to_json, from_json
from common.logger import log


class MessageSendMode(EnumBase):
    ASYNC = "async"
    SYNC = "sync"


class KafkaProducerACKS(EnumBase):
    NO_WAIT = 0
    WAIT_LEADER = 1
    WAIT_ALL = -1


class KafkaLib(EnumBase):
    KAFKA_PYTHON = "kafka-python"
    CONFLUENT_KAFKA = "confluent-kafka"


class Serializer(object):
    @classmethod
    def byte_str_serializer(cls, data):
        if data is None:
            return None
        if isinstance(data, str):
            return data
        return str(data).encode("utf-8")

    @classmethod
    def json_serializer(cls, data):
        return to_json(data).encode("utf-8")

    @classmethod
    def pickle_serializer(cls, data):
        return pickle.dumps(data)


class Deserializer(object):
    @classmethod
    def identity_deserializer(cls, data):
        return data

    @classmethod
    def str_deserializer(cls, data):
        return str(data)

    @classmethod
    def int_deserializer(cls, data):
        return int(data)

    @classmethod
    def json_deserializer(cls, data):
        try:
            if type(data) == bytes:
                data = data.decode()
            return from_json(data)
        except Exception as err:
            print(f"json: cant deserialize message: {data}")
            raise err

    @classmethod
    def pickle_deserializer(cls, data):
        return pickle.loads(data)


class KafkaClientError(Exception):
    pass


class KafkaClientConnectError(KafkaClientError):
    pass


class KafkaMessage(object):
    def __init__(self, key, offset, partition, topic, value):
        self.key = key
        self.offset = offset
        self.partition = partition
        self.topic = topic
        self.value = value

    @classmethod
    def from_confluent_kafka(
            cls,
            msg,
            key_deserializer=lambda x: x,
            value_deserializer=lambda x: x,
    ):
        return cls(
            key=key_deserializer(msg.key()),
            offset=msg.offset(),
            partition=msg.partition(),
            topic=msg.topic(),
            value=value_deserializer(msg.value()),
        )


class ProducerAdapter(object):
    def __init__(self, *args, **kwargs):
        self._producer = None

    def send(self, topic, key, value, *args, **kwargs):
        raise NotImplementedError

    def flush(self, *args, **kwargs):
        return self._producer.flush(*args, **kwargs)

    def close(self, *args, **kwargs):
        if hasattr(self._producer, "close"):
            self._producer.close(*args, **kwargs)


class ConfluentAdapterMixin(object):
    @classmethod
    def _parse_config(cls, config):
        parsed_config = {
            key.replace('_', '.'): value
            for key, value in config.items()
        }

        if "bootstrap.servers" not in parsed_config:
            return parsed_config

        parsed_config["bootstrap.servers"] = ",".join(
            parsed_config["bootstrap.servers"]
        )
        return parsed_config

    @classmethod
    def _confluent_error_code(cls, name):
        return getattr(confluent_kafka.KafkaError, name)


class PythonKafkaProducerAdapter(ProducerAdapter):
    def __init__(self, config):
        super(PythonKafkaProducerAdapter, self).__init__()
        self._config = deepcopy(config)
        self._producer = PythonProducer(**self._config)

    def send(self, topic, key, value, *args, **kwargs):
        return self._producer.send(
            topic=topic, key=key, value=value, *args, **kwargs
        )


class ConfluentKafkaProducerAdapter(ProducerAdapter, ConfluentAdapterMixin):
    def __init__(self, config):
        super(ConfluentKafkaProducerAdapter, self).__init__()
        self._config = deepcopy(config)
        self._key_serializer = self._config.pop("key_serializer", lambda x: x)
        self._value_serializer = self._config.pop("value_serializer", lambda x: x)
        self._producer = confluent_kafka.Producer(
            self._parse_config(self._config)
        )

    def send(self, topic, key, value, *args, **kwargs):
        return self._producer.produce(
            topic=topic,
            key=self._key_serializer(key),
            value=self._value_serializer(value),
            *args, **kwargs
        )


class KafkaProducer(object):
    """
    Wrapper class of kafka-python and confluent-kafka Producer
    :param bootstrap_servers: list of kafka brokers
    :param kafka_lib: `kafka-python` or `confluent-kafka` lib
    :param message_send_mode: `sync` or `async`, `sync` mode is only compatible
    with `kafka-python` lib
    :param synchronous_send_timeout: (second) wait time send message synchronously
    :param key_serializer: function to serialize message key to bytes
    :type key_serializer: callable
    :param value_serializer: function to serialize message value to bytes
    :type: value_serializer: callable
    For kafka-python:
        key_serializer and value_serializer are passed into Producer class
    For confluent-kafka:
        key_serializer and value_serializer are applied to message before sending

    Other parameters are passed directly to Producer class
    (for either kafka-python or confluent-kafka)

    Example usage:
    >>> KAFKA_PRODUCER_CONFIG = {
    >>>     "bootstrap_servers": ["localhost:9092"]
    >>> }
    >>> producer = KafkaProducer(KAFKA_PRODUCER_CONFIG)
    >>> producer.send("topic", "key", "value")
    """
    _default_key_serializer = Serializer.byte_str_serializer
    _default_value_serializer = Serializer.json_serializer
    _default_acks = KafkaProducerACKS.WAIT_ALL
    _default_retries = 3
    _default_max_in_flight_requests_per_connection = 1

    _default_message_send_mode = MessageSendMode.ASYNC
    _default_synchronous_send_timeout = 10
    _default_kafka_lib = KafkaLib.KAFKA_PYTHON

    _adapter_mapping = {
        KafkaLib.KAFKA_PYTHON: PythonKafkaProducerAdapter,
        KafkaLib.CONFLUENT_KAFKA: ConfluentKafkaProducerAdapter,
    }

    def __init__(self, config, **kwargs):
        self._config = deepcopy(config)
        self._config.update(kwargs)
        assert "bootstrap_servers" in self._config, "bootstrap_servers is required"

        if "key_serializer" not in self._config:
            self._config["key_serializer"] = self._default_key_serializer
        if "value_serializer" not in self._config:
            self._config["value_serializer"] = self._default_value_serializer
        if "acks" not in self._config:
            self._config["acks"] = self._default_acks
        if "retries" not in self._config:
            self._config["retries"] = self._default_retries
        if "max_in_flight_requests_per_connection" in self._config:
            self._config["max_in_flight_requests_per_connection"] = \
                self._default_max_in_flight_requests_per_connection

        # synchronous message send config
        self._message_send_mode = self._config.pop(
            "message_send_mode", self._default_message_send_mode
        )
        assert self._message_send_mode in MessageSendMode.VALUE_TO_NAME, \
            "invalid message_send_mode"
        self._synchronous_send_timeout = self._config.pop(
            "synchronous_send_timeout", self._default_synchronous_send_timeout
        )
        self._kafka_lib = self._config.pop(
            "kafka_lib", self._default_kafka_lib
        )
        assert self._kafka_lib in KafkaLib.VALUE_TO_NAME, "invalid_kafka_lib"
        if self._kafka_lib == KafkaLib.CONFLUENT_KAFKA:
            assert self._message_send_mode == MessageSendMode.ASYNC, \
                "confluent-kafka lib does not support synchronous producer"

        self._producer = None
        self._is_connected = False

    def connect(self):
        try:
            producer_adapter = self._adapter_mapping.get(self._kafka_lib)
            self._producer = producer_adapter(self._config)
            self._is_connected = True
        except Exception as err:
            log.exception(
                "kafka_producer_failed_to_connect|config=%s,err=%s",
                self._config, err
            )
            self._is_connected = False
        return self._is_connected

    def disconnect(self):
        if not self._producer:
            return
        self._producer.flush()
        self._producer.close()
        self._producer = None
        self._is_connected = False

    def flush(self):
        return self._producer.flush()

    def reconnect(self):
        self.disconnect()
        return self.connect()

    def _send(self, topic, key, value, connect_retry=1):
        if not self._is_connected:
            if not self.connect():
                raise KafkaClientConnectError()

        while connect_retry >= 0:
            try:
                record = self._producer.send(
                    topic=topic,
                    key=key,
                    value=value,
                )
                if self._message_send_mode == MessageSendMode.SYNC:
                    record = record.get(
                        timeout=self._synchronous_send_timeout
                    )

                return record
            except Exception as err:
                if connect_retry:
                    connect_retry -= 1
                    self.reconnect()
                else:
                    raise KafkaClientError(err)

    def send(self, topic, key, value, connect_retry=1, raise_errors=True):
        try:
            return self._send(topic, key, value, connect_retry=connect_retry)
        except KafkaClientError as err:
            log.exception(
                "kafka_produce_message_exception|topic=%s,message=%s,key=%s,error=%s",
                topic, value, key, err
            )
            if raise_errors:
                raise
            return None


class ConsumerAdapter(object):
    def __init__(self, *args, **kwargs):
        self._consumer = None

    def close(self, *args, **kwargs):
        raise NotImplementedError

    def commit(self, *args, **kwargs):
        raise NotImplementedError

    def poll(self, *args, **kwargs):
        raise NotImplementedError

    def seek(self, *args, **kwargs):
        raise NotImplementedError


class ExceptionWrapper(object):
    @classmethod
    def python_kafka_wrapper(cls):
        def wrap(func):
            def _func(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except PythonKafkaConsumerAdapter.KAFKA_CONNECT_FAIL_ERRORS as err:
                    raise KafkaClientConnectError(err)
                except Exception as err:
                    raise KafkaClientError(err)

            return _func

        return wrap

    @classmethod
    def confluent_wrapper(cls):
        def wrap(func):
            def _func(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except confluent_kafka.KafkaException as err:
                    if err.args[0] in ConfluentConsumerAdapter.CONNECT_ERRORS:
                        raise KafkaClientConnectError(err)
                    else:
                        raise KafkaClientError(err)

            return _func

        return wrap


class PythonKafkaConsumerAdapter(ConsumerAdapter):
    KAFKA_CONNECT_FAIL_ERRORS = [
        FailedPayloadsError,
        KafkaUnavailableError,
        UnknownError,
        LeaderNotAvailableError,
        UnknownTopicOrPartitionError,
        NotLeaderForPartitionError,
    ]

    @ExceptionWrapper.python_kafka_wrapper()
    def __init__(self, config):
        super(PythonKafkaConsumerAdapter, self).__init__()
        self._config = deepcopy(config)
        self._consumer = PythonConsumer(**self._config)

    @ExceptionWrapper.python_kafka_wrapper()
    def close(self, *args, **kwargs):
        return self._consumer.close(*args, **kwargs)

    @ExceptionWrapper.python_kafka_wrapper()
    def commit(self, *args, **kwargs):
        return self._consumer.commit(*args, **kwargs)

    @ExceptionWrapper.python_kafka_wrapper()
    def poll(self, timeout, max_records):
        raw_messages = self._consumer.poll(
            timeout_ms=int(timeout * 1000), max_records=max_records
        )
        filtered_messages = []
        for _, messages in raw_messages.items():
            filtered_messages.extend(messages)
        return filtered_messages

    @ExceptionWrapper.python_kafka_wrapper()
    def seek(self, *args, **kwargs):
        return self._consumer.seek(*args, **kwargs)

    @ExceptionWrapper.python_kafka_wrapper()
    def subscribe(self, topics, listener=None):
        return self._consumer.subscribe(topics=topics, listener=listener)


class ConfluentConsumerAdapter(ConsumerAdapter, ConfluentAdapterMixin):
    CONNECT_ERRORS = [
        confluent_kafka.KafkaError.NETWORK_EXCEPTION,
        confluent_kafka.KafkaError.UNKNOWN,
        confluent_kafka.KafkaError.REQUEST_TIMED_OUT,
        confluent_kafka.KafkaError.INVALID_SESSION_TIMEOUT,
    ]

    @ExceptionWrapper.confluent_wrapper()
    def __init__(self, config):
        super(ConfluentConsumerAdapter, self).__init__()
        self._config = deepcopy(config)
        self._key_deserializer = self._config.pop(
            "key_deserializer", lambda x: x
        )
        self._value_deserializer = self._config.pop(
            "value_deserializer", lambda x: x
        )
        self._consumer = confluent_kafka.Consumer(
            self._parse_config(self._config)
        )

    def filter_messages(self, raw_messages):
        filtered_messages = []
        for message in raw_messages:
            if message.error():
                error = message.error()
                # no more messages
                if error.code() == self._confluent_error_code("_PARTITION_EOF"):
                    continue
                log.error(
                    "consumer_message_error|config=%s,error_code=%s",
                    self._config, error.code()
                )

            try:
                filtered_messages.append(
                    KafkaMessage.from_confluent_kafka(
                        message,
                        key_deserializer=self._key_deserializer,
                        value_deserializer=self._value_deserializer,
                    )
                )
            except Exception as err:
                log.exception(
                    "consumer_deserialize_message_error|config=%s,message=%s,desc=%s",
                    self._config, message, err
                )
        return filtered_messages

    @ExceptionWrapper.confluent_wrapper()
    def close(self, *args, **kwargs):
        return self._consumer.close(*args, **kwargs)

    @ExceptionWrapper.confluent_wrapper()
    def commit(self, *args, **kwargs):
        return self._consumer.commit(*args, **kwargs)

    @ExceptionWrapper.confluent_wrapper()
    def poll(self, timeout, max_records):
        raw_messages = self._consumer.consume(
            timeout=timeout, num_messages=max_records
        )
        return self.filter_messages(raw_messages)

    @ExceptionWrapper.confluent_wrapper()
    def seek(self, *args, **kwargs):
        return self._consumer.seek(*args, **kwargs)

    def on_assign(self, *args, **kwargs):
        pass

    def on_revoke(self, *args, **kwargs):
        pass

    @ExceptionWrapper.confluent_wrapper()
    def subscribe(self, topics, on_assign=None, on_revoke=None):
        if on_assign is None:
            on_assign = self.on_assign
        if on_revoke is None:
            on_revoke = self.on_revoke

        return self._consumer.subscribe(
            topics=topics, on_assign=on_assign, on_revoke=on_revoke
        )


class KafkaConsumer(object):
    """
    Wrapper class for kafka-python and confluent-kafka Consumer
    :param bootstrap_servers: list of kafka brokers
    :param group_id: consumer group
    :param kafka_lib: `kafka-python` or `confluent-kafka` lib
    :param connect_retries: number of retry attempts when connect error
    :param connect_retry_backoff: (second) base wait time before attempt to reconnect
    :param poll_timeout: wait time at each poll if no new message is available
    :param max_poll_records: max records to retrieve at each poll

    When using kafka-python lib:
    :param rebalance_listener: callback class to handle rebalance events
    :type rebalance_listener: kafka.ConsumerRebalanceListener
    When using confluent-kafka lib:
    :param on_assign: callback function to handle new partitions assignment
    :param on_revoke: callback function to handle partitions revocation

    Other parameters are passed directly to Consumer class
    (for either kafka-python or confluent-kafka)

    Example usage:
    >>> KAFKA_CONSUMER_CONFIG = {
    >>> 	"bootstrap_servers": ["localhost:9092"],
    >>> 	"group_id": "group.1",
    >>> }
    >>> class Consumer(KafkaConsumer):
    >>> 	def on_messages(self, messages):
    >>> 		pass  # do smt with `messages`
    >>>
    >>> consumer = Consumer(["topic1", "topic2"], KAFKA_CONSUMER_CONFIG)
    >>> consumer.start()
    """
    _default_key_deserializer = Deserializer.int_deserializer
    _default_value_deserializer = Deserializer.json_deserializer
    _default_enable_auto_commit = False
    _default_auto_offset_reset = 'latest'
    _default_kafka_lib = KafkaLib.CONFLUENT_KAFKA
    _default_poll_timeout = 1
    _default_max_poll_records = 200
    _default_connect_retries = 3
    _default_connect_retry_backoff = 1

    def __init__(self, topics, config, **kwargs):
        self._topics = topics[:]
        self._config = deepcopy(config)
        self._config.update(kwargs)
        assert "bootstrap_servers" in self._config, "bootstrap_servers is required"
        assert "group_id" in self._config, "group_id is required"

        if "key_deserializer" not in self._config:
            self._config["key_deserializer"] = self._default_key_deserializer
        if "value_deserializer" not in self._config:
            self._config["value_deserializer"] = self._default_value_deserializer
        if "max_poll_records" not in self._config:
            self._config["max_poll_records"] = self._default_max_poll_records
        if "enable_auto_commit" not in self._config:
            self._config["enable_auto_commit"] = self._default_enable_auto_commit

        self._kafka_lib = self._config.pop(
            "kafka_lib", self._default_kafka_lib
        )
        assert self._kafka_lib in KafkaLib.VALUE_TO_NAME, "invalid_kafka_lib"
        self._rebalance_listener = self._config.pop("rebalance_listener", None)
        self._on_assign = self._config.pop("on_assign", None)
        self._on_revoke = self._config.pop("on_revoke", None)
        self._poll_timeout = self._config.pop(
            "poll_timeout", self._default_poll_timeout
        )
        self._max_poll_records = self._config.pop("max_poll_records")
        self._connect_retries = self._config.pop(
            "connect_retries", self._default_connect_retries
        )
        self._connect_retry_backoff = self._config.pop(
            "connect_retry_backoff", self._default_connect_retry_backoff
        )

        self._consumer = None
        self._is_running = False
        self._is_connected = False

    def connect(self):
        try:
            if self._kafka_lib == KafkaLib.KAFKA_PYTHON:
                self._consumer = PythonKafkaConsumerAdapter(self._config)
                self._consumer.subscribe(
                    topics=self._topics,
                    listener=self._rebalance_listener,
                )
            elif self._kafka_lib == KafkaLib.CONFLUENT_KAFKA:
                self._consumer = ConfluentConsumerAdapter(self._config)
                self._consumer.subscribe(
                    topics=self._topics,
                    on_assign=self._on_assign,
                    on_revoke=self._on_revoke,
                )
            self._is_connected = True
        except Exception as err:
            log.exception(
                "kafka_consumer_failed_to_connect|config=%s,error=%s",
                self._config, err
            )
            self._is_connected = False

        return self._is_connected

    def disconnect(self, commit=True):
        if self._is_connected:
            if commit:
                self.commit()
            self._consumer.close()
            self._consumer = None
            self._is_connected = False

    def reconnect(self):
        for i in range(self._connect_retries):
            self.disconnect()
            self.connect()
            if self._is_connected:
                break
            # avoid reconnection storm
            time.sleep(
                random.uniform(0.9, 1.1) *
                (self._connect_retry_backoff ** i)
            )

        return self._is_connected

    def commit(self, *args, **kwargs):
        self._consumer.commit(*args, **kwargs)

    def _refresh_connections(self):
        pass

    def on_messages(self, messages):
        pass

    def post_process_messages(self, messages):
        self.commit()

    def _graceful_shutdown(self, sig, frame):
        log.info(
            "consumer_shutting_down_gracefully|config=%s,sig=%s",
            self._config, sig
        )
        self.stop()

    def _register_signals(self):
        signal.signal(signal.SIGTERM, self._graceful_shutdown)

    def start(self):
        self._is_running = True
        if not self.connect():
            return
        self._register_signals()

        while self._is_running:
            self._refresh_connections()
            try:
                messages = self._consumer.poll(
                    timeout=self._poll_timeout,
                    max_records=self._max_poll_records,
                )
                self.on_messages(messages)
                self.post_process_messages(messages)
            except KafkaClientConnectError:
                self.reconnect()
            except Exception as err:
                log.exception(
                    "consumer_exception|config=%s, desc=%s",
                    self._config, err
                )

        self.disconnect()

    def stop(self):
        self._is_running = False
