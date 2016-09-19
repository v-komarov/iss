#coding:utf-8


from django.conf.urls import url
from iss.monitor.views import EventList


urlpatterns = [
    url(r'events/page/(?P<page>\d+)/$', EventList.as_view()),
]
