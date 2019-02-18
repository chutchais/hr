from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from . import views
from .views import (WorkingListView,WorkingSectionListView,WorkingCreate,WorkingUpdate,WorkingDelete,
					WorkingStatusListView,ProcessWorking)

urlpatterns = [
    # url(r'^$', WorkingListView.as_view(), name='list'),
   	path('working/', WorkingListView.as_view(), name='list'),
    path('working/<slug:section>/<slug:en>/add', WorkingCreate.as_view(), name='add'),
    path('working/<int:pk>', WorkingUpdate.as_view(), name='detail'),
    path('working/<slug:pk>/delete', WorkingDelete.as_view(), name='delete'),
    path('working/<slug:pk>/process/<slug:action>', ProcessWorking, name='process'),
    path('working/<slug:department>', WorkingListView.as_view(), name='department-list'),
    path('status/<slug:status>', WorkingStatusListView.as_view(), name='status-list'),

]