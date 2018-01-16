#coding:utf-8
from __future__ import unicode_literals

import datetime
from pytz import timezone

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)



### Показатели
class marks(models.Model):
    name = models.CharField(max_length=30,verbose_name='Показатель')
    order = models.IntegerField(default=0, verbose_name='Порядок' )
    visible = models.BooleanField(default=True, verbose_name='Отображать' )


    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name = 'Показатель'
        verbose_name_plural = 'Показатели'



### Отметка показателей
class working_log(models.Model):
    mark = models.ForeignKey(marks,verbose_name='Показатели')
    working = models.ForeignKey('working_time', on_delete=models.CASCADE, null=True, default=None)
    datetime_create = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(default=None, verbose_name='Длительность в секундах', null=True)
    comment = models.TextField(verbose_name='Коментарий', default="", null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.mark



### Учет рабочего времени
class working_time(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    datetime_begin = models.DateTimeField(auto_now_add=True, verbose_name='Начало периода')
    datetime_end = models.DateTimeField(auto_now=True, null=True, verbose_name='Завершение периода')
    current = models.BooleanField(default=True)

    def __unicode__(self):
        return self.user

    ### Подсчет длительности рабочего времени
    def get_work_hour(self):

        ### Если смена еще не завершена
        if self.current:
            duration = int((datetime.datetime.now(krsk_tz) - self.datetime_begin).total_seconds()/3600)
            #print self.datetime_begin, datetime.datetime.now(krsk_tz)
        ### Если смена уже завешена
        else:
            duration = int((self.datetime_end - self.datetime_begin).total_seconds()/3600)

        return duration




    ### Подсчет длительности перерыва в мин
    def get_relax_min(self):

        ### Перебор перерывов
        duration = 0
        for item in self.working_relax_set.all():

            if item.current:
                duration += int((datetime.datetime.now(krsk_tz) - item.datetime_begin).total_seconds() / 60)
            else:
                duration += int((item.datetime_end - item.datetime_begin).total_seconds() / 60)

        return duration





### Учет перерывов в работе
class working_relax(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    working = models.ForeignKey(working_time, on_delete=models.CASCADE, null=True, default=None)
    datetime_begin = models.DateTimeField(auto_now_add=True, verbose_name='Начало перерыва')
    datetime_end = models.DateTimeField(auto_now=True, null=True, verbose_name='Завершение перерыва')
    current = models.BooleanField(default=True)

    def __unicode__(self):
        return self.user

