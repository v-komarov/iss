#coding:utf-8

from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from iss.localdicts.models import regions, address_city, address_house



### Заказы по регионам
class orders(models.Model):
    region = models.ForeignKey(regions, null=True, verbose_name='Регион')
    order = models.IntegerField(default=1, verbose_name='Порядковый номер')
    model = models.CharField(max_length=100, verbose_name='Артикул/марка', default="")
    name = models.CharField(max_length=400, verbose_name='Наименование товара', default="")
    ed = models.CharField(max_length=10, verbose_name='Единица измерения', default="шт")
    count = models.IntegerField(default=0, verbose_name='Количество', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Цена за единицу', default=0.00)
    rowsum = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Сумма по позиции', default=0.00 )
    b2b_b2o = models.IntegerField(default=0, verbose_name='Подключения B2B+B2O', null=True)
    investment = models.IntegerField(default=0, verbose_name='Инвестпроекты', null=True)
    to = models.IntegerField(default=0, verbose_name='ТО сетей связи', null=True)
    tz = models.TextField(verbose_name='Тех.задание', default="")
    author = models.CharField(max_length=100, default="")
    datetime_update = models.DateTimeField(null=True, auto_now=True)
    comment = models.CharField(max_length=255, default="", verbose_name='Коментарий')

    def __unicode__(self):
        return self.name



### Инвентаризация
class reestr(models.Model):
    region = models.ForeignKey(regions, null=True, verbose_name='Регион', blank=True)
    god_balans = models.CharField(max_length=50, verbose_name='Год постановки на баланс', default="", blank=True)
    original = models.CharField(max_length=50, verbose_name='Ссылка на оригинал', default="", blank=True)
    net = models.CharField(max_length=50, verbose_name='Сеть', default="", blank=True)
    city = models.ForeignKey(address_city, null=True, verbose_name='Населенный пункт', blank=True)
    project_code = models.CharField(max_length=100, verbose_name='Код проекта', default="", blank=True)
    invnum = models.CharField(max_length=100, db_index=True, default="", verbose_name='Инвентарный номер', blank=True)
    start_date = models.CharField(max_length=20, db_index=True, default="", verbose_name='Дата ввода в эксплуатацию', blank=True)
    ed_os = models.CharField(max_length=20, default="", verbose_name='Кол-во ед. ОС', blank=True)
    name = models.TextField(verbose_name='Наименование оборудования/объекта ОС', default="", blank=True)
    comcode = models.TextField(verbose_name='Комкод', default="", blank=True)
    serial = models.TextField(default="", verbose_name='Серийные номера и пр.информация', blank=True)
    nomen = models.TextField(default="", verbose_name='Номенклатурный номер', blank=True)
    ed = models.CharField(max_length=20, verbose_name='Единица измерения', default="шт", blank=True)
    count = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='Количество', null=True, default=0.00, blank=True)
    price = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True, verbose_name='Цена руб.коп.', default=0.00)
    rowsum = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name='Всего руб.коп.', default=0.00)
    actos1 = models.CharField(max_length=100, db_index=True, default="", verbose_name='Номер акта ОС1', blank=True)
    group = models.CharField(max_length=50, verbose_name='Номер амортизационной группы', default="", blank=True)
    age = models.CharField(max_length=50, verbose_name='Срок полезного использования', default="", blank=True)
    address = models.TextField(default="", verbose_name='Адрес установки', blank=True)
    dwdm = models.TextField(verbose_name='Информационная колонка DWDM', default="", blank=True)
    tdm = models.TextField(verbose_name='Информационная колонка TDM', default="", blank=True)
    sdh = models.TextField(verbose_name='Информационная колонка SDH', default="", blank=True)
    ip = models.TextField(verbose_name='Информационная колонка IP', default="", blank=True)
    atm = models.TextField(verbose_name='Информационная колонка ATM', default="", blank=True)
    emcs = models.TextField(verbose_name='Информационная колонка ЕМЦС', default="", blank=True)

    res_count = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='Результат фактическое количество', null=True, default=0.00, blank=True)
    res_serial = models.TextField(default="", verbose_name='Результат серийные номера', blank=True)
    res_invnum = models.CharField(max_length=100, db_index=True, default="", verbose_name='Результат инвентарный номер', blank=True)

    author = models.CharField(max_length=100, default="")
    datetime_update = models.DateTimeField(null=True, auto_now=True)



    def __unicode__(self):
        return self.name



    def get_absolute_url(self):
        return reverse('edit-reestr', kwargs={'pk': self.pk})
