#coding:utf-8

"""iss URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from iss.begin.views import Begin,MainMenu,LogOut

urlpatterns = [
    url(r'^$', Begin),
    url(r'^begin/', include('iss.begin.urls')),
    url(r'^mainmenu/$', MainMenu),
    url(r'^monitor/',include('iss.monitor.urls')),
    url(r'^working/',include('iss.working.urls')),
    url(r'^equipment/',include('iss.equipment.urls')),
    url(r'^inventory/',include('iss.inventory.urls')),
    url(r'^regions/',include('iss.regions.urls')),
    url(r'^maps/',include('iss.maps.urls')),
    url(r'^logout/$', LogOut),
    url(r'^onyma/', include('iss.onyma.urls')),
    url(r'^exams/', include('iss.exams.urls')),
    url(r'^admin/', admin.site.urls),
]
