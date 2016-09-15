#coding:utf-8


from	django import	forms
from iss.localdicts.models import TzList



tz_list = []
for item in TzList.objects.all().order_by("tz_label"):
    tz_list.append([item.tz_id,item.tz_label])





class	LoginForm(forms.Form):
    login = forms.CharField(label='Логин',required=False)
    passwd = forms.CharField(label='Пароль',widget=forms.TextInput(attrs={'type':'password'}),required=False)
    tz = forms.ChoiceField(label='Часовой пояс', choices=tz_list,required=False)

