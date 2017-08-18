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
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404
from django.db import connections
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.base import TemplateView,RedirectView
from django.contrib.auth.models import User


from iss.mydecorators import group_required, anonymous_required

from iss.exams.models import questions, sections, tests
from iss.exams.forms import QuestionForm, TestForm






@login_required(login_url='/')
@group_required(group='exams', redirect_url='/exams/questions/')
### Создание "Пустого" вопроса перед редактированием
def CreateQestion(request):

    sec = sections.objects.get(pk=int(request.session['exams-section'], 10))
    q = questions.objects.create(name='Новый вопрос', section=sec)
    #request.session['question_id'] = q.id

    return redirect('/exams/questions/update/%s/1/' % q.id)





@login_required(login_url='/')
@group_required(group='exams', redirect_url='/exams/questions/')
### Создание "Пустого" теста перед редактированием
def CreateTest(request):

    sec = sections.objects.get(pk=int(request.session['exams-section'], 10))
    t = tests.objects.create(name='Новый тест', section=sec)

    return redirect('/exams/tests/update/%s/1/' % t.id)






### Список вопросов
class QuestionsList(ListView):

    model = questions
    template_name = "exams/questions_list.html"

    paginate_by = 2



    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='exams',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        request.session['page'] = kwargs.get('page')
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):


        if self.session.has_key('exams-section'):
            section = sections.objects.get(pk=int(self.session["exams-section"], 10))
            data = questions.objects.filter(section=section).order_by('name')
        else:
            data = []

        n = 1
        ### Порядковый номер
        for item in data:
            item.truth = item.answers_set.filter(truth=True).count()
            item.order = n
            n += 1

        return data







    def get_context_data(self, **kwargs):
        context = super(QuestionsList, self).get_context_data(**kwargs)

        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        context['sections'] = sections.objects.order_by('name')
        context['section'] = self.session['exams-section'] if self.session.has_key('exams-section') else "0"
        context['page'] = self.session['page']

        return context







### Редактировать вопрос
@method_decorator(login_required(login_url='/'), name='dispatch')
@method_decorator(group_required(group='exams', redirect_url='/exams/questions/'), name='dispatch')
class QuestionUpdate(TemplateView):

    template_name = 'exams/question_data.html'

    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='exams', redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        request.session['question_id'] = kwargs.get('question')
        request.session['page'] = kwargs.get('page')
        self.request = request
        self.session = request.session
        self.user = request.user


        return super(QuestionUpdate, self).dispatch(request, *args, **kwargs)




    def get_context_data(self, **kwargs):
        context = super(QuestionUpdate, self).get_context_data(**kwargs)

        q = questions.objects.get(pk=self.session['question_id'])

        context['question_id'] = q.id

        form = QuestionForm(instance=q)
        form.fields['section'].widget.attrs['disabled'] = True
        context['form'] = form

        context['page'] = self.session['page']

        return context





### Список тестов
class TestsList(ListView):

    model = tests
    template_name = "exams/tests_list.html"

    paginate_by = 2



    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='exams',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        request.session['tests_page'] = kwargs.get('page')
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):


        if self.session.has_key('exams-section'):
            section = sections.objects.get(pk=int(self.session["exams-section"], 10))
            data = tests.objects.filter(section=section).order_by('name')
        else:
            data = []

        n = 1
        ### Порядковый номер
        for item in data:
            item.order = n
            n += 1

        return data






    def get_context_data(self, **kwargs):
        context = super(TestsList, self).get_context_data(**kwargs)

        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        context['sections'] = sections.objects.order_by('name')
        context['section'] = self.session['exams-section'] if self.session.has_key('exams-section') else "0"

        return context




### Редактировать тест
@method_decorator(login_required(login_url='/'), name='dispatch')
@method_decorator(group_required(group='exams', redirect_url='/exams/questions/'), name='dispatch')
class TestUpdate(ListView):

    model = questions
    template_name = 'exams/test_data.html'

    paginate_by = 3


    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='exams', redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        request.session['test_id'] = kwargs.get('test')
        self.request = request
        self.session = request.session
        self.user = request.user


        return super(TestUpdate, self).dispatch(request, *args, **kwargs)



    def get_queryset(self):

        t = tests.objects.get(pk=self.session['test_id'])


        if self.session.has_key('exams-section'):
            section = sections.objects.get(pk=int(self.session["exams-section"], 10))
            data = questions.objects.filter(section=section).order_by('name')
        else:
            data = []

        n = 1
        ### Порядковый номер
        for item in data:

            ### Определение включен вопрос в тест или нет
            if t.questions.filter(pk=item.id).exists():
                item.question_ok = True
            else:
                item.question_ok = False

            item.order = n
            n += 1

        return data





    def get_context_data(self, **kwargs):
        context = super(TestUpdate, self).get_context_data(**kwargs)

        t = tests.objects.get(pk=self.session['test_id'])

        context['test_id'] = t.id

        form = TestForm(instance=t)
        form.fields['section'].widget.attrs['disabled'] = True
        context['form'] = form

        context['tests_page'] = self.session['tests_page']


        return context







### Список тестов для обученния
class LearnList(ListView):

    model = tests
    template_name = "exams/learn_list.html"

    paginate_by = 50



    @method_decorator(login_required(login_url='/'))
    def dispatch(self, request, *args, **kwargs):
        request.session['learn_page'] = kwargs.get('page')
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):


        if self.session.has_key('exams-section'):
            section = sections.objects.get(pk=int(self.session["exams-section"], 10))
            data = tests.objects.filter(section=section, learning=True).order_by('name')
        else:
            data = []

        n = 1
        ### Порядковый номер
        for item in data:
            item.order = n
            n += 1

        return data






    def get_context_data(self, **kwargs):
        context = super(LearnList, self).get_context_data(**kwargs)

        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        context['sections'] = sections.objects.order_by('name')
        context['section'] = self.session['exams-section'] if self.session.has_key('exams-section') else "0"
        context['learn_page'] = self.session['learn_page']

        return context





### Обучение
class TestLearning(TemplateView):

    template_name = 'exams/learning.html'

    def dispatch(self, request, *args, **kwargs):
        request.session['test_id'] = kwargs.get('test')
        request.session['page'] = kwargs.get('page')
        self.request = request
        self.session = request.session
        self.user = request.user


        return super(TestLearning, self).dispatch(request, *args, **kwargs)






    def get_context_data(self, **kwargs):
        context = super(TestLearning, self).get_context_data(**kwargs)

        t = tests.objects.get(pk=self.session['test_id'])

        context['page'] = self.session['page']

        context['test_data'] = tests.objects.get(pk=self.session['test_id'])

        return context

