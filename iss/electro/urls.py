#coding:utf-8


from django.conf.urls import url

from iss.electro.views import DevicesTypes, Placements, DevicesList, EditDevice
from iss.electro.jsondata import get_json


urlpatterns = [
    url(r'devicestypes/$', DevicesTypes.as_view()),
    url(r'placements/$', Placements.as_view()),
    url(r'deviceslist/(?P<page>\d+)/$', DevicesList.as_view()),
    url(r'editdevice/(?P<pk>\d+)/$', EditDevice.as_view()),
    url(r'jsondata/$', get_json),

]
