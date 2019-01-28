#coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
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




### Структура размещения устройств электрооборудования
class placements(MPTTModel):
    name = models.CharField(max_length=200,verbose_name='Размещение')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    def __unicode__(self):
        return self.name

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by=['name']


mptt.register(placements, order_insertion_by=['name'])
mptt.register(devicestypes, order_insertion_by=['name'])




### Список устройств
class deviceslist(models.Model):
    serial = models.CharField(max_length=50,verbose_name='Серийный номер', default="")
    devicetype = models.ForeignKey('devicestypes', verbose_name='Тип устройства', null=True)
    placement = models.ForeignKey('placements', verbose_name='Размещение', null=True)
    name = models.CharField(max_length=200,verbose_name='Название')
    comment = models.TextField(default="", verbose_name='Комментарий')
    address = models.CharField(max_length=200,verbose_name='Адрес', default="")
    datetime_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    author = models.ForeignKey(User, on_delete=models.PROTECT)

    def __unicode__(self):
        return self.name

