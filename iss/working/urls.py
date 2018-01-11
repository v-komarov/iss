#coding:utf-8


from django.conf.urls import url
from iss.working.views import WorkCard
from iss.working.jsondata import get_json


urlpatterns = [
    url(r'card/$', WorkCard.as_view()),
    url(r'jsondata/$', get_json),
]
