#coding:utf-8


from django.conf.urls import url
from iss.monitor.views import EventList, AccidentList, MessageList, Zkl
from iss.monitor.jsondata import get_json
from iss.monitor.filedata import get_filedata,get_drpfile



urlpatterns = [
    url(r'events/page/(?P<page>\d+)/$', EventList.as_view()),
    url(r'events/jsondata/$', get_json),
    url(r'events/filedata/$', get_filedata),
    url(r'accident/filedata/$', get_drpfile),
    url(r'accidents/page/(?P<page>\d+)/$', AccidentList.as_view()),
    url(r'messages/page/(?P<page>\d+)/$', MessageList.as_view()),
    url(r'zkl/$', Zkl.as_view()),
]
