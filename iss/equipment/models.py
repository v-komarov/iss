#coding:utf-8

from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField


## Устройства
class devices_ip(models.Model):
    ipaddress = models.GenericIPAddressField(max_length=255,db_index=True,null=True)
    device_descr = models.CharField(max_length=255,db_index=True,null=True)
    device_location = models.CharField(max_length=255,db_index=True,null=True)
    device_name = models.CharField(max_length=255, db_index=True, null=True)
    device_domen = models.CharField(max_length=255, db_index=True, null=True, default=None)
    chassisid = models.CharField(max_length=255,db_index=True,null=True)
    lldp_neighbor_mac = ArrayField(models.CharField(max_length=100),blank=True,default=[],null=True,db_index=True)
    device_serial = models.CharField(max_length=100,db_index=True,default="")
    update = models.DateTimeField(auto_now=True, null=True)
    no_rewrite = models.BooleanField(default=False)  # Не опрашивать, не переписывать
    access = models.BooleanField(default=True) # При опросе последний раз
    ports = JSONField(default={})
    data = JSONField(default={})

    class Meta:
        unique_together = ('ipaddress', 'device_domen')

### Лог ошибок доступа
class device_access_error(models.Model):
    ipaddress = models.GenericIPAddressField(max_length=255,db_index=True,null=True)
    device_domen = models.CharField(max_length=255, db_index=True, null=True, default=None)
    create = models.DateTimeField(auto_now_add=True,null=True)


### Опорные узлы
class footnodes(models.Model):
    ipaddress = models.GenericIPAddressField(max_length=255,db_index=True,null=True)
    device_domen = models.CharField(max_length=255, db_index=True, null=True, default=None)
    descr = models.CharField(max_length=255, db_index=True, null=True)
    location = models.CharField(max_length=255, db_index=True, null=True)
    name = models.CharField(max_length=255, db_index=True, null=True)
    domen = models.CharField(max_length=255, db_index=True, null=True, default=None)
    data = JSONField(default={})
    chassisid = models.CharField(max_length=255, db_index=True, null=True)
    serial = models.CharField(max_length=100, db_index=True, default="")


### Агрегаторы
class agregators(models.Model):
    ipaddress = models.GenericIPAddressField(max_length=255,db_index=True,null=True)
    uplink_ports = ArrayField(models.IntegerField(),blank=True,default=[],null=True,db_index=True)
    device_domen = models.CharField(max_length=255, db_index=True, null=True, default=None)
    descr = models.CharField(max_length=255, db_index=True, null=True)
    location = models.CharField(max_length=255, db_index=True, null=True)
    name = models.CharField(max_length=255, db_index=True, null=True)
    domen = models.CharField(max_length=255, db_index=True, null=True, default=None)
    footnode = models.ForeignKey(footnodes,null=True)
    data = JSONField(default={})
    chassisid = models.CharField(max_length=255, db_index=True, null=True)

    class Meta:
        unique_together = ('ipaddress', 'domen')


### Список адресов для snmp запросов
class scan_iplist(models.Model):
    ipaddress = models.GenericIPAddressField(max_length=255,db_index=True)
    device_domen = models.CharField(max_length=255, db_index=True, null=True, default=None)
    community = models.CharField(max_length=255, db_index=True, null=True, default=None)
    snmp_ver = models.IntegerField(null=True, default=2)

    def __unicode__(self):
        return self.ipaddress

    class Meta:
        unique_together = ('ipaddress', 'device_domen')
        verbose_name = 'Адрес'
        verbose_name_plural = 'Список адресов'
