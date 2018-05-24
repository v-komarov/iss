#coding:utf-8


from django.conf.urls import url

from iss.blocks.views import BlocksList


urlpatterns = [
    url(r'blocklist/(?P<page>\d+)/$', BlocksList.as_view()),
]
