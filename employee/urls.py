from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

from django.urls import path
from .views import (login,UserListView,UserDetailView,upload)


urlpatterns = [
	# Page
	url(r'^$',login,name='login'),
	path('upload',upload,name='upload'),
	path('<int:pk>', UserDetailView.as_view(), name='employee-detail'),
]