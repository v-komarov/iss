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
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from iss.mydecorators import group_required,anonymous_required

from iss.localdicts.models import address_city, address_house
from iss.blocks.models import buildings, block_managers
from iss.inventory.models import devices

from iss.blocks.forms import CompanyEditForm, HouseEditForm






### Список домов
class BlocksList(ListView):



    model = buildings
    template_name = "blocks/blockslist.html"

    paginate_by = 100



    @method_decorator(login_required(login_url='/'))
    #@method_decorator(group_required(group='project',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):


        if self.session.has_key("filter_company"):
            filter = pickle.loads(self.session["filter_company"])


            if filter["company"] == "":
                data = block_managers.objects.order_by("name")
            else:
                data = block_managers.objects.filter(name__icontains=filter["company"]).order_by("name")

            data1 = []


            if not filter["city"] == "" and not filter["street"] == "" and not filter["house"] == "":
                for item in list(data):
                    if item.buildings_set.filter(address__city_id = int(filter["city"])).exists() and item.buildings_set.filter(address__street__name__icontains = filter["street"]).exists() and item.buildings_set.filter(address__house__icontains = filter["house"]).exists():
                        data1.append(item)

            elif filter["city"] == "" and not filter["street"] == "" and not filter["house"] == "":
                for item in list(data):
                    if item.buildings_set.filter(address__street__name__icontains = filter["street"]).exists() and item.buildings_set.filter(address__house__icontains = filter["house"]).exists():
                        data1.append(item)

            elif not filter["city"] == "" and filter["street"] == "" and not filter["house"] == "":
                for item in list(data):
                    if item.buildings_set.filter(address__city_id = int(filter["city"])).exists() and item.buildings_set.filter(address__house__icontains = filter["house"]).exists():
                        data1.append(item)

            elif not filter["city"] == "" and not filter["street"] == "" and filter["house"] == "":
                for item in list(data):
                    if item.buildings_set.filter(address__city_id = int(filter["city"])).exists() and item.buildings_set.filter(address__street__name__icontains = filter["street"]).exists():
                        data1.append(item)

            elif not filter["city"] == "" and filter["street"] == "" and filter["house"] == "":
                for item in list(data):
                    if item.buildings_set.filter(address__city_id = int(filter["city"])).exists():
                        data1.append(item)

            elif filter["city"] == "" and not filter["street"] == "" and filter["house"] == "":
                for item in list(data):
                    if item.buildings_set.filter(address__street__name__icontains = filter["street"]).exists():
                        data1.append(item)

            if filter["city"] == "" and filter["street"] == "" and not filter["house"] == "":
                for item in list(data):
                    if item.buildings_set.filter(address__house__icontains = filter["house"]).exists():
                        data1.append(item)


            data = data1



        else:

            data = []

        return data



    def get_context_data(self, **kwargs):
        context = super(BlocksList, self).get_context_data(**kwargs)
        context["city"] = address_city.objects.order_by("name")
        context["filter_company"] = pickle.loads(self.session["filter_company"]) if self.session.has_key("filter_company") else {'city': "", 'street': "", "house": "", "company": ""}


        return context







### Список возможных адресов
class AddressList(ListView):



    model = buildings
    template_name = "blocks/addresslist.html"

    paginate_by = 100



    @method_decorator(login_required(login_url='/'))
    #@method_decorator(group_required(group='project',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):

        if self.session.has_key("filter_addresslist"):

            filter_value = pickle.loads(self.session["filter_addresslist"])

            data = address_house.objects.exclude(city=None).exclude(street=None).exclude(house=None).order_by('city','street','house')
            data = data.filter(city_id=int(filter_value["city"],10)) if filter_value["city"] != "" else data
            data = data.filter(street__name__icontains=filter_value["street"]) if filter_value["city"] != "" else data
            data = data.filter(house__icontains=filter_value["house"]) if filter_value["house"] != "" else data

            return data

        else:

            return []



    def get_context_data(self, **kwargs):
        context = super(AddressList, self).get_context_data(**kwargs)
        context["city"] = address_city.objects.order_by("name")
        context["filter"] = pickle.loads(self.session["filter_addresslist"]) if self.session.has_key("filter_addresslist") else {'city': "", 'street': "", "house": ""}

        return context






### Список домов
class HouseList(ListView):

    model = buildings
    template_name = "blocks/houselist.html"

    paginate_by = 100

    @method_decorator(login_required(login_url='/'))
    # @method_decorator(group_required(group='project',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)



    def get_queryset(self):


        data = buildings.objects.order_by('address__city__name','address__street__name','address__house')


        if self.session.has_key("filter_company"):
            filter = pickle.loads(self.session["filter_company"])

            if not filter["company"] == "":
                data = data.exclude(block_manager=None).filter(block_manager__name__icontains=filter["company"])

            if not filter["city"] == "":
                data = data.filter(address__city_id = int(filter["city"]))

            if not filter["street"] == "":
                data = data.filter(address__street__name__icontains = filter["street"])



        return data



    def get_context_data(self, **kwargs):
        context = super(HouseList, self).get_context_data(**kwargs)
        context["city"] = address_city.objects.order_by("name")
        context["filter_company"] = pickle.loads(self.session["filter_company"]) if self.session.has_key("filter_company") else {'city': "", 'street': "", "house": "", "company": ""}

        return context






### Основная форма редактирования данных компании
class CompanyEdit(UpdateView):

    model = block_managers
    form_class = CompanyEditForm
    template_name = "blocks/company_edit.html"
    success_url = '/blocks/company_edit/edit/1/'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(CompanyEdit, self).dispatch(request, *args, **kwargs)




    def get_context_data(self, **kwargs):
        context = super(CompanyEdit, self).get_context_data(**kwargs)
        context["comp"] = self.get_object()

        return context



    def form_valid(self, form):
        form.instance.rowsum = form.instance.price * form.instance.count
        return super(CompanyEdit, self).form_valid(form)






### Основная форма редактирования данных дома
class HouseEdit(UpdateView):

    model = buildings
    form_class = HouseEditForm
    template_name = "blocks/house_edit.html"
    success_url = '/blocks/house_edit/edit/1/'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(HouseEdit, self).dispatch(request, *args, **kwargs)




    def get_context_data(self, **kwargs):
        context = super(HouseEdit, self).get_context_data(**kwargs)
        house = self.get_object()
        context["house"] = house
        if house.address:
            context["devices"] = devices.objects.filter(address=house.address)
        else:
            context["devices"] = []

        return context



    def form_valid(self, form):
        form.instance.rowsum = form.instance.price * form.instance.count
        return super(HouseEdit, self).form_valid(form)



