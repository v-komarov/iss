#coding:utf-8

from __future__ import unicode_literals

import datetime

from django.db import models
from django.contrib.postgres.fields import JSONField
from iss.localdicts.models import address_companies,address_house,ports,slots,port_status,slot_status,interfaces,device_status,logical_interfaces_prop_list




port_use = port_status.objects.get(name='Используется')
port_reserv = port_status.objects.get(name='Резерв')
port_tech = port_status.objects.get(name='Технологический')
prop = logical_interfaces_prop_list.objects.get(name='ipv4')
onyma = logical_interfaces_prop_list.objects.get(name='onyma')


### Виды и модели устройств
class devices_scheme(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', unique=True)
    scheme_device = JSONField(default={})
    author = models.CharField(max_length=100,default="")
    datetime_create = models.DateTimeField(auto_now_add=True,null=True)

    def __unicode__(self):
        return self.name

    ### Количество портов
    def get_ports_count(self):
        return len(self.scheme_device["ports"])

    ### Количество слотов
    def get_slots_count(self):
        return len(self.scheme_device["slots"])

    ### Количестов комбо
    def get_combo_count(self):
        return len(self.scheme_device["combo"])





### Все устройства
class devices(models.Model):
    name = models.CharField(max_length=255,db_index=True,null=True)
    company = models.ForeignKey(address_companies)
    address = models.ForeignKey(address_house)
    serial = models.CharField(max_length=100, db_index=True, default="")
    data = JSONField(default={})
    device_scheme = models.ForeignKey(devices_scheme,null=True)
    author = models.CharField(max_length=100, default="")
    datetime_create = models.DateTimeField(auto_now_add=True, null=True)
    status = models.ForeignKey(device_status,null=True)
    device_parent = models.ForeignKey('devices',default=None,null=True)



    def __unicode__(self):
        return self.name


    def getstatus(self):
        status = self.status.name if self.status else ""
        return status

    ### Строка географического адреса
    def getaddress(self):

        city = self.address.city.name if self.address.city else ''
        street = self.address.street.name if self.address.street else ''
        house = self.address.house if self.address.house else ''

        return "%s %s %s" % (city,street,house)



    ### Подсчет количества используемых портов и комбо портов
    def getzkl(self):
        return self.devices_ports_set.all().filter(status=port_use).count() + self.devices_combo_set.all().filter(status_port=port_use).count()



    ### Портов технологических
    def get_tech_ports(self):
        return self.devices_ports_set.filter(status=port_tech).count()


    ### Портов пользовательских
    def get_use_ports(self):
        return self.devices_ports_set.filter(status=port_use).count()


    ### Портов в резерве
    def get_reserv_ports(self):
        return self.devices_ports_set.filter(status=port_reserv).count()


    #### Комбо порты технологические
    def get_tech_combo(self):
        return self.devices_combo_set.filter(status_port=port_tech).count()


    #### Комбо порты пользовательские
    def get_use_combo(self):
        return self.devices_combo_set.filter(status_port=port_use).count()


    #### Комбо порты пользовательские
    def get_reserv_combo(self):
        return self.devices_combo_set.filter(status_port=port_reserv).count()


    #### Список связанных сетевых элементов
    def get_netelems(self):
        netelems = []

        for el in self.netelems_set.all():
            netelems.append({
                'id':el.id,
                'name':el.name
            })

        return netelems




    #### ip адреса управления
    def get_manage_ip(self):

        manage = []

        #### Обход связанных сетевых элементов
        for el in self.netelems_set.all():
            ### Обход связанных логических интерфейсов
            for li in el.logical_interfaces_set.all():
                ### Обход свойств логичского интерфейса
                for p in li.logical_interfaces_prop_set.filter(prop=prop,logical_interface__name='manage'):
                    manage.append(p.val)

        return manage



    ### Количество портов
    def get_ports_count(self):
        return self.devices_ports_set.count()


    ### Количество комбо портов
    def get_combo_count(self):
        return self.devices_combo_set.count()


    ### Количество слотов
    def get_slots_count(self):
        return self.device_link.count()




    ### Создание портов устройства согласно модели
    def mkports(self,author=""):
        if self.device_scheme != None:
            if self.device_scheme.scheme_device.has_key("ports"):
                for item in self.device_scheme.scheme_device["ports"].keys():
                    ### Тип порта
                    port_type = ((self.device_scheme.scheme_device["ports"])[item])["type"]
                    p = ports.objects.get(name=port_type)
                    ### Статус порта
                    status = port_status.objects.get(pk=3)
                    devices_ports.objects.create(
                        device=self,
                        port=p,
                        num = item,
                        status = status,
                        author=author
                    )
            else:

                return "ports doesn't exist!"

        else:

            return "scheme is empty!"

        return "ok"




    ### Создание слотов устройства согласно модели
    def mkslots(self,author=""):
        if self.device_scheme != None:
            if self.device_scheme.scheme_device.has_key("slots"):
                for item in self.device_scheme.scheme_device["slots"].keys():
                    ### Тип слота
                    slot_type = ((self.device_scheme.scheme_device["slots"])[item])["type"]
                    s = slots.objects.get(name=slot_type)
                    ### Статус слота
                    status = slot_status.objects.get(pk=2)
                    devices_slots.objects.create(
                        device=self,
                        slot=s,
                        num = item,
                        status = status,
                        author = author
                    )

            else:

                return "slots doesn't exist!"

        else:

            return "scheme is empty!"

        return "ok"




    ### Создание комбо портов
    def mkcombo(self,author=""):

        if self.device_scheme != None:
            if self.device_scheme.scheme_device.has_key("combo"):
                for item in self.device_scheme.scheme_device["combo"].keys():
                    ### Тип порта
                    port_type = (((self.device_scheme.scheme_device["combo"])[item])["port"] )["type"]
                    p = ports.objects.get(name=port_type)
                    ### Тип слота
                    slot_type = (((self.device_scheme.scheme_device["combo"])[item])["slot"])["type"]
                    s = slots.objects.get(name=slot_type)
                    ### Статус слота
                    status_s = slot_status.objects.get(pk=2)
                    ### Статус порта
                    status_p = port_status.objects.get(pk=3)

                    devices_combo.objects.create(
                        device = self,
                        slot = s,
                        port = p,
                        num = item,
                        status_port = status_p,
                        status_slot = status_s,
                        author = author
                    )

            else:

                return "combo doesn't exist!"

        else:

            return "scheme is empty!"

        return "ok"




    ### Создание списка свойств
    def mkprop(self,author=""):

        if self.device_scheme != None:
            if self.device_scheme.scheme_device.has_key("properties"):
                for item in self.device_scheme.scheme_device["properties"]:

                    devices_properties.objects.create(
                        device = self,
                        name = item,
                        author=author
                    )

            else:

                return "properties doesn't exist!"

        else:

            return "scheme is empty!"

        return "ok"




    ### Удаление свойств , портов, слотов и комбо элемента
    def clearenv(self):
        devices_properties.objects.filter(device=self).delete()
        devices_ports.objects.filter(device=self).delete()
        devices_slots.objects.filter(device=self).delete()
        devices_combo.objects.filter(device=self).delete()

        return "ok"




### Перемещение устройств
class devices_removal(models.Model):
    device = models.ForeignKey(devices)
    address = models.ForeignKey(address_house)
    author = models.CharField(max_length=100, default="")
    datetime_create = models.DateTimeField(auto_now_add=True, null=True)
    comment = models.TextField(default="")




### Статусы устройств
class devices_statuses(models.Model):
    device = models.ForeignKey(devices)
    author = models.CharField(max_length=100, default="")
    datetime_create = models.DateTimeField(auto_now_add=True, null=True)
    comment = models.TextField(default="")
    status = models.ForeignKey(device_status, null=True)





### Набор свойств устройства (определяется моделью)
class devices_properties(models.Model):
    device = models.ForeignKey(devices)
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=255,default="")
    author = models.CharField(max_length=100,default="")
    datetime_update = models.DateTimeField(auto_now=True,null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('device', 'name', 'value')




### Порты на устройствах
class devices_ports(models.Model):
    device = models.ForeignKey(devices)
    port = models.ForeignKey(ports)
    num = models.CharField(max_length=5,default="")
    status = models.ForeignKey(port_status)
    author = models.CharField(max_length=100,default="")
    datetime_update = models.DateTimeField(auto_now=True,null=True)
    comment = models.CharField(max_length=255,default="")

    def __unicode__(self):
        return self.num


    ### Список договоров на связанном с портом интерфейсе
    def get_dogcode_list(self):
        result = []
        for li in self.logical_interfaces_set.all():
            for p in li.logical_interfaces_prop_set.filter(prop=onyma):
                result.append(p.val)

        return " ".join(result)



    class Meta:
        unique_together = ('device', 'port', 'num')






### Слоты на устройствах
class devices_slots(models.Model):
    device = models.ForeignKey(devices,related_name="device_link")
    slot = models.ForeignKey(slots)
    num = models.CharField(max_length=5,default="")
    status = models.ForeignKey(slot_status)
    device_component = models.ForeignKey(devices,null=True,related_name="slots_link")
    author = models.CharField(max_length=100,default="")
    datetime_update = models.DateTimeField(auto_now=True,null=True)
    comment = models.CharField(max_length=255,default="")

    def __unicode__(self):
        return self.num

    class Meta:
        unique_together = ('device', 'slot', 'num')





### Для комбо
class devices_combo(models.Model):
    device = models.ForeignKey(devices)
    slot = models.ForeignKey(slots)
    port = models.ForeignKey(ports)
    num = models.CharField(max_length=5,default="")
    status_slot = models.ForeignKey(slot_status)
    status_port = models.ForeignKey(port_status)
    author = models.CharField(max_length=100,default="")
    datetime_update = models.DateTimeField(auto_now=True,null=True)
    comment = models.CharField(max_length=255,default="")

    def __unicode__(self):
        return self.num

    class Meta:
        unique_together = ('device', 'port', 'slot', 'num')





### Сетевые элементы
class netelems(models.Model):
    name = models.CharField(max_length=100,unique=True)
    device = models.ManyToManyField(devices) # связь с аппаратной частью
    author = models.CharField(max_length=100, default="")
    datetime_create = models.DateTimeField(auto_now_add=True, null=True)


    def __unicode__(self):
        return self.name



    ### Список договоров на сетевом элементе
    def get_dogcode_list(self):
        result = []
        for li in self.logical_interfaces_set.all():
            for p in li.logical_interfaces_prop_set.filter(prop=onyma):
                result.append(p.val)

        return " ".join(result)




### Логические интерфейсы
class logical_interfaces(models.Model):
    name = models.CharField(max_length=100)
    netelem = models.ForeignKey(netelems)
    comment = models.CharField(max_length=200)
    ports = models.ManyToManyField(devices_ports)

    def __unicode__(self):
        return self.name


    ### Вывод информации по зкл
    def get_zkl(self,ip):

        port_use = port_status.objects.get(name='Используется')
        port_reserv = port_status.objects.get(name='Резерв')
        port_tech = port_status.objects.get(name='Технологический')

        ### Определение сетевого элемента
        ne = self.netelem
        ### Список связанных устройств
        use =  []
        for dev in ne.device.all():


            use.append({
                'sysname':ne.name,
                'ip':ip,
                'address':dev.getaddress(),
                'port_use':dev.devices_ports_set.filter(status=port_use).count() + dev.devices_combo_set.filter(status_port=port_use).count(),
                'port_reserv':dev.devices_ports_set.filter(status=port_reserv).count() + dev.devices_combo_set.filter(status_port=port_reserv).count(),
                'port_tech':dev.devices_ports_set.filter(status=port_tech).count() + dev.devices_combo_set.filter(status_port=port_tech).count()
            })

        return use


    ### Формирование списка id устройст , связанных с ip адресом управления
    def get_dev_list(self):

        dev_list = []

        ### Определение сетевого элемента
        ne = self.netelem
        ### Список связанных устройств
        for dev in ne.device.all():
            if not dev.id in dev_list:
                dev_list.append(dev.id)

        return dev_list




    ### Проверка существует ли приязанный к этому интерфейсу договор
    def check_dogcode(self,dogcode):
        if self.logical_interfaces_prop_set.all().filter(prop=onyma,val=dogcode).exists():
            return True
        else:
            return False







### Свойства логических интерфейсов
class logical_interfaces_prop(models.Model):
    logical_interface = models.ForeignKey(logical_interfaces)
    prop = models.ForeignKey(logical_interfaces_prop_list)
    val = models.CharField(max_length=100,null=True)
    comment = models.CharField(max_length=200)
