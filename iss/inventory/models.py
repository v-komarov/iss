#coding:utf-8

from __future__ import unicode_literals

import datetime

from django.db import models
from django.contrib.postgres.fields import JSONField
from iss.localdicts.models import address_companies,address_house,ports,slots,port_status,slot_status,interfaces,device_status



### Виды и модели устройств
class devices_scheme(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', unique=True)
    scheme_device = JSONField(default={})
    author = models.CharField(max_length=100,default="")
    datetime_create = models.DateTimeField(auto_now_add=True,null=True)

    def __unicode__(self):
        return self.name






### Модели интерфейсов
class interfaces_scheme(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', unique=True)
    scheme_interface = JSONField(default={})
    author = models.CharField(max_length=100, default="")
    datetime_create = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.name





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


    def __unicode__(self):
        return self.name


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

    def __unicode__(self):
        return self.num

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

    def __unicode__(self):
        return self.num

    class Meta:
        unique_together = ('device', 'port', 'slot', 'num')




### Сетевые интерфейсы
class netinterfaces(models.Model):
    value = models.CharField(max_length=100)
    interface = models.ForeignKey(interfaces,null=True)
    port = models.ManyToManyField(devices_ports)




### Сетевые элементы
class netelems(models.Model):
    name = models.CharField(max_length=100,unique=True)
    netinterface = models.ManyToManyField(netinterfaces)
    device = models.ManyToManyField(devices)
    author = models.CharField(max_length=100, default="")
    datetime_create = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.name




### Договора клиентов на порту
class client_dogovor(models.Model):
    port = models.OneToOneField(netinterfaces)
    dogovor = models.CharField(max_length=20)



