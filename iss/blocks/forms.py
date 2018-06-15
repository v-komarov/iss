#coding: utf-8




from django.forms import ModelForm
from django import forms



from iss.blocks.models import block_managers



### Форма редактирования элемента компании
class CompanyEditForm(ModelForm):
    name = forms.CharField(label="Название", widget=forms.TextInput(attrs={'class':'input-xm', 'size':60}))
    inn = forms.CharField(label="ИНН", widget=forms.TextInput(attrs={'class':'input-xm', 'size':60}))
    phone = forms.CharField(label="Телефон", widget=forms.TextInput(attrs={'class':'input-xm', 'size':60}))
    email = forms.CharField(label="email", widget=forms.TextInput(attrs={'class':'input-xm', 'size':60}))
    contact = forms.CharField(label="Контакт", widget=forms.Textarea(attrs={'class':'input-xm', 'rows':4, 'cols':58}))
    address2 = forms.CharField(label="Фактический адрес")
    address_law2 = forms.CharField(label="Юридический адрес")




    def __init__(self, *args, **kwargs):
        super(CompanyEditForm, self).__init__(*args, **kwargs)
        self.fields['address2'].initial = self.instance.address.getaddress()
        self.fields['address_law2'].initial = self.instance.address_law.getaddress()
        self.fields['address2'].widget.attrs = {'address_id': self.instance.address.id, 'class':'input-xm', 'size':60}
        self.fields['address_law2'].widget.attrs = {'address_id': self.instance.address_law.id, 'class':'input-xm', 'size':60}


    class Meta:
        model = block_managers
        fields = ['name', 'address2', 'address_law2', 'inn', 'contact', 'phone', 'email', ]




### Форма редактирования элемента дома
class HouseEditForm(ModelForm):
    numstoreys = forms.IntegerField(label="Этажность", widget=forms.TextInput(attrs={'class':'input-xm', 'size':60}))
    numentrances = forms.IntegerField(label="Количество подъездов", widget=forms.TextInput(attrs={'class':'input-xm', 'size':60}))
    numfloars = forms.CharField(label="Количество квартир", widget=forms.TextInput(attrs={'class':'input-xm', 'size':60}))
    address2 = forms.CharField(label="Адрес")
    access = forms.CharField(label="Условие доступа", widget=forms.TextInput(attrs={'class':'input-xm', 'size':60}))
    manager = forms.CharField(label="Управление")



    def __init__(self, *args, **kwargs):
        super(HouseEditForm, self).__init__(*args, **kwargs)
        self.fields['address2'].initial = self.instance.address.getaddress()
        self.fields['address2'].widget.attrs = {'address_id': self.instance.address.id, 'class':'input-xm', 'size':60}
        if self.instance.block_manager:
            self.fields['manager'].initial = self.instance.block_manager.name
            self.fields['manager'].widget.attrs = {'class':'input-xm', 'size':60, 'manager_id':self.instance.block_manager.id}
        else:
            self.fields['manager'].initial = ""
            self.fields['manager'].widget.attrs = {'class':'input-xm', 'size':60}


    class Meta:
        model = block_managers
        fields = [ 'address2','numstoreys', 'numentrances', 'numfloars', 'access', 'manager' ]
