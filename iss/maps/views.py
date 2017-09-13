#coding:utf-8

import pickle

from importlib import import_module
from django.conf import settings
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore

import datetime
from pytz import timezone

from django.db import connections
from django.db.models import Q
from django.db.models import Count
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404
from django.db import connections
from django.http import HttpResponse
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.base import TemplateView,RedirectView


from iss.mydecorators import group_required,anonymous_required

from iss.localdicts.models import address_city
from iss.monitor.models import accidents




tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)

start = datetime.datetime(2017, 7, 9, 12, 0, 0, 0, timezone(tz))



### Отображение аварий на картах городов и населенных пунктов
class MapsAccidents(TemplateView):

    template_name = 'maps/accidents.html'


    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='maps', redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user



        return super(MapsAccidents, self).dispatch(request, *args, **kwargs)




    def get_context_data(self, **kwargs):
        context = super(MapsAccidents, self).get_context_data(**kwargs)

        if self.session.has_key('tz'):
            context['tz']= self.session['tz']
        else:
            context['tz']= 'UTC'

        city_list = address_city.objects.order_by('name')
        for item in city_list:
            item.geo_ok = item.geo_ok()

        context['accidents'] = accidents.objects.filter(acc_start__gt=start).order_by('-acc_start')
        context['city_list'] = city_list

        return context





### Поиск оборудования по ip адресу
class MapsFindIp(TemplateView):

    template_name = 'maps/findip.html'


    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='maps', redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user



        return super(MapsFindIp, self).dispatch(request, *args, **kwargs)




    def get_context_data(self, **kwargs):
        context = super(MapsFindIp, self).get_context_data(**kwargs)

        if self.session.has_key('tz'):
            context['tz']= self.session['tz']
        else:
            context['tz']= 'UTC'


        return context






### Отображение портов устройств доступа на картах городов и населенных пунктов
class MapsPorts(TemplateView):

    template_name = 'maps/ports.html'


    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user



        return super(MapsPorts, self).dispatch(request, *args, **kwargs)




    def get_context_data(self, **kwargs):
        context = super(MapsPorts, self).get_context_data(**kwargs)

        if self.session.has_key('tz'):
            context['tz']= self.session['tz']
        else:
            context['tz']= 'UTC'

        city_list = address_city.objects.order_by('name')
        for item in city_list:
            item.geo_ok = item.geo_ok()

        context['accidents'] = accidents.objects.filter(acc_start__gt=start).order_by('-acc_start')
        context['city_list'] = city_list

        return context

