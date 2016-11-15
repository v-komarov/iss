#coding:utf-8


from django.conf.urls import url

from iss.equipment.views import EquipmentList,FootNodeList,AgregatorsList,Topology
from iss.equipment.jsondata import get_json


urlpatterns = [
    url(r'topology/$', Topology.as_view()),
    url(r'equipmant/$', EquipmentList.as_view()),
    url(r'agregators/page/(?P<page>\d+)/$', AgregatorsList.as_view()),
    url(r'footnodes/page/(?P<page>\d+)/$', FootNodeList.as_view()),
    url(r'devices/page/(?P<page>\d+)/$', EquipmentList.as_view()),
    url(r'devices/jsondata/$', get_json),
]
