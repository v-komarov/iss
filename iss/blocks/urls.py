#coding:utf-8


from django.conf.urls import url

from iss.blocks.views import BlocksList, AddressList, CompanyEdit, HouseEdit, HouseList, ContractList
from iss.blocks.jsondata import get_json
from iss.blocks.filedata import uploadfile, gethdfsfile



urlpatterns = [
    url(r'blocklist/(?P<page>\d+)/$', BlocksList.as_view()),
    url(r'houselist/(?P<page>\d+)/$', HouseList.as_view()),
    url(r'addresslist/(?P<page>\d+)/$', AddressList.as_view()),
    url(r'contractlist/(?P<page>\d+)/$', ContractList.as_view()),
    url(r'companyedit/(?P<pk>\d+)/$', CompanyEdit.as_view()),
    url(r'houseedit/(?P<pk>\d+)/$', HouseEdit.as_view()),
    url(r'jsondata/$', get_json),
    url(r'upload-company/$', uploadfile),
    url(r'readfilecompany/$', gethdfsfile)
]

