#coding:utf-8


from django.conf.urls import url

from iss.maps.jsondata import get_json
from iss.maps.views import MapsAccidents, MapsFindIp

urlpatterns = [
    url(r'accidents/$', MapsAccidents.as_view()),
    url(r'findip/$', MapsFindIp.as_view()),
    url(r'jsondata/$', get_json),
]
