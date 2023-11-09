from .models import *
from codebase_lib.utils import *
from common.utils import get_timestamp
import json


def add_async_task(async_data, async_type):
	async_task = MeTripExtDB.AsyncTask(
		type=async_type,
		status=AsyncTaskStatus.PENDING,
		data=json.dumps(async_data),
		retry_count=0,
		created_on=get_timestamp(),
		updated_on=get_timestamp()
	)
	async_task.save()
	log.info('add_async_task,type=%s,data=%s', async_type, async_data)
	return async_task


def add_async_tasks(async_tasks):
	if not async_tasks:
		return
	new_tasks = []
	for task in async_tasks:
		async_task = MeTripExtDB.AsyncTask(
			type=task['async_type'],
			status=AsyncTaskStatus.PENDING,
			data=json.dumps(task['async_data']),
			retry_count=0,
			created_on=get_timestamp(),
			updated_on=get_timestamp()
		)
		new_tasks.append(async_task)
	MeTripExtDB.AsyncTask.objects.bulk_create(new_tasks)
