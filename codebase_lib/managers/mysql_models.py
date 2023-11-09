from codebase_lib import config
from common import dbmodel

db = dbmodel.get_db()
if not db:
	db = dbmodel.init_db(config.DATABASE_BACKEND, None)
models = db

class DnguyenDB:
	class DnguyenDBConfig:
		class Config:
			db_for_read = 'dnguyen_db.slave'
			db_for_write = 'dnguyen_db.master'

	class D_User(DnguyenDBConfig, db.Model):
		id = models.BigAutoField(primary_key=True)
		name = models.CharField(max_length=250)

		class Meta:
			managed = False
			db_table = 'user'

	# class AppStats(DnguyenDBConfig, db.Model):
	# 	id = db.BigAutoField(primary_key=True)
	# 	client_type = db.IntegerField()
	# 	date = db.DateTimeField()
	# 	count = db.IntegerField()
	# 	ref_type = db.CharField(max_length=3)
	#
	# 	class Meta:
	# 		managed = False
	# 		db_table = 'app_stats'

class MeTripDB:
	class MeTripDBConfig:
		class Config:
			db_for_read = 'metrip_db.slave'
			db_for_write = 'metrip_db.master'

	class App(MeTripDBConfig, db.Model):
		app_id = db.PositiveIntegerField(primary_key=True)
		app_name = db.CharField(max_length=64)
		session_key = db.CharField(max_length=128)
		# access_key = db.CharField(max_length=128)
		token_exchange_time = db.PositiveIntegerField()
		token_session_time = db.PositiveIntegerField()
		type = db.PositiveIntegerField()
		flag = db.PositiveBigIntegerField()
		description = db.CharField(max_length=1024)
		created_on = db.DateTimeField()
		updated_on = db.DateTimeField()

		class Meta:
			db_table = 'app'

	class AppApi(MeTripDBConfig, db.Model):
		id = db.PositiveBigAutoField(primary_key=True)
		service_id = db.PositiveIntegerField()
		ip = db.CharField(max_length=64)
		api = db.CharField(max_length=128)
		memo = db.CharField(max_length=256)
		created_on = db.DateTimeField()

		class Meta:
			db_table = 'app_api'

	class AppServiceMapping(MeTripDBConfig, db.Model):
		id = db.IntegerField(primary_key=True)
		app_id = db.IntegerField()
		service_id = db.IntegerField()
		client_type = db.IntegerField()
		min_client_version = db.IntegerField()
		access_key = db.CharField(max_length=128)
		status = db.IntegerField()

		class Meta:
			managed = False
			db_table = 'app_service_mapping'
			unique_together = (('min_client_version', 'service_id', 'client_type', 'app_id'),)

	class Setting(MeTripDBConfig, db.Model):
		id = db.BigIntegerField(primary_key=True)
		name = db.CharField(max_length=200)
		value = db.CharField(max_length=500)
		updated_by = db.BigIntegerField()
		updated_on = db.DateTimeField()

		class Meta:
			managed = False
			db_table = 'setting'

	class DevicePlatform(models.Model):
		id = models.IntegerField(primary_key=True)
		app_id = models.IntegerField()
		client_type = models.IntegerField()
		name = models.CharField(max_length=100)
		aws_arn = models.CharField(max_length=250)
		status = models.IntegerField()
		created_on = models.DateTimeField()
		updated_on = models.DateTimeField()

		class Meta:
			managed = False
			db_table = 'device_platform'

	class DeviceToken(models.Model):
		id = models.BigAutoField(primary_key=True)
		token = models.CharField(max_length=250)
		app_id = models.IntegerField()
		client_type = models.IntegerField()
		client_version = models.IntegerField()
		unique_id = models.CharField(max_length=200)
		status = models.IntegerField()
		receive_push = models.IntegerField(default=1)
		uid = models.BigIntegerField(blank=True, null=True)
		city_id = models.IntegerField(blank=True, null=True)
		language_id = models.IntegerField(blank=True, null=True)
		aws_endpoint_arn = models.CharField(max_length=250)
		latitude = db.DecimalField(max_digits=18, decimal_places=12, default=0, null=False)
		longitude = db.DecimalField(max_digits=18, decimal_places=12, default=0, null=False)
		created_on = models.DateTimeField(auto_now_add=True)
		updated_on = models.DateTimeField(auto_now_add=True)

		class Meta:
			managed = False
			db_table = 'device_token'

	class SnsTopic(models.Model):
		code = models.CharField(primary_key=True, max_length=100)
		topic_arn = models.CharField(max_length=200)
		attributes = models.TextField()
		created_on = models.DateTimeField(auto_now_add=True)

		class Meta:
			managed = False
			db_table = 'sns_topic'

	class SnsTopicSubscribe(models.Model):
		id = models.BigAutoField(primary_key=True)
		topic_code = models.CharField(max_length=100)
		topic_arn = models.CharField(max_length=200)
		device_id = models.BigIntegerField()
		endpoint_arn = models.CharField(max_length=200)
		subscription_arn = models.CharField(max_length=200)
		attributes = models.TextField()
		created_on = models.DateTimeField()
		updated_on = models.DateTimeField()

		class Meta:
			managed = False
			db_table = 'sns_topic_subscribe'

	class UserGroup(MeTripDBConfig, db.Model):
		id = db.AutoField(primary_key=True)
		name = db.CharField(unique=True, max_length=100)
		status = db.IntegerField()
		description = db.CharField(max_length=200, blank=True, null=True)
		created_by = db.BigIntegerField()
		created_on = db.DateTimeField()
		updated_by = db.BigIntegerField()
		updated_on = db.DateTimeField()

		class Meta:
			managed = False
			db_table = 'user_group'

	class UserGroupItem(MeTripDBConfig, db.Model):
		id = db.AutoField(primary_key=True)
		group_id = db.IntegerField()
		uid = db.BigIntegerField()

		class Meta:
			managed = False
			db_table = 'user_group_item'
			unique_together = (('group_id', 'uid'),)

	# class AppStats(MeTripDBConfig, db.Model):
	# 	id = db.BigAutoField(primary_key=True)
	# 	client_type = db.IntegerField()
	# 	date = db.DateTimeField()
	# 	count = db.IntegerField()
	# 	ref_type = db.CharField(max_length=3)
	#
	# 	class Meta:
	# 		managed = False
	# 		db_table = 'app_stats'

	class User(MeTripDBConfig, db.Model):
		id = db.BigAutoField(primary_key=True)
		username = db.CharField(unique=True, max_length=128)
		email = db.CharField(unique=True, max_length=128, null=True)
		password = db.CharField(max_length=50, blank=True, null=True)
		password_salt = db.CharField(max_length=10, blank=True, null=True)
		status = db.IntegerField(default=1)
		last_login_time = db.DateTimeField(blank=True, null=True)
		last_activity_time = db.DateTimeField(blank=True, null=True)
		last_ip_address = db.CharField(max_length=128, blank=True, null=True)
		language_id = db.IntegerField(default=1)
		created_on = db.DateTimeField()
		first_name = db.CharField(max_length=512, blank=True, null=True)
		last_name = db.CharField(max_length=512, blank=True, null=True)
		gender = db.IntegerField(default=0)
		birthday = db.DateTimeField(blank=True, null=True)
		avatar = db.CharField(max_length=200, blank=True, null=True)
		address = db.CharField(max_length=1024, blank=True, null=True)
		city_id = db.IntegerField(default=0)
		district_id = db.IntegerField(default=0)
		ward_id = db.IntegerField(default=0)
		total_views = db.IntegerField(default=0)
		total_reviews = db.IntegerField(default=0)
		total_pictures = db.IntegerField(default=0)
		total_checkin = db.IntegerField(default=0)
		total_points = db.IntegerField(default=0)
		app_id = db.IntegerField()
		auto_update_social_avatar = db.BooleanField(default=True)
		account_activation_token = db.CharField(max_length=128)
		birthday = db.DateTimeField(blank=True, null=True)
		login_type = db.IntegerField(default=0)
		client_type = db.IntegerField(default=0)
		client_version = db.IntegerField(default=0)
		cover = db.CharField(max_length=200, blank=True, null=True)
		total_plans = db.IntegerField(default=0)
		total_followings = db.IntegerField(default=0)
		total_followers = db.IntegerField(default=0)
		bio = db.CharField(max_length=500, blank=True, null=True)

		class Meta:
			managed = False
			db_table = 'user'

# -------------------------------------------------------------------------
# extend DB
# -------------------------------------------------------------------------

class MeTripExtDB:
	class MeTripExtDBConfig:
		class Config:
			db_for_read = 'metrip_ext_db.slave'
			db_for_write = 'metrip_ext_db.master'

	class EmailAccount(MeTripExtDBConfig, db.Model):
		id = db.IntegerField(primary_key=True)
		email = db.CharField(max_length=50)
		display_name = db.CharField(max_length=50)
		host = db.CharField(max_length=100, blank=True, null=True)
		port = db.CharField(max_length=5, blank=True, null=True)
		username = db.CharField(max_length=100, blank=True, null=True)
		password = db.CharField(max_length=100, blank=True, null=True)
		ssl_enabled = db.IntegerField()
		use_default_credential = db.IntegerField()

		class Meta:
			managed = False
			db_table = 'email_account'

	class QueuedEmail(MeTripExtDBConfig, db.Model):
		id = db.BigAutoField(primary_key=True)
		to_email = db.CharField(max_length=100)
		from_email = db.CharField(max_length=200)
		priority = db.IntegerField()
		created_on = db.DateTimeField(auto_now_add=True)
		sent_on = db.DateTimeField(blank=True, null=True)
		retry_count = db.IntegerField(default=0)
		status = db.IntegerField(default=1)
		to_name = db.CharField(max_length=200, blank=True, null=True)
		from_name = db.CharField(max_length=200)
		subject = db.CharField(max_length=200)
		body = db.TextField()
		cc = db.CharField(max_length=200, blank=True, null=True)
		bcc = db.CharField(max_length=200, blank=True, null=True)
		email_account_id = db.IntegerField()
		plain_text = db.TextField()
		result = db.CharField(max_length=500)
		last_try_on = db.DateTimeField(blank=True, null=True)

		class Meta:
			managed = False
			db_table = 'queued_email'

	class AsyncTask(MeTripExtDBConfig, db.Model):
		id = db.BigAutoField(primary_key=True)
		type = db.IntegerField()
		status = db.IntegerField(default=1)
		retry_count = db.IntegerField(default=0)
		data = db.TextField()
		created_on = db.IntegerField()
		updated_on = db.IntegerField()
		result = db.TextField()
		scheduled = db.DateTimeField(auto_now_add=True)

		class Meta:
			managed = False
			db_table = 'async_task'

	class QueuedNotification(MeTripExtDBConfig, db.Model):
		id = db.BigAutoField(primary_key=True)
		type = db.IntegerField()
		status = db.IntegerField(default=1)
		retry_count = db.IntegerField(default=0)
		data = db.TextField()
		created_on = db.DateTimeField()
		updated_on = db.DateTimeField()
		sent_on = db.DateTimeField()
		result = db.TextField()

		class Meta:
			managed = False
			db_table = 'queued_notification'

