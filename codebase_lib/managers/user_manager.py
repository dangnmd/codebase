from django.db.models import Q
import uuid
from django.db import transaction, IntegrityError
from django.db.models import Count
import random
from common.logger import log
from codebase_lib import config
from codebase_lib.constants import *
from codebase_lib.managers import setting_manager, encrypt_manager, async_task_manager
from codebase_lib.utils import *
from codebase_lib import image_service
from codebase_lib.services.user_service import *

def get_user_auth_info_by_uid(uid):
	if not uid:
		return None
	user_infos = get_user_account_by_ids([uid])
	user_info = None
	if user_infos:
		user_info = user_infos[uid]
	if not user_info:
		return None
	data = {
		"uid": user_info.id,
		"email": user_info.email,
		"username": user_info.username,
		"salt": user_info.password_salt,
		"status": user_info.status
	}
	return data
