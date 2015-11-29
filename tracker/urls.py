# === Manager ===
# tracker/500000000/home.html
# tracker/500000000/project/1/process.html
# tracker/500000000/project/1/people.html
# tracker/500000000/project/1/summary.html

# === Developer ===
# tracker/100000000/home.html
# tracker/100000000/project/1.html
# tracker/100000000/project/1/dev_mode.html
# tracker/100000000/project/1/debug_mode.html
# tracker/100000000/project/1/manage_mode.html
# tracker/100000000/project/1/report.html

from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from . import views

urlpatterns = [
    # http://localhost:8000/tracker/
    url(r'^$', views.userlogin, name='userlogin'),
    url(r'^manager/(?P<user_id>[0-9]+)/home/$', views.managerhome, name='managerhome'),
    url(r'^developer/(?P<user_id>[0-9]+)/home/$', views.developerhome, name='developerhome'),

############### manager ############
    # http://localhost:8000/tracker/50000000/createproject/
    url(r'^(?P<user_id>[0-9]{8})/createproject/$', views.createproject, name='createproject'),
    # http://localhost:8000/tracker/50000000/project/1/
    url(r'^(?P<user_id>[0-9]+)/project/(?P<project_id>[0-9]+)/$', views.viewproject, name='viewproject'),
    # http://localhost:8000/tracker/50000000/project/1/people/
    url(r'^(?P<user_id>[0-9]+)/project/(?P<project_id>[0-9]+)/people/$', views.people, name='people'),
    # http://localhost:8000/tracker/50000000/project/1/summary/
    url(r'^(?P<user_id>[0-9]+)/project/(?P<project_id>[0-9]+)/summary/$', views.summary, name='summary'),

############### developer #############
    # http://localhost:8000/tracker/Defect/50000000/home/
    url(r'^Defect/(?P<defect_id>[0-9]+)/$', views.showDefect, name='showdefect'),

    url(r'^(?P<user_id>[0-9]+)/workonproject/(?P<project_id>[0-9]+)/timing/$', views.timing, name='timing'),
    url(r'^(?P<user_id>[0-9]+)/workonproject/(?P<project_id>[0-9]+)/$', views.workonproject, name='workonproject'),

    # http://localhost:8000/tracker/50000000/reportdefect/
    url(r'^(?P<id>[0-9]{8})/reportdefect/$', views.reportDefect, name='reportdefect'),
    
   
    # http://localhost:8000/tracker/50000000/project/1/
    url(r'^(?P<user_id>[0-9]{8})/project/(?P<project_id>[0-9]+)/$', views.index, name='index'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()

