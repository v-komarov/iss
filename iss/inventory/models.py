#coding:utf-8

from __future__ import unicode_literals

import datetime

from django.db import models
from django.contrib.postgres.fields import JSONField
from iss.localdicts.models import address_companies,address_house,ports,slots,port_status,slot_status,interfaces



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




### Порты на устройствах
class devices_ports(models.Model):
    device = models.ForeignKey(devices)
    port = models.ForeignKey(ports)
    num = models.IntegerField()
    status = models.ForeignKey(port_status)



### Слоты на устройствах
class devices_slots(models.Model):
    device = models.ForeignKey(devices)
    slot = models.ForeignKey(slots)
    status = models.ForeignKey(slot_status)




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



### Договора клиентов на порту
class client_dogovor(models.Model):
    port = models.OneToOneField(netinterfaces)
    dogovor = models.CharField(max_length=20)



