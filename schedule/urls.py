from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from . import views
from .views import WorkingListView,WorkingSectionListView,WorkingCreate,WorkingUpdate,WorkingDelete

urlpatterns = [
    url(r'^$', WorkingListView.as_view(), name='list'),
   
    path('/<slug:section>/<slug:en>/add', WorkingCreate.as_view(), name='add'),
    # path('/<slug:section>/<slug:en>/<int:year>/<int:month>/<int:day>', WorkingUpdate.as_view(), name='update')
    path('/<int:pk>', WorkingUpdate.as_view(), name='detail'),
    path('/<slug:pk>/delete', WorkingDelete.as_view(), name='delete'),
    path('/<slug:department>', WorkingListView.as_view(), name='department-list'),

    # url(r'(?P<slug>[-\w]+)/create$', BayPlanCreateView.as_view(),name='create'),
    # url(r'(?P<slug>[-\w]+)/delete$', BayPlanDeleteView.as_view(),name='delete'),
    # url(r'(?P<slug>[-\w]+)/edit$', BayPlanUpdateView.as_view(),name='edit'),
    # url(r'(?P<slug>[-\w]+)/container$', BayPlanUpdateView.as_view(),name='container'),
    # url(r'container/(?P<pk>\d+)/$', BayPlanCreateView.as_view(),name='container'),
    # url(r'^$', ItemListView.as_view(),name='list'),
]