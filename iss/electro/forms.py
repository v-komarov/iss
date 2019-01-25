#coding: utf-8

from django.forms import ModelForm
from django import forms
from mptt.forms import TreeNodeChoiceField

from iss.electro.models import devicestypes


### Форма добавления и редактирования элемента типа оборудования
class DevicesTypesForm(ModelForm):
    name = forms.CharField(widget=forms.DateInput(format="%d.%m.%Y"), label="Наименование")
    parent = TreeNodeChoiceField(queryset=devicestypes.objects.all(),level_indicator=u'+--', label="Родительский элемент")
    class Meta:
        model = devicestypes
        fields = ['name','parent']

    def __init__(self, *args, **kwargs):
        super(DevicesTypesForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'class':'form-control input-sm'}
        self.fields['parent'].widget.attrs = {'class':'form-control input-sm'}
