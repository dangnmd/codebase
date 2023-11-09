from django.conf.urls import url
from .views import swagger

urlpatterns = [
	url(r'^api/swagger$', swagger.api_index),
	url(r'^s2s/swagger$', swagger.s2s_index),
]
