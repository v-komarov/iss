#coding:utf-8



from __future__ import unicode_literals


import uuid
import datetime
import random
import networkx as nx


from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

from iss.localdicts.models import regions, address_city, proj_temp




### Определение id элемента в словаре по stage_order
def order2id(order,rows):

    for item in rows:
        if order == item["stage_order"]:
            return item["id"]

    return None



### Поиск по id элемента в списке словарей
def id2res(id,rows):

    for item in rows:
        if id == item["id"]:
            return item

    return None



### вычисление вышестоящего id по иерархическому номеру (1.2.3...)
def order2parent(order, rows):

    orderlen = len(order)

    if orderlen < 2:
        return 0

    for item in rows:
        if order != item["stage_order"] and order[0:orderlen-1] == item["stage_order"]:
            return item["id"]

    return None




### рассчет дат с учетом выходных дней
def date_plus(date,delta):

    ## Добавляем по одному дню и проверяем на субботу или воскресенье
    while delta != 0:
        date = date + datetime.timedelta(days=1)
        if date.weekday() < 5:
            delta = delta - 1

    return date




### вычисление количества дней между датами
def working_days(date1,date2):

    days = 0
    ## Добавляем по одному дню и проверяем на субботу или воскресенье
    while date1 < date2:
        date1 = date1 + datetime.timedelta(days=1)
        if date1.weekday() < 5:
            days += 1
    return days




### Проверка даты, попадает ли на выходной день
def check_day(date):

    while date.weekday() >= 5:
        date = date + datetime.timedelta(days=1)

    return date





### Запись в базу
def write_rows(rows, heads):

    for item in rows:
        stage = proj_stages.objects.get(pk=item['id'])
        if item['begin'] != "" and item['end'] != "":
            stage.begin = datetime.datetime.strptime(item['begin'], '%d.%m.%Y')
            stage.end = datetime.datetime.strptime(item['end'], '%d.%m.%Y')
        else:
            stage.begin = None
            stage.end = None

        ### Расчет продолжительности заголовочных пунктов
        if stage.begin and stage.end and item['id'] in heads:
            stage.days = working_days(stage.begin, stage.end)

        stage.save()

    return "ok"




### Выборка элементов ветви, проверка все ли начальные элементы с определенными begin, end, вычисление наследуемых дат
def branch2head(path, paths, rows):

    ### выбор элементов ветви по условию у всех элементов должно быть совпадение без начального элемента
    branch = []
    for i in paths:
        if i[1:] == path[1:]:
            branch.append(i)

    ### проверка начальных элементов ветви - есть ли определенность для begin и end
    for j in branch:
        item = id2res(j[0], rows)
        if (item['begin'] == "" or item['end'] == "") and item['depend_on'] == []:
            return None
        if (item['begin'] == "" or item['end'] == "") and item['depend_on'] != []:
            ### вычисление зависимости
            item_depend = id2res(order2id(item['depend_on'], rows) , rows)
            if item_depend['begin'] == "" or item_depend['end'] == "":
                return None
            else:
                return {'result': 'depend', 'id': item['id'], 'depend_id': item_depend['id']}


    ### Если для всех начальных элементов begin и end определены - вычисляем наследуемые даты (даты наследуются в заголовочных пунктах)
    begin = datetime.datetime.strptime(id2res(branch[0][0], rows)['begin'], '%d.%m.%Y') # первоначально
    end = datetime.datetime.strptime(id2res(branch[0][0], rows)['end'], '%d.%m.%Y') # первоначально


    for item in branch:
        item = id2res(j[0], rows)
        b = datetime.datetime.strptime(item['begin'], '%d.%m.%Y')
        e = datetime.datetime.strptime(item['end'], '%d.%m.%Y')
        if b < begin:
            begin = b
        if e > end:
            end = e

    return {'result':'ok','branch': branch, 'begin': begin, 'end': end}







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









### Список проектов
class proj(models.Model):
    name = models.CharField(max_length=100, default="", verbose_name='Название проекта')
    start = models.DateField(null=True, default=None, verbose_name='Начало проекта')
    temp = models.ForeignKey(proj_temp, on_delete=models.PROTECT, verbose_name='Шаблон проекта')
    status = models.CharField(max_length=100, default="Новый", verbose_name='Статус проекта')
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    datetime_create = models.DateTimeField(null=True, auto_now_add=True)

    def __unicode__(self):
        return self.filename


    ### Создание словаря из этапов проекта
    def make_dict(self):
        ### Загрузка данных из базы в словарь (чтобы не дергать каждое вычисление базу)
        rows = []
        for item in self.proj_stages_set.all():
            rows.append({
                'id': item.id,
                'stage_order': item.stage_order,
                'days': item.days if item.days else 0,
                'deferment': item.deferment if item.deferment else 0,
                'depend_on': item.depend_on["stages"],
                'begin': '',
                'end': ''
            })

        return rows



    ### Формирование графа из словоря этапов проекта
    def make_graph(self,rows):

        ### Формирование графа
        G = nx.Graph()
        G.add_node(0, {'days': 0})
        for item in rows:
            ### Добавление узлов
            G.add_node(item["id"], {'days': 0})

        return G



    ### Добавление связей согласно структуры нумерации
    def graph_edge_order(self, G, rows):
        for item in rows:
            G.add_edges_from([(item['id'], order2parent(item['stage_order'], rows))])

        return G


    ### Формирование списка исполняемых узлов (пунктов)
    def actions(self, G):

        actions = [] ### id исполняемых пунктов
        ### Соседи
        for node in G.nodes():
            neighbous = G.neighbors(node)
            ### Если только один сосед
            if len(neighbous) == 1 and node != 0:
                actions.append(node) ### Сохранение списка исполняемых узлов

        return actions


    ### Формирование списка узлов заголовков (пунктов)
    def heads(self, G):

        heads = []  ### id пунктов заголовков
        ### Соседи
        for node in G.nodes():
            neighbous = G.neighbors(node)
            ### Если соседей больше одного
            if len(neighbous) > 1 and node != 0:
                heads.append(node)  ### Сохранение списка

        return heads



    ### Формирование списка всех путей от каждого узла к 0 узлу
    def paths_stages(self, G):
        paths = [] ### все пути - из каждого пункта к корню проекта (0)
        for node in G.nodes():
            ### Вывод всех путей
            if node != 0:
                for path in nx.all_simple_paths(G, node, 0):
                    ### Берем пути только с длинной более 2
                    if len(path) > 2:
                        paths.append(path)

        return paths



    #### Добавление связий на основании зависимостей
    #def graph_edge_depend(self, G, rows):
    #    for item in rows:
    #        if item['depend_on'] != []:
    #            G.add_edges_from([ (order2id(item['depend_on'], rows), item['id']) ])

    #    return G




    ### расчет дат и длительности этапов проекта
    def calculate_dates(self):

        ### Словарь из этапов проекта
        rows = self.make_dict()

        ### Формирование графа
        G = self.make_graph(rows)

        ### Добавление связей согласно структуры нумерации
        G = self.graph_edge_order(G, rows)

        ### Установка дней для исполняемых пунктов, вычисление путей
        actions = self.actions(G)

        for node in G.nodes():
            if node in actions:
                ### Установка атрибута days для исполняемых пунктов
                G.node[node]['days'] = id2res(node, rows)['days']


        ### Добавление связей согласно зависимостей (depend_on)
        #G = self.graph_edge_depend(G, rows)

        ### Атрибуты узлов days
        node_days = nx.get_node_attributes(G, 'days')

        ### Список путей
        paths = self.paths_stages(G)

        #### Первоначальное заполнение независимых полей исполняемых узлов
        for path in paths:
            if path[0] in actions:
                item = id2res(path[0], rows)
                begin = check_day(self.start + datetime.timedelta(days=item['deferment']))
                end = date_plus(begin, item['days'])
                for x in rows:
                    if x['id'] == path[0] and id2res(path[0], rows)['depend_on'] == []:
                        ### Запись
                        x['begin'] = begin.strftime('%d.%m.%Y')
                        x['end'] = end.strftime('%d.%m.%Y')


        ### Обработка пунктов выше от начальных в каждом пути через случайный выбор
        while len(paths) > 0:
            ### Выбор случайного пути
            path = random.choice(paths)
            ### Выбор ветки, определение все ли начальные элементы этой ветки с определенными begin и end
            res = branch2head(path, paths, rows)
            print path, res
            if res != None:
                if res['result'] =='ok':
                    print path, res['begin'], res['end']
                    ### Запись наследуемых дат
                    for y in rows:
                        if y['id'] == path[1]:
                            y['begin'] = check_day((res['begin'] + datetime.timedelta(days=y['deferment']))).strftime('%d.%m.%Y')
                            y['end'] = check_day((res['end'] + datetime.timedelta(days=y['deferment']))).strftime('%d.%m.%Y')

                    ### Удаление отработанной ветки из списка путей
                    for t in res['branch']:
                        paths.remove(t)
                ### Обработка зависимого пункта
                if res['result'] == 'depend':
                    ### окончание одного является началом другого + 1 день
                    item = id2res(res['id'], rows)
                    depend_item = id2res(res['depend_id'], rows)
                    begin = check_day(datetime.datetime.strptime(depend_item['end'], '%d.%m.%Y') + datetime.timedelta(days=item['deferment']+1))
                    end = date_plus(begin, item['days'])
                    for z in rows:
                        if z['id'] == item['id']:
                            z['begin'] = begin.strftime('%d.%m.%Y')
                            z['end'] = end.strftime('%d.%m.%Y')


        #for n in G.nodes():
        #    print node_days[n]



        ### Запись словаря этапов в базу
        heads = self.heads(G)
        write_rows(rows, heads)



        return G






### Этапы проекта
class proj_stages(models.Model):
    name = models.CharField(max_length=100, default="", verbose_name='Название этапа')
    stage_order = JSONField(default={}, verbose_name='Порядковый номер')
    days = models.IntegerField(null=True, default=1, verbose_name='Длительность этапа')
    deferment = models.IntegerField(null=True, default=0, verbose_name='Отложенность')
    begin = models.DateField(null=True, default=None)
    end = models.DateField(null=True, default=None)
    depend_on = JSONField(default={'stages':[]}, verbose_name='Зависит от')
    proj = models.ForeignKey(proj, on_delete=models.PROTECT, verbose_name='Связь с проектом')
    workers = models.ManyToManyField(User)
    percent = models.IntegerField(default=0, verbose_name='Процент выполнения')


    def __unicode__(self):
        return self.filename




### Файлы проекта
class load_proj_files(models.Model):
    id = models.CharField(max_length=255, primary_key=True, default=uuid.uuid4, editable=False)
    stage = models.ForeignKey(proj_stages, null=True, on_delete=models.PROTECT, verbose_name='Связь с этапом')
    filename = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    datetime_load = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.filename





### Заметки по проекту с привязкой к этапу
class proj_notes(models.Model):

    datetime = models.DateTimeField(db_index=True, null=True, auto_now_add=True)
    note = models.TextField(default="")
    stage = models.ForeignKey(proj_stages, null=True, on_delete=models.PROTECT, verbose_name='Связь с этапом')
    author = models.ForeignKey(User, on_delete=models.PROTECT)

    def __unicode__(self):
        return self.note
