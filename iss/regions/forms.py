#coding: utf-8

from django.forms import ModelForm
from django import forms
from iss.regions.models import orders, proj, proj_stages, proj_steps

### Форма ввода и отображения позиции заказа
class OrderForm(ModelForm):
    class Meta:
        model = orders
        fields = ['region', 'order', 'model', 'name', 'ed', 'price', 'b2b_b2o', 'investment', 'to','comment', 'tz']



### Форма отображения и корректировки данных сообщения
"""
class MessageForm(ModelForm):
    class Meta:
        model = messages
        fields = ['head', 'message_type', 'message', 'status']
"""


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
    class Meta:
        model = proj_stages
        fields = ['order', 'name', 'days', 'depend_on']


### Форма редактирования шага проекта
class StepForm(ModelForm):
    depend_on = forms.CharField(label='Зависит от')
    class Meta:
        model = proj_steps
        fields = ['order', 'name', 'days', 'depend_on']
