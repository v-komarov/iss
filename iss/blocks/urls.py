#coding:utf-8


from django.conf.urls import url

from iss.blocks.views import BlocksList, AddressList, CompanyEdit, HouseEdit
from iss.blocks.jsondata import get_json



urlpatterns = [
    url(r'blocklist/(?P<page>\d+)/$', BlocksList.as_view()),
    url(r'addresslist/(?P<page>\d+)/$', AddressList.as_view()),
    url(r'companyedit/(?P<pk>\d+)/$', CompanyEdit.as_view()),
    url(r'houseedit/(?P<pk>\d+)/$', HouseEdit.as_view()),
    url(r'jsondata/$', get_json),
]
