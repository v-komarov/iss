#coding:utf-8



from __future__ import unicode_literals


import uuid
import datetime
import random
import networkx as nx
from decimal import Decimal
from chardet.universaldetector import UniversalDetector

from django.utils import timezone
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.core.validators import MaxValueValidator, MinValueValidator


from iss.localdicts.models import regions, address_city, proj_temp, address_house, address_companies, blocks, business, passing, rates, stages, init_reestr_proj, ProjDocTypes, message_type




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









### Список проектов
class proj(models.Model):
    name = models.CharField(max_length=100, default="", verbose_name='Название проекта')
    start = models.DateField(null=True, default=None, verbose_name='Начало проекта')
    temp = models.ForeignKey(proj_temp, on_delete=models.PROTECT, verbose_name='Шаблон проекта')
    status = models.CharField(max_length=100, default="Новый", verbose_name='Статус проекта')
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    datetime_create = models.DateTimeField(null=True, auto_now_add=True)

    def __unicode__(self):
        return self.name


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



        ### Атрибуты узлов days
        node_days = nx.get_node_attributes(G, 'days')


        ### Список всех узлов
        nodes_list = G.nodes()
        nodes_list.remove(0)

        #### Первоначальное заполнение независимых полей исполняемых узлов
        for node in actions:
            item = id2res(node, rows)
            begin = check_day(self.start + datetime.timedelta(days=item['deferment']))
            end = date_plus(begin, item['days'])
            for x in rows:
                if x['id'] == node and id2res(node, rows)['depend_on'] == []:
                    ### Запись
                    x['begin'] = begin.strftime('%d.%m.%Y')
                    x['end'] = end.strftime('%d.%m.%Y')
                    ### Исключение из списка узлов уже обработанные
                    nodes_list.remove(node)


        #### обход каждого оставшегося узла
        while len(nodes_list) > 0:
            node = random.choice(nodes_list)

            ### исполняемы или заголовочный
            if node in actions:
                ### Для исполняемых - обработка зависимых пунктов
                res = id2res(node, rows)
                depend_item = id2res(order2id(res['depend_on'], rows), rows)
                if depend_item['begin'] != "" and depend_item['end'] != "":
                    begin = check_day(datetime.datetime.strptime(depend_item['end'], '%d.%m.%Y') + datetime.timedelta(
                        days=item['deferment'] + 1))
                    end = date_plus(begin, item['days'])
                    for z in rows:
                        if z['id'] == node:
                            z['begin'] = begin.strftime('%d.%m.%Y')
                            z['end'] = end.strftime('%d.%m.%Y')
                    nodes_list.remove(node)

            else:
                ### Для заголовочных

                ### Определение нижестоящих соседей узла
                if nx.has_path(G, node, 0) and node != 0 :
                    points = list( set(G.neighbors(node)) - set(nx.shortest_path(G, node, 0))  )
                    if 0 in points:
                        points.remove(0)

                    if len(points) > 0:
                        ### Если для нижестоящих установлены даты
                        date_ok = True
                        for p in points:
                            print id2res(p, rows)
                            if id2res(p, rows)['begin'] == "" or id2res(p, rows)['end'] == "":
                                date_ok = False


                        if date_ok:
                            ### вычисление дат
                            begin = datetime.datetime.strptime(id2res(points[0], rows)['begin'],'%d.%m.%Y')  # первоначально
                            end = datetime.datetime.strptime(id2res(points[0], rows)['end'],'%d.%m.%Y')  # первоначально
                            for p in points:
                                item = id2res(p, rows)
                                b = datetime.datetime.strptime(item['begin'], '%d.%m.%Y')
                                e = datetime.datetime.strptime(item['end'], '%d.%m.%Y')
                                if b < begin:
                                    begin = b
                                if e > end:
                                    end = e

                            ### Запись наследуемых дат
                            for y in rows:
                                if y['id'] == node:
                                    y['begin'] = check_day((begin + datetime.timedelta(days=y['deferment']))).strftime('%d.%m.%Y')
                                    y['end'] = check_day((end + datetime.timedelta(days=y['deferment']))).strftime('%d.%m.%Y')

                                    nodes_list.remove(node)

                    else:
                        nodes_list.remove(node)



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
    problem = JSONField(default={'problem': False, 'comment': ''}, verbose_name='Отказ/Проблема')


    def __unicode__(self):
        return self.name




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







#### Реестр проектов и проекты в стадии проработки
class reestr_proj(models.Model):
    proj_kod = models.CharField(max_length=100, default="00/0000000/0000000/00", verbose_name='Код проекта')
    proj_other = models.CharField(max_length=20, default="000000", verbose_name='Код связи с ЕИСУП')
    proj_level = models.CharField(max_length=2, default="00", verbose_name='Порядковый номер подпроекта')
    region = models.ForeignKey(regions, on_delete=models.PROTECT, verbose_name='Регион', null=True)
    proj_name = models.CharField(max_length=200, verbose_name='Название проекта')
    #addresses = models.ManyToManyField(address_house)
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Автор проекта')
    proj_init = models.ForeignKey(init_reestr_proj, on_delete=models.PROTECT, verbose_name='Инициатор проекта', null=True)
    executor = models.ForeignKey(address_companies, on_delete=models.PROTECT, verbose_name='Реализатор проекта', null=True, related_name="executor_company")
    business = models.ForeignKey(business, on_delete=models.PROTECT, verbose_name='Направление бизнеса', null=True)
    stage = models.ForeignKey(stages, on_delete=models.PROTECT, verbose_name='Стадия проекта', null=True)
    stage_date = models.DateField(auto_now=True, null=True, verbose_name='Дата установки стадии')
    stage_user = models.ForeignKey(User, related_name='stage_author', on_delete=models.PROTECT, verbose_name='Стадию установил', default=None, null=True)
    comment = models.TextField(verbose_name='Описание проекта', default="", null=True)
    contragent = models.CharField(max_length=100, default="", verbose_name='Контрагент')
    passing = models.ForeignKey(passing, on_delete=models.PROTECT, verbose_name='Признак переходящего проекта', null=True)
    rates = models.ForeignKey(rates, on_delete=models.PROTECT, verbose_name='Доходность', null=True)
    date_create = models.DateField(auto_now_add=True, null=True)
    date_service = models.DateField(verbose_name='Дата оказания услуги', null=True)
    data = JSONField(default={}, verbose_name='Данные')
    main_proj = models.ForeignKey('self', on_delete=models.PROTECT, verbose_name='Родительский элемент', null=True, related_name="level")
    search_index = models.TextField(verbose_name='Поисковый индекс', null=True, default="")
    object_price = models.DecimalField(default=Decimal('0.00'), max_digits=9, decimal_places=2, verbose_name='Стоимость объекта (руб.коп.)', validators=[MinValueValidator(Decimal('0.00'))])
    smr_price = models.DecimalField(default=Decimal('0.00'), max_digits=9, decimal_places=2, verbose_name='Стоимость СМР (руб.коп.)', validators=[MinValueValidator(Decimal('0.00'))])
    other_price = models.DecimalField(default=Decimal('0.00'), max_digits=9, decimal_places=2, verbose_name='Стоимость оборудования, инструментов (руб.коп.)', validators=[MinValueValidator(Decimal('0.00'))] )
    process = models.BooleanField(default=True, verbose_name='Флаг проектов в сотоянии проработки')
    comment_last = models.TextField(verbose_name='Последний коментарий', default="", null=True)
    comment_last_datetime = models.DateTimeField(auto_now_add=True, null=True)


    def __unicode__(self):
        return self.proj_kod


    ### Формирование индекса поиска
    def create_search_index(self):
        search_index = set()

        detector = UniversalDetector()

        ### Код проекта
        try:
            search_index.add(self.proj_kod.decode("utf-8"))
        except:
            search_index.add(self.proj_kod)


        ## Название проекта
        for w in self.proj_name.split():
            try:
                search_index.add(w.decode("utf-8"))
            except:
                search_index.add(w)


        ### Инициатор проекта
        if self.proj_init:
            try:
                search_index.add(self.proj_init.name.decode("utf-8"))
            except:
                search_index.add(self.proj_init.name)

        ### Реализатор проекта
        if self.executor:
            try:
                search_index.add(self.executor.name.decode("utf-8"))
            except:
                search_index.add(self.executor.name)

        ### Этапы
        if self.stage:
            try:
                search_index.add(self.stage.getfullname().decode("utf-8"))
            except:
                search_index.add(self.stage.getfullname())


        ### Адрес
        if self.data.has_key('address'):
            for addr in self.data["address"]:
                try:
                    search_index.add(addr["city"].decode("utf-8"))
                except:
                    search_index.add(addr["city"])
                try:
                    search_index.add(addr["street"].decode("utf-8"))
                except:
                    search_index.add(addr["street"])

        ### Контрагент
        for w in self.contragent.split():
            try:
                search_index.add(w.decode("utf-8"))
            except:
                search_index.add(w)

        ### Исполнители
        for ex in self.reestr_proj_exec_date_set.all():
            if ex.worker:
                for w in ex.worker.get_full_name().split():
                    try:
                        search_index.add(w.decode("utf-8"))
                    except:
                        search_index.add(w)

        ### Связь с другими системами
        if self.data.has_key('other_system'):
            for code in self.data['other_system']:
                try:
                    search_index.add(code['other_name'].decode("utf-8"))
                except:
                    search_index.add(code['other_name'])
                try:
                    search_index.add(code['other_code'].decode("utf-8"))
                except:
                    search_index.add(code['other_code'])


        detector.close()


        self.search_index = u"".join(list(search_index))
        self.save()



        return "ok"



    ### Определение новый коментарий или нет
    def check_new_comment(self):

        if self.comment_last == "":
            return False

        if (timezone.now() - self.comment_last_datetime).total_seconds()//3600 <= 24:
            return True
        else:
            return False







### История стадий проекта
class stages_history(models.Model):
    reestr_proj = models.ForeignKey(reestr_proj, null=True, on_delete=models.PROTECT, verbose_name='Связь реестром проектов')
    stage = models.ForeignKey(stages, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    datetime_create = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.stage.name





### Файлы реестра проекта
class reestr_proj_files(models.Model):
    id = models.CharField(max_length=255, primary_key=True, default=uuid.uuid4, editable=False)
    reestr_proj = models.ForeignKey(reestr_proj, null=True, on_delete=models.PROTECT, verbose_name='Связь реестром проектов')
    filename = models.CharField(max_length=100)
    doctype = models.ForeignKey(ProjDocTypes, on_delete=models.PROTECT, verbose_name='Тип документа', null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    datetime_load = models.DateTimeField(auto_now_add=True)
    checked = models.BooleanField(default=False, verbose_name='Документ проверен')

    def __unicode__(self):
        return self.filename





### Коментарии реестра проектов
class reestr_proj_comment(models.Model):
    comment = models.TextField(verbose_name='Коментарий', default="", null=True)
    reestr_proj = models.ForeignKey(reestr_proj, null=True, on_delete=models.PROTECT, verbose_name='Связь реестром проектов')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    datetime_create = models.DateTimeField(auto_now_add=True)
    log = models.BooleanField(default=False) # Лог или сообщение


    def __unicode__(self):
        return self.comment




### Исполнители и даты реестра проектов
class reestr_proj_exec_date(models.Model):
    date1 = models.DateField(verbose_name='Дата с', null=True)
    date2 = models.DateField(verbose_name='Дата до', null=True)
    stage = models.ForeignKey(stages, on_delete=models.PROTECT, null=True, verbose_name="Стадия")
    worker = models.ForeignKey(User, on_delete=models.PROTECT, null=True, verbose_name="Исполнитель", related_name="worker")
    reestr_proj = models.ForeignKey(reestr_proj, null=True, on_delete=models.PROTECT, verbose_name='Связь реестром проектов')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    datetime_edit = models.DateTimeField(auto_now=True)
    block = models.ForeignKey(blocks, on_delete=models.PROTECT, verbose_name='Ответственное подразделение', null=True)

    def __unicode__(self):
        return self.stage.name




### история отправки сообщений
class reestr_proj_messages_history(models.Model):
    message_type = models.ForeignKey(message_type, null=True, on_delete=models.PROTECT, verbose_name='Связь с типом сообщений')
    reestr_proj = models.ForeignKey(reestr_proj, null=True, on_delete=models.PROTECT, verbose_name='Связь реестром проектов')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    emails = models.CharField(max_length=200, verbose_name='Список email', default="")
    datetime_create = models.DateTimeField(auto_now_add=True)





### Склады список
class store_list(models.Model):
    name = models.CharField(max_length=100, default="", db_index=True)
    region = models.ForeignKey(regions, on_delete=models.PROTECT, verbose_name='Регион', null=True)
    comment = models.CharField(max_length=200, default="", blank=True, verbose_name="Коментарий, адрес")


    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

        unique_together = (("name", "region"),)



### Складские остатки
class store_rest(models.Model):
    store = models.ForeignKey(store_list, on_delete=models.PROTECT, verbose_name="Склад")
    eisup = models.CharField(max_length=100, default="", db_index=True, verbose_name="Код ЕИСУП")
    name = models.CharField(max_length=200, default="", db_index=True, verbose_name="Наименование номенклатуры")
    mol = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="МОЛ")
    rest = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Остаток', default=0.00)
    datetime_update = models.DateTimeField(auto_now=True)
    serial = models.CharField(max_length=100, default="", db_index=True, verbose_name="Серийный номер")
    dimension = models.CharField(max_length=20, default="", verbose_name="Ед. из.")
    accounting_code = models.CharField(max_length=20, default="", db_index=True, verbose_name="Счет учета")




### Расход со склада
class store_out(models.Model):
    datetime_update = models.DateTimeField(auto_now_add=True, db_index=True)
    store_rest = models.ForeignKey(store_rest, on_delete=models.PROTECT, verbose_name="ссылка на остаток")
    q = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Количество', default=0.00)
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Автор изменений")
    comment = models.CharField(max_length=200, default="", verbose_name="Комментарий")
    avr = models.ForeignKey("avr", on_delete=models.PROTECT, verbose_name="Связь с АВР", null=True)
    proj_kod = models.CharField(max_length=100, default="", db_index=True, verbose_name="Код проекта")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', default=0.00)


### Поступление на склад
class store_in(models.Model):
    datetime_update = models.DateTimeField(auto_now_add=True, db_index=True)
    store_rest = models.ForeignKey(store_rest, on_delete=models.PROTECT, verbose_name="ссылка на остаток")
    q = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Количество', default=0.00)
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Автор изменений")
    comment = models.CharField(max_length=200, default="", verbose_name="Комментарий")
    kis_kod = models.CharField(max_length=10, default="", db_index=True, verbose_name="Код КИС ТМЦ")




### Перемещение
class store_carry(models.Model):
    datetime_update = models.DateTimeField(auto_now_add=True, db_index=True)
    store_rest = models.ForeignKey(store_rest, on_delete=models.PROTECT, verbose_name="ссылка на остаток")
    q = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Количество', default=0.00)
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Автор изменений")
    comment = models.CharField(max_length=200, default="", verbose_name="Комментарий")
    store_to = models.ForeignKey(store_list, on_delete=models.PROTECT, verbose_name="Склад")




### Логи действий по остаткам
class store_rest_log(models.Model):
    datetime_update = models.DateTimeField(auto_now_add=True, db_index=True)
    store_rest = models.ForeignKey(store_rest, on_delete=models.PROTECT, verbose_name="ссылка на остаток")
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Автор изменений")
    q = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Количество', default=0.00)
    action = models.CharField(max_length=100, default="", verbose_name="Действие")






### Статусы АВР
class status_avr(models.Model):
    name = models.CharField(max_length=100, default="", verbose_name="Название статуса")
    emails = models.TextField(default="", verbose_name="Адреса email рассылки", blank=True)
    allow = models.CharField(max_length=100, default="", verbose_name="Список id разрешенных статустов через запятую", blank=True)
    stuff = models.BooleanField(default=False, verbose_name="Разрешено добавлять материал")
    price = models.BooleanField(default=False, verbose_name="Разрешено устанавливать цену")


    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус АВР'
        verbose_name_plural = 'Статусы АВР'






### Акты АВР
class avr(models.Model):
    region = models.ForeignKey(regions, on_delete=models.PROTECT, verbose_name='Регион', null=True)
    city = models.ForeignKey(address_city, on_delete=models.PROTECT, verbose_name='Город', null=True)
    objnet = models.CharField(max_length=200, default="", verbose_name="Объект сети")
    address = models.CharField(max_length=200, default="", verbose_name="Адрес")
    datetime_avr = models.DateTimeField(null=True, verbose_name="Дата АВР")
    datetime_work = models.DateTimeField(null=True, verbose_name="Дата выезда")
    status = models.ForeignKey(status_avr, on_delete=models.PROTECT, verbose_name='Статус')
    staff = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="МОЛ", related_name="mol")
    area = models.CharField(max_length=200, default="", verbose_name="Участок")
    complex = models.CharField(max_length=200, default="", verbose_name="Пусковой комплекс")
    commission = models.ForeignKey("avr_commission", on_delete=models.PROTECT, verbose_name="Коммиссия", null=True, default=None)

    datetime_create = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Автор")




### Логи по АВР
class avr_logs(models.Model):
    avr = models.ForeignKey(avr, on_delete=models.PROTECT, verbose_name='АВР')
    datetime_update = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Автор изменений")
    action = models.CharField(max_length=250, default="", verbose_name="Действие")
    log = models.BooleanField(default=True)




### Файлы АВР
class avr_files(models.Model):
    id = models.CharField(max_length=255, primary_key=True, default=uuid.uuid4, editable=False)
    avr = models.ForeignKey(avr, null=True, on_delete=models.PROTECT, verbose_name='Связь с АВР')
    filename = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    datetime_load = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.filename




### АВР история статусов
class avr_status_history(models.Model):
    avr = models.ForeignKey(avr, on_delete=models.PROTECT, verbose_name='АВР')
    datetime_create = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Автор")
    status = models.ForeignKey(status_avr, on_delete=models.PROTECT, verbose_name='Статус')




### АВР затраты ГСМ
class avr_gsm(models.Model):
    avr = models.ForeignKey(avr, on_delete=models.PROTECT, verbose_name='АВР')
    consumer = models.CharField(max_length=100, default="", verbose_name="Потребитель")
    km = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Кол-во км пробега', default=0.00)
    h = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Кол-во мото часов', default=0.00)
    petrol = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='ГСМ, л.', default=0.00)
    kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Полная масса груза в кг.', default=0.00)
    norma = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='либо л./100км либо л./час', default=0.00)
    summa = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Итоговая сумма в руб.', default=0.00)
    comment = models.CharField(max_length=100, default="", verbose_name="Комментарий")
    datetime_create = models.DateTimeField(auto_now_add=True, db_index=True)




### АВР исполнители
class avr_workers(models.Model):
    avr = models.ForeignKey(avr, on_delete=models.PROTECT, verbose_name='АВР')
    worker = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Исполнитель")
    h = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Кол-во ч. в раб. время', default=0.00)
    h_day = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Кол-во ч. не раб. вр.день', default=0.00)
    h_night = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Кол-во ч. не раб. вр.ночь', default=0.00)
    summa = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Итоговая сумма в руб.', default=0.00)
    comment = models.CharField(max_length=100, default="", verbose_name="Комментарий")
    datetime_create = models.DateTimeField(auto_now_add=True, db_index=True)



### АВР справочник комиссий
class avr_commission(models.Model):
    name = models.CharField(max_length=100, default="", verbose_name="Название")
    position = models.TextField(default="", verbose_name="Должность") # Формат заполнения - разделитель записей - точка с запятой
    sign = models.TextField(default="", verbose_name="Подпись") # Формат заполнения - разделитель записей - точка с запятой

    class Meta:
        verbose_name = 'Состав комиссии'
        verbose_name_plural = 'Составы комиссий'


