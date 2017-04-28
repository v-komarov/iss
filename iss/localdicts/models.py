#coding:utf-8

from __future__ import unicode_literals

from django.db import models
from django import template
from django.contrib.postgres.fields import JSONField



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
        verbose_name = 'Статус оперативного журнала'
        verbose_name_plural = 'Статусы оперативного журнала'



class Severity(models.Model):
    name = models.CharField(max_length=30,verbose_name='Важность')


    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name = 'Важность оперативного журнала'
        verbose_name_plural = 'Важность оперативного журнала'



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

        return self.name



    def getaddress(self):

        city = self.city.name if self.city else ""
        street = self.street.name if self.street else ""
        house = self.house if self.house else ""

        return ("{city} {street} {house}".format(city=city,street=street,house=house)).strip()


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






class email_templates(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название шаблона', unique=True)
    address_list = models.CharField(max_length=100, verbose_name='Список адресов')
    template = models.TextField(default="", verbose_name='Шаблон')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Шаблон оповещения'
        verbose_name_plural = 'Шаблоны оповещений'





class address_templates(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название шаблона', unique=True)
    template = models.TextField(default="", verbose_name='Шаблон')

    def __unicode__(self):
        return self.name

    ### Вызов шаблонизатора
    def gettempl(self,data):
        t = template.Template(self.template)
        c = template.Context({'data': data})
        return t.render(c)


    class Meta:
        verbose_name = 'Шаблон адреса'
        verbose_name_plural = 'Шаблоны адресов'




class ports(models.Model):
    name = models.CharField(max_length=100, verbose_name='Вид порта', unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Вид порта'
        verbose_name_plural = 'Виды портов'




class slots(models.Model):
    name = models.CharField(max_length=100, verbose_name='Вид слота', unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Вид слота'
        verbose_name_plural = 'Виды слотов'




# Допустимые логические интерфейсы
class interfaces(models.Model):
    name = models.CharField(max_length=100, verbose_name='Интерфейс', unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Интерфейс'
        verbose_name_plural = 'Интерфейсы'




# Статусы слотов
class slot_status(models.Model):
    name = models.CharField(max_length=100, verbose_name='Статус слота', unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус слота'
        verbose_name_plural = 'Статусы слотов'




# Статусы портов
class port_status(models.Model):
    name = models.CharField(max_length=100, verbose_name='Статус порта', unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус порта'
        verbose_name_plural = 'Статусы портов'





# Статусы устройств
class device_status(models.Model):
    name = models.CharField(max_length=100, verbose_name='Статус устройства', unique=True)


    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name = 'Статус устройства'
        verbose_name_plural = 'Статусы устройств'




### Справочник свойств логических интерфейсов
class logical_interfaces_prop_list(models.Model):
    name = models.CharField(max_length=100, verbose_name='Свойство логического интерфейса', unique=True)
    comment = models.CharField(max_length=200, verbose_name='Описание',null=True)


    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name = 'Свойство логического интерфейса'
        verbose_name_plural = 'Свойства логических интерфейсов'

