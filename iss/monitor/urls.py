#coding:utf-8


from django.conf.urls import url
from iss.monitor.views import EventList
from iss.monitor.jsondata import get_json
from iss.monitor.filedata import get_filedata



urlpatterns = [
    url(r'events/page/(?P<page>\d+)/$', EventList.as_view()),
    url(r'events/jsondata/$', get_json),
    url(r'events/filedata/$', get_filedata),
]
