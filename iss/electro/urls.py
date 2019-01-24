#coding:utf-8


from django.conf.urls import url

from iss.electro.views import DevicesTypes


urlpatterns = [
    url(r'devicestypes/$', DevicesTypes.as_view()),
]
