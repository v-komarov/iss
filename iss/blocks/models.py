#coding:utf-8

from __future__ import unicode_literals


from decimal import Decimal


from django.db import models
from django import template
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User

from iss.localdicts.models import address_house






### Дома, стоения
class buildings(models.Model):
    address = models.ForeignKey(address_house, verbose_name="Адрес", null=True)
    numstoreys = models.IntegerField(default=0, verbose_name="Этажность")
    numentrances = models.IntegerField(default=0, verbose_name="Кол-во поъездов")
    numfloars = models.IntegerField(default=0, verbose_name="Число квартир")
    access = models.CharField(max_length=250, verbose_name='Условие доступа', default="")

    www_id = models.IntegerField(default=0, verbose_name="Идентификатор с сайта")

    block_manager = models.ForeignKey('block_managers', verbose_name="Управляющая компания", null=True)

    def __unicode__(self):
        return self.address.getaddress()


    class Meta:
        verbose_name = 'Дом'
        verbose_name_plural = 'Дома'




### Управляющие компании , тсж, пр...
class block_managers(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', default="", db_index=True)
    address = models.ForeignKey(address_house, verbose_name="Адрес фактический", null=True, default=None, related_name="addr_real")
    address_law = models.ForeignKey(address_house, verbose_name="Адрес юридический", null=True, related_name="addr_law", default=None)
    phone = models.TextField(default="")
    contact = models.TextField(default="")
    email = models.TextField(default="")
    inn = models.CharField(max_length=10, verbose_name='ИНН', default="", db_index=True)

    www_id = models.IntegerField(default=0, verbose_name="Идентификатор с сайта")


    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name = 'Управляющая компания'
        verbose_name_plural = 'Управляющие компании'






### Коментарии и логи
class comments_logs(models.Model):
    comment = models.TextField(verbose_name='Коментарий', default="", null=True)
    manager = models.ForeignKey(block_managers, null=True, on_delete=models.PROTECT, verbose_name='Связь с компанией')
    house = models.ForeignKey(buildings, null=True, on_delete=models.PROTECT, verbose_name='Связь с домом')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    datetime_create = models.DateTimeField(auto_now_add=True)
    log = models.BooleanField(default=False) # Лог или сообщение


    def __unicode__(self):
        return self.comment




### Договоры с компаниями
class contracts(models.Model):
    company = models.ForeignKey(block_managers, on_delete=models.PROTECT, verbose_name='Связь с компанией')
    num = models.CharField(max_length=30, verbose_name="Номер договора", db_index=True)
    date_begin = models.DateField(verbose_name="Начало договора", db_index=True)
    date_end = models.DateField(verbose_name="Завершение договора", db_index=True)
    goon = models.BooleanField(default=False, verbose_name="Возможность продления")
    money = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Сумма договора', default=0.00)
    period = models.ForeignKey('pay_period', on_delete=models.PROTECT, verbose_name="Периодичность оплаты")
    datetime_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания")
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Создал договор")
    manager = models.ForeignKey(User, related_name="contract_manager", on_delete=models.PROTECT, verbose_name="Ответственный", db_index=True)


    def __unicode__(self):
        return self.num



### Периодичность оплаты
class pay_period(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название периодичности")


    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name = 'Периодичность оплаты'
        verbose_name_plural = 'Периодичность оплат'

