#coding:utf-8


from django.conf.urls import url

from iss.blocks.views import BlocksList, AddressList
from iss.blocks.jsondata import get_json



urlpatterns = [
    url(r'blocklist/(?P<page>\d+)/$', BlocksList.as_view()),
    url(r'addresslist/(?P<page>\d+)/$', AddressList.as_view()),
    url(r'jsondata/$', get_json),
]
