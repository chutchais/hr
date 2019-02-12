from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

from .views import (login)


urlpatterns = [
	# Page
	url(r'^$',login,name='login'),
]