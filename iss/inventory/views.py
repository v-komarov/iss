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



from iss.inventory.models import devices_scheme,netelems,devices
from iss.localdicts.models import Status,Severity,address_companies,port_status,slot_status,device_status,logical_interfaces_prop_list,address_house

from iss.mydecorators import group_required,anonymous_required

from django.contrib.auth.models import User


dev_use = device_status.objects.get(name="Используется")



### Схемы данных устройств
class DeviceSchemeList(ListView):

    model = devices_scheme
    template_name = "inventory/devicescheme_list.html"

    paginate_by = 50



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



















### Сетевые элементы
class NetElementsList(ListView):

    model = netelems
    template_name = "inventory/netelements_list.html"

    paginate_by = 50



    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='inventory',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):

        data = netelems.objects.order_by('name')

        return data







    def get_context_data(self, **kwargs):
        context = super(NetElementsList, self).get_context_data(**kwargs)

        if self.session.has_key('tz'):
            context['tz']= self.session['tz']
        else:
            context['tz']= 'UTC'


        return context







### Редактирование и наполнение данными сетевого элемента
class NetElement(TemplateView):

    template_name = 'inventory/edit_netelement.html'


    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='inventory',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user

        if self.request.GET.has_key("elem"):
            self.session["elem"] = self.request.GET["elem"]


        return super(NetElement, self).dispatch(request, *args, **kwargs)




    def get_context_data(self, **kwargs):
        context = super(NetElement, self).get_context_data(**kwargs)

        if self.session.has_key('tz'):
            context['tz']= self.session['tz']
        else:
            context['tz']= 'UTC'

        context["interface_prop_list"] = logical_interfaces_prop_list.objects.all()

        context["elem"] = self.session["elem"]
        #elem = netelems.objects.get(pk=self.request["elem"])

        return context








### Устройства
class DevicesList(ListView):

    model = devices
    template_name = "inventory/devices_list.html"

    paginate_by = 50



    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='inventory',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):

        q = []


        if self.session.has_key("search_device"):
            if len(self.session['search_device']) >= 3:
                for search in self.session['search_device'].split(" "):
                    if search != " ":
                        q.append("Q(device_scheme__name__icontains='%s') | Q(serial__icontains='%s') | Q(address__street__name__icontains='%s') | Q(address__house__icontains='%s')" % (search,search,search,search))

        if len(q) == 0:
            return devices.objects.order_by('address')
        else:
            str_q = " & ".join(q)
            str_sql = "devices.objects.filter(%s).order_by('address')" % str_q

        return eval(str_sql)










    def get_context_data(self, **kwargs):
        context = super(DevicesList, self).get_context_data(**kwargs)

        if self.session.has_key('tz'):
            context['tz']= self.session['tz']
        else:
            context['tz']= 'UTC'

        # Справочник схем
        context['scheme'] = devices_scheme.objects.order_by('name')
        # Справочник компаний
        context['company'] = address_companies.objects.order_by('name')


        # search
        if self.session.has_key('search_device'):
            context['search_device'] = self.session['search_device']
        else:
            context['search_device'] = ""


        return context






### Редактирование и наполнение данными устройства
class Device(TemplateView):

    template_name = 'inventory/edit_device.html'


    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='inventory',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user

        #if self.request.GET.has_key("dev"):
        #    self.session["dev"] = self.request.GET["dev"]


        return super(Device, self).dispatch(request, *args, **kwargs)




    def get_context_data(self, **kwargs):
        context = super(Device, self).get_context_data(**kwargs)

        if self.session.has_key('tz'):
            context['tz']= self.session['tz']
        else:
            context['tz']= 'UTC'

        context['status_port_list'] = port_status.objects.all()
        context['status_slot_list'] = slot_status.objects.all()
        context['status_device_list'] = device_status.objects.all()

        #context["elem"] = self.session["elem"]
        #elem = netelems.objects.get(pk=self.request["elem"])

        return context






### Аудит портов
class DevicesAuditPorts(ListView):

    model = devices
    template_name = "inventory/audit_ports.html"

    paginate_by = 0



    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='inventory',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):


        if self.session.has_key("address_id") and self.session["address_id"] != 'undefined':

            addr = address_house.objects.get(pk=int(self.session["address_id"],10))

            ### Когда определен только город
            if addr.city and addr.street == None and addr.house == None:
                return devices.objects.filter(address__city = addr.city,status=dev_use).order_by('address__street__name')

            ### Когда определен город и улица
            elif addr.city and addr.street and addr.house == None:
                return devices.objects.filter(address__city = addr.city,address__street = addr.street,status=dev_use).order_by('address__house')


            ### Когда определены город, улица, дом
            elif addr.city and addr.street and addr.house:
                return devices.objects.filter(address__city=addr.city, address__street=addr.street, address__house=addr.house,status=dev_use).all()

            else:
                return []


        else:
            return []







    def get_context_data(self, **kwargs):
        context = super(DevicesAuditPorts, self).get_context_data(**kwargs)

        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'

        context["address_label"] = self.session["address_label"] if self.session.has_key("address_label") else ''



        return context

