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

from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /tracker/
    url(r'^$', views.index, name='index'),
    # http://localhost:8000/tracker/50000000/home/
    url(r'^(?P<id>[0-9]{8})/home/$', views.home, name='home'),
    # http://localhost:8000/tracker/50000000/timing/
    url(r'^(?P<id>[0-9]{8})/timing/$', views.timing, name='timing'),
    # http://localhost:8000/tracker/50000000/project/1/summary/
    url(r'^(?P<user_id>[0-9]{8})/project/(?P<project_id>[0-9]+)/summary/$', views.summary, name='summary'),
]
