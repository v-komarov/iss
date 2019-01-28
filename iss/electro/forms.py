#coding: utf-8

from django.forms import ModelForm
from django import forms
from mptt.forms import TreeNodeChoiceField

from iss.electro.models import devicestypes, placements


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



### Форма добавления и редактирования элемента размещения
class PlacementForm(ModelForm):
    name = forms.CharField(widget=forms.DateInput(format="%d.%m.%Y"), label="Наименование")
    parent = TreeNodeChoiceField(queryset=placements.objects.all(),level_indicator=u'+--', label="Родительский элемент")
    class Meta:
        model = placements
        fields = ['name','parent']

    def __init__(self, *args, **kwargs):
        super(PlacementForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'class':'form-control input-sm'}
        self.fields['parent'].widget.attrs = {'class':'form-control input-sm'}



### Форма для фильтра справочника видов оборудования
class FilterDeviceTypeForm(ModelForm):
    filter = TreeNodeChoiceField(queryset=devicestypes.objects.all(), level_indicator=u'+--', label="Фильтр")

    class Meta:
        model = devicestypes
        fields = ['filter']

    def __init__(self, *args, **kwargs):
        super(FilterDeviceTypeForm, self).__init__(*args, **kwargs)
        self.fields['filter'].widget.attrs = {'class': 'form-control input-sm'}




### Форма для фильтра справочника размещения
class FilterPlacementForm(ModelForm):
    filter = TreeNodeChoiceField(queryset=placements.objects.all(),level_indicator=u'+--', label="Фильтр")
    class Meta:
        model = placements
        fields = ['filter']

    def __init__(self, *args, **kwargs):
        super(FilterPlacementForm, self).__init__(*args, **kwargs)
        self.fields['filter'].widget.attrs = {'class':'form-control input-sm'}




### Форма для фильтра списка устройств
class FilterDevicesForm(ModelForm):
    filter_d = TreeNodeChoiceField(queryset=devicestypes.objects.all(),level_indicator=u'+--', label="Тип")
    filter_p = TreeNodeChoiceField(queryset=placements.objects.all(),level_indicator=u'+--', label="Размещение")
    class Meta:
        model = devicestypes
        fields = ['filter_d','filter_p']

    def __init__(self, *args, **kwargs):
        super(FilterDevicesForm, self).__init__(*args, **kwargs)
        self.fields['filter_d'].widget.attrs = {'class':'form-control input-sm'}
        self.fields['filter_p'].widget.attrs = {'class':'form-control input-sm'}


