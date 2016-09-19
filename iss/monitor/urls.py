#coding:utf-8


from django.conf.urls import url
from iss.monitor.views import EventList


urlpatterns = [
    url(r'events/$', EventList.as_view()),
]
