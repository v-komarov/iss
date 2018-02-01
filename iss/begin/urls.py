#coding:utf-8


from django.conf.urls import url
from iss.begin.jsondata import get_json
from iss.begin.views import AccessRefused, UserAttrs



urlpatterns = [
    url(r'jsondata/$', get_json),
    url(r'access-refused/$', AccessRefused),
    url(r'userattrs/$', UserAttrs)
]
