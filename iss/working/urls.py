#coding:utf-8


from django.conf.urls import url
from iss.working.views import WorkCard, MakeReports, Events, Reports, StartDesktop, PhoneHistory, GraphHistory, PhoneHistoryGroup
from iss.working.jsondata import get_json


urlpatterns = [
    url(r'card/$', WorkCard.as_view()),
    url(r'desktop/$', StartDesktop.as_view()),
    url(r'phone/$', PhoneHistory.as_view()),
    url(r'phonehistory/(?P<group>\d+)/$', PhoneHistoryGroup.as_view()),
    url(r'graph/$', GraphHistory.as_view()),
    url(r'jsondata/$', get_json),
    url(r'makereports/(?P<page>\d+)/$', MakeReports.as_view()),
    url(r'events/(?P<pk>\d+)/$', Events.as_view()),
    url(r'reports/(?P<page>\d+)/$', Reports.as_view()),
]
