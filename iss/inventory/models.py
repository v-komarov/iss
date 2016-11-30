#coding:utf-8

from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField
from iss.localdicts.models import devices_type,address_companies,address_house




### Все устройства
class devices(models.Model):
    name = models.CharField(max_length=255,db_index=True,null=True)
    device_type = models.ForeignKey(devices_type)
    company = models.ForeignKey(address_companies)
    address = models.ForeignKey(address_house)
    serial = models.CharField(max_length=100, db_index=True, default="")
    data = JSONField(default={})
