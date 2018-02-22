#coding: utf-8



from django.forms import ModelForm
from django import forms

from django.contrib.auth.models import User




# Форма ввода
class phonefilter(forms.Form):
    phones = forms.CharField(label="Список номеров")
    date1 = forms.CharField(label="Начало периода")
    date2 = forms.CharField(label="Конец периода")
    in_out = forms.ChoiceField(label="Входящие/исходящие", choices=[(0,"Входящие"),(1,"Исходящие")])

