#coding:utf-8

from django.core import validators

from	django import	forms
from django.forms import ModelForm
from iss.localdicts.models import TzList
from iss.monitor.models import Profile


tz_list = []
for item in TzList.objects.all().order_by("tz_label"):
    tz_list.append([item.tz_id,item.tz_label])




### Форма входа
class LoginForm(forms.Form):
    login = forms.CharField(label='Логин',required=False)
    passwd = forms.CharField(label='Пароль',widget=forms.TextInput(attrs={'type':'password'}),required=False)
    tz = forms.ChoiceField(label='Часовой пояс', choices=tz_list,required=False)



### Форма ввода данных нового пользователя
class NewUserForm(forms.Form):
    login = forms.CharField(validators=[validators.validate_slug], label='Логин', required=True)
    passwd = forms.CharField(validators=[validators.validate_slug], label='Пароль', widget=forms.TextInput(attrs={'type':'password'}),required=True)
    email = forms.EmailField(validators=[validators.validate_slug], label='email', required=True)
    firstname = forms.CharField(validators=[validators.validate_slug], label='Имя', required=True)
    lastname = forms.CharField(validators=[validators.validate_slug], label='Фамилия', required=True)




### Форма редактирования атрибутов пользователя
class UserAttrsForm(forms.Form):
    id = forms.CharField(label="id", widget=forms.TextInput(attrs={'hidden':'hidden'}), required = False)
    first_name = forms.CharField(label="Имя", required = False)
    last_name = forms.CharField(label="Фамилия", required = False)
    surname = forms.CharField(label="Отчетсво", required = False)
    job = forms.CharField(label="Должность", required = False)
    email = forms.CharField(label="Email", required = False)
    phone = forms.CharField(label="Внутренний телефон", required = False)

