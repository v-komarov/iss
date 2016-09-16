#coding:utf-8

from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField


class events(models.Model):
    datetime_evt = models.DateTimeField()
    data = JSONField(default={})

