#coding:utf-8


from django.conf.urls import url
from iss.regions.views import Orders, Reestr
from iss.regions.jsondata import get_json
from iss.regions.filedata import get_orders_region



urlpatterns = [
    url(r'orders/$', Orders.as_view()),
    url(r'reestr/page/(?P<page>\d+)/$', Reestr.as_view()),
    url(r'jsondata/$', get_json),
    url(r'filedata/$', get_orders_region),
]
