#coding: utf-8

from django.forms import ModelForm
from django import forms
from iss.exams.models import questions, answers, tests

### Форма ввода и отображения вопроса
class QuestionForm(ModelForm):
    class Meta:
        model = questions
        fields = ['name', 'section',]



### Форма данных варианта ответа
class AnswerForm(ModelForm):
    class Meta:
        model = answers
        fields = ['name', 'truth', ]



### Форма ввода и отображения теста
class TestForm(ModelForm):
    class Meta:
        model = tests
        fields = ['name', 'section', 'testtime', 'mistakes', 'learning']

