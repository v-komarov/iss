#coding:utf-8


from django.conf.urls import url
from iss.regions.views import Orders, Reestr, ReestrUpdate, ReestrCreate, ProjList, ProjStagesList, TaskList, ReestrProjList, ReestrProjEdit
from iss.regions.jsondata import get_json
from iss.regions.filedata import get_orders_region, upload, getfile, projexcel, projgant, projtemp, uploadfile_page2, uploadfile_page4, getfile2


urlpatterns = [
    url(r'reestrproj/page/(?P<page>\d+)/$', ReestrProjList.as_view()),
    url(r'reestrproj/upload-p2/$', uploadfile_page2),
    url(r'reestrproj/upload-p4/$', uploadfile_page4),
    url(r'reestrproj/edit/(?P<pk>\d+)/$', ReestrProjEdit.as_view()),
    url(r'reestrproj/readfile/$', getfile2),
    url(r'orders/$', Orders.as_view()),
    url(r'reestr/page/(?P<page>\d+)/$', Reestr.as_view()),
    url(r'reestr/edit/(?P<pk>\d+)/$', ReestrUpdate.as_view(), name='edit-reestr'),
    url(r'reestr/edit/add/$', ReestrCreate.as_view(), name='add-reestr'),
#    url(r'docs/$', DocsList.as_view()),
#    url(r'docs/edit/add/$', DocsUpdate.as_view(action='create')),
#    url(r'docs/edit/update/$', DocsUpdate.as_view(action='update')),
    url(r'jsondata/$', get_json),
    url(r'filedata/$', get_orders_region),
    url(r'proj/page/(?P<page>\d+)/$', ProjList.as_view()),
    url(r'proj/edit/(?P<project>\d+)/$', ProjStagesList.as_view()),
    url(r'proj/upload/$', upload),
    url(r'proj/readfile/$', getfile),
    url(r'proj/temp/(?P<project>\d+)/$', projtemp),
    url(r'proj/excel/(?P<project>\d+)/$', projexcel),
    url(r'proj/gant/(?P<project>\d+)/$', projgant),
    url(r'workertask/(?P<page>\d+)/$', TaskList.as_view()),
]
