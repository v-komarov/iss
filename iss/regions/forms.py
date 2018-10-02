#coding: utf-8




from django.forms import ModelForm
from django import forms

from django.contrib.auth.models import User


from iss.regions.models import orders, proj, proj_stages, reestr_proj, reestr_proj_exec_date, avr, avr_gsm, avr_workers, avr_commission
from iss.localdicts.models import stages, regions, address_city



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
                  'comment', 'object_price', 'smr_price', 'other_price']



### Форма исполнителей и дат по стадиям реестра проектов
class WorkersDatesStagesForm(ModelForm):
    date1 = forms.CharField(widget=forms.DateInput(format="%d.%m.%Y"), label="Дата с")
    date2 = forms.CharField(widget=forms.DateInput(format="%d.%m.%Y"), label="Дата до")

    def __init__(self, *args, **kwargs):
        super(WorkersDatesStagesForm, self).__init__(*args, **kwargs)
        users = User.objects.order_by("first_name")
        workers = [("","-------")]
        workers.extend([(user.pk, user.get_full_name()) for user in users])

        self.fields['worker'].choices = workers
        stages_choices = [("","-----"),]
        for item in stages.objects.filter(level=None).order_by("name"):
            stages_choices.append((item.id,item.name))
            for item2 in item.stage2.all():
                stages_choices.append((item2.id, "    "+item2.name))

        self.fields['stage'].choices = stages_choices

    class Meta:
        model = reestr_proj_exec_date
        fields = ['stage', 'date1', 'date2', 'worker', 'block']




### Форма АВР
class AVRForm(ModelForm):

    region = forms.ChoiceField(label="Регион")
    city = forms.ChoiceField(label="Город")
    objnet = forms.CharField(label="Объект сети", widget=forms.TextInput(attrs={'class':'input-sm class100' }))
    area = forms.CharField(label="Участок", widget=forms.TextInput(attrs={'class':'input-sm class100' }))
    complex = forms.CharField(label="Пусковой комплекс", widget=forms.TextInput(attrs={'class':'input-sm class100' }))
    address = forms.CharField(label="Адрес", widget=forms.TextInput(attrs={'class':'input-sm class100'}))
    datetime_avr = forms.CharField(label="Дата АВР", widget=forms.DateTimeInput(attrs={'class':'input-sm class100'}, format="%d.%m.%Y"))
    datetime_work = forms.CharField(label="Дата выезда", widget=forms.DateTimeInput(attrs={'class':'input-sm class100'}, format="%d.%m.%Y"))
    staff = forms.ChoiceField(label="МОЛ")
    commission = forms.ChoiceField(label="Комиссия")


    class Meta:
        model = avr
        fields = ['region', 'city', 'objnet', 'address', 'datetime_avr', 'datetime_work', 'status', 'staff', 'area', 'complex', 'commission']






### Форма создания АВР
class NewAVRForm(AVRForm):

    def __init__(self, *args, **kwargs):
        super(NewAVRForm, self).__init__(*args, **kwargs)
        self.fields['region'].widget.attrs = {'class':'form-control input-sm col-sm-2'}
        self.fields['city'].widget.attrs = {'class':'form-control input-sm col-sm-2'}
        self.fields['staff'].widget.attrs = {'class':'form-control input-sm col-sm-2'}
        self.fields['commission'].widget.attrs = {'class':'form-control input-sm col-sm-2'}

        users = User.objects.order_by("first_name")
        user_list = [("","-------")]
        user_list.extend([(user.pk, user.get_full_name()) for user in users])

        self.fields['staff'].choices = user_list

        rs = regions.objects.order_by("name")
        region_list = [("","-------")]
        region_list.extend([(x.id, x.name) for x in rs])

        self.fields['region'].choices = region_list

        cs = address_city.objects.order_by("name")
        city_list = [("","-------")]
        city_list.extend([(x.id, x.name) for x in cs])

        self.fields['city'].choices = city_list

        comm = avr_commission.objects.order_by("name")
        comm_list = [("","-------")]
        comm_list.extend([(x.id, x.name) for x in comm])
        self.fields['commission'].choices = comm_list




    class Meta:
        model = avr
        fields = ['region', 'city', 'objnet', 'address', 'datetime_avr', 'datetime_work', 'staff', 'area', 'complex', 'commission']







### Форма редактирования АВР
class EditAVRForm(AVRForm):

    avr_id = forms.CharField(label="id", widget=forms.TextInput(attrs={'hidden': 'hidden'}))
    status = forms.IntegerField(label="status", widget=forms.TextInput(attrs={'hidden': 'hidden'}))
    stuff_allow = forms.CharField(label="stuff_allow", widget=forms.TextInput(attrs={'hidden': 'hidden'}))
    price_allow = forms.CharField(label="price_allow", widget=forms.TextInput(attrs={'hidden': 'hidden'}))

    def __init__(self, *args, **kwargs):
        super(EditAVRForm, self).__init__(*args, **kwargs)
        self.fields['region'].widget.attrs = {'class':'form-control input-sm col-sm-2'}
        self.fields['city'].widget.attrs = {'class':'form-control input-sm col-sm-2'}
        self.fields['staff'].widget.attrs = {'class':'form-control input-sm col-sm-2', 'disabled':'disabled'}
        self.fields['commission'].widget.attrs = {'class':'form-control input-sm col-sm-2'}

        users = User.objects.order_by("first_name")
        user_list = [("","-------")]
        user_list.extend([(user.pk, user.get_full_name()) for user in users])

        self.fields['staff'].choices = user_list

        rs = regions.objects.order_by("name")
        region_list = [("","-------")]
        region_list.extend([(x.id, x.name) for x in rs])

        self.fields['region'].choices = region_list

        cs = address_city.objects.order_by("name")
        city_list = [("","-------")]
        city_list.extend([(x.id, x.name) for x in cs])

        self.fields['city'].choices = city_list

        self.fields["avr_id"].initial = self.instance.id
        self.fields["status"].initial = self.instance.status.id
        self.fields["stuff_allow"].initial = "yes" if self.instance.status.stuff else "no"
        self.fields["price_allow"].initial = "yes" if self.instance.status.price else "no"

        comm = avr_commission.objects.order_by("name")
        comm_list = [("","-------")]
        comm_list.extend([(x.id, x.name) for x in comm])
        self.fields['commission'].choices = comm_list




    class Meta:

        model = avr
        fields = ['avr_id', 'region', 'city', 'objnet', 'address', 'datetime_avr', 'datetime_work', 'staff', 'area', 'complex', 'commission']






### Форма ГСМ
class GSMForm(ModelForm):



    class Meta:
        model = avr_gsm
        fields = ['consumer', 'km', 'h', 'petrol', 'kg', 'comment',]




### Форма трудозатрат
class WorkerForm(ModelForm):

    staff = forms.ChoiceField(label="Исполнитель")

    def __init__(self, *args, **kwargs):
        super(WorkerForm, self).__init__(*args, **kwargs)
        self.fields['staff'].widget.attrs = {'class':'form-control input-sm col-sm-2'}

        users = User.objects.order_by("first_name")
        user_list = [("","-------")]
        user_list.extend([(user.pk, user.get_full_name()) for user in users])

        self.fields['staff'].choices = user_list


    class Meta:
        model = avr_workers
        fields = ['staff', 'h', 'h_day', 'h_night', 'comment']

