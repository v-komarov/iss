#coding:utf-8
from django.shortcuts import render

from django.views.generic import ListView, UpdateView
from django.contrib.auth.decorators import login_required, permission_required
from iss.mydecorators import group_required,anonymous_required
from django.utils.decorators import method_decorator

from iss.electro.models import devicestypes, placements, deviceslist
from iss.electro.forms import DevicesTypesForm, PlacementForm, FilterPlacementForm, FilterDeviceTypeForm, FilterDevicesForm, EditDeviceForm



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

        data = deviceslist.objects.order_by('devicetype','placement','name')

        if self.session.has_key('filter-deviceslist-d'):
            data = data.filter(devicetype__in=devicestypes.objects.get(pk=int(self.session['filter-deviceslist-d'])).get_descendants(include_self=True))

        if self.session.has_key('filter-deviceslist-p'):
            data = data.filter(placement__in=placements.objects.get(pk=int(self.session['filter-deviceslist-p'])).get_descendants(include_self=True))


        return data



    def get_context_data(self, **kwargs):
        context = super(DevicesList, self).get_context_data(**kwargs)
        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        context['filter'] = FilterDevicesForm()
        context['search_d'] = self.session['filter-deviceslist-d'] if self.session.has_key('filter-deviceslist-d') else ""
        context['search_p'] = self.session['filter-deviceslist-p'] if self.session.has_key('filter-deviceslist-p') else ""

        return context




### Основная форма редактирования данных устройства
class EditDevice(UpdateView):

    model = deviceslist
    form_class = EditDeviceForm
    template_name = "electro/editdevice.html"
    success_url = '/electro/deviceslist/1/'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(EditDevice, self).dispatch(request, *args, **kwargs)



    def get_context_data(self, **kwargs):
        context = super(EditDevice, self).get_context_data(**kwargs)
        context["device"] = self.get_object()

        return context



    def form_valid(self, form):
        form.instance.rowsum = form.instance.price * form.instance.count
        return super(EditDevice, self).form_valid(form)


