#coding:utf-8

from __future__ import unicode_literals

import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
import datetime
from iss.localdicts.models import Status,Severity





class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    settings = JSONField(default={})



### События
class events(models.Model):

    id = models.CharField(max_length=255,primary_key=True, default=uuid.uuid4, editable=False)
    source = models.CharField(max_length=255,db_index=True,default="")
    datetime_evt = models.DateTimeField(db_index=True,null=True,auto_now=True)
    uuid = models.CharField(max_length=255,db_index=True,null=True,default=uuid.uuid4,)
    first_seen = models.DateTimeField(db_index=True,null=True)
    update_time = models.DateTimeField(db_index=True,null=True)
    last_seen = models.DateTimeField(db_index=True,null=True)
    event_class = models.CharField(max_length=255,db_index=True,null=True)
    severity_id = models.ForeignKey(Severity,db_index=True,null=True)
    manager = models.CharField(max_length=255,db_index=True,null=True)
    device_system = models.CharField(max_length=255,db_index=True,null=True)
    device_group = models.CharField(max_length=255,db_index=True,null=True)
    device_class = models.CharField(max_length=255,db_index=True,null=True)
    device_net_address = models.CharField(max_length=255,db_index=True,null=True)
    device_location = models.CharField(max_length=255,db_index=True,null=True)
    element_identifier = models.CharField(max_length=255,db_index=True,null=True)
    element_sub_identifier = models.CharField(max_length=255,null=True)
    status_id = models.ForeignKey(Status,db_index=True,null=True)
    update_row = models.DateTimeField(auto_now=True,null=True)

    data = JSONField(default={})
    agregator = models.BooleanField(db_index=True,default=False)
    agregation = models.BooleanField(db_index=True,default=False)

    byhand = models.BooleanField(db_index=True,default=False)
    bymail = models.BooleanField(db_index=True,default=False)

    summary = models.CharField(max_length=255,db_index=True,null=True)


### Оповещения
class messages(models.Model):
    datetime_message = models.DateTimeField(db_index=True,null=True,auto_now_add=True)
    message_title = models.CharField(max_length=255,default="")
    accsident_num = models.IntegerField(db_index=True,null=False,unique=True,default=0)
    email_list = models.CharField(max_length=255,db_index=True,default="")
    author = models.CharField(max_length=255,db_index=True,default="")
    data = JSONField(default={})
    event = models.ForeignKey(events,db_index=True,null=True)



