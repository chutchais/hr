from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

from django.urls import path

from . import views

from .views import (CompanyDetailView,
					CompanyListView)


urlpatterns = [
	# Page
	# url(r'^$',CompanyListView.as_view(),name='list'),
    # url(r'^(?P<slug>[-\w]+)/$',CompanyDetailView.as_view(),name='detail'),
    path('', CompanyListView.as_view(),name='list'),
]