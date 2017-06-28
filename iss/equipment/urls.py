#coding:utf-8


from django.conf.urls import url

from iss.equipment.views import EquipmentList,FootNodeList,AgregatorsList,Topology
from iss.equipment.jsondata import get_json
from iss.equipment.apidata import get_apidata,get_apidata2




urlpatterns = [
    url(r'topology/$', Topology.as_view()),
    url(r'equipmant/$', EquipmentList.as_view()),
    url(r'agregators/page/(?P<page>\d+)/$', AgregatorsList.as_view()),
    url(r'footnodes/page/(?P<page>\d+)/$', FootNodeList.as_view()),
    url(r'devices/page/(?P<page>\d+)/$', EquipmentList.as_view()),
    url(r'devices/jsondata/$', get_json),
    url(r'devices/apidata/$', get_apidata),
    url(r'devices/apidata2/$', get_apidata2),
]
