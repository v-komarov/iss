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



class accident_group(models.Model):
    name = models.CharField(max_length=100,verbose_name='Название группы')
    name_short = models.CharField(max_length=10,verbose_name='Краткое название группы')


    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name = 'Группа аварии'
        verbose_name_plural = 'Группы аварий'





class accident_list(models.Model):
    name = models.CharField(max_length=100,verbose_name='Название аварии')
    name_short = models.CharField(max_length=10,verbose_name='Краткое название аварии')
    accident_group = models.ForeignKey(accident_group, verbose_name='Группа аварии')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Авария'
        verbose_name_plural = 'Аварии'




class accident_cats(models.Model):
    name = models.CharField(max_length=100,verbose_name='Название категории')
    cat = models.CharField(max_length=10,verbose_name='Номер категории')
    accident = models.ForeignKey(accident_list, verbose_name='Аварии')


    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name = 'Категория аварии'
        verbose_name_plural = 'Категории аварий'





class address_city(models.Model):
    name = models.CharField(max_length=100, verbose_name='Город',unique=True)

    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'



class address_street(models.Model):
    name = models.CharField(max_length=100, verbose_name='Улица',unique=True)

    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name = 'Улица'
        verbose_name_plural = 'Улицы'







class address_house(models.Model):
    iss_address_id = models.IntegerField(null=True,verbose_name='ИСС код')
    city = models.ForeignKey(address_city, verbose_name='Город', on_delete=models.PROTECT)
    street = models.ForeignKey(address_street, verbose_name='Улица', null=True, on_delete=models.PROTECT)
    house = models.CharField(max_length=100, verbose_name='Дом', null=True)


    def __unicode__(self):
        return self.house


    class Meta:
        verbose_name = 'Дом'
        verbose_name_plural = 'Дома'

        unique_together = ('iss_address_id', 'city','street','house')






class address_companies(models.Model):
    name = models.CharField(max_length=100, verbose_name='Компания', unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'





class devices_type(models.Model):
    name = models.CharField(max_length=100, verbose_name='Вид устройства', unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Вид устройства'
        verbose_name_plural = 'Виды устройств'






class email_templates(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название шаблона', unique=True)
    address_list = models.CharField(max_length=100, verbose_name='Список адресов')
    template = models.TextField(default="", verbose_name='Шаблон')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Шаблон оповещения'
        verbose_name_plural = 'Шаблоны оповещений'


