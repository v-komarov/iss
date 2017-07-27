#coding:utf-8


from django.conf.urls import url
from iss.regions.views import Orders, Reestr, ReestrUpdate, ReestrCreate
from iss.regions.jsondata import get_json
from iss.regions.filedata import get_orders_region



urlpatterns = [
    url(r'orders/$', Orders.as_view()),
    url(r'reestr/page/(?P<page>\d+)/$', Reestr.as_view()),
    url(r'reestr/edit/(?P<pk>\d+)/$', ReestrUpdate.as_view(), name='edit-reestr'),
    url(r'reestr/edit/add/$', ReestrCreate.as_view(), name='add-reestr'),
    url(r'jsondata/$', get_json),
    url(r'filedata/$', get_orders_region),
]
