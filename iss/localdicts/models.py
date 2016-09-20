#coding:utf-8

from __future__ import unicode_literals

from django.db import models



class TzList(models.Model):
    tz_id = models.CharField(max_length=30,verbose_name='Значение',unique=True)
    tz_label = models.CharField(max_length=30,verbose_name='Видимое для выбора значение')

    def __unicode__(self):
        return self.tz_label


    class Meta:
        verbose_name = 'Часовой пояс'
        verbose_name_plural = 'Часовые пояса'



class Status(models.Model):
    name = models.CharField(max_length=30,verbose_name='Статуса')


    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'



class Severity(models.Model):
    name = models.CharField(max_length=30,verbose_name='Важность')


    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name = 'Важность'
        verbose_name_plural = 'Важность'

