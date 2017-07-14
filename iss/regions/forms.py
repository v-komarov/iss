#coding: utf-8

from django.forms import ModelForm
from iss.regions.models import orders

### Форма ввода и отображения позиции заказа
class OrderForm(ModelForm):
    class Meta:
        model = orders
        fields = ['region', 'order', 'model', 'name', 'ed', 'count', 'price', 'comment']
