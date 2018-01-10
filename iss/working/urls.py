#coding:utf-8


from django.conf.urls import url
from iss.working.views import WorkList


urlpatterns = [
    url(r'card/$', WorkList.as_view()),
]
