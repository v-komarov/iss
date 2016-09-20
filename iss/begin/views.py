#coding:utf-8

from pytz import timezone

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.utils.timezone import activate


from iss.begin.forms import LoginForm


import iss.settings


"""
class Begin(TemplateView):

    template_name = "index.html"
    form_class = LoginForm

    @csrf_protect
    def get(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        c = RequestContext(request,{"ROOT_URL":iss.settings.ROOT_URL,'form': form})
        return render_to_response(self.template_name, c)


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        c = RequestContext(request,{"ROOT_URL":iss.settings.ROOT_URL,'form': form})
        if form.is_valid():
            login = form.cleaned_data["login"]
            passwd = form.cleaned_data["passwd"]
            tz = form.cleaned_data["tz"]
            request.session['timezone'] = tz
            print("tz",request.session['timezone'])
            user = authenticate(username=login, password=passwd)
            #print(request.POST,user)
            #if user is not None:
            return HttpResponseRedirect('/mainmenu/')

        return render_to_response(self.template_name, c)


    #@csrf_protect
    #def dispatch(self, *args, **kwargs):
    #    return super(Begin, self).dispatch(*args, **kwargs)


"""


def Begin(request):

    form = LoginForm(request.POST)

    if request.method == "POST":
        if form.is_valid():
            log_in = form.cleaned_data["login"]
            passwd = form.cleaned_data["passwd"]
            tz = form.cleaned_data["tz"]
            user = authenticate(username=log_in, password=passwd)

            if user is not None and user.is_active:
                login(request,user)
                activate(timezone(tz))
                request.session['tz'] = tz
                return HttpResponseRedirect('/mainmenu/')


    c = RequestContext(request, locals())
    return render_to_response("begin.html", c)





def MainMenu(request):

    template_name = "mainmenu.html"

    c = RequestContext(request,locals())
    return render_to_response(template_name, c)




def LogOut(request):

    logout(request)

    return HttpResponseRedirect('/')
