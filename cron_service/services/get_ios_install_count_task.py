from codebase_lib.utils import *
from codebase_lib.managers.setting_manager import *

from datetime import datetime, timedelta, date
import csv
from codebase_lib.config import APPLE_CONNECT_API
from common.utils import date_range
import appstoreconnect


def get_ios_install_count_task():
	apple_install_count = AppleInstallCount()
	apple_install_count.run()


def get_installed_count(reporting_date):
	report_file = "ios_report.csv"
	apple_connect_api = appstoreconnect.Api(APPLE_CONNECT_API['APP_STORE_KEY_ID'], APPLE_CONNECT_API['STORE_AUTH_KEY'], APPLE_CONNECT_API['ISSUER_ID'])
	apple_connect_api.download_sales_and_trends_reports(
		filters={'vendorNumber': APPLE_CONNECT_API['VENDOR_NUMBER'], 'frequency': 'DAILY', 'reportDate': str(reporting_date)}, save_to=report_file)
	# read and extract data from csv file
	with open(report_file) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter="\t")
		line_count = 0
		data_dict = {}
		for row in csv_reader:
			if line_count == 0:
				line_count += 1
				continue
			try:
				line_count += 1
				# log.info(row[0])
				#data = row[0].split("\t")
				product_type = row[6]  # 7F, 1F
				units = row[7]
				if product_type not in data_dict:
					data_dict[product_type] = 0
				data_dict[product_type] += int(units)
			except Exception as ex:
				log.warn('get_installed_count|date=%s,data=%s,ex=%s', reporting_date, row[0], str(ex))
	return data_dict


class AppleInstallCount(object):

	def run(self):
		try:
			#dbmodel.get_db().refresh_db_connections()
			client_type = ClientType.IOS
			log.data("get_ios_install_count|started")
			latest_updated_data = DnguyenDB.AppStats.objects.filter(client_type=client_type).order_by('-date').first()
			if not latest_updated_data:
				start_date = datetime.now().date() - timedelta(days=365)
			else:
				start_date = latest_updated_data.date + timedelta(days=1)
			max_request_days = APPLE_CONNECT_API['MAX_REQUESTS_PER_CRON_TASK']
			end_date = min((start_date + timedelta(days=max_request_days)), datetime.now().date() + timedelta(-1))
			total_success = 0
			for single_date in date_range(start_date, end_date):
				date_to_get_report = single_date
				data_dict = get_installed_count(date_to_get_report)
				if not data_dict:
					continue
				for data_key, count in data_dict.items():
					obj, created = DnguyenDB.AppStats.objects.update_or_create(
						defaults={
							'count': count
						},
						ref_type=data_key,
						date=date_to_get_report,
						client_type=client_type
					)
					if not obj:
						log.warn('get_ios_install_count|failed_to_update_data,date=%s,client_type=%s,ref_type=%s,data=%s', date_to_get_report, client_type, data_key,count)
				total_success += 1
			log.data('get_ios_install_count|end,total_request=%s,success=%s,start_date=%s,end_date=%s', max_request_days, total_success, start_date, end_date)

		except Exception as error:
			log.exception("get_ios_install_count|except=%s", error)




