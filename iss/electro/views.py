#coding:utf-8
from django.shortcuts import render

from django.views.generic import ListView
from django.contrib.auth.decorators import login_required, permission_required
from iss.mydecorators import group_required,anonymous_required
from django.utils.decorators import method_decorator

from iss.electro.models import devicestypes
from iss.electro.forms import DevicesTypesForm



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
        context['all_nodes'] = devicestypes.objects.all()
        context['form'] = DevicesTypesForm()


        return context

