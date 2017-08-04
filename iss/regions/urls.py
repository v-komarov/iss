#coding:utf-8


from django.conf.urls import url
from iss.regions.views import Orders, Reestr, ReestrUpdate, ReestrCreate, DocsList, DocsUpdate, ProjList, ProjStagesList
from iss.regions.jsondata import get_json
from iss.regions.filedata import get_orders_region



urlpatterns = [
    url(r'orders/$', Orders.as_view()),
    url(r'reestr/page/(?P<page>\d+)/$', Reestr.as_view()),
    url(r'reestr/edit/(?P<pk>\d+)/$', ReestrUpdate.as_view(), name='edit-reestr'),
    url(r'reestr/edit/add/$', ReestrCreate.as_view(), name='add-reestr'),
    url(r'docs/$', DocsList.as_view()),
    url(r'docs/edit/add/$', DocsUpdate.as_view(action='create')),
    url(r'docs/edit/update/$', DocsUpdate.as_view(action='update')),
    url(r'jsondata/$', get_json),
    url(r'filedata/$', get_orders_region),
    url(r'proj/page/(?P<page>\d+)/$', ProjList.as_view()),
    url(r'proj/edit/$', ProjStagesList.as_view()),
]
