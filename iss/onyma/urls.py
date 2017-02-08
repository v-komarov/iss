#coding:utf-8


from django.conf.urls import url

from iss.onyma.apidata import get_apidata,get_apidata2


urlpatterns = [
    url(r'apidata/$', get_apidata),
    url(r'apidata2/$', get_apidata2),
]
