#coding:utf-8


from django.conf.urls import url

from iss.maps.jsondata import get_json
from iss.maps.views import MapsAccidents

urlpatterns = [
    url(r'accidents/$', MapsAccidents.as_view()),
    url(r'jsondata/$', get_json),
]
