from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from . import views
from .views import (WorkingListView,WorkingSectionListView,WorkingCreate,WorkingUpdate,WorkingDelete,
					WorkingStatusListView,ProcessWorking,import_working_data,confirm_working,
                    WorkingSectionListView,WorkingSectionDetailView,export_working_xls,
                    WorkingSectionMonthlyView,WorkingSectionDailyListView,deleteWorking,export_working_csv,
                    actionWorking)

urlpatterns = [
    # url(r'^$', WorkingListView.as_view(), name='list'),
   	path('working/', WorkingListView.as_view(), name='list'),
   	
    path('working/confirm', confirm_working, name='confirm'),
    path('working/<slug:section>/<slug:en>/add', WorkingCreate.as_view(), name='add'),
    
    path('working/<int:pk>', WorkingUpdate.as_view(), name='detail'),
    path('working/<slug:pk>/delete', WorkingDelete.as_view(), name='delete'),
    path('working/<slug:pk>/process/<slug:action>', ProcessWorking, name='process'),
    
    path('status/<slug:status>', WorkingStatusListView.as_view(), name='status-list'),

    path('working/department/<slug:department>', WorkingListView.as_view(), name='department-list'),

    path('working/section', WorkingSectionListView.as_view(), name='section-list'),
    path('working/section/<slug:section>', WorkingSectionMonthlyView.as_view(), name='section-detail'),
    path('working/section/<slug:section>/<slug:status>',WorkingStatusListView.as_view(), name='section-status'),
    path('working/section/<slug:section>/<int:year>/<int:month>', WorkingSectionMonthlyView.as_view(), name='section-monthly'),
    path('working/section/<slug:section>/<int:year>/<int:month>/<int:day>', WorkingSectionDailyListView.as_view(), name='section-daily'),
    path('working/section/<slug:section>/<int:year>/<int:month>/<int:day>/delete', deleteWorking, name='section-daily-delete'),
    path('working/section/<slug:section>/<int:year>/<int:month>/<int:day>/process/<slug:action>', actionWorking, name='section-daily-action'),
    path('working/section/<slug:section>/<int:year>/<int:month>/upload', import_working_data, name='section-upload'),
    path('working/section/<slug:section>/<int:year>/<int:month>/download', export_working_xls, name='section-download'),
    path('working/section/<slug:section>/<int:year>/<int:month>/download/<slug:company>', export_working_csv, name='section-download-csv'),

]



    # path('working/', WorkingListView.as_view(), name='list'),
    # path('working/upload', import_working_data, name='upload'),
    # path('working/confirm', confirm_working, name='confirm'),
    # path('working/<slug:section>/<slug:en>/add', WorkingCreate.as_view(), name='add'),
    # path('working/<slug:section>', WorkingListView.as_view(), name='section-list'),
    # path('working/<int:pk>', WorkingUpdate.as_view(), name='detail'),
    # path('working/<slug:pk>/delete', WorkingDelete.as_view(), name='delete'),
    # path('working/<slug:pk>/process/<slug:action>', ProcessWorking, name='process'),
    # path('working/<slug:department>', WorkingListView.as_view(), name='department-list'),
    # path('status/<slug:status>', WorkingStatusListView.as_view(), name='status-list'),