"""hr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
# from django.urls import pathinclude
from django.conf.urls import include, url
from .routers import router
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib.auth.views import LoginView,LogoutView

from django.urls import path
from . import views

urlpatterns = [
    # Admin
    url(r'^admin/', admin.site.urls),
    url(r'^login', LoginView.as_view(),name='login'),
    url(r'^logout', LogoutView.as_view(),name='logout'),
    url(r'^schedule/', include(('schedule.urls','schedule'),namespace='schedule')),
    url(r'^employee/', include(('employee.urls','employee'),namespace='employee')),

    
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),

    url(r'^',views.home ,name='home'),
    # # Token
    url(r'^api/login/', include(('employee.urls','user'),namespace='login')),
    url(r'^api/token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^api/token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
]

from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
    
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = 'HR - Overtime Approval System'