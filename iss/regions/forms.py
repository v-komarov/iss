#coding: utf-8

from django.forms import ModelForm
from django import forms
from iss.regions.models import orders, proj, proj_stages, reestr_proj

### Форма ввода и отображения позиции заказа
class OrderForm(ModelForm):
    class Meta:
        model = orders
        fields = ['region', 'order', 'model', 'name', 'ed', 'price', 'b2b_b2o', 'investment', 'to', 'comment', 'tz']




### Форма создания нового проекта
class ProjForm(ModelForm):
    class Meta:
        model = proj
        fields = ['name', 'start', 'temp', ]



### Форма редактирования проекта
class ProjForm2(ModelForm):
    class Meta:
        model = proj
        fields = ['name', 'start', ]



### Форма редактирования этапа проекта
class StageForm(ModelForm):
    depend_on = forms.CharField(label='Зависит от')
    stage_order = forms.CharField(label='Порядковый номер')
    class Meta:
        model = proj_stages
        fields = ['stage_order', 'name', 'days', 'deferment', 'depend_on']




### Форма создание элемента реестра проектов
class ReestrProjCreateForm(ModelForm):
    class Meta:
        model = reestr_proj
        fields = ['proj_name', 'proj_other', 'proj_level', 'proj_init', 'proj_type', 'block', 'region']




### Форма редактирования элемента реестра проектов
class ReestrProjUpdateForm(ModelForm):
    proj_kod = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}), label="Код проекта")
    class Meta:
        model = reestr_proj
        fields = ['rates', 'passing', 'contragent', 'business', 'author', 'proj_type', 'proj_init', 'proj_kod',
                  'proj_name', 'proj_other', 'proj_level', 'proj_type', 'block', 'region', 'author', 'executor',
                  'comment']


