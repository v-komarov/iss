#coding:utf-8
from django.conf.urls import url

from iss.exams.views import QuestionsList, QuestionUpdate, CreateQestion, TestsList, CreateTest, TestUpdate, TestLearning, ExamList, TestExamining, ResultsList
from iss.exams.jsondata import get_json
from iss.exams.filedata import report, QuestionsExam, ProtocolExam, report2, report3


urlpatterns = [
    url(r'questions/(?P<page>\d+)/$', QuestionsList.as_view()),
    url(r'jsondata/$', get_json),
    url(r'questions/add/$', CreateQestion),
    url(r'questions/update/(?P<question>\d+)/(?P<page>\d+)/$', QuestionUpdate.as_view()),
    url(r'tests/(?P<page>\d+)/$', TestsList.as_view()),
    url(r'tests/add/$', CreateTest),
    url(r'tests/update/(?P<test>\d+)/(?P<page>\d+)/$', TestUpdate.as_view()),
    url(r'learning/(?P<test>\d+)/(?P<page>\d+)/$', TestLearning.as_view()),
    url(r'examlist/(?P<page>\d+)/$', ExamList.as_view()),
    url(r'examining/(?P<test>\d+)/(?P<page>\d+)/$', TestExamining.as_view()),
    url(r'results/(?P<page>\d+)/$', ResultsList.as_view()),
    url(r'report/$', report),
    url(r'report2/$', report2),
    url(r'report3/$', report3),
    url(r'protocol/(?P<result>\d+)/$', ProtocolExam),
    url(r'questionsexam/(?P<result>\d+)/$', QuestionsExam),

]


