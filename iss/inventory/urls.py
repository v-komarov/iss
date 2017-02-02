#coding:utf-8


from django.conf.urls import url
from iss.inventory.views import DeviceSchemeList



urlpatterns = [
    url(r'devicescheme/page/(?P<page>\d+)/$', DeviceSchemeList.as_view()),
]
