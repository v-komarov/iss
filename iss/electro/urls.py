#coding:utf-8


from django.conf.urls import url

from iss.electro.views import DevicesTypes, Placements
from iss.electro.jsondata import get_json


urlpatterns = [
    url(r'devicestypes/$', DevicesTypes.as_view()),
    url(r'placements/$', Placements.as_view()),
    url(r'jsondata/$', get_json),

]
