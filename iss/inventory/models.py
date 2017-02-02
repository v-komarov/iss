#coding:utf-8

from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField
from iss.localdicts.models import address_companies,address_house



### Виды и модели устройств
class devices_scheme(models.Model):
    name = models.CharField(max_length=100, verbose_name='Вид устройства', unique=True)
    scheme_device = JSONField(default={})

    def __unicode__(self):
        return self.name




### Все устройства
class devices(models.Model):
    name = models.CharField(max_length=255,db_index=True,null=True)
    company = models.ForeignKey(address_companies)
    address = models.ForeignKey(address_house)
    serial = models.CharField(max_length=100, db_index=True, default="")
    data = JSONField(default={})
    device_type = models.ForeignKey(devices_scheme,null=True)






