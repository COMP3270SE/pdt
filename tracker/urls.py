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
    # http://localhost:8000/tracker/50000000/home/
    # url(r'^(?P<user_id>[0-9]{8})/home/$', views.home, name='home'),
    url(r'^manager/(?P<user_id>[0-9]+)/home/$', views.managerhome, name='managerhome'),
    url(r'^developer/(?P<user_id>[0-9]+)/home/$', views.developerhome, name='developerhome'),

    # http://localhost:8000/tracker/50000000/createproject/
    url(r'^(?P<user_id>[0-9]{8})/createproject/$', views.createproject, name='createproject'),
    # http://localhost:8000/tracker/50000000/project/1/
    url(r'^(?P<user_id>[0-9]{8})/project/(?P<project_id>[0-9]+)/$', views.viewproject, name='viewproject'),
    # http://localhost:8000/tracker/Defect/50000000/home/
    url(r'^Defect/(?P<defect_id>[0-9]+)/$', views.showDefect, name='showdefect'),
    # http://localhost:8000/tracker/50000000/timing/
    url(r'^(?P<id>[0-9]{8})/timing/$', views.timing, name='timing'),
    # http://localhost:8000/tracker/50000000/reportdefect/
    url(r'^(?P<id>[0-9]{8})/reportdefect/$', views.reportDefect, name='reportdefect'),
    # http://localhost:8000/tracker/50000000/project/1/people/
    url(r'^(?P<user_id>[0-9]{8})/project/(?P<project_id>[0-9]+)/people/$', views.people, name='people'),
    # http://localhost:8000/tracker/50000000/project/1/summary/
    url(r'^(?P<user_id>[0-9]{8})/project/(?P<project_id>[0-9]+)/summary/$', views.summary, name='summary'),
    # http://localhost:8000/tracker/login
    url(r'^login/$', views.userlogin, name='userlogin'),
    # http://localhost:8000/tracker/50000000/project/1/
    url(r'^(?P<user_id>[0-9]{8})/project/(?P<project_id>[0-9]+)/$', views.index, name='index'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()

