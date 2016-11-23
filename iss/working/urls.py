#coding:utf-8


from django.conf.urls import url
from iss.working.views import WorkList


urlpatterns = [
    url(r'worklist/page/(?P<page>\d+)/$', WorkList.as_view()),
]
