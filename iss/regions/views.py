#coding:utf-8

import pickle
import operator
from natsort import natsorted
from operator import itemgetter


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
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.base import TemplateView,RedirectView
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


from iss.localdicts.models import regions, address_city, stages, ProjDocTypes, proj_other_system, message_type, init_reestr_proj, blocks, address_companies
from iss.regions.models import orders, proj, proj_stages, reestr_proj, store_rest, store_out, store_in, store_rest_log, store_carry, avr
from iss.regions.forms import ProjForm, ProjForm2, StageForm, ReestrProjCreateForm, ReestrProjUpdateForm, WorkersDatesStagesForm, NewAVRForm, EditAVRForm

from iss.mydecorators import group_required,anonymous_required

from iss.regions.filters import reestr_proj_filter








### Формирование уровень ориентированного списка стадий
def stages_pretty():
    stages_dict = natsorted(stages.objects.all(), key=lambda x: x.name.split('.')[:-1])
    for x in stages_dict:
        dep = len(x.name.split("."))
        x.name = '&nbsp;&nbsp;&nbsp;&nbsp;' * dep + x.name if dep > 2 else x.name
    return stages_dict






### Заказы
class Orders(ListView):

    model = orders
    template_name = "regions/orders.html"

    paginate_by = 0



    #@method_decorator(login_required(login_url='/'))
    #@method_decorator(group_required(group='inventory',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):


            return []







    def get_context_data(self, **kwargs):
        context = super(Orders, self).get_context_data(**kwargs)

        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        context['regions_list'] = regions.objects.order_by('name')



        return context











### Проекты (список)
class ProjList(ListView):

    model = proj
    template_name = "regions/projlist.html"

    paginate_by = 100



    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='project',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):

        data = proj.objects.order_by('-datetime_create')

        return data







    def get_context_data(self, **kwargs):
        context = super(ProjList, self).get_context_data(**kwargs)

        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        context['form']= ProjForm()


        return context







### Этапы проекта (список)
class ProjStagesList(ListView):

    model = proj_stages
    template_name = "regions/projstageslist.html"

    paginate_by = 0



    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='project',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        request.session["proj_id"] = kwargs.get('project')
        self.request = request
        self.session = request.session
        self.user = request.user
        self.proj = proj.objects.get(pk=int(self.session["proj_id"], 10))
        self.actions = []
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):

        data = proj_stages.objects.filter(proj=self.proj)

        ### Вычисление пунктов исполнения
        rows = self.proj.make_dict()
        G = self.proj.make_graph(rows)
        G = self.proj.graph_edge_order(G, rows)
        self.actions = self.proj.actions(G)

        for item in data:
            item.order = ".".join(["%s" % x for x in item.stage_order])
            item.depend = ".".join(["%s" % x for x in item.depend_on["stages"]])
            item.action = True if item.id in self.actions else False


        return data







    def get_context_data(self, **kwargs):
        context = super(ProjStagesList, self).get_context_data(**kwargs)

        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        context['form']= ProjForm2(instance=self.proj)
        context['user_list']= User.objects.order_by('first_name')
        context['stageform']= StageForm()
        context['project']= self.session["proj_id"]

        ### Вычисление пунктов исполнения
        context['actions'] = self.actions



        return context





### Задачи исполнителей
class TaskList(ListView):

    model = proj_stages
    template_name = "regions/workertask.html"

    paginate_by = 100



    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='project',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):

        begin = self.session['begin_date'] if self.session.has_key('begin_date') else datetime.datetime.today() - datetime.timedelta(days=30)
        end = self.session['end_date'] if self.session.has_key('end_date') else datetime.datetime.today() + datetime.timedelta(days=30)

        data = proj_stages.objects.filter( (Q(begin__gte=begin) & Q(end__lte=end)) | (Q(begin__gte=begin) & Q(begin__lte=end)) | (Q(end__gte=begin) & Q(end__lte=end)) ).order_by('-begin')

        data2 = []
        if self.session.has_key('user_id'):
            u = User.objects.get(pk=self.session['user_id'])
            for i in data:
                if u in i.workers.all():
                    data2.append(i)
            return data2
        else:

            return data







    def get_context_data(self, **kwargs):
        context = super(TaskList, self).get_context_data(**kwargs)
        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        context['begin_date'] = self.session['begin_date'] if self.session.has_key('begin_date') else datetime.datetime.today() - datetime.timedelta(days=30)
        context['end_date'] = self.session['end_date'] if self.session.has_key('end_date') else datetime.datetime.today() + datetime.timedelta(days=30)
        context['user_id'] = self.session['user_id'] if self.session.has_key('user_id') else ""
        context['user_list'] = User.objects.order_by('first_name')

        return context







### реестр проектов (таблица - список)
class ReestrProjList(ListView):



    model = reestr_proj
    template_name = "regions/reestrproj/reestrprojlist.html"

    paginate_by = 100



    @method_decorator(login_required(login_url='/'))
    #@method_decorator(group_required(group='project',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):

        data = reestr_proj.objects.filter(process=False).order_by("-comment_last_datetime")
        try:
            data = reestr_proj_filter(data,pickle.loads(self.session["filter_dict"])) if self.session.has_key("filter_dict") else data
        except:
            pass

        return data






    def get_context_data(self, **kwargs):
        context = super(ReestrProjList, self).get_context_data(**kwargs)
        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        context['form'] = ReestrProjCreateForm()
        context['search_text'] = self.session['search_text'] if self.session.has_key('search_text') else ""

        context['stages'] = stages_pretty()
        context['init'] = init_reestr_proj.objects.order_by('name')

        users = User.objects.order_by("first_name")
        workers = [("","---")]
        workers.extend([(user.pk, user.get_full_name()) for user in users])
        context['users'] = workers

        context['blocks'] = blocks.objects.order_by('name')
        context['real'] = address_companies.objects.order_by('name')

        context['filter_dict'] = pickle.loads(self.session['filter_dict']) if self.session.has_key('filter_dict') else {'search_text':'','systems':'','initiator':'','real':'','stage':'','stage_date1':'','stage_date2':'', 'stage_chif':'','executor':'', 'executor_date1':'','executor_date2':'','department':'','create_date1':'','create_date2':''}

        return context










### Изменение реестра проекта
class ReestrProjEdit(UpdateView):
    model = reestr_proj
    form_class = ReestrProjUpdateForm
    template_name = "regions/reestrproj/reestrprojedit.html"
    success_url = '/regions/reestrproj/reestrproj/edit/1/'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ReestrProjEdit, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(ReestrProjEdit, self).get_context_data(**kwargs)
        context["proj"] = self.get_object()
        context['stages'] = stages_pretty()
        context['task'] = WorkersDatesStagesForm()
        context['doctypes'] = ProjDocTypes.objects.order_by('name')
        context['form2'] = ReestrProjCreateForm()
        context['other_system'] = proj_other_system.objects.order_by("name")
        context['message_type'] = message_type.objects.order_by("name")

        return context


    def form_valid(self, form):
        #form.instance.rowsum = form.instance.price * form.instance.count
        return super(ReestrProjEdit, self).form_valid(form)








### Подготовка проектов (таблица - список)
class ProcessProjList(ListView):



    model = reestr_proj
    template_name = "regions/processproj/processprojlist.html"

    paginate_by = 100



    @method_decorator(login_required(login_url='/'))
    #@method_decorator(group_required(group='project',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):


        data = reestr_proj.objects.filter(process=True).order_by("-comment_last_datetime")
        try:
            data = reestr_proj_filter(data,pickle.loads(self.session["filter_dict"])) if self.session.has_key("filter_dict") else data
        except:
            pass


        return data






    def get_context_data(self, **kwargs):
        context = super(ProcessProjList, self).get_context_data(**kwargs)
        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        context['form'] = ReestrProjCreateForm()
        context['search_text'] = self.session['search_text'] if self.session.has_key('search_text') else ""

        context['stages'] = stages_pretty()
        context['init'] = init_reestr_proj.objects.order_by('name')

        users = User.objects.order_by("first_name")
        workers = [("","---")]
        workers.extend([(user.pk, user.get_full_name()) for user in users])
        context['users'] = workers

        context['blocks'] = blocks.objects.order_by('name')
        context['real'] = address_companies.objects.order_by('name')

        context['filter_dict'] = pickle.loads(self.session['filter_dict']) if self.session.has_key('filter_dict') else {'search_text':'','systems':'','initiator':'','real':'','stage':'','stage_date1':'','stage_date2':'', 'stage_chif':'','executor':'', 'executor_date1':'','executor_date2':'','department':'','create_date1':'','create_date2':''}

        return context






### Изменение подготавливаемого проекта
class ProcessProjEdit(UpdateView):
    model = reestr_proj
    form_class = ReestrProjUpdateForm
    template_name = "regions/processproj/processprojedit.html"
    success_url = '/regions/processproj/processproj/edit/1/'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ProcessProjEdit, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(ProcessProjEdit, self).get_context_data(**kwargs)
        context["proj"] = self.get_object()
        context['stages'] = stages_pretty()
        context['task'] = WorkersDatesStagesForm()
        context['doctypes'] = ProjDocTypes.objects.order_by('name')
        context['form2'] = ReestrProjCreateForm()
        context['other_system'] = proj_other_system.objects.order_by("name")
        context['message_type'] = message_type.objects.order_by("name")

        return context


    def form_valid(self, form):
        #form.instance.rowsum = form.instance.price * form.instance.count
        return super(ProcessProjEdit, self).form_valid(form)








### Склад
class Store(ListView):



    model = reestr_proj
    template_name = "regions/store/storerest.html"

    paginate_by = 100



    @method_decorator(login_required(login_url='/'))
    #@method_decorator(group_required(group='project',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):


        data = store_rest.objects.order_by('store','mol','name')

        if self.session.has_key("store") and self.session["store"] !="":
            data = data.filter(store__id=int(self.session["store"]))

        if self.session.has_key("mol") and self.session["mol"] != "":
            data = data.filter(mol__id=int(self.session["mol"]))

        if self.session.has_key("region") and self.session["region"] != "":
            data = data.filter(store__region__id=int(self.session["region"]))

        if self.session.has_key("search_text") and self.session["search_text"] != "":
            data = data.filter(Q(name__icontains=self.session["search_text"]) | Q(eisup__icontains=self.session["search_text"]) | Q(serial__icontains=self.session["search_text"]))

        return data






    def get_context_data(self, **kwargs):
        context = super(Store, self).get_context_data(**kwargs)
        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        data = store_rest.objects.all()
        context['store_list'] = data.distinct('store')
        context['mol_list'] = data.distinct('mol')
        context['region_list'] = data.distinct('store__region')
        context['search_text'] = self.session['search_text'] if self.session.has_key('search_text') else ""

        context['search'] = self.session["search_text"] if self.session.has_key('search_text') else ""
        context['region'] = self.session["region"] if self.session.has_key('region') else ""
        context['store'] = self.session["store"] if self.session.has_key('store') else ""
        context['mol'] = self.session["mol"] if self.session.has_key('mol') else ""



        return context




### Склад - расход
class StoreOut(ListView):



    model = reestr_proj
    template_name = "regions/store/storeout.html"

    paginate_by = 100



    @method_decorator(login_required(login_url='/'))
    #@method_decorator(group_required(group='project',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):


        data = store_out.objects.order_by('-datetime_update')

        if self.session.has_key("store") and self.session["store"] !="":
            data = data.filter(store_rest__store__id=int(self.session["store"]))

        if self.session.has_key("mol") and self.session["mol"] != "":
            data = data.filter(store_rest__mol__id=int(self.session["mol"]))

        if self.session.has_key("region") and self.session["region"] != "":
            data = data.filter(store_rest__store__region__id=int(self.session["region"]))

        if self.session.has_key("search_text") and self.session["search_text"] != "":
            data = data.filter(Q(store_rest__name__icontains=self.session["search_text"]) | Q(store_rest__eisup__icontains=self.session["search_text"]))

        return data






    def get_context_data(self, **kwargs):
        context = super(StoreOut, self).get_context_data(**kwargs)
        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        data = store_rest.objects.all()
        context['store_list'] = data.distinct('store')
        context['mol_list'] = data.distinct('mol')
        context['region_list'] = data.distinct('store__region')
        context['search_text'] = self.session['search_text'] if self.session.has_key('search_text') else ""

        context['search'] = self.session["search_text"] if self.session.has_key('search_text') else ""
        context['region'] = self.session["region"] if self.session.has_key('region') else ""
        context['store'] = self.session["store"] if self.session.has_key('store') else ""
        context['mol'] = self.session["mol"] if self.session.has_key('mol') else ""



        return context







### Склад - перемещение
class StoreCarry(ListView):



    model = reestr_proj
    template_name = "regions/store/storecarry.html"

    paginate_by = 100



    @method_decorator(login_required(login_url='/'))
    #@method_decorator(group_required(group='project',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):


        data = store_carry.objects.order_by('-datetime_update')

        if self.session.has_key("store") and self.session["store"] !="":
            data = data.filter(store_rest__store__id=int(self.session["store"]))

        if self.session.has_key("mol") and self.session["mol"] != "":
            data = data.filter(store_rest__mol__id=int(self.session["mol"]))

        if self.session.has_key("region") and self.session["region"] != "":
            data = data.filter(store_rest__store__region__id=int(self.session["region"]))

        if self.session.has_key("search_text") and self.session["search_text"] != "":
            data = data.filter(Q(store_rest__name__icontains=self.session["search_text"]) | Q(store_rest__eisup__icontains=self.session["search_text"]))

        return data






    def get_context_data(self, **kwargs):
        context = super(StoreCarry, self).get_context_data(**kwargs)
        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        data = store_rest.objects.all()
        context['store_list'] = data.distinct('store')
        context['mol_list'] = data.distinct('mol')
        context['region_list'] = data.distinct('store__region')
        context['search_text'] = self.session['search_text'] if self.session.has_key('search_text') else ""

        context['search'] = self.session["search_text"] if self.session.has_key('search_text') else ""
        context['region'] = self.session["region"] if self.session.has_key('region') else ""
        context['store'] = self.session["store"] if self.session.has_key('store') else ""
        context['mol'] = self.session["mol"] if self.session.has_key('mol') else ""



        return context








### Склад - поступление
class StoreIn(ListView):

    model = reestr_proj
    template_name = "regions/store/storein.html"

    paginate_by = 100

    @method_decorator(login_required(login_url='/'))
    # @method_decorator(group_required(group='project',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):

        data = store_in.objects.order_by('-datetime_update')

        if self.session.has_key("store") and self.session["store"] != "":
            data = data.filter(store_rest__store__id=int(self.session["store"]))

        if self.session.has_key("mol") and self.session["mol"] != "":
            data = data.filter(store_rest__mol__id=int(self.session["mol"]))

        if self.session.has_key("region") and self.session["region"] != "":
            data = data.filter(store_rest__store__region__id=int(self.session["region"]))

        if self.session.has_key("search_text") and self.session["search_text"] != "":
            data = data.filter(
                Q(store_rest__name__icontains=self.session["search_text"]) | Q(store_rest__eisup__icontains=self.session["search_text"]))

        return data




    def get_context_data(self, **kwargs):
        context = super(StoreIn, self).get_context_data(**kwargs)
        context['tz'] = self.session['tz'] if self.session.has_key('tz') else 'UTC'
        data = store_rest.objects.all()
        context['store_list'] = data.distinct('store')
        context['mol_list'] = data.distinct('mol')
        context['region_list'] = data.distinct('store__region')
        context['search_text'] = self.session['search_text'] if self.session.has_key('search_text') else ""

        context['search'] = self.session["search_text"] if self.session.has_key('search_text') else ""
        context['region'] = self.session["region"] if self.session.has_key('region') else ""
        context['store'] = self.session["store"] if self.session.has_key('store') else ""
        context['mol'] = self.session["mol"] if self.session.has_key('mol') else ""

        return context






### Склад - история изменений
class StoreHistory(ListView):



    model = reestr_proj
    template_name = "regions/store/storehistory.html"

    paginate_by = 100



    @method_decorator(login_required(login_url='/'))
    #@method_decorator(group_required(group='project',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):


        data = store_rest_log.objects.order_by('-datetime_update')

        if self.session.has_key("store") and self.session["store"] !="":
            data = data.filter(store_rest__store__id=int(self.session["store"]))

        if self.session.has_key("mol") and self.session["mol"] != "":
            data = data.filter(store_rest__mol__id=int(self.session["mol"]))

        if self.session.has_key("region") and self.session["region"] != "":
            data = data.filter(store_rest__store__region__id=int(self.session["region"]))

        if self.session.has_key("search_text") and self.session["search_text"] != "":
            data = data.filter(Q(store_rest__name__icontains=self.session["search_text"]) | Q(store_rest__eisup__icontains=self.session["search_text"]) | Q(store_rest__serial__icontains=self.session["search_text"]))

        return data






    def get_context_data(self, **kwargs):
        context = super(StoreHistory, self).get_context_data(**kwargs)
        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        data = store_rest.objects.all()
        context['store_list'] = data.distinct('store')
        context['mol_list'] = data.distinct('mol')
        context['region_list'] = data.distinct('store__region')
        context['search_text'] = self.session['search_text'] if self.session.has_key('search_text') else ""

        context['search'] = self.session["search_text"] if self.session.has_key('search_text') else ""
        context['region'] = self.session["region"] if self.session.has_key('region') else ""
        context['store'] = self.session["store"] if self.session.has_key('store') else ""
        context['mol'] = self.session["mol"] if self.session.has_key('mol') else ""



        return context







### Загрузка складских остатков отдельным интерфейсом
class LoadStore(ListView):



    model = reestr_proj
    template_name = "regions/store/loadstore.html"

    paginate_by = 100



    @method_decorator(login_required(login_url='/'))
    #@method_decorator(group_required(group='project',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):



        return []






    def get_context_data(self, **kwargs):
        context = super(LoadStore, self).get_context_data(**kwargs)
        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'

        users = User.objects.order_by("first_name")
        context['staff'] = [(user.pk, user.get_full_name()) for user in users]
        context['regions'] = regions.objects.order_by("name")


        return context








### Список АВР
class AvrList(ListView):



    model = reestr_proj
    template_name = "regions/avr/avrlist.html"

    paginate_by = 100



    @method_decorator(login_required(login_url='/'))
    #@method_decorator(group_required(group='project',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):

        data = avr.objects.order_by("-datetime_avr")

        return data




    def get_context_data(self, **kwargs):
        context = super(AvrList, self).get_context_data(**kwargs)
        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'

        context["form"] = NewAVRForm()


        return context






### Карточка АВР
class AVREdit(UpdateView):
    model = avr
    form_class = EditAVRForm
    template_name = "regions/avr/avredit.html"
    success_url = '/regions/avr/avr/edit/1/'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(AVREdit, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(AVREdit, self).get_context_data(**kwargs)
        context["avr"] = self.get_object()
        return context


    def form_valid(self, form):
        #form.instance.rowsum = form.instance.price * form.instance.count
        return super(AVREdit, self).form_valid(form)


