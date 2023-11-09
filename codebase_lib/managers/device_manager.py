from codebase_lib.constants import CommonStatus
from codebase_lib.managers import async_task_manager, chat_manager
from codebase_lib.managers.push_app_manager import *
from datetime import datetime

def get_device_by_unique_id(unique_id):
	return MeTripDB.DeviceToken.objects.filter(unique_id=unique_id).first()

def register_token(token, app_id, client_type, client_version, unique_id, uid, city_id, language_id, latitude, longitude):
	if not token or not app_id or not client_type:
		return None
	device_token = get_device_by_unique_id(unique_id)
	register_token_info = {
		'old_token': '',
		'old_endpoint_arn': '',
		'new_token': token
	}
	update_device_token = {
		'token': token,
		'app_id': app_id,
		'client_type': client_type,
		'status': CommonStatus.ACTIVE,
		'uid': uid if uid else 0,
		'language_id': language_id,
		'city_id': city_id,
		'latitude': latitude,
		'longitude': longitude,
		'client_version': client_version,
		'updated_on': datetime.now()
	}
	if device_token:
		register_token_info['old_token'] = device_token.token
		register_token_info['old_endpoint_arn'] = device_token.aws_endpoint_arn
	where_clause = {'unique_id': unique_id}
	device_token, created = MeTripDB.DeviceToken.objects.update_or_create(defaults=update_device_token, **where_clause)
	uid = uid if uid else 0
	async_data = {
		'app_id': app_id,
		'client_type': client_type,
		'uid': uid,
		'device_id': device_token.id,
		'language_id': language_id,
		'register_token_info': register_token_info
	}
	async_task_manager.add_async_task(async_data, AsyncTaskType.REGISTER_PUSH_DEVICE_TOKEN)
	chat_manager.update_user_token(uid, client_type, token)
	return device_token

def update_settings(app_id, client_type, unique_id, receive_push):
	device_token = MeTripDB.DeviceToken.objects.filter(unique_id=unique_id, client_type=client_type, app_id=app_id).first()
	if not device_token:
		return None
	device_token.receive_push = receive_push
	device_token.updated_on = datetime.now()
	device_token.save()
	if not receive_push:
		chat_manager.update_user_token(0, client_type, device_token.token)
	else:
		chat_manager.update_user_token(device_token.uid, client_type, device_token.token)
	return device_token



