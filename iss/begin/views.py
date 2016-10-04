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
