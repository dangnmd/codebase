from codebase_lib.managers.models import *
from codebase_lib.managers.cache_manager import simple_cache_data, key_cache_data, CACHE_KEY_FUNC_GET_USER_INFO, CACHE_KEY_FUNC_GET_UID_BY_GROUP

def get_display_name(first_name, last_name, user_name):
	if first_name and last_name:
		return "%s %s" % (first_name.title(), last_name.title())
	elif first_name:
		return first_name.title()
	elif last_name:
		return last_name.title()
	else:
		return user_name

def get_users_info(uids, fields):
	users = MeTripDB.User.objects.filter(id__in=uids).values(*fields)
	result = {}
	for user in users:
		result[user['id']] = user
	return result

@key_cache_data(**CACHE_KEY_FUNC_GET_USER_INFO)
def get_user_account_by_ids(uids):
	customer_records = MeTripDB.User.objects.filter(id__in=uids).all()
	return {item.id: item for item in customer_records}

@simple_cache_data(lambda cache_prefix, group_id: cache_prefix % group_id, **CACHE_KEY_FUNC_GET_UID_BY_GROUP)
def get_uids_by_group(group_id):
	uids = MeTripDB.UserGroupItem.objects.filter(group_id=group_id).values_list("uid", flat=True).all()
	return list(uids)

def update_account_status(uid, status):
	return MeTripDB.User.objects.filter(id=uid).update(status=status)

