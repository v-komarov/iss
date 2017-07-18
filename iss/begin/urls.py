#coding:utf-8


from django.conf.urls import url
from iss.begin.jsondata import get_json



urlpatterns = [
    url(r'jsondata/$', get_json),
]
