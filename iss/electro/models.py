#coding:utf-8
from __future__ import unicode_literals

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
import mptt


### Типы устройств электрооборудования
class devicestypes(MPTTModel):
    name = models.CharField(max_length=200,verbose_name='Тип устройства')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    def __unicode__(self):
        return self.name

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by=['name']


mptt.register(devicestypes, order_insertion_by=['name'])