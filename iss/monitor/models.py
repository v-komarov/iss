#coding:utf-8

from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField

import datetime


class events(models.Model):

    source = models.CharField(max_length=255,db_index=True,default="")

    datetime_evt = models.DateTimeField(db_index=True,null=True)
    uuid = models.CharField(max_length=255,unique=True,db_index=True,null=True)
    first_seen = models.DateTimeField(db_index=True,null=True)
    update_time = models.DateTimeField(db_index=True,null=True)
    last_seen = models.DateTimeField(db_index=True,null=True)
    event_class = models.CharField(max_length=255,db_index=True,null=True)
    severity_id = models.IntegerField(db_index=True,null=True)
    manager = models.CharField(max_length=255,db_index=True,null=True)
    device_system = models.CharField(max_length=255,db_index=True,null=True)
    device_group = models.CharField(max_length=255,db_index=True,null=True)
    device_class = models.CharField(max_length=255,db_index=True,null=True)
    device_net_address = models.CharField(max_length=255,db_index=True,null=True)
    device_location = models.CharField(max_length=255,db_index=True,null=True)
    element_identifier = models.CharField(max_length=255,db_index=True,null=True)
    element_sub_identifier = models.CharField(max_length=255,null=True)
    status_id = models.IntegerField(db_index=True,null=True)
    update_row = models.DateTimeField(auto_now=True,null=True)

    data = JSONField(default={})

