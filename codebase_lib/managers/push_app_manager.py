from common.utils import *
from .models import *
from codebase_lib.constants import AsyncTaskStatus, AsyncTaskType, CommonStatus
import json
from codebase_lib.aws_service import SNSClient
from codebase_lib.managers import setting_manager, async_task_manager, localization_manager, common_manager
from codebase_lib.managers.cache_manager import simple_cache_data, CACHE_KEY_GET_PUSH_TOPIC_BY_CODE
from datetime import datetime
from codebase_lib.utils import datetime_to_string, DATETIME_FORMAT_MS, build_push_payload, build_message_attribulte
from codebase_lib.constants import *
from common import faktory
from common.faktory import  worker
from common.faktory._proto import *
from common import logger
import random
import time
from codebase_lib.managers.faktory_manager import FaktoryClient
from codebase_lib.constants import FaktoryJobType


push_notification_faktory_client = FaktoryClient(FaktoryJobType.PUSH_NOTIFICATION)

sns_client = SNSClient(config.AWS_SNS_CONFIG)

@simple_cache_data(lambda cache_prefix, code:  cache_prefix % (code), **CACHE_KEY_GET_PUSH_TOPIC_BY_CODE)
def get_topic(code):
	topic = MeTripDB.SnsTopic.objects.filter(code=code).values('code', 'topic_arn').first()
	if not topic:
		log.warn('sns_topic|not_existed,code=%s', code)
		return None
	return topic

def get_aws_platform_arn(app_id, client_type):
	platform_arn = MeTripDB.DevicePlatform.objects.filter(app_id=app_id, client_type=client_type, status=CommonStatus.ACTIVE).values('aws_arn').first()
	if platform_arn:
		return platform_arn['aws_arn']
	return ''


def get_news_topic():
	new_topic_code = setting_manager.get_setting(setting_manager.SettingKey.PUSH_NEW_TOPIC_NAME, setting_manager.SettingKeyDefault.PUSH_NEW_TOPIC_NAME)
	return get_topic(new_topic_code)

def push_to_endpoint(endpoint_arn, push_data, message_attributes):
	if not push_data:
		return 'empty_push_data'
	try:
		result = sns_client.publish(endpoint_arn, push_data, message_attributes)
		log.info('push_to_endpoint,result=%s', result)
		return
	except Exception as ex:
		log.exception('push_to_endpoint_failed,exception=%s,endpoint=%s,push_data=%s', ex, endpoint_arn, push_data)
		if 'EndpointDisabled' in ex.message:
			MeTripDB.SnsTopicSubscribe.objects.filter(endpoint_arn=endpoint_arn).delete()
			MeTripDB.DeviceToken.objects.filter(aws_endpoint_arn=endpoint_arn).delete()
			log.info('device_token|deleted,endpoint_arn=%s', endpoint_arn)
			sns_client.delete_endpoint(endpoint_arn)
			log.info('device_token|deleted_aws_endpoint_arn=%s', endpoint_arn)
		return ex.message

def register_platform_endpoint(register_info):
	if not register_info:
		log.warn('register_platform_endpoint|empty_register_info')
		return None
	register_token_info = register_info['register_token_info']
	device_id = register_info['device_id']
	app_id = register_info['app_id']
	client_type = register_info['client_type']
	uid = register_info.get('uid', 0)
	language_id = register_info.get('language_id', 0)
	if not register_token_info['new_token']:
		log.warn('register_platform_endpoint|device_id=%s,empty_device_token', device_id)
		return None
	update_device_token = {}
	token = register_token_info['new_token']
	aws_endpoint_arn = get_endpoint_arn(device_id)
	update_needed = False
	create_needed = False if aws_endpoint_arn else True
	custom_user_data = json.dumps({'uid': uid, 'update_time': datetime_to_string(datetime.now(), DATETIME_FORMAT_MS)})
	if create_needed:
		aws_endpoint_arn = create_platform_endpoint(app_id, client_type, token, custom_user_data)
		create_needed = False
		if not aws_endpoint_arn:
			return None
	try:
		platform_endpoint = sns_client.get_platform_endpoint(aws_endpoint_arn)
		change_custom_user_data = platform_endpoint.attributes['CustomUserData'] != json.dumps(custom_user_data)
		if platform_endpoint.attributes['Token'] != token or platform_endpoint.attributes['Enabled'] != 'true' or change_custom_user_data:
			update_needed = True
	except Exception as error:
		create_needed = True
	if create_needed:
		aws_endpoint_arn = create_platform_endpoint(app_id, client_type, token, custom_user_data)
		if not aws_endpoint_arn:
			return None
	if update_needed:
		platform_endpoint = sns_client.get_platform_endpoint(aws_endpoint_arn)
		update_attributes = {
			'Token': token,
			'Enabled': 'true',
			'CustomUserData': custom_user_data

		}
		platform_endpoint.set_attributes(Attributes=update_attributes)
		log.info('register_platform_endpoint|device_id=%s,update_attributes,endpoint_arn=%s', device_id, aws_endpoint_arn)
	update_device_token['aws_endpoint_arn'] = aws_endpoint_arn
	update_device_token['token'] = token
	update_device_token['updated_on'] = datetime.now()
	MeTripDB.DeviceToken.objects.filter(id=device_id).update(**update_device_token)
	if register_token_info['old_endpoint_arn'] and register_token_info['old_endpoint_arn'] != aws_endpoint_arn:
		delete_application_endpoint(register_token_info['old_endpoint_arn'])
		log.info('register_platform_endpoint|device_id=%s,delete_old_platform_endpoint_success,endpoint_arn=%s', device_id, register_token_info['old_endpoint_arn'])
	subscribe_to_news_topic(device_id, aws_endpoint_arn, client_type, language_id)
	return aws_endpoint_arn

def subscribe_to_news_topic(device_id, aws_endpoint_arn, client_type, language_id):
	topic = get_news_topic()
	if not topic:
		log.warn('register_endpoint_platform|device_id=%s,success,but_no_news_topic_to_subscribe', device_id)
		return True
	# attributes = {
	# 	'client_type': [str(client_type)],
	# 	'language_id': [str(language_id)]
	# }
	subscribe_endpoint_to_topic(topic['code'], topic['topic_arn'], device_id, aws_endpoint_arn, {})
	log.info('register_endpoint_platform|device_id=%s,success,subscribed_to_topic=%s', device_id, topic['topic_arn'])

def get_endpoint_arn(device_id):
	device_token = MeTripDB.DeviceToken.objects.filter(id=device_id).first()
	if not device_token:
		return None
	return device_token.aws_endpoint_arn

# def add_push_to_endpoint_task(endpoint_arn, push_data):
# 	data = {
# 		'endpoint_arn': endpoint_arn,
# 		'push_data': push_data
# 	}
# 	new_task = MeTripExtDB.QueuedNotification(
# 		type=NotifyType.NEWS,
# 		status=AsyncTaskStatus.PENDING,
# 		data=json.dumps(data),
# 		retry_count=0,
# 		created_on=get_timestamp(),
# 		updated_on=get_timestamp()
# 	)
# 	new_task.save()

def create_platform_endpoint(app_id, client_type, device_token, custom_user_data='', attributes={}):
	platform_arn = get_aws_platform_arn(app_id, client_type)
	if not platform_arn:
		log.warn('register_platform_endpoint|failed,no_platform_arn,app_id=%s,client_type=%s,token=%s', app_id, client_type, device_token)
		return None
	try:
		reply = sns_client.create_platform_application_endpoint(platform_arn, device_token, custom_user_data, attributes)
		if not reply:
			log.warn('create_platform_endpoint|failed,platform_arn=%s,device_token=%s,custom_user_data=%s,attributes=%s', platform_arn, device_token, custom_user_data, attributes)
			return None
		return reply['EndpointArn']
	except Exception as error:
		log.exception('create_platform_endpoint|error=%s,platform_arn=%s,device_token=%s,custom_user_data=%s,attributes=%s', error, platform_arn, device_token, custom_user_data, attributes)
		return None

def delete_application_endpoint(endpoint_arn):
	deleted_rows, deleted_obj = MeTripDB.DeviceToken.objects.filter(aws_endpoint_arn=endpoint_arn).delete()
	log.info('delete_endpoint|endpoint=%s,rows=%s', endpoint_arn, deleted_rows)
	sns_client.delete_endpoint(endpoint_arn)
	subscriptions = MeTripDB.SnsTopicSubscribe.objects.filter(endpoint_arn=endpoint_arn).all()
	if subscriptions:
		for sub in subscriptions:
			sns_client.unsubscribe(sub.subscription_arn)
		MeTripDB.SnsTopicSubscribe.objects.filter(endpoint_arn=endpoint_arn).delete()

def set_subscription_attributes(topic_code, endpoint_arn, attributes):
	subscription = MeTripDB.SnsTopicSubscribe.objects.filter(topic_code=topic_code, endpoint_arn=endpoint_arn).first()
	if not subscription:
		return None
	sns_client.subscription_set_attributes(subscription.subscription_arn, attributes)
	return subscription.subscription_arn

def subscribe_endpoint_to_topic(topic_code, topic_arn, device_id, endpoint_arn, attributes={}):
	subscription_arn = set_subscription_attributes(topic_code, endpoint_arn, attributes)
	if not subscription_arn:
		filter_policy = {}
		if attributes:
			filter_policy = {
				'FilterPolicy': json.dumps(attributes)
			}
		result = sns_client.subscribe(topic_arn, "application", endpoint_arn, filter_policy)
		subscription_arn = result['SubscriptionArn']
		subscription = MeTripDB.SnsTopicSubscribe(
			topic_code=topic_code,
			topic_arn=topic_arn,
			device_id=device_id,
			endpoint_arn=endpoint_arn,
			subscription_arn=subscription_arn,
			attributes=attributes,
			created_on=datetime.now(),
			updated_on=datetime.now()
		)
		subscription.save()
	return subscription_arn

def publish_to_topic(topic_arn, push_data, message_attributes={}):
	if not push_data:
		return 'empty_push_data'
	try:
		result = sns_client.publish_to_topic(topic_arn, push_data, message_attributes)
		return result
	except Exception as ex:
		log.exception('publish_to_topic_failed,topic=%s,push_data=%s,exception=%s', topic_arn, push_data, ex)
		return ex.message

def publish_news(new_id, message, uri, track_id, time_to_live=0, message_filters=None, uid=0, user_group_id=0):
	push_data = build_push_payload(message, uri, track_id, NotifyType.NEWS, new_id)
	message_attributes = build_message_attribulte(time_to_live)
	if not uid and not user_group_id:
		news_topic = get_news_topic()
		if not news_topic:
			log.warn('publish_news|invalid_news_topic')
			return
		return publish_to_topic(news_topic['topic_arn'], push_data, message_attributes)
	uids = set()
	if uid:
		uids.add(uid)
	if user_group_id:
		group = MeTripDB.UserGroup.objects.filter(id=user_group_id, status=CommonStatus.ACTIVE).first()
		if group:
			group_uids = MeTripDB.UserGroupItem.objects.filter(group_id=user_group_id).values_list('uid', flat=True)[:1000]
			if group_uids:
				for uid in group_uids:
					uids.add(uid)
	if not uids:
		log.warn('publish_news|exit_without_push_to_any_users,message=%s,uid=%s,user_group_id=%s', message, uid, user_group_id)
		return
	return push_message_to_users(uids, message, uri, NotifyType.NEWS, new_id, track_id, ttl=time_to_live)

def push_message_to_users(uids, message, uri, notify_type, notify_id, track_id='', ttl=0):
	if not uids:
		log.warn('push_message_to_users,invalid_uids=%s', uids)
		return
	devices = MeTripDB.DeviceToken.objects.filter(uid__in=uids, status=CommonStatus.ACTIVE, receive_push=1).values('id', 'aws_endpoint_arn', 'client_type', 'language_id')
	if not devices:
		log.warn('push_message_to_users,do_not_have_any_devices,uids=%s', uids)
		return
	endpoints = []
	for device in devices:
		endpoints.append(device['aws_endpoint_arn'])
	push_message_to_enpoints(endpoints, message, uri, notify_type, notify_id, track_id, ttl)

def push_message_to_devices(devices, message, uri, notify_type, notify_id, track_id='', ttl=0):
	if not devices:
		log.warn('push_message_to_devices,invalid_devices=%s', devices)
		return
	devices = MeTripDB.DeviceToken.objects.filter(unique_id__in=devices, status=CommonStatus.ACTIVE, receive_push=1).values('id', 'aws_endpoint_arn', 'client_type', 'language_id')
	if not devices:
		log.warn('push_message_to_devices,do_not_have_any_devices,uids=%s', devices)
		return
	endpoints = []
	for device in devices:
		endpoints.append(device['aws_endpoint_arn'])
	push_message_to_enpoints(endpoints, message, uri, notify_type, notify_id, track_id, ttl)

def add_queue_notification(data, type):
	task = MeTripExtDB.QueuedNotification(
		type=type,
		status=NotifyStatus.PENDING,
		data=json.dumps(data),
		retry_count=0,
		created_on=datetime.now(),
		updated_on=datetime.now()
	)
	task.save()
	log.info('add_async_task,type=%s,data=%s', type, data)
	return task

def push_message_to_enpoints(endpoints, message, uri, notify_type, notify_id, track_id='', ttl=0):
	if not endpoints:
		log.warn('push_message_to_enpoints,no_endpoints')
		return
	message = strip_html(message)
	payload = build_push_payload(message, uri, track_id, notify_type, notify_id)

	for endpoint in endpoints:
		push_data = {
			'endpoint_arn': endpoint,
			'push_data': payload,
			'ttl': ttl
		}

		new_queue = add_queue_notification(push_data, notify_type)
		if not new_queue:
			log.warn('push_message_to_enpoints,can_not_create_queue,push_data=%s', push_data)
			return
		queue_args = [new_queue.id, 0]
		push_notification_faktory_client.add_queues([queue_args])

def push_message_to_user(uid, uri, message_format, message_args, track_id, notify_type, notify_id):
	devices = MeTripDB.DeviceToken.objects.filter(uid=uid, status=CommonStatus.ACTIVE, receive_push=1).values('id', 'aws_endpoint_arn', 'client_type', 'language_id')
	if devices:
		messages_dict = {}
		for device in devices:
			language_id = device['language_id']
			if language_id not in messages_dict:
				format_message = localization_manager.get_locale(message_format, common_manager.get_language_code_by_id(language_id))
				push_message = format_message % tuple(message_args)
				push_message = strip_html(push_message)
				messages_dict[language_id] = {'message': push_message, 'endpoints': []}
			messages_dict[language_id]['endpoints'].append(device['aws_endpoint_arn'])
		for language_id, message in list(messages_dict.items()):
			push_message_to_enpoints(message['endpoints'], message['message'], uri, notify_type, notify_id, track_id)
