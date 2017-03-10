#coding:utf-8


from django.conf.urls import url
from iss.inventory.views import DeviceSchemeList,InterfaceSchemeList,NetElementsList,NetElement,DevicesList,Device
from iss.inventory.jsondata import get_json
from iss.inventory.filedata import get_device_scheme



urlpatterns = [
    url(r'devicescheme/page/(?P<page>\d+)/$', DeviceSchemeList.as_view()),
    url(r'interfacescheme/page/(?P<page>\d+)/$', InterfaceSchemeList.as_view()),
    url(r'netelements/page/(?P<page>\d+)/$', NetElementsList.as_view()),
    url(r'devices/page/(?P<page>\d+)/$', DevicesList.as_view()),
    url(r'netelementdata/$', NetElement.as_view()),
    url(r'devicedata/$', Device.as_view()),
    url(r'jsondata/$', get_json),
    url(r'jsondata/scheme_device/$', get_device_scheme),
]
