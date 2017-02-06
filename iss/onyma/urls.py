#coding:utf-8


from django.conf.urls import url

from iss.onyma.apidata import get_apidata


urlpatterns = [
    url(r'apidata/$', get_apidata),
]
