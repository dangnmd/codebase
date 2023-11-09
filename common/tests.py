# -*- coding: utf-8 -*-
# pylint: skip-file

try:
	import unittest2 as unittest
except:
	import unittest
import time
import random
from . import crypt
from . import conhash
from . import gtcpclient
from . import utils
from .gdpquery import *

TEST_DB_PASSWORD = '****'

class TestCommon(unittest.TestCase):

	def test_crypt(self):
		for _ in range(0, 100):
			key = crypt.random_bytes(32)
			data = crypt.random_bytes(random.randint(0, 1024))
			cipher = crypt.garena_aes_encrypt(data, key)
			decrypt_data = crypt.garena_aes_decrypt(cipher, key)
			self.assertEqual(data, decrypt_data)
		for _ in range(0, 100):
			keys = [random.randint(0, 0xffffffff) for _ in range(0, 4)]
			data = crypt.random_bytes(random.randint(0, 1024))
			cipher = crypt.garena_xtea_encrypt_native(data, keys)
			decrypt_data = crypt.garena_xtea_decrypt_native(cipher, keys)
			self.assertEqual(data, decrypt_data)
		for _ in range(0, 100):
			keys = [random.randint(0, 0xffffffff) for _ in range(0, 4)]
			data = random.randint(0, 0xffffffffffffffff)
			cipher = crypt.xtea_encrypt(data, keys)
			decrypt_data = crypt.xtea_decrypt_native(cipher, keys)
			self.assertEqual(data, decrypt_data)
			cipher = crypt.xtea_encrypt_native(data, keys)
			decrypt_data = crypt.xtea_decrypt(cipher, keys)
			self.assertEqual(data, decrypt_data)
		for _ in range(0, 100):
			keys = [random.randint(0, 0xffffffff) for _ in range(0, 4)]
			data = random.randint(0, 0xffffffffffffffff)
			cipher = crypt.xtea_encrypt(data, keys, n=64)
			decrypt_data = crypt.xtea_decrypt_native(cipher, keys, 64)
			self.assertEqual(data, decrypt_data)
			cipher = crypt.xtea_encrypt_native(data, keys, 128)
			decrypt_data = crypt.xtea_decrypt(cipher, keys, n=128)
			self.assertEqual(data, decrypt_data)
		for _ in range(0, 100):
			keys = [random.randint(0, 0xffffffff) for _ in range(0, 4)]
			data = crypt.random_bytes(random.randint(0, 1024))
			cipher = crypt.garena_xtea_encrypt_native(data, keys)
			decrypt_data = crypt.garena_xtea_decrypt(cipher, keys)
			self.assertEqual(data, decrypt_data)
			cipher = crypt.garena_xtea_encrypt(data, keys)
			decrypt_data = crypt.garena_xtea_decrypt_native(cipher, keys)
			self.assertEqual(data, decrypt_data)

	def test_conhash(self):
		c = conhash.ConHash()
		c.add_node("titanic", 32, 1)
		c.add_node("terminator2018", 24, 2)
		c.add_node("Xenomorph", 25, 3)
		c.add_node("True Lies", 10, 4)
		c.add_node("avantar", 48, 5)
		self.assertEqual("Xenomorph", c.lookup("test1"))
		self.assertEqual("avantar", c.lookup("test2"))
		self.assertEqual("titanic", c.lookup("test3"))

from . import cache
from memcache import SERVER_MAX_KEY_LENGTH
from memcache import Client

class FooStruct(object):
	def __init__(self):
		self.bar = "baz"

	def __str__(self):
		return "A FooStruct"

	def __eq__(self, other):
		if isinstance(other, FooStruct):
			return self.bar == other.bar
		return 0


class CacheClientTestCase(unittest.TestCase):
	_client = None

	@classmethod
	def setUpClass(cls):
		config = {
			'memory': {
				'type': 'memory',
				'default_timeout': 7 * 24 * 60 * 60,
			},
			'memcache0': {
				'type': 'memcached',
				'host': '122.11.129.31',
				'port': 11211,
				'default_timeout': 7 * 24 * 60 * 60,
			},
			'memcache1': {
				'type': 'memcached',
				'host': '122.11.129.31',
				'port': 11211,
				'default_timeout': 7 * 24 * 60 * 60,
				'key_prefix': 'test.',
			},
			'memcache2': {
				'type': 'memcached',
				'host': '203.117.172.31',
				'port': 11211,
				'default_timeout': 7 * 24 * 60 * 60,
				'key_prefix': 'test.',
			},
			'pymemcache': {
				'type': 'pymemcached',
				'host': '122.11.129.31',
				'port': 11211,
				'default_timeout': 7 * 24 * 60 * 60,
				'key_prefix': 'test.',
			},
			'nullcache': {
				'type': 'null',
			},
			'redis': {
				'type': 'redis',
				'host': '203.117.172.31',
				'port': 6389,
				'default_timeout': 7 * 24 * 60 * 60,
				'key_prefix': 'test.',
			},
			'rawredis': {
				'type': 'rawredis',
				'host': '203.117.172.31',
				'port': 6389,
				'default_timeout': 7 * 24 * 60 * 60,
				'key_prefix': 'test.',
			},
			'ssdb': {
				'type': 'ssdb',
				'host': '203.116.50.232',
				'port': 8888,
				'key_prefix': 'test.',
			},
			'replication': {
				'type': 'replication',
				'default': True,
				'caches': {
					'replication.main': {
						'type': 'distribution',
						'caches': {
							'distribution.1': {
								'type': 'memcached',
								'host': '122.11.129.31',
								'port': 11211,
								'default_timeout': 7 * 24 * 60 * 60,
								'key_prefix': 'test.',
								'replica': 32
							},
							'distribution.2': {
								'type': 'memcached',
								'host': '203.117.172.31',
								'port': 11211,
								'default_timeout': 7 * 24 * 60 * 60,
								'key_prefix': 'test.',
								'replica': 32
							}
						}
					},
					'replication.bak': {
						'type': 'distribution',
						'caches': {
							'distribution.1': {
								'type': 'memcached',
								'host': '203.117.172.31',
								'port': 11211,
								'default_timeout': 7 * 24 * 60 * 60,
								'key_prefix': 'test.',
								'replica': 32
							},
							'distribution.2': {
								'type': 'memcached',
								'host': '122.11.129.31',
								'port': 11211,
								'default_timeout': 7 * 24 * 60 * 60,
								'key_prefix': 'test.',
								'replica': 32
							}
						}
					}
				}
			},
			'multilayer': {
				'type': 'multilayer',
				'caches': [
					{
						'type': 'memory',
						'default_timeout': 60,
						'trim_interval': 60
					},
					{
						'type': 'memcached',
						'host': '203.117.172.31',
						'port': 11211,
						'default_timeout': 7 * 24 * 60 * 60,
						'key_prefix': 'test.',
					}
				]
			}
		}
		cache.init_cache(config)

	def check_setget(self, key, value):
		cache.set(key, value)
		newval = cache.get(key)
		self.assertEqual(newval, value)

	def test_setget(self):
		self.check_setget("a_string", "some random string")
		self.check_setget("an_integer", 42)

	def test_delete(self):
		self.check_setget("long", int(1 << 30))
		result = cache.delete("long")
		self.assertEqual(result, True)
		self.assertEqual(cache.get("long"), None)

	def test_get_list(self):
		self.check_setget("gm_a_string", "some random string")
		self.check_setget("gm_an_integer", 42)
		self.check_setget("gm_abc", 33)
		self.check_setget("gm_cde", 34)
		self.assertEqual(
			cache.get_list(["gm_a_string", "gm_an_integer", "gm_abc", "gm_cde"]),
			['some random string', 42, 33, 34])

	def test_get_many(self):
		self.check_setget("gm_a_string", "some random string")
		self.check_setget("gm_an_integer", 42)
		self.check_setget("gm_abc", 33)
		self.check_setget("gm_cde", 34)
		self.assertEqual(
			cache.get_many(["gm_a_string", "gm_an_integer", "gm_abc", "gm_cde"]),
			{"gm_a_string": "some random string", "gm_an_integer": 42, "gm_abc": 33, "gm_cde": 34})

	def test_add(self):
		self.check_setget("key_exists", "random string")
		self.assertFalse(cache.add("key_exists", "default"))
		self.assertEqual(cache.get("key_exists"), "random string")
		cache.delete("key_exists")
		self.assertTrue(cache.add("key_exists", "default"))
		self.assertEqual(cache.get("key_exists"), "default")

	def test_inc_decr(self):
		self.assertTrue(cache.set('abc', "21"))
		self.assertEqual(cache.get('abc'), '21')
		self.assertEqual(cache.incr('abc'), 22)
		self.assertEqual(cache.incr('abc'), 23)
		self.assertEqual(cache.get('abc'), '23')
		self.assertEqual(cache.decr('abc', 2), 21)
		self.assertEqual(cache.incr('abc', 3), 24)

	def test_set_many(self):
		mapping = {"a_string": "str", "a_integer": 21}
		self.assertTrue(cache.set_many(mapping))
		self.assertEqual(cache.get_many(["a_string", "a_integer"]), {"a_string": "str", "a_integer": 21})

	def test_replication(self):
		self.assertTrue(cache.get_cache('replication').delete('replication'))
		self.assertIsNone(cache.get_cache('replication').get('replication'))
		self.assertTrue(cache.get_cache('replication').set('replication', 'abc'))
		self.assertEqual(cache.get_cache('memcache1').get('replication'), 'abc')
		self.assertEqual(cache.get_cache('memcache2').get('replication'), 'abc')

	def test_delete_many(self):
		self.check_setget("gm_a_string", "some random string")
		self.check_setget("gm_an_integer", 42)
		self.check_setget("gm_abc", 33)
		self.check_setget("gm_cde", 34)
		self.assertTrue(cache.delete_many(['gm_a_string', 'gm_an_integer', 'gm_abc', 'gm_cde']))
		self.assertIsNone(cache.get('gm_a_string'))
		self.assertIsNone(cache.get('gm_an_integer'))
		self.assertIsNone(cache.get('gm_abc'))
		self.assertIsNone(cache.get('gm_cde'))

	def test_get_unknown_value(self):
		self.assertEqual(cache.get("unknown_value"), None)

	def test_setget_foostruct(self):
		f = FooStruct()
		self.check_setget("foostruct", f)

	def test_sending_spaces(self):
		try:
			cache.set("this has spaces", 1)
		except Exception as err:
			self.assertTrue("characters not allowed" in err.args[0] or "error 11" in err.args[0])
		else:
			self.fail(
				"Expected Client.MemcachedKeyCharacterError, nothing raised")

	def test_sending_control_characters(self):
		try:
			cache.set("this\x10has\x11control characters\x02", 1)
		except Exception as err:
			self.assertTrue("characters not allowed" in err.args[0] or "bad command line format" in err.args[0])
		else:
			self.fail(
				"Expected Client.MemcachedKeyCharacterError, nothing raised")

	def test_sending_key_too_long(self):
		client = cache.get_cache('memcache0')
		try:
			client.set('a' * SERVER_MAX_KEY_LENGTH + 'a', 1)
		except Exception as err:
			self.assertTrue("length is >" in err.args[0] or "too long" in err.args[0])
		else:
			self.fail(
				"Expected Client.MemcachedKeyLengthError, nothing raised")

		# These should work.
		client.set('a' * SERVER_MAX_KEY_LENGTH, 1)

	def test_official_memcache_client(self):
		client = Client(["122.11.129.31:11211"], debug=0)
		client.delete("official_client")
		self.assertTrue(client.set("official_client", "should be true"))
		self.assertEqual(client.get("official_client"), "should be true")
		self.assertEqual(client.get("official_client"), cache.get_cache('memcache0').get("official_client"))
		cache.get_cache('replication').delete('our_client')
		self.assertTrue(cache.get_cache('replication').set("our_client", "test"))
		self.assertEqual(cache.get_cache('replication').get('our_client'), 'test')
		self.assertEqual(client.get('test.our_client'), 'test')

	def test_serdser(self):
		client = cache.get_cache('pymemcache')
		self.assertEqual(client.set('abc', [1, 2, 'abc']), True)
		self.assertEqual(client.get('abc'), [1, 2, 'abc'])
		self.assertEqual(client.delete('abc'), True)
		self.assertTrue(client.delete_many(['abc', 'cde'], noreply=True))

	def _test_client(self, client, string_only=False, plain_data=True, support_data_types=False, support_expire=False):
		client.delete('abc')
		self.assertTrue(client.set('abc', 'cde', noreply=True))
		self.assertEqual(client.get('abc'), 'cde')
		self.assertEqual(client.delete('abc'), True)
		self.assertEqual(client.delete('abc', noreply=True), True)
		if string_only:
			data = {'abc': 'cde', 'long': '1223'}
		else:
			data = {'abc': 'cde', 'long': 1223}
		self.assertTrue(client.set_many(data))
		self.assertEqual(client.get_list(list(data.keys())), list(data.values()))
		self.assertEqual(client.get_many(list(data.keys())), data)
		self.assertEqual(client.delete_many(list(data.keys())), True)
		self.assertEqual(client.get_list(list(data.keys())), [None for key in list(data.keys())])
		self.assertEqual(client.get_many(list(data.keys())), {})
		self.assertEqual(client.delete_many(list(data.keys()), noreply=True), True)
		self.assertIsNone(client.get(list(data.keys())[0]))

		if plain_data:
			client.set('n', '0')
			self.assertEqual(client.incr('n'), 1)
			self.assertEqual(client.get('n'), '1')
			self.assertEqual(client.decr('n'), 0)
			self.assertEqual(client.get('n'), '0')

		client.delete_many(['abc', 'abc_timeout'])
		self.assertTrue(client.set('abc', 'cde', timeout=0))
		self.assertEqual(client.get('abc'), 'cde')
		self.assertTrue(client.set('abc_timeout', 'def', timeout=1))
		self.assertEqual(client.get('abc_timeout'), 'def')
		client.delete_many(['abc_add', 'abc_add_timeout'])
		client.set('abc_add_alread_exist', 'exist')
		self.assertTrue(client.add('abc_add', 'add', timeout=0))
		self.assertEqual(client.get('abc_add'), 'add')
		self.assertTrue(client.add('abc_add_timeout', 'add', timeout=1))
		self.assertEqual(client.get('abc_add_timeout'), 'add')
		self.assertFalse(client.add('abc_add_alread_exist', 'abc'))
		self.assertEqual(client.get('abc_add_alread_exist'), 'exist')
		if string_only:
			data = {'set_1': '1', 'set_2': '2', 'set_3': '[1, ]'}
		else:
			data = {'set_1': '1', 'set_2': 2, 'set_3': [1, ]}
		self.assertTrue(client.set_many(data, timeout=0))
		self.assertEqual(client.get_many(list(data.keys())), data)
		if string_only:
			data_timeout = {'set_1_timeout': '1', 'set_2_timeout': '2', 'set_3_timeout': '[1, ]'}
		else:
			data_timeout = {'set_1_timeout': '1', 'set_2_timeout': 2, 'set_3_timeout': [1, ]}
		self.assertTrue(client.set_many(data_timeout, timeout=1))
		self.assertEqual(client.get_many(list(data_timeout.keys())), data_timeout)
		time.sleep(3)
		self.assertEqual(client.get('abc'), 'cde')
		self.assertIsNone(client.get('abc_timeout'))
		self.assertEqual(client.get('abc_add'), 'add')
		self.assertIsNone(client.get('abc_add_timeout'))
		self.assertEqual(client.get_many(list(data.keys())), data)
		self.assertEqual(client.get_many(list(data_timeout.keys())), {})
		self.assertEqual(client.get_many(list(data.keys()) + list(data_timeout.keys())), data)
		client.delete_many(list(data.keys()) + list(data_timeout.keys()))

		self.assertTrue(client.set('unicode', "1"))
		self.assertEqual(client.get('unicode'), "1")
		self.assertEqual(client.get('unicode'), "1")
		self.assertTrue(client.set('测试', "2"))
		self.assertEqual(client.get('测试'), "2")
		self.assertEqual(client.get('\xe6\xb5\x8b\xe8\xaf\x95'), "2")
		self.assertTrue(client.set('\xe6\xb5\x8b\xe8\xaf\x95', "3"))
		self.assertEqual(client.get('\xe6\xb5\x8b\xe8\xaf\x95'), "3")
		self.assertEqual(client.get('测试'), "3")

		if support_data_types:
			#list
			if string_only:
				data = ['1', '2']
			else:
				data = ['1', 2]
			self.assertTrue(client.delete('list'))
			self.assertEqual(client.llen('list'), 0)
			self.assertEqual(client.lrange('list'), [])
			self.assertIsNone(client.lindex('list', 0))
			for v in data:
				self.assertTrue(client.lpush('list', v))
			self.assertEqual(client.llen('list'), len(data))
			self.assertEqual(client.lrange('list'), data[::-1])
			for v in data:
				self.assertEqual(client.rpop('list'), v)
			self.assertEqual(client.llen('list'), 0)
			for v in data:
				self.assertTrue(client.rpush('list', v))
			self.assertEqual(client.llen('list'), len(data))
			self.assertEqual(client.lrange('list'), data)
			for v in data:
				self.assertEqual(client.lpop('list'), v)
			self.assertEqual(client.llen('list'), 0)
			for v in data:
				self.assertTrue(client.rpush('list', v))
			self.assertEqual(client.brpop('list'), data[-1])
			self.assertEqual(client.blpop('list'), data[0])
			self.assertEqual(client.blpop('list', 1), None)
			self.assertTrue(client.ltrim('list', 0, 0))
			self.assertEqual(client.llen('list'), 0)
			for v in data:
				self.assertTrue(client.rpush('list', v))
			self.assertEqual(client.lindex('list', 0), data[0])
			self.assertEqual(client.lindex('list', -1), data[-1])
			self.assertEqual(client.lrange('list', 0, 1), data[0:2])
			self.assertEqual(client.lrange('list', 1, -1), data[1:])
			self.assertTrue(client.ltrim('list', 1, -1))
			self.assertEqual(client.llen('list'), len(data[1:]))
			self.assertEqual(client.lrange('list'), data[1:])
			self.assertTrue(client.delete('list'))

			#set
			if string_only:
				data = set(['1', '2'])
			else:
				data = set(['1', 2])
			self.assertTrue(client.delete('set'))
			self.assertEqual(client.scard('set'), 0)
			self.assertEqual(client.smembers('set'), set())
			self.assertIsNone(client.srandmember('set'))
			for v in data:
				self.assertFalse(client.sismember('set', v))
				self.assertTrue(client.sadd('set', v))
				self.assertTrue(client.sismember('set', v))
			self.assertEqual(client.scard('set'), len(data))
			self.assertEqual(client.smembers('set'), data)
			self.assertIn(client.srandmember('set'), data)
			for v in data:
				self.assertTrue(client.srem('set', v))
			self.assertTrue(client.delete('set'))
			self.assertEqual(client.scard('set'), 0)
			self.assertEqual(client.smembers('set'), set())
			self.assertIsNone(client.srandmember('set'))
			self.assertTrue(client.delete('set'))

			#hash
			if string_only:
				data = {'set_1': '1', 'set_2': '2'}
			else:
				data = {'set_1': '1', 'set_2': 2}
			self.assertTrue(client.delete('hash'))
			self.assertEqual(client.hgetall('hash'), {})
			self.assertEqual(client.hlen('hash'), 0)
			self.assertIsNone(client.hget('hash', 'set_1'))
			self.assertFalse(client.hexists('hash', 'set_1'))
			self.assertTrue(client.hset('hash', 'set_1', data['set_1']))
			self.assertEqual(client.hget('hash', 'set_1'), data['set_1'])
			self.assertTrue(client.hexists('hash', 'set_1'))
			self.assertFalse(client.hexists('hash', 'set_2'))
			self.assertTrue(client.hset('hash', 'set_2', data['set_2']))
			self.assertEqual(client.hget('hash', 'set_2'), data['set_2'])
			self.assertTrue(client.hexists('hash', 'set_2'))
			self.assertEqual(client.hgetall('hash'), data)
			self.assertEqual(client.hlen('hash'), len(data))
			self.assertTrue(client.hdel('hash', 'set_1'))
			self.assertIsNone(client.hget('hash', 'set_1'))
			self.assertTrue(client.hdel('hash', 'set_2'))
			self.assertEqual(client.hlen('hash'), 0)
			self.assertFalse(client.hexists('hash', 'set_1'))
			self.assertFalse(client.hexists('hash', 'set_2'))
			self.assertEqual(client.hgetall('hash'), {})
			self.assertTrue(client.delete('hash'))
			self.assertEqual(client.hgetall('hash'), {})

			#hash
			if string_only:
				data = [('1', 10), ('2', 20), ('3', 30)]
			else:
				data = [('1', 10), (2, 20), ('3', 30)]
			values = [v for v, s in data]
			self.assertTrue(client.delete('zset'))
			self.assertEqual(client.zcard('zset'), 0)
			self.assertEqual(client.zcount('zset', 0, 100), 0)
			self.assertEqual(client.zrange('zset', 0, 1), [])
			self.assertEqual(client.zrangebyscore('zset', 0, 100), [])
			i = 0
			for v, s in data:
				self.assertIsNone(client.zscore('zset', v))
				self.assertIsNone(client.zrank('zset', v))
				self.assertTrue(client.zadd('zset', v, s))
				self.assertEqual(client.zscore('zset', v), s)
				self.assertEqual(client.zrank('zset', v), i)
				i += 1
			self.assertEqual(client.zcard('zset'), len(data))
			self.assertEqual(client.zcount('zset', 0, 100), len(data))
			self.assertEqual(client.zrange('zset', 0, -1), values)
			self.assertEqual(client.zrangebyscore('zset', 0, 100), values)
			self.assertEqual(client.zrange('zset', 0, -1, withscores=True), data)
			self.assertEqual(client.zrangebyscore('zset', 0, 100, withscores=True), data)
			self.assertEqual(client.zrange('zset', 0, len(data)-1, reverse=True, withscores=True), data[::-1])
			self.assertEqual(client.zrangebyscore('zset', 0, 100, reverse=True, withscores=True), data[::-1])
			for v, s in data:
				self.assertTrue(client.zrem('zset', v))
				self.assertIsNone(client.zscore('zset', v))
				self.assertIsNone(client.zrank('zset', v))
			self.assertEqual(client.zcard('zset'), 0)
			self.assertEqual(client.zcount('zset', 0, 100), 0)
			self.assertEqual(client.zrange('zset', 0, 1), [])
			self.assertEqual(client.zrangebyscore('zset', 0, 100), [])
			for v, s in data:
				self.assertTrue(client.zadd('zset', v, s))
			self.assertEqual(client.zincrby('zset', data[0][0], 2), data[0][1] + 2)
			self.assertEqual(client.zscore('zset', data[0][0]), data[0][1] + 2)
			self.assertEqual(client.zremrangebyrank('zset', 0, 1), 2)
			self.assertEqual(client.zrange('zset', 0, 1, withscores=True), data[2:])
			self.assertTrue(client.delete('zset'))
			for v, s in data:
				self.assertTrue(client.zadd('zset', v, s))
			self.assertTrue(client.zadd('zset', data[0][0], data[0][1]))
			self.assertEqual(client.zremrangebyrank('zset', 0, 1, reverse=True), 2)
			self.assertEqual(client.zrange('zset', 0, 1, withscores=True), data[:1])
			self.assertTrue(client.delete('zset'))
			for v, s in data:
				self.assertTrue(client.zadd('zset', v, s))
			self.assertEqual(client.zremrangebyscore('zset', 0, 20), 2)
			self.assertEqual(client.zcount('zset', 0, 100), 1)
			self.assertTrue(client.delete('zset'))
			for v, s in data:
				self.assertTrue(client.zadd('zset', v, s))
			self.assertEqual(client.zunionstore('zset', ['zset', 'zset']), 3)
			self.assertEqual(client.zrange('zset', 0, -1, withscores=True), [(k, v*2) for (k, v) in data])
			self.assertTrue(client.delete('zset'))

		if support_expire:
			self.assertTrue(client.set('exp', 'value', 3))
			time.sleep(1.1)
			self.assertEqual(client.get('exp'), 'value')
			client.expire('exp', 1)
			self.assertEqual(client.get('exp'), 'value')
			time.sleep(1.1)
			self.assertIsNone(client.get('exp'))

	def test_memory_client(self):
		self._test_client(cache.get_cache('memory'))

	def test_memcached_client(self):
		self._test_client(cache.get_cache('memcache0'), support_expire=True)

	def test_pymemcache_client(self):
		self._test_client(cache.get_cache('pymemcache'), support_expire=True)

	def test_redis_client(self):
		self._test_client(cache.get_cache('redis'), plain_data=False, support_data_types=True, support_expire=True)

	def test_redis_client_expire(self):
		client = cache.get_cache('redis')
		self.assertTrue(client.delete('zset'))
		data = [('1', 10), ('2', 20)]
		for v, s in data:
			self.assertTrue(client.zadd('zset', v, s))
		self.assertTrue(client.expire('zset', 2))
		self.assertEqual(client.zrange('zset', 0, -1, withscores=True), data)
		time.sleep(4)
		self.assertEqual(client.zrange('zset', 0, -1, withscores=True), [])
		self.assertTrue(client.delete('zset'))

	def test_rawredis_client(self):
		self._test_client(cache.get_cache('rawredis'), string_only=True, support_data_types=True)

	def test_ssdb_client(self):
		self._test_client(cache.get_cache('ssdb'), string_only=True)

	def test_multilayer_client(self):
		self._test_client(cache.get_cache('multilayer'))

def test_perf(name, test_round, func, params=()):
	start = time.time()
	for _ in range(test_round):
		func(*params)
	end = time.time()
	print((name, ':', end - start, 's'))
	print(('avg : ', (end - start) * 1000000 / test_round, 'us'))

def create_random_bytes():
	while True:
		print('input length: ')
		length = int(eval(input()))
		print((crypt.random_bytes(length).encode('hex')))

def create_django_secret_key():
	print((crypt.create_django_secret_key()))

def test_tcp_client():
	client = gtcpclient.GTcpClient('www.google.com', 80)
	client.send('test')
	print((client.receive()))

def test_data_cache():
	from . import datacache
	print('test cache 1')
	test_cache = datacache.DataCacheTable(timeout=5, load_data_func=lambda key: time.time())
	print((test_cache.get_data(1)))
	time.sleep(1)
	print((test_cache.get_data(1)))
	time.sleep(1)
	print((test_cache.get_data(2)))
	time.sleep(4)
	print((test_cache.get_data(1)))
	print('test cache 2')
	class TestCache2(datacache.DataCacheTable):
		def _load_data(self, key):
			return time.time()
	test_cache2 = TestCache2(timeout=5)
	print((test_cache2.get_data(1)))
	time.sleep(1)
	print((test_cache2.get_data(1)))
	time.sleep(1)
	print((test_cache2.get_data(2)))
	time.sleep(4)
	print((test_cache2.get_data(1)))

def test_tcp_async_client():
	def on_connect(client):
		print(('connect', client.id))
		client.send('GET / HTTP/1.1\r\n\r\n')
	def on_receive_packet(client, packet):
		print((packet.encode('hex')))
	def on_disconnect(client):
		print(('disconnect', client.id))
	from . import gtcpasyncclient
	client = gtcpasyncclient.GTcpAsyncClient('test', '127.0.0.1', 12345, on_receive_packet, on_connect, on_disconnect)
	client.send('test')
	from . import event_loop
	event_loop.run()

def test_event_loop():
	from . import event_loop
	def simple_print(s):
		print(s)
	event_loop.add_timeout(1, simple_print, 'timeout')
	event_loop.add_interval_timer(0.5, simple_print, 'interval')
	event_loop.add_callback(simple_print, 'callback')
	print('start')
	event_loop.run()

def test_mysql_client():
	from . import mysqlclient
	client = mysqlclient.MysqlClient('203.117.172.31', 3306, 'generalquery', 'TODO:fill', 'test_db')
	results = client.query('SELECT * FROM test_tab WHERE id <= %s', 3)
	print(results)

def test_gdp_client():
	init_gdp_client_manager({
		'main': {
			'ip': '203.117.172.31',
			'port': 12004,
			'default': True
		}
	})
	query = GetUserAccountLite(79805389)
	query.run()
	print((query.result))
	query = IMGetBuddies(79805389)
	query.run()
	print([r.buddyid for r in query.result])
	query = IMAddBuddyPB(uid=79805389, buddyid=79805391, relation=1, createdate=int(time.time()))
	print((query.params))
	print((query.run()))
	query = IMGetBuddies(79805389)
	query.run()
	print([r.buddyid for r in query.result])

def test_utils_str():
	s = '测试一下'
	print((s.encode('utf-8').encode('hex')))
	print((utils.truncate_unicode(s, 8)))
	print((utils.truncate_unicode(s, 9)))
	print((utils.truncate_unicode(s, 10)))
	print((utils.truncate_unicode(s, 11)))
	print((utils.truncate_unicode(s, 12)))

def test_cache():
	cache.init_cache({
		'main': {
			'type': 'memcached',
			'host': '203.117.172.31',
			'port': 11211,
			'default_timeout': 7 * 24 * 60 * 60,
			'key_prefix': 'test',
			'default': True,
		},
		'distribution': {
			'type': 'distribution',
			'method': 'mod',
			'key_regex': r'\w+\.(\d+)',
			'factor': 2,
			'caches': {
				'0': {
					'type': 'memcached',
					'host': '203.117.172.31',
					'port': 11211,
					'default_timeout': 7 * 24 * 60 * 60,
					'key_prefix': 'test'
				},
				'1': {
					'type': 'memcached',
					'host': '203.117.172.31',
					'port': 11212,
					'default_timeout': 7 * 24 * 60 * 60,
					'key_prefix': 'test'
				}
			}
		}
	})
	cache.set('key1', 'value')
	print((cache.get('key1')))
	print((cache.get('key2')))
	print((cache.get_cache('main').get('key1')))
	dclient = cache.get_cache('distribution')
	print('-distribution-')
	print((dclient.get('user.100000')))
	print((dclient.get('user.100001')))
	print((dclient.set('user.100000', 'value1')))
	print((dclient.get('user.100000')))
	print((dclient.set('user.100001', 'value2')))
	print((dclient.get('user.100001')))

def test_crontask():
	from . import crontask
	@crontask.register_task('* * * * * *', group=1)
	def print_time():
		print((time.time()))
	@crontask.register_task('*/5 * * * * *', group=1)
	def print_hello():
		print('hello')
	@crontask.register_task('* * * * * *', group=1)
	def slow_task():
		time.sleep(2.5)
		print('slow')
	crontask.run()

def test_pb_validator():
	from .pbdata import GdpProtocol_pb2
	d1 = GdpProtocol_pb2.Request()
	d1.id = 100
	d1.queries.add()
	q1 = d1.queries[0]
	q1.name = 'test'
	q1.params.append('test')
	q1.option = 1
	from .pbutils import PBValidator
	s1 = {
		"type": "object",
		"properties": {
			"id": {"type": "integer", "minimum": 1, "maximum": 2**32-1},
			"queries": {
				"type": "array",
				"items": {
					"type": "object",
					"properties": {
						"name": {"type": "string", "minLength": 4, "maxLength": 30, "pattern": r"\w+"},
						"params": {
							"type": "array",
							"items": {"type": "bytes", "length": 4, "minLength": 4, "maxLength": 4},
						},
						"option": {"type": "integer", "minimum": 0, "maximum": 256}
					},
					"required": ["name", "params", "option"]
				},
				"minItems": 1,
				"maxItems": 1
			}
		},
		"required": ["id", "queries"]
	}
	v1 = PBValidator(s1)
	print(('\n'.join(v1.iter_errors(d1))))
	'''
	from jsonschema import Draft4Validator
	jv = Draft4Validator(s1)
	from pbutils import pb_to_dict
	dd1 = pb_to_dict(d1)
	test_perf('test_pb_validator', 1000, lambda :'\n'.join(v1.iter_errors(d1)))
	test_perf('test_pb_to_dict', 1000, lambda :pb_to_dict(d1))
	test_perf('test_json_validator_pb', 1000, lambda :'\n'.join([e.message for e in jv.iter_errors(pb_to_dict(d1))]))
	test_perf('test_json_validator_json', 1000, lambda :'\n'.join([e.message for e in jv.iter_errors(dd1)]))
	'''

def test_form_validator():
	from .form_validator import FormValidator
	s = {
		"type": "object",
		"properties": {
			"int_list": {
				"type": "array",
				"items": {"type": "integer", "minimum": 1, "maximum": 2**32-1},
				"minItems": 1,
				"maxItems": 10,
				"delimiter": ","
			},
			"number": {"type": "number", "minimum": 1, "maximum": 10},
			"string": {"type": "string", "minLength": 4, "maxLength": 30, "pattern": r"\w+"},
			"bytes": {"type": "bytes", "minLength": 1, "maxLength": 20, "encoding": "urlbase64"},
		},
		"required": ["int_list", "number", "string", "bytes"]
	}
	d = {
		'int_list': '1,2',
		'number': '1.2',
		'string': '1234',
		'bytes': '-__='
	}
	v = FormValidator(s)
	print((v.normalize(d)))
	s1 = {
		"type": "object",
		"properties": {
			"int": {"type": "integer", "minimum": 1, "maximum": 2**32-1},
			"string": {"type": "string", "minLength": 4, "maxLength": 30},
		},
		"required": ["int", "string"]
	}
	d = {'int': 10, 'string': 'test'}
	v1 = FormValidator(s1)
	from django.conf import settings
	settings.configure(USE_I18N=False)
	from django import forms
	class DjangoTestForm(forms.Form):
		int = forms.IntegerField(min_value=1, max_value=2**32-1, required=True)
		string = forms.CharField(min_length=4, max_length=30, required=True)
	test_perf('test_form_validator', 1000, lambda: v1.normalize(d))
	test_perf('test_django_form', 1000, lambda: DjangoTestForm(d).is_valid())

def test_sqlalchemy_model():

	from . import dbmodel

	config = {
		'test_db.master': {
			'type': 'mysql',
			'host': '203.117.172.31',
			'port': 3306,
			'user': 'generalquery',
			'password': TEST_DB_PASSWORD,
			'db': 'test_db',
			'charset': 'utf8',
			'conn_recycle_timeout': 60 * 60,
		},
		'test_db.slave': {
			'type': 'mysql',
			'host': '203.117.172.31',
			'port': 3306,
			'user': 'generalquery',
			'password': TEST_DB_PASSWORD,
			'db': 'test_db',
			'charset': 'utf8',
			'conn_recycle_timeout': 60 * 60,
		},
	}

	db = dbmodel.init_db('sqlalchemy', config, True)

	class TestDB:

		class TestTab(db.Model):
			__dbmaster__ = 'test_db.master'	#master db id
			__dbslave__ = 'test_db.slave'	#slave db id
			__tablename__ = 'test3_tab'	#table name
			id = db.Column(db.Integer, primary_key=True, autoincrement=True)
			value = db.Column(db.Unicode(4), nullable=True)

	#add by save
	row = TestDB.TestTab(value='v0')
	row.save()

	#query
	result = TestDB.TestTab.query().all()
	for row in result:
		print((row.id, row.value))

	#update by query
	row = TestDB.TestTab.query().filter_by(id=1).one()
	row.value = 'v1'
	row.save()

	#update by execute
	TestDB.TestTab.execute().filter_by(id=1).update({'value': 'v2'})

	#delete by query
	TestDB.TestTab.query().filter_by(id=1).one().delete()

	#delete by execute
	TestDB.TestTab.execute().filter_by(id=1).delete()

def test_ssdb():
	config = {
		'ssdb': {
			'type': 'ssdb',
			'host': '203.116.50.232',
			'port': 8888,
			'default': True,
		}
	}
	cache.init_cache(config)
	print((cache.set('key', '1')))
	print((cache.get('key')))
	print((cache.get_list(('key', 'key2'))))
	print((cache.set_many({'key2': 'v2', 'key3': 'v3'})))
	print((cache.get_many(('key', 'key2', 'key3'))))
	print((cache.add('key3', 'v')))
	print((cache.delete('key3')))
	print((cache.add('key3', 'v')))
	print((cache.delete_many(('key2', 'key3', 'key4'))))
	print((cache.decr('key')))
	print((cache.decr('key')))
	print((cache.incr('key')))
	print((cache.set('key', '1', 10)))
	print((cache.set_many({'key2': 'v2', 'key3': 'v3'}, 1)))
	print((cache.get('key3')))
	time.sleep(1)
	print((cache.get('key3')))
	print((cache.hgetall('hkey')))
	print((cache.hget('hkey', 'key1')))
	print((cache.hset('hkey', 'key1', 'v1')))
	print((cache.hgetall('hkey')))
	print((cache.hget('hkey', 'key1')))
	print((cache.hdel('hkey', 'key1')))
	print((cache.hget('hkey', 'key1')))
	print((cache.delete('hkey')))

def test_asynctask():
	def sleep_and_print(sec, text):
		time.sleep(sec)
		print(text)
	from . import asynctask
	print('main 1')
	asynctask.run(sleep_and_print, (1.5, 'async 1'))
	time.sleep(1)
	print('main 2')
	asynctask.run(sleep_and_print, (0.1, 'async 2'))
	time.sleep(1)
	print('main 3')
	asynctask.run(sleep_and_print, (0, 'async 3'))

def test_django_model():
	from . import dbmodel
	config = {
		'default': {},
		'test.read': {
			'ENGINE': 'django.db.backends.mysql',
			'NAME': 'test_db',
			'USER': 'generalquery',
			'PASSWORD': TEST_DB_PASSWORD,
			'HOST': '203.117.172.31',
			'PORT': '3306',
			'CONN_MAX_AGE': 3600,
			'OPTIONS': {'charset': 'utf8mb4'},
		},
		'test.write': {
			'ENGINE': 'django.db.backends.mysql',
			'NAME': 'test_db',
			'USER': 'generalquery',
			'PASSWORD': TEST_DB_PASSWORD,
			'HOST': '203.117.172.31',
			'PORT': '3306',
			'CONN_MAX_AGE': 3600,
			'OPTIONS': {'charset': 'utf8mb4'},
		},
		'daily_log_db': {
			'ENGINE': 'django.db.backends.mysql',
			'NAME': 'daily_log_db',
			'USER': 'generalquery',
			'PASSWORD': TEST_DB_PASSWORD,
			'HOST': '203.116.180.206',
			'PORT': '6606',
			'CONN_MAX_AGE': 3600,
			'OPTIONS': {'charset': 'utf8mb4'},
		},
	}

	dbmodel.init_db('django', config, True)

	from .dbmodel import db

	class TestTab(db.AdvancedModel):
		id = db.PositiveAutoField(primary_key=True)
		value = db.CharField(max_length=4)
		class Config:
			db_for_read = 'test.read'
			db_for_write = 'test.write'
		class Meta:
			app_label = ''
			db_table = 'test3_tab'

	print((TestTab.objects.filter(id=30)[0].value))

	#TestTab(id=35, value='Test').save()

	class UserLoginTab(db.PartitionModel):
		id = db.BigAutoField(primary_key=True)
		uid = db.PositiveBigIntegerField()
		login_ip = db.CharField(max_length=15)
		login_time = db.PositiveIntegerField()
		source = db.CharField(max_length=32)
		class Config:
			db_for_all = 'daily_log_db'
			partition_func = db.partition_by_datetime('%Y%m%d')
		class Meta:
			app_label = ''
			db_table = 'user_login_tab_%s'

	print('query 1')
	q = UserLoginTab(partition_key=time.time())
	q = q.objects.filter(uid=200070)
	for d in q:
		print((d.uid, d.login_time))

	print('query 2')
	q = UserLoginTab(partition_key=time.time()).objects.filter(uid=5102878)
	for d in q:
		print((d.uid, d.login_time))

	print('query 3')
	q = UserLoginTab(partition_key=time.time() - 24*3600).objects.filter(uid=200070)
	for d in q:
		print((d.uid, d.login_time))

	print('query 4')
	q = UserLoginTab(partition_key=time.time()).objects.filter(uid=133213386)
	for d in q:
		print((d.uid, d.login_time))

	print('save 1')
	q = UserLoginTab(partition_key=time.time()).new(uid=10000, login_ip='0.0.0.0', login_time=time.time(), source='')
	print((q.save()))


def test_kafka_client():
	from .kafka_client import KafkaConsumer, KafkaProducer

	producer = KafkaProducer('122.11.130.70:9092', 'test_kafka', 0)
	print((producer.produce("Hello!")))

	consumer = KafkaConsumer('122.11.130.70:9092', 'test_kafka', 0, 'test_consumer_group')
	for offset, value in consumer.consume():
		print((offset, value))


def test_gevent_utils():
	import socket
	from .gevent_utils import gevent_context
	# use monkey_context as context manager
	with gevent_context():
		print((socket.socket.__module__))  # gevent.socket

	print((socket.socket.__module__))  # socket

	# use m onkey_context as decorator
	@gevent_context
	def test_decorator(requests, data):
		print((socket.socket.__module__))  # gevent.socket

	test_decorator('', {})

	print((socket.socket.__module__))  # scoket

	# more complex example
	import requests
	import gevent
	def task(n):
		print(('task %s start' % n))
		requests.get('https://www.google.com.sg')
		print(('task %s end' % n))
	# 1 the normal sync way
	queryset = list(range(5))
	for model in queryset:
		task(model)
	print()
	# 2 the async way without monkey patch
	tasklist = [gevent.spawn(task, model) for model in queryset]
	gevent.joinall(tasklist)
	print()
	# 3 the async way with monkey patch
	with gevent_context():
		# the async way which requires monkey patch
		tasklist = [gevent.spawn(task, model) for model in queryset]
		gevent.joinall(tasklist)
	# when out of the scope, modules being monkey patched are back to normal
	print((socket.socket.__module__))
	print()
	# 4 the better way
	from gevent.queue import Queue, Empty
	tasks = Queue(2)
	def worker(name):
		try:
			while True:
				task = tasks.get(timeout=1)
				print(('%s got task %s' % (name, task)))
				requests.get('https://www.google.com.sg')
		except Empty:
			print('boss went back home, no more work!')

	def liujing():
		queryset = list(range(5))
		for model in queryset:
			tasks.put(model)
		print('boss assigned all tasks, going back home')

	workers = ['xianyou', 'mengchi']
	with gevent_context():
		gevent.joinall([gevent.spawn(liujing)] + [gevent.spawn(worker, w) for w in workers])

def test_client_pool():
	from .client_pool import ClientPool
	def creator():
		import _thread
		return _thread.get_ident()
	pool = ClientPool(creator, size=2)
	threads = []
	def test(n):
		print((n, 'start'))
		with pool.get() as d:
			print((n, 'get', d))
			time.sleep(2)
		print((n, 'end'))
	from threading import Thread
	for i in range(6):
		t = Thread(target=test, args=(i,))
		t.start()
		threads.append(t)
	for t in threads:
		t.join()

def test_local_client():
	from .client_pool import ThreadLocalClient
	def creator():
		import _thread
		return _thread.get_ident()
	pool = ThreadLocalClient(creator)
	threads = []
	def test(n):
		print((n, 'start'))
		print((n, pool.get()))
		time.sleep(1)
		print((n, pool.get()))
		print((n, 'end'))
	from threading import Thread
	for i in range(6):
		t = Thread(target=test, args=(i,))
		t.start()
		threads.append(t)
	for t in threads:
		t.join()

def test_gwebservice():
	from .gwebservice import rsaEncrypt, GWS_KEY
	test_data = "test_sample"
	crypt_data = rsaEncrypt(test_data)

	# Decryption test (m2crypto/pycrypto compatible)
	import base64
	from Crypto.PublicKey import RSA
	key = RSA.importKey(GWS_KEY)
	t = key.encrypt(base64.b64decode(crypt_data), 0)[0]
	plain_data = t[key.size() / 8 - len(test_data):]
	assert plain_data == test_data


def console_test():
	create_random_bytes()
	#create_django_secret_key()
	#test_tcp_client()
	#test_data_cache()
	#test_tcp_async_client()
	#test_event_loop()
	#test_mysql_client()
	#test_gdp_client()
	#test_utils_str()
	#test_cache()
	#test_crontask()
	#test_pb_validator()
	#test_form_validator()
	#test_sqlalchemy_model()
	#test_ssdb()
	#test_asynctask()
	#test_django_model()
	#test_kafka_client()
	#test_gevent_utils()
	#test_client_pool()
	#test_local_client()
	#test_gwebservice()
	return

if __name__ == '__main__':
	unittest.main()
	#console_test()
