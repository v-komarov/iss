#coding: utf-8




from django.forms import ModelForm
from django import forms

from django.contrib.auth.models import User


from iss.regions.models import orders, proj, proj_stages, reestr_proj, reestr_proj_exec_date
from iss.localdicts.models import stages



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
        fields = ['proj_name', ]




### Форма редактирования элемента реестра проектов
class ReestrProjUpdateForm(ModelForm):
    proj_kod = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}), label="Код проекта")
    date_service = forms.CharField(widget=forms.DateInput(format="%d.%m.%Y"), label="Дата оказания услуги")
    class Meta:
        model = reestr_proj
        fields = ['rates', 'passing', 'contragent', 'business', 'author', 'proj_init', 'proj_kod', 'date_service',
                  'proj_name', 'proj_other', 'region', 'author', 'executor',
                  'comment']



### Форма исполнителей и дат по стадиям реестра проектов
class WorkersDatesStagesForm(ModelForm):
    date1 = forms.CharField(widget=forms.DateInput(format="%d.%m.%Y"), label="Дата с")
    date2 = forms.CharField(widget=forms.DateInput(format="%d.%m.%Y"), label="Дата до")

    def __init__(self, *args, **kwargs):
        super(WorkersDatesStagesForm, self).__init__(*args, **kwargs)
        users = User.objects.order_by("first_name")
        self.fields['worker'].choices = [(user.pk, user.get_full_name()) for user in users]
        stages_choices = [("","-----"),]
        for item in stages.objects.filter(level=None).order_by("name"):
            stages_choices.append((item.id,item.name))
            for item2 in item.stage2.all():
                stages_choices.append((item2.id, "    "+item2.name))

        self.fields['stage'].choices = stages_choices

    class Meta:
        model = reestr_proj_exec_date
        fields = ['stage', 'date1', 'date2', 'worker', 'block']