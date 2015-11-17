from django.conf.urls import patterns, url
from . import views
import views

urlpatterns = patterns('',
                       url(r'^$', views.home, name='home'),
                       url(r'^login/(\w*)', views.login, name='login'),
                       )