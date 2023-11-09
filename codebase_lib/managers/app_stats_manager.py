from datetime import date, timedelta

from codebase_lib.managers.mysql_models import *


MapRefType = {
	'deletions': '100F'
}

APP_STATS_REPORT_DATE_FORMAT = "%m/%d/%y"


def update_or_create_app_stats(item):
	return MeTripDB.AppStats.objects.update_or_create(
		defaults={
			'count': item.pop('count')
		},
		**item
	)
