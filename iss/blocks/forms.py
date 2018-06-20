#coding: utf-8




from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User


from iss.blocks.models import block_managers, contracts



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



### Форма ввода и редактирования договоров
class ContractForm(ModelForm):


    def __init__(self, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)
        self.fields['num'].widget.attrs = {'class':'input-xm'}
        self.fields['num'].widget.attrs['style'] = 'width: 170px;'
        self.fields['date_begin'].widget.attrs = {'class':'input-xm'}
        self.fields['date_begin'].widget.attrs['style'] = 'width: 170px;'
        self.fields['date_end'].widget.attrs = {'class':'input-xm'}
        self.fields['date_end'].widget.attrs['style'] = 'width: 170px;'
        self.fields['money'].widget.attrs = {'class':'input-xm'}
        self.fields['money'].widget.attrs['style'] = 'width: 170px;'
        self.fields['period'].widget.attrs = {'class':'form-control input-sm'}
        self.fields['period'].widget.attrs['style'] = 'width: 170px;'
        self.fields['manager'].widget.attrs = {'class':'form-control input-sm'}
        self.fields['manager'].widget.attrs['style'] = 'width: 170px;'

        users = User.objects.order_by("first_name")
        user_list = [("","-------")]
        user_list.extend([(user.pk, user.get_full_name()) for user in users])

        self.fields['manager'].choices = user_list

    class Meta:
        model = contracts
        fields = ['num', 'date_begin', 'date_end', 'goon', 'manager', 'money', 'period',]

