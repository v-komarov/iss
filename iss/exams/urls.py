#coding:utf-8
from django.conf.urls import url

from iss.exams.views import QuestionsList, QuestionUpdate, CreateQestion, TestsList, CreateTest, TestUpdate
from iss.exams.jsondata import get_json


urlpatterns = [
    url(r'questions/$', QuestionsList.as_view()),
    url(r'jsondata/$', get_json),
    url(r'questions/add/$', CreateQestion),
    url(r'questions/update/(?P<question>\d+)/$', QuestionUpdate.as_view()),
    url(r'tests/(?P<page>\d+)/$', TestsList.as_view()),
    url(r'tests/add/$', CreateTest),
    url(r'tests/update/(?P<test>\d+)/$', TestUpdate.as_view()),

]


