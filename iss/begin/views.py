#coding:utf-8

from pytz import timezone

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.utils.timezone import activate


from iss.begin.forms import LoginForm, UserAttrsForm


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






def AccessRefused(request):

    template_name = "begin/access_refused.html"

    c = RequestContext(request,locals())
    return render_to_response(template_name, c)







def LogOut(request):

    logout(request)

    return HttpResponseRedirect('/')




### Форма атрибутов пользователя
def UserAttrs(request):

    if request.user.is_authenticated():

        user = request.user

        #form.fields['first_name'].initial = user.first_name
        #form.fields['last_name'].initial = user.last_name
        #form.fields['email'].initial = user.email
        #form.fields['phone'].initial = user.profile.phone

        form = UserAttrsForm(request.POST)

        if request.method == "POST":
            if form.is_valid():
                first_name = form.cleaned_data["first_name"]
                last_name = form.cleaned_data["last_name"]
                surname = form.cleaned_data["surname"]
                job = form.cleaned_data["job"]
                email = form.cleaned_data["email"]
                phone = form.cleaned_data["phone"]

                user.first_name = first_name.strip()
                user.last_name = last_name.strip()
                user.email = email.strip()
                user.save()

                prof = user.profile
                prof.phone = phone
                prof.surname = surname.strip()
                prof.job = job.strip()
                prof.save()



        else:
            form = UserAttrsForm(
                initial={"first_name": user.first_name, "last_name": user.last_name, "email": user.email,
                         "phone": user.profile.phone, "surname": user.profile.surname, "job": user.profile.job})

        c = RequestContext(request, locals())
        return render_to_response("begin/userattrs.html", c)

    else:
        return HttpResponseRedirect("/")
