import boto3
import json
from codebase_lib.utils import log

class SNSClient(object):

	def __init__(self, config):
		self.sns_client = boto3.client(
			'sns',
			aws_access_key_id=config['ACCESS_KEY'],
			aws_secret_access_key=config['SECRET_KEY'],
			region_name=config['REGION']
		)
		self.sns_resource = boto3.resource(
			'sns',
			aws_access_key_id=config['ACCESS_KEY'],
			aws_secret_access_key=config['SECRET_KEY'],
			region_name=config['REGION']
		)

	def publish(self, endpoint_arn, push_data, message_attributes=None):
		if message_attributes:
			return self.sns_client.publish(TargetArn=endpoint_arn, Message=json.dumps(push_data), MessageStructure='json', MessageAttributes=message_attributes)
		else:
			return self.sns_client.publish(TargetArn=endpoint_arn, Message=json.dumps(push_data), MessageStructure='json')

	def create_platform_application_endpoint(self, platform_arn, token, custom_user_data=None, attributes=None):
		return self.sns_client.create_platform_endpoint(PlatformApplicationArn=platform_arn, Token=token, CustomUserData=custom_user_data, Attributes=attributes)

	def delete_endpoint(self, endpoint_arn):
		self.sns_client.delete_endpoint(EndpointArn=endpoint_arn)
		log.info('delete_aws_endpoint|endpoint=%s', endpoint_arn)

	def subscribe(self, topic_arn, protocol, endpoint_arn, attributes):
		return self.sns_client.subscribe(TopicArn=topic_arn, Protocol=protocol, Endpoint=endpoint_arn, Attributes=attributes, ReturnSubscriptionArn=True)

	def publish_to_topic(self, topic_arn, push_data, message_attributes):
		log.info('publish_to_topic|topic_arn=%s,push_data=%s,message_attrs=%s', topic_arn, push_data, message_attributes)
		if message_attributes:
			return self.sns_client.publish(TopicArn=topic_arn, Message=json.dumps(push_data), MessageStructure='json', MessageAttributes=message_attributes)
		return self.sns_client.publish(TopicArn=topic_arn, Message=json.dumps(push_data), MessageStructure='json')

	def subscription_set_attributes(self, subscription_arn, attributes):
		self.sns_client.set_subscription_attributes(SubscriptionArn=subscription_arn, AttributeName="FilterPolicy", AttributeValue=json.dumps(attributes))

	def unsubscribe(self, subscription_arn):
		subscription = self.sns_resource.Subscription(subscription_arn)
		subscription.delete()
		log.info('delete_aws_subscription|subscription=%s', subscription_arn)

	def get_platform_endpoint(self, endpoint_arn):
		return self.sns_resource.PlatformEndpoint(endpoint_arn)

class SQSClient(object):

	def __init__(self, config):
		self.sqs_client = boto3.client(
			'sqs',
			aws_access_key_id=config['ACCESS_KEY'],
			aws_secret_access_key=config['SECRET_KEY'],
			region_name=config['REGION']
		)

	def get_messages(self, queue_url):
		max_number_of_messages = 10
		visibility_timeout = 10
		wait_time_seconds = 10
		sqs_messages = self.sqs_client.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=max_number_of_messages, VisibilityTimeout=visibility_timeout, WaitTimeSeconds=wait_time_seconds)
		return sqs_messages

	def delete_message(self, queue_url, receipt_handle):
		self.sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
