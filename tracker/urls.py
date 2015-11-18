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
    # tracker/X00000000/home.html
    url(r'^(?P<id>[0-9]{8})/home/$', views.home, name='home'),
]
