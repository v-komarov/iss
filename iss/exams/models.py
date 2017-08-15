#coding:utf-8



from __future__ import unicode_literals


import uuid

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField


### Разделы тестирования
class sections(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Раздел')

    def __unicode__(self):
        return self.name



### Вопросы тестирования
class questions(models.Model):
    name = models.CharField(max_length=200, verbose_name='Ответ')
    section = models.ForeignKey(sections, null=True, on_delete=models.PROTECT, verbose_name='Связь с разделом')

    def __unicode__(self):
        return self.name



### Ответы тестирования
class answers(models.Model):
    name = models.CharField(max_length=200, verbose_name='Ответ')
    question = models.ForeignKey(sections, null=True, on_delete=models.PROTECT, verbose_name='Связь с вопросом')
    truth = models.BooleanField(default=False, verbose_name='Правильный ответ')

    def __unicode__(self):
        return self.name



### Тесты
class tests(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название теста')
    section = models.ForeignKey(sections, null=True, on_delete=models.PROTECT, verbose_name='Связь с разделом')
    questions = models.ManyToManyField(questions)
    testtime = models.IntegerField(default=0, verbose_name='Продолжительность теста в минутах')
    mistakes = models.IntegerField(default=0, verbose_name='Максимальное количество ошибок для сдачи')
    learning = models.BooleanField(default=False, verbose_name='Доступен для тренировки, обучения')

    def __unicode__(self):
        return self.name
