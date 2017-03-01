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
from django.shortcuts import render_to_response
from django.db import connections
from django.http import HttpResponse
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required



from iss.inventory.models import devices_scheme
from iss.localdicts.models import Status,Severity

from iss.mydecorators import group_required,anonymous_required

from django.contrib.auth.models import User





### Схемы данных устройств
class DeviceSchemeList(ListView):

    model = devices_scheme
    template_name = "inventory/devicescheme_list.html"

    paginate_by = 100



    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='inventory',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):

        data = devices_scheme.objects.order_by('name')

        return data







    def get_context_data(self, **kwargs):
        context = super(DeviceSchemeList, self).get_context_data(**kwargs)

        if self.session.has_key('tz'):
            context['tz']= self.session['tz']
        else:
            context['tz']= 'UTC'


        return context













### Схемы данных логических интерфейсов
class InterfaceSchemeList(ListView):

    model = devices_scheme
    template_name = "inventory/interfacescheme_list.html"

    paginate_by = 100



    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='inventory',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):

        data = devices_scheme.objects.order_by('name')

        return []







    def get_context_data(self, **kwargs):
        context = super(InterfaceSchemeList, self).get_context_data(**kwargs)

        if self.session.has_key('tz'):
            context['tz']= self.session['tz']
        else:
            context['tz']= 'UTC'


        return context

