#coding:utf-8


from django.conf.urls import url
from iss.monitor.views import event_list


urlpatterns = [
    url(r'events/$', event_list),
]
