from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /tracker/
    url(r'^$', views.index, name='index'),
    # ex: /5/time/
    url(r'^(?P<uid>[0-9]+)/time/$', views.current_datetime, name='current_datetime'),
    # ex: /tracker/5/
    url(r'^(?P<uid>[0-9]+)/$', views.detail, name='detail'),
    # ex: /tracker/5/results/
    url(r'^(?P<uid>[0-9]+)/results/$', views.results, name='results'),
    # ex: /tracker/5/vote/
    url(r'^(?P<uid>[0-9]+)/vote/$', views.vote, name='vote'), 
]
