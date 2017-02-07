#coding:utf-8


from django.conf.urls import url
from iss.inventory.views import DeviceSchemeList
from iss.inventory.jsondata import get_json



urlpatterns = [
    url(r'devicescheme/page/(?P<page>\d+)/$', DeviceSchemeList.as_view()),
    url(r'jsondata/$', get_json),
]
