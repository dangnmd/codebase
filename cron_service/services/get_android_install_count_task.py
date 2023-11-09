from codebase_lib.utils import *
from codebase_lib.managers.setting_manager import *
from google.cloud import storage
from google.oauth2 import service_account
import os
import csv
import codecs
from datetime import datetime, timedelta, date
from codebase_lib.config import ANDROID_GOOGLE_CLOUD_STORAGE_API
from common.utils import date_range


def get_android_install_count_task():
	android_install_count = AndroidInstallCount()
	android_install_count.run()


def get_monthly_install_count(month):
	filename = 'android_report.csv'
	final_url = ANDROID_GOOGLE_CLOUD_STORAGE_API['BASE_URL'] + str(month) + '_overview.csv'
	# start authorization process
	service_account.Credentials.from_service_account_file(ANDROID_GOOGLE_CLOUD_STORAGE_API['SERVICE_ACCOUNT_FILE'], scopes=ANDROID_GOOGLE_CLOUD_STORAGE_API['SCOPES'])
	os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ANDROID_GOOGLE_CLOUD_STORAGE_API['SERVICE_ACCOUNT_FILE']
	# Access google cloud storage bucket
	storage_client = storage.Client()
	bucket = storage_client.get_bucket(ANDROID_GOOGLE_CLOUD_STORAGE_API['BUCKET_NAME'])
	# Download report from bucket
	start_time = get_timestamp_ms()
	blob = bucket.blob(final_url)
	if not blob:
		elapsed = get_timestamp_ms() - start_time
		log.warn('get_android_install_count|elapsed=%s,unable_to_get_blob_from_the_bucket,date=%s', elapsed, month)
		return ''
	blob.download_to_filename(filename)
	elapsed = get_timestamp_ms() - start_time
	log.info('get_android_install_count|elapsed=%s,request_monthly_report_success,date=%s', elapsed, month)
	return filename

def get_install_count_by_file(file_name):
	# Decode file for reading
	csv_reader = csv.reader(codecs.open(file_name, 'rU', 'utf-16'))
	data_list = []
	# Each row in the file is represented as a list
	header_row = next(csv_reader)
	for row in csv_reader:
		data_date = row[0]
		cell_index = 2
		for cell in row[2::]:
			data_list.append({
				'date': data_date,
				'ref_type': header_row[cell_index],
				'count': cell,
				'client_type': ClientType.ANDROID
			})
			cell_index += 1
	return data_list

class AndroidInstallCount(object):
	def run(self):
		try:
			#dbmodel.get_db().refresh_db_connections()
			client_type = ClientType.ANDROID
			log.data("get_android_install_count|started")
			latest_updated_data = DnguyenDB.AppStats.objects.filter(client_type=client_type).order_by('-date').first()
			if not latest_updated_data:
				latest_update = date(2019, 1, 1)
			else:
				latest_update = latest_updated_data.date + timedelta(days=1)
			if latest_update >= datetime.now().date() + timedelta(days=-2):
				log.info("get_android_install_count|no_need_to_get_data,latest_update=%s", latest_updated_data.date)
				return
			reporting_month = latest_update.strftime("%Y%m")
			filedata = get_monthly_install_count(reporting_month)
			if not filedata:
				return
			data_list = get_install_count_by_file(filedata)
			if not data_list:
				return
			for item in data_list:
				if parse_string_to_date(item['date'], DATE_FORMAT).date() < latest_update:
					continue
				obj, created = DnguyenDB.AppStats.objects.update_or_create(
					defaults={
						'count': item.pop('count')
					},
					**item
				)
				if not obj:
					log.warn('get_android_install_count|failed_to_update_data,date=%s,client_type=%s,ref_type=%s,data=%s', item['date'], client_type, item['ref_type'], item['count'])
			log.data('get_android_install_count|end')
		except Exception as error:
			log.exception("get_android_install_count|except=%s", error)





