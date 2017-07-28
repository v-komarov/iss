#coding: utf-8

from django.forms import ModelForm
from iss.regions.models import orders, messages

### Форма ввода и отображения позиции заказа
class OrderForm(ModelForm):
    class Meta:
        model = orders
        fields = ['region', 'order', 'model', 'name', 'ed', 'price', 'b2b_b2o', 'investment', 'to','comment', 'tz']



### Форма отображения и корректировки данных сообщения
class MessageForm(ModelForm):
    class Meta:
        model = messages
        fields = ['head', 'message_type', 'message', 'status']
