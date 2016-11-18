#coding:utf-8

import pickle

from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from iss.mydecorators import group_required,anonymous_required

from iss.equipment.models import devices_ip,footnodes,agregators






class EquipmentList(ListView):


    model = devices_ip
    template_name = "equipment/devices_list.html"
    paginate_by = 100


    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='devices',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.session = request.session
        return super(ListView, self).dispatch(request, *args, **kwargs)



    def get_queryset(self):


        q = []
        if self.session.has_key("notaccess"):
            q.append("Q(access=%s)" % False)

        if self.session.has_key("norewrite"):
            q.append("Q(no_rewrite=%s)" % True)

        if self.session.has_key("search"):
            if len(self.session['search']) >= 3:
                for search in self.session['search'].split(" "):
                    print search
                    if search != " ":
                        q.append("(Q(ipaddress__icontains='%s') | Q(device_name__icontains='%s') | Q(device_location__icontains='%s') | Q(device_descr__icontains='%s') | Q(device_location__icontains='%s') | Q(chassisid__icontains='%s') | Q(device_serial__icontains='%s'))" % (search,search,search,search,search,search,search))

        if len(q) == 0:
            return devices_ip.objects.all().order_by('ipaddress')
        else:
            str_q = " & ".join(q)
            str_sql = "devices_ip.objects.filter(%s).order_by('ipaddress')" % str_q

        return eval(str_sql)








    def get_context_data(self, **kwargs):
        context = super(EquipmentList, self).get_context_data(**kwargs)


        if self.session.has_key('tz'):
            context['tz']= self.session['tz']
        else:
            context['tz']= 'UTC'

        if self.session.has_key('notaccess'):
            context["notaccess"] = True
        else:
            context["notaccess"] = False

        if self.session.has_key('norewrite'):
            context["norewrite"] = True
        else:
            context["norewrite"] = False

        # search
        if self.session.has_key('search'):
            context['search'] = self.session['search']
        else:
            context['search'] = ""


        return context





class FootNodeList(ListView):


    model = footnodes
    template_name = "equipment/footnode_list.html"
    paginate_by = 100


    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='devices',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.session = request.session
        return super(ListView, self).dispatch(request, *args, **kwargs)




    def get_queryset(self):


        return footnodes.objects.all().order_by("ipaddress")








    def get_context_data(self, **kwargs):
        context = super(FootNodeList, self).get_context_data(**kwargs)

        ii = []
        for i in devices_ip.objects.all().distinct('device_domen'):
            ii.append(i.device_domen)


        context['domen'] = ii

        if self.session.has_key('tz'):
            context['tz']= self.session['tz']
        else:
            context['tz']= 'UTC'


        return context





class AgregatorsList(ListView):


    model = agregators
    template_name = "equipment/agregators_list.html"
    paginate_by = 100


    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='devices',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.session = request.session
        return super(ListView, self).dispatch(request, *args, **kwargs)




    def get_queryset(self):

        q = []

        if self.session.has_key("search"):
            if len(self.session['search']) >= 3:
                for search in self.session['search'].split(" "):
                    print search
                    if search != " ":
                        q.append("(Q(ipaddress__icontains='%s') | Q(name__icontains='%s') | Q(location__icontains='%s') | Q(descr__icontains='%s') | Q(chassisid__icontains='%s') | Q(serial__icontains='%s'))" % (search,search,search,search,search,search))

        if len(q) == 0:
            return agregators.objects.all().order_by('ipaddress')
        else:
            str_q = " & ".join(q)
            str_sql = "agregators.objects.filter(%s).order_by('ipaddress')" % str_q

        return eval(str_sql)











    def get_context_data(self, **kwargs):
        context = super(AgregatorsList, self).get_context_data(**kwargs)


        ii = []
        for i in devices_ip.objects.all().distinct('device_domen'):
            ii.append(i.device_domen)

        context['domen'] = ii


        fn = []
        for node in footnodes.objects.all():
            fn.append({
                'id':node.id,
                'name':"%s %s" % (node.ipaddress,node.location),
                'domen':node.domen
            })
        context['footnodes'] = fn



        if self.session.has_key('tz'):
            context['tz']= self.session['tz']
        else:
            context['tz']= 'UTC'

        # search
        if self.session.has_key('search'):
            context['search'] = self.session['search']
        else:
            context['search'] = ""


        return context








class Topology(ListView):


    model = agregators
    template_name = "equipment/topology.html"
    paginate_by = 100


    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='devices',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.session = request.session
        return super(ListView, self).dispatch(request, *args, **kwargs)




    def get_queryset(self):


        return []








    def get_context_data(self, **kwargs):
        context = super(Topology, self).get_context_data(**kwargs)

        if self.session.has_key('tz'):
            context['tz']= self.session['tz']
        else:
            context['tz']= 'UTC'


        return context



