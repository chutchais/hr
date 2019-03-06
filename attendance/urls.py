from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from . import views
from .views import (AttendanceFileListView,AttendanceFileCreate,
					AttendanceFileDeleteView,AttendanceFileDetailView,
					process_file)

urlpatterns = [
	path('', AttendanceFileListView.as_view(), name='list'),
	path('upload', AttendanceFileCreate.as_view(), name='upload'),
	path('<slug:pk>', AttendanceFileDetailView.as_view(), name='detail'),
	path('<slug:pk>/process', process_file, name='process'),
	path('<slug:pk>/delete', AttendanceFileDeleteView.as_view(), name='delete'),
   	]