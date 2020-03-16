"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from accounts import views as user_views
from django.urls import path, re_path, include
from post.views import (
	create_view,
	)
from .views import (
	Home_Page, 
	About_Page, 
	Contact_Page,
	)
from searches.views import search_view

urlpatterns = [
    path('csp-admin/', admin.site.urls),
    path('', Home_Page),
    path('about/', About_Page),
    path('contact/', Contact_Page),
    path('blog-new/', create_view),
    path('blog/', include("post.urls") ),
    path('search/', search_view),
    url(r'^signup/$', views.signup_view, name="signup" ),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^login/$', views.login_view, name="login" ),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^profile/$', user_views.profile, name="profile"),
    url(r'^reset-password/$', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    url(r'^reset-password/done/$', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset-password-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    url(r'^reset-password-complete/$', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    # re_path(r'^blog/(?P<slug>\w+)/$', detail_page),
    # path('blog/', detail_page),
]

if settings.DEBUG: # test mode
	from django.conf.urls.static import static
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)