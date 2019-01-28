#coding:utf-8
from django.shortcuts import render

from django.views.generic import ListView
from django.contrib.auth.decorators import login_required, permission_required
from iss.mydecorators import group_required,anonymous_required
from django.utils.decorators import method_decorator

from iss.electro.models import devicestypes, placements, deviceslist
from iss.electro.forms import DevicesTypesForm, PlacementForm, FilterPlacementForm, FilterDeviceTypeForm, FilterDevicesForm



# Типы устройств
class DevicesTypes(ListView):

    model = devicestypes
    template_name = "electro/devicestypes.html"

    paginate_by = 0



    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='electro',redirect_url='/begin/access-refused/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user


        return super(ListView, self).dispatch(request, *args, **kwargs)



    def get_queryset(self):

        data = []

        return data



    def get_context_data(self, **kwargs):
        context = super(DevicesTypes, self).get_context_data(**kwargs)
        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        if self.session.has_key('filter-devicetype'):
            context['all_nodes'] = devicestypes.objects.get(pk=self.session['filter-devicetype']).get_descendants(include_self=True)
        else:
            context['all_nodes'] = devicestypes.objects.all()
        context['form'] = DevicesTypesForm()
        context['filter'] = FilterDeviceTypeForm()
        context['search'] = self.session['filter-devicetype'] if self.session.has_key('filter-devicetype') else ""


        return context





# Структура размещения
class Placements(ListView):

    model = placements
    template_name = "electro/placements.html"

    paginate_by = 0



    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='electro',redirect_url='/begin/access-refused/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user


        return super(ListView, self).dispatch(request, *args, **kwargs)



    def get_queryset(self):

        data = []

        return data



    def get_context_data(self, **kwargs):
        context = super(Placements, self).get_context_data(**kwargs)
        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        if self.session.has_key('filter-placement'):
            context['all_nodes'] = placements.objects.get(pk=self.session["filter-placement"]).get_descendants(include_self=True)
        else:
            context['all_nodes'] = placements.objects.all()
        context['form'] = PlacementForm()
        context['filter'] = FilterPlacementForm()
        context['search'] = self.session['filter-placement'] if self.session.has_key('filter-placement') else ""

        return context





# Список оборудования
class DevicesList(ListView):

    model = deviceslist
    template_name = "electro/deviceslist.html"

    paginate_by = 50



    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='electro',redirect_url='/begin/access-refused/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user


        return super(ListView, self).dispatch(request, *args, **kwargs)



    def get_queryset(self):

        data = []

        return data



    def get_context_data(self, **kwargs):
        context = super(DevicesList, self).get_context_data(**kwargs)
        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        #if self.session.has_key('filter-placement'):
        #    context['all_nodes'] = placements.objects.get(pk=self.session["filter-placement"]).get_descendants(include_self=True)
        #else:
        #    context['all_nodes'] = placements.objects.all()
        #context['form'] = PlacementForm()
        context['filter'] = FilterDevicesForm()
        #context['search'] = self.session['filter-placement'] if self.session.has_key('filter-placement') else ""

        return context

