from django.contrib.auth.models import User
from social.exceptions import AuthForbidden

def load_user(uid, *args, **kwargs):
	try:
		user = User.objects.get(email=uid)
		return {'user': user}
	except:
		raise AuthForbidden(kwargs['backend'])
