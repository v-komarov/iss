#coding: utf-8




from django.forms import ModelForm
from django import forms



from iss.blocks.models import block_managers



### Форма редактирования элемента компании
class CompanyEditForm(ModelForm):
    name = forms.CharField(label="Название", widget=forms.TextInput(attrs={'class':'input-xm', 'size':80}))
    inn = forms.CharField(label="ИНН", widget=forms.TextInput(attrs={'class':'input-xm', 'size':80}))
    phone = forms.CharField(label="Телефон", widget=forms.TextInput(attrs={'class':'input-xm', 'size':80}))
    email = forms.CharField(label="email", widget=forms.TextInput(attrs={'class':'input-xm', 'size':80}))
    contact = forms.CharField(label="Контакт", widget=forms.Textarea(attrs={'class':'input-xm', 'rows':4, 'cols':78}))
    address2 = forms.CharField(label="Фактический адрес")
    address_law2 = forms.CharField(label="Юридический адрес")




    def __init__(self, *args, **kwargs):
        super(CompanyEditForm, self).__init__(*args, **kwargs)
        self.fields['address2'].initial = self.instance.address.getaddress()
        self.fields['address_law2'].initial = self.instance.address_law.getaddress()
        self.fields['address2'].widget.attrs = {'address_id': self.instance.address.id, 'class':'input-xm', 'size':80}
        self.fields['address_law2'].widget.attrs = {'address_id': self.instance.address_law.id, 'class':'input-xm', 'size':80}


    class Meta:
        model = block_managers
        fields = ['name', 'address2', 'address_law2', 'inn', 'contact', 'phone', 'email', ]
