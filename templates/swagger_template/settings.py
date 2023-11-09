import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'templates').replace('\\', '/')],
		'APP_DIRS': True,
		'OPTIONS': {},
	},
]
