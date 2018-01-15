#coding:utf-8


from django.conf.urls import url
from iss.begin.jsondata import get_json
from iss.begin.views import AccessRefused



urlpatterns = [
    url(r'jsondata/$', get_json),
    url(r'access-refused/$', AccessRefused),
]
