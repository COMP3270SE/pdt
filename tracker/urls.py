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
    # ex: /5/time/
    url(r'^(?P<uid>[0-9]{8})/time/$', views.current_datetime, name='current_datetime'),
    # ex: /tracker/5/results/
    url(r'^(?P<uid>[0-9]){8}/results/$', views.results, name='results'),
    # ex: /tracker/5/vote/
    url(r'^(?P<uid>[0-9]{8})/vote/$', views.vote, name='vote'), 
    # tracker/X00000000/home/
    url(r'^(?P<id>[0-9]{8})/home/$', views.home, name='home'),
    # tracker/X00000000/home/
    url(r'^(?P<id>[0-9]{8})/timing/$', views.timing, name='timing'),
    # tracker/500000000/project/1/summary.html
    url(r'^(?P<user_id>[0-9]{8})/project/(?P<project_id>[0-9]+)/summary$', views.summary, name='summary'),
]
