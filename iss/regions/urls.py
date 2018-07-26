#coding:utf-8


from django.conf.urls import url
from iss.regions.views import Orders, ProjList, ProjStagesList, TaskList, ReestrProjList, ReestrProjEdit, ProcessProjList, ProcessProjEdit, Store, StoreOut, StoreIn, StoreHistory, StoreCarry, LoadStore, AvrList, AVREdit
from iss.regions.jsondata import get_json
from iss.regions.filedata import get_orders_region, upload, getfile, projexcel, projgant, projtemp, uploadfile_page2, uploadfile_page4, getfile2, reestrprojexcel, reestrprojexcelall, uploadfile_store, uploadfile_avr, get_avr_file


urlpatterns = [
    url(r'reestrproj/page/(?P<page>\d+)/$', ReestrProjList.as_view()),
    url(r'processproj/page/(?P<page>\d+)/$', ProcessProjList.as_view()),
    url(r'reestrproj/upload-p2/$', uploadfile_page2),
    url(r'reestrproj/upload-p4/$', uploadfile_page4),
    url(r'reestrproj/edit/(?P<pk>\d+)/$', ReestrProjEdit.as_view()),
    url(r'processproj/edit/(?P<pk>\d+)/$', ProcessProjEdit.as_view()),
    url(r'reestrproj/readfile/$', getfile2),
    url(r'reestrproj/excel/(?P<typeproj>\w+)/$', reestrprojexcel),
    url(r'reestrproj/excelall/(?P<typeproj>\w+)/$', reestrprojexcelall),
    url(r'orders/$', Orders.as_view()),
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
    url(r'store/page/(?P<page>\d+)/$', Store.as_view()),
    url(r'storeout/page/(?P<page>\d+)/$', StoreOut.as_view()),
    url(r'storein/page/(?P<page>\d+)/$', StoreIn.as_view()),
    url(r'storecarry/page/(?P<page>\d+)/$', StoreCarry.as_view()),
    url(r'storehistory/page/(?P<page>\d+)/$', StoreHistory.as_view()),
    url(r'store/upload-eisup/$', uploadfile_store),
    url(r'store/loadstore/$', LoadStore.as_view()),
    url(r'avr/page/(?P<page>\d+)/$', AvrList.as_view()),
    url(r'avr/(?P<pk>\d+)/$', AVREdit.as_view()),
    url(r'avr/upload-file/$', uploadfile_avr),
    url(r'readfileavr/$', get_avr_file),
]
