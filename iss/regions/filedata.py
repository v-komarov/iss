#coding:utf-8


from	django.http	import	HttpResponse, HttpResponseRedirect


import xlwt
import tempfile
import os
import StringIO
import cStringIO
import datetime
import mimetypes
import json
from decimal import Decimal
import pickle
import urllib


from operator import itemgetter

import pandas as pd
from pandas import ExcelFile


from matplotlib import rc
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import matplotlib.dates
from matplotlib.dates import WEEKLY, MONTHLY, DateFormatter, rrulewrapper, RRuleLocator
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


from snakebite.client import Client


from iss.regions.models import orders, load_proj_files, proj_stages, proj, reestr_proj_files, reestr_proj, reestr_proj_comment, store_list, store_rest, store_rest_log, avr, avr_logs, avr_files
from iss.localdicts.models import regions, ProjDocTypes
from iss.regions.filters import reestr_proj_filter

from iss.regions.docforms import doc1,doc2


mimetypes.init()
mimetypes.add_type('application/xslt+xml','.xslx')



### Данные по заказам выбранного региона
def get_orders_region(request):

    if request.GET.has_key("action") and request.GET["action"] == "getorders":
        region_id = request.GET["region"]


        region = regions.objects.get(pk=int(region_id, 10))


        book = xlwt.Workbook()
        sh = book.add_sheet(region.name)
        sh.col(1).width = 5000
        sh.col(2).width = 10000
        sh.col(10).width = 20000
        sh.col(11).width = 30000


        ### Заголовок
        sh.write(0, 0, u"№п/п")
        sh.write(0, 1, u"Артикул/марка")
        sh.write(0, 2, u"Наименование товара")
        sh.write(0, 3, u"Ед.изм.")
        sh.write(0, 4, u"Кол-во")
        sh.write(0, 5, u"Начальная цена за единицу товара, в руб. без НДС с учетов всех расходов")
        sh.write(0, 6, u"Начальная цена договора, в руб. без НДС с учетов всех расходов")
        sh.write(0, 7, u"Подключения B2B+B2O")
        sh.write(0, 8, u"Инвестпроекты")
        sh.write(0, 9, u"ТО сетей связи")
        sh.write(0, 10, u"Коментарий")
        sh.write(0, 11, u"Тех.задание")

        n = 1
        for row in orders.objects.filter(region=region).order_by('order'):
            sh.write(n, 0, row.order)
            sh.write(n, 1, row.model)
            sh.write(n, 2, row.name)
            sh.write(n, 3, row.ed)
            sh.write(n, 4, row.count)
            sh.write(n, 5, row.price)
            sh.write(n, 6, row.rowsum)
            sh.write(n, 7, row.b2b_b2o)
            sh.write(n, 8, row.investment)
            sh.write(n, 9, row.to)
            sh.write(n, 10, row.comment)
            sh.write(n, 11, row.tz)

            n += 1





    if request.GET.has_key("action") and request.GET["action"] == "getordersall":

        book = xlwt.Workbook()
        sh = book.add_sheet(u"МР-Сибирь")
        sh.col(1).width = 5000
        sh.col(2).width = 10000
        sh.col(10).width = 20000
        sh.col(11).width = 30000


        ### Заголовок
        sh.write(0, 0, u"№п/п")
        sh.write(0, 1, u"Артикул/марка")
        sh.write(0, 2, u"Наименование товара")
        sh.write(0, 3, u"Ед.изм.")
        sh.write(0, 4, u"Кол-во")
        sh.write(0, 5, u"Начальная цена за единицу товара, в руб. без НДС с учетов всех расходов")
        sh.write(0, 6, u"Начальная цена договора, в руб. без НДС с учетов всех расходов")
        sh.write(0, 7, u"Подключения B2B+B2O")
        sh.write(0, 8, u"Инвестпроекты")
        sh.write(0, 9, u"ТО сетей связи")
        sh.write(0, 10, u"Коментарий")
        sh.write(0, 11, u"Тех.задание")

        n = 1
        for row in orders.objects.order_by('name', 'ed'):
            sh.write(n, 0, row.order)
            sh.write(n, 1, row.model)
            sh.write(n, 2, row.name)
            sh.write(n, 3, row.ed)
            sh.write(n, 4, row.count)
            sh.write(n, 5, row.price)
            sh.write(n, 6, row.rowsum)
            sh.write(n, 7, row.b2b_b2o)
            sh.write(n, 8, row.investment)
            sh.write(n, 9, row.to)
            sh.write(n, 10, row.comment)
            sh.write(n, 11, row.tz)

            n += 1






    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename="orders.xls"'
    book.save(response)
    return response




### Загрузка файлов
def upload(request):

    stage_id = request.POST["stage_id"]

    stage = proj_stages.objects.get(pk=int(stage_id, 10))



    filename = request.FILES['fileupload'].name
    filedata = request.FILES['fileupload'].read()

    rec = load_proj_files.objects.create(
        stage = stage,
        filename = filename.strip(),
        user = request.user
    )

    ### Запись во временный файл
    tf = tempfile.NamedTemporaryFile(delete=False)
    f = open(tf.name, 'w')
    f.write(filedata)
    f.close()


    run = 'curl -i -X PUT -T %s -L "http://10.6.0.135:50070/webhdfs/v1/projects/%s?user.name=root&op=CREATE&overwrite=true&replication=2"' % (tf.name, rec.id)
    os.system(run)


    ### Удаление временного файла
    os.remove(tf.name)


    return HttpResponseRedirect('/regions/proj/edit/%s/' % request.session["proj_id"])





### Получение файла
def getfile(request):

    if request.method == "GET":
        file_id = request.GET["file_id"]
        file_name = request.GET["file_name"]


        ### временный файл
        tfile = "/tmp/{file_id}".format(file_id=file_id)


        client = Client('10.6.0.135', 9000)
        for x in client.copyToLocal(['/projects/%s' % file_id], tfile):
            print x

        f = open(tfile, 'r')
        data = f.read()
        f.close()

        ### Удаление временного файла
        os.remove(tfile)

        content_type =  mimetypes.types_map[".%s" % file_name.split('.')[-1]]

        response = HttpResponse(data, content_type=content_type)
        #response = HttpResponse(data, content_type="application/octet-stream")
        response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
        return response





### Вывод excel файла
def projexcel(request, project):

    ### id проекта
    proj_id = project
    pj = proj.objects.get(pk=int(proj_id, 10))

    ### Вычисление пунктов исполнения
    rows = pj.make_dict()
    G = pj.make_graph(rows)
    G = pj.graph_edge_order(G, rows)
    actions = pj.actions(G)

    style_bold = xlwt.easyxf('font: bold 1;')
    style_normal = xlwt.easyxf('')

    book = xlwt.Workbook()

    sh = book.add_sheet(pj.name)
    sh.col(1).width = 15000
    sh.col(6).width = 15000

    ### Заголовок
    sh.write(0, 0, u"№п/п", style=style_bold)
    sh.write(0, 1, u"Название", style=style_bold)
    sh.write(0, 2, u"Длительность дней", style=style_bold)
    sh.write(0, 3, u"Начало", style=style_bold)
    sh.write(0, 4, u"Завершение", style=style_bold)
    sh.write(0, 5, u"Зависит от", style=style_bold)
    sh.write(0, 6, u"Исполнители", style=style_bold)
    sh.write(0, 7, u"Выполнено %", style=style_bold)

    n = 1 ## Строка в листе
    ### Этапы проекта
    stages = [item for item in pj.proj_stages_set.all().values()]

    ### Сортировка
    sort_keys = [item['stage_order'] for item in stages]
    sort_keys.sort()
    while len(sort_keys) > 0:
        key = sort_keys[0]
        for item in stages:
            row_id = item['id']
            if item['stage_order'] == key:

                action_style = style_normal if row_id in actions else style_bold

                workers = [w for w in proj_stages.objects.get(pk=row_id).workers.all()]

                sh.write(n, 0, ".".join(["%s" % x for x in item['stage_order']]) , style=action_style)
                sh.write(n, 1, item['name'], style=action_style)
                sh.write(n, 2, item['days'] if item['days'] else "", style=action_style)
                sh.write(n, 3, item['begin'].strftime('%d.%m.%Y') if item['begin'] else "", style=action_style)
                sh.write(n, 4, item['end'].strftime('%d.%m.%Y') if item['end'] else "", style=action_style)
                sh.write(n, 5, ",".join(["%s" % x for x in item['depend_on']["stages"]]), style=action_style)
                sh.write(n, 6, ",".join([w.get_full_name() for w in workers]), style=action_style)
                sh.write(n, 7, item['percent'] if row_id in actions else "", style=action_style)

                sort_keys.remove(key)
                n += 1


    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename="%s.xls"' % pj.name.encode("utf-8")
    book.save(response)
    return response






### Выгрузка шаблона проекта
def projtemp(request, project):

    pj = proj.objects.get(pk=int(project, 10))
    name =pj.name

    response_data = u"{{'name':'{name}', 'stages':[\n".format(name=name)

    stages = [item for item in pj.proj_stages_set.all().values()]
    ### Сортировка
    sort_keys = [item['stage_order'] for item in stages]
    sort_keys.sort()
    while len(sort_keys) > 0:
        key = sort_keys[0]
        for item in stages:
            if item['stage_order'] == key:
                response_data += u"{{ 'order':{order}, 'name': '{name}', 'days':{days}, 'depend_on':{depend_on} }},\n".format(order=item['stage_order'], name=item['name'], days=item['days'], depend_on=item['depend_on']['stages'])
                sort_keys.remove(key)


    response = HttpResponse(content_type="text/plan")
    response['Content-Disposition'] = 'attachment; filename="temp.txt"'
    response.write(response_data + u"]}")

    return response






### Диаграмма Ганта
def projgant(request,project):

    ## Отображение без DISPLAY
    plt.switch_backend('agg')

    ## Отображение кирилицы
    font = {'family': 'DejaVu Sans',
            'weight': 'normal'}
    rc('font', **font)


    pr = proj.objects.get(pk=project)

    ### Вычисление пунктов исполнения
    rows = pr.make_dict()
    G = pr.make_graph(rows)
    G = pr.graph_edge_order(G, rows)
    actions = pr.actions(G)

    ylabels = []
    customDates = []
    ylabels_done = []
    #
    ### Этапы проекта
    stages = [item for item in pr.proj_stages_set.all().values()]
    ### Сортировка
    sort_keys = [item['stage_order'] for item in stages]
    sort_keys.sort()
    while len(sort_keys) > 0:
        key = sort_keys[0]
        for item in stages:
            if item['stage_order'] == key:
                if item['id'] in actions:
                    ylabels.append(item['name'])
                    customDates.append([matplotlib.dates.date2num(item['begin']), matplotlib.dates.date2num(item['end'])])
                    if item['percent'] == 100:
                        ylabels_done.append(item['name'])

                sort_keys.remove(key)



    ilen = len(ylabels)
    pos = np.arange(0.5, ilen * 0.5 + 0.5, 0.5)
    task_dates = {}
    for i, task in enumerate(ylabels):
        task_dates[task] = customDates[i]
    #fig = Figure()
    fig = plt.figure(figsize=(20, 8))

    ax = fig.add_subplot(111)

    ### заголовок
    ax.set_title(u'Проект: %s' % pr.name)

    for i in range(len(ylabels)):
        start_date, end_date = task_dates[ylabels[i]]
        if ylabels[i] in ylabels_done:
            ax.barh((i * 0.5) + 0.5, end_date - start_date, left=start_date, height=0.3, align='center', edgecolor='lightgreen', color='green', alpha=0.8)
        else:
            ax.barh((i * 0.5) + 0.5, end_date - start_date, left=start_date, height=0.3, align='center', edgecolor='lightgreen', color='orange', alpha=0.8)
    locsy, labelsy = plt.yticks(pos, ylabels)
    plt.setp(labelsy, fontsize=10)
    #    ax.axis('tight')
    ax.set_ylim(ymin=-0.1, ymax=ilen * 0.5 + 0.5)
    ax.grid(color='g', linestyle=':')
    ax.xaxis_date()
    rule = rrulewrapper(WEEKLY, interval=1)
    loc = RRuleLocator(rule)
    formatter = DateFormatter("%d.%m.%Y")
    #formatter = DateFormatter("%d-%b")

    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(formatter)
    labelsx = ax.get_xticklabels()
    plt.setp(labelsx, rotation=30, fontsize=10)

    font = font_manager.FontProperties(size='small')
    ax.legend(loc=1, prop=font)

    ax.invert_yaxis()
    fig.autofmt_xdate()

    canvas=FigureCanvas(fig)


    response = HttpResponse(content_type="image/png")
    response['Content-Disposition'] = 'attachment; filename="gantt.png"'
    canvas.print_png(response)

    return response





### Загрузка файла (реестр проектов закладка показателей)
def uploadfile_page2(request):


    if request.method == 'POST':

        if request.POST.has_key("reestrproj") and request.FILES.has_key("file"):

            reestrproj = request.POST["reestrproj"]

            filename = request.FILES['file'].name
            filedata = request.FILES['file'].read()

            file_extension = os.path.splitext(filename)[-1]

            if file_extension != ".xls" and file_extension != ".xlsx":

                return HttpResponse("""
                <html><head><script type="text/javascript">
                    window.top.ClearUploadP2();
                    alert("Формат файла не поддерживается!");
                </script></head></html>
                """)

            else:

                rp = reestr_proj.objects.get(pk=int(reestrproj, 10))

                excel_data = ExcelFile(StringIO.StringIO(filedata))
                df = excel_data.parse(excel_data.sheet_names[0], header=None)
                df=df.fillna("")
                ht = df.to_html(header=False,index=False, float_format=lambda x: '%10.2f' % x, classes="table table-bordered small").encode('utf-8')

                data = rp.data
                data["excel"] = ht
                rp.data = data
                rp.save()

                reestr_proj_comment.objects.create(
                    reestr_proj = rp,
                    user = request.user,
                    comment = u"Загружена таблица показателей",
                    log=True
                )



    return HttpResponse("""
    <html><head><script type="text/javascript">
        window.top.ClearUploadP2();
        window.top.GetTableExcel();
        window.top.GetListComments();
    </script></head></html>
    """)





### Загрузка файлов реестра проектов
def uploadfile_page4(request):

    reestrproj_id = request.POST["reestr_proj_id"]

    reestrproj = reestr_proj.objects.get(pk=int(reestrproj_id, 10))


    filetype = request.POST['filetype']
    filename = request.FILES['fileuploadhdfs'].name
    filedata = request.FILES['fileuploadhdfs'].read()

    fity =  None if filetype == "" else ProjDocTypes.objects.get(pk=int(filetype,10))

    rec = reestr_proj_files.objects.create(
        reestr_proj = reestrproj,
        filename = filename.strip(),
        doctype = fity,
        user = request.user
    )

    reestr_proj_comment.objects.create(
        reestr_proj=reestrproj,
        user=request.user,
        comment=u"Загружен документ %s" % filename,
        log=True
    )

    ### Запись во временный файл
    tf = tempfile.NamedTemporaryFile(delete=False)
    f = open(tf.name, 'w')
    f.write(filedata)
    f.close()


    run = 'curl -i -X PUT -T %s -L "http://10.6.0.135:50070/webhdfs/v1/projects/%s?user.name=root&op=CREATE&overwrite=true&replication=2"' % (tf.name, rec.id)

    os.system(run)


    ### Удаление временного файла
    os.remove(tf.name)


    return HttpResponse("""
    <html><head><script type="text/javascript">
        window.top.ClearUploadP4();
        window.top.GetListHdfsFiles();
        window.top.GetListComments();
    </script></head></html>
    """)






### Получение файла реестра проектов
def getfile2(request):

    if request.method == "GET":
        file_id = request.GET["file_id"]
        file_name = request.GET["file_name"]

        file_name = urllib.unquote(file_name).encode("utf-8")

        ### временный файл
        tfile = "/tmp/{file_id}".format(file_id=file_id)


        client = Client('10.6.0.135', 9000)
        for x in client.copyToLocal(['/projects/%s' % file_id], tfile):
            print x

        f = open(tfile, 'r')
        data = f.read()
        f.close()

        ### Удаление временного файла
        os.remove(tfile)

        content_type =  mimetypes.types_map[".%s" % file_name.split('.')[-1]]

        response = HttpResponse(data, content_type=content_type)
        #response = HttpResponse(data, content_type="application/octet-stream")
        response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
        return response








### Вывод реестра проектов в excel файл
def reestrprojexcel(request,typeproj):


    book = xlwt.Workbook()

    sh = book.add_sheet(u"Реестр проектов")

    style_bold = xlwt.easyxf('font: bold 1;')
    style_normal = xlwt.easyxf('')

    style_wrap = xlwt.easyxf('align: wrap yes')


    sh.col(0).width = 10000
    sh.col(2).width = 15000
    sh.col(3).width = 15000
    sh.col(4).width = 15000
    sh.col(6).width = 15000
    sh.col(7).width = 15000
    sh.col(8).width = 15000
    sh.col(13).width = 15000
    sh.col(14).width = 15000
    sh.col(15).width = 30000

    ### Заголовок
    sh.write(0, 0, u"Код", style=style_bold)
    sh.write(0, 1, u"Том", style=style_bold)
    sh.write(0, 2, u"Стадия", style=style_bold)
    sh.write(0, 3, u"Название", style=style_bold)
    sh.write(0, 4, u"Описание", style=style_bold)
    sh.write(0, 5, u"ЕИСУП", style=style_bold)
    sh.write(0, 6, u"Контрагент", style=style_bold)
    sh.write(0, 7, u"Инициатор", style=style_bold)
    sh.write(0, 8, u"Реализатор", style=style_bold)
    sh.write(0, 9, u"Направление бизнеса", style=style_bold)
    sh.write(0, 10, u"Дата оказания услуги", style=style_bold)
    sh.write(0, 11, u"Доходность", style=style_bold)
    sh.write(0, 12, u"Признак переходящего проекта", style=style_bold)
    sh.write(0, 13, u"Адресный перечень", style=style_bold)
    sh.write(0, 14, u"Исполнители", style=style_wrap)
    sh.write(0, 15, u"Коментарии", style=style_wrap)
    sh.write(0, 16, u"Стоимость объекта", style=style_bold)
    sh.write(0, 17, u"СМР стоимость", style=style_bold)
    sh.write(0, 18, u"Стоимость оборудования, инстраметов", style=style_bold)


    ### Получение данных
    if typeproj == "reestr":
        data = reestr_proj.objects.filter(process=False).order_by("-comment_last_datetime")
        try:
            data = reestr_proj_filter(data, pickle.loads(request.session["filter_dict"])) if request.session.has_key("filter_dict") else data
        except:
            pass
    else:
        data = reestr_proj.objects.filter(process=True).order_by("-comment_last_datetime")
        try:
            data = reestr_proj_filter(data, pickle.loads(request.session["filter_dict"])) if request.session.has_key("filter_dict") else data
        except:
            pass


    n = 1 ## Строка в листе
    for row in data:
        sh.write(n, 0, row.proj_kod, style=style_normal)
        sh.write(n, 1, row.proj_level, style=style_normal)
        sh.write(n, 2, row.stage.getfullname() if row.stage else "", style=style_normal)
        sh.write(n, 3, row.proj_name, style=style_normal)
        sh.write(n, 4, row.comment, style=style_normal)
        sh.write(n, 5, row.proj_other, style=style_normal)
        sh.write(n, 6, row.contragent, style=style_normal)
        sh.write(n, 7, row.proj_init.name if row.proj_init else "", style=style_normal)
        sh.write(n, 8, row.executor.name if row.executor else "", style=style_normal)
        sh.write(n, 9, row.business.name if row.business else "", style=style_normal)
        sh.write(n, 10, row.date_service.strftime("%d.%m.%Y") if row.date_service else "", style=style_normal)
        sh.write(n, 11, row.rates.name if row.rates else "", style=style_normal)
        sh.write(n, 12, row.passing.name if row.passing else "", style=style_normal)

        ### Адресный перечень
        address_list = ""
        if row.data.has_key("address"):
            for addr in row.data["address"]:
                address_list =  address_list + u"{city} {street} {house}; ".format(city=addr["city"],street=addr["street"],house=addr["house"])

        sh.write(n, 13, address_list, style=style_normal)

        ### Исполнители
        worker_list = ""
        for w in row.reestr_proj_exec_date_set.all():
            worker_list = worker_list + u"{worker} ({stage} {date1} - {date2}); ".format(worker=w.worker.get_full_name() if w.worker != None else "", stage=w.stage.name if w.stage else "", date1=w.date1.strftime("%d.%m.%Y") if w.date1 else "", date2=w.date2.strftime("%d.%m.%Y") if w.date2 else "")

        sh.write(n, 14, worker_list, style=style_normal)

        ### Комментарии
        comments = ""
        for c in row.reestr_proj_comment_set.all():
            comments = comments + u"{comment} [{worker} {date}]; ".format(comment=c.comment, worker=c.user.get_full_name(), date=c.datetime_create.strftime("%d.%m.%Y"))

        sh.write(n, 15, comments, style=style_normal)

        sh.write(n, 16, row.object_price, style=style_normal)
        sh.write(n, 17, row.smr_price, style=style_normal)
        sh.write(n, 18, row.other_price, style=style_normal)


        n += 1


    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename="Реестр проектов.xls"'
    book.save(response)
    return response







### Вывод всех  показателей реестра проектов в excel файл
def reestrprojexcelall(request,typeproj):


    book = xlwt.Workbook()

    style_bold = xlwt.easyxf('font: bold 1;')
    style_normal = xlwt.easyxf('')

    style_wrap = xlwt.easyxf('align: wrap yes')



    ### Получение данных
    if typeproj == "reestr":
        data = reestr_proj.objects.filter(process=False).order_by("-comment_last_datetime")
        try:
            data = reestr_proj_filter(data, pickle.loads(request.session["filter_dict"])) if request.session.has_key("filter_dict") else data
        except:
            pass
    else:
        data = reestr_proj.objects.filter(process=True).order_by("-comment_last_datetime")
        try:
            data = reestr_proj_filter(data, pickle.loads(request.session["filter_dict"])) if request.session.has_key("filter_dict") else data
        except:
            pass



    for page in data:
        if page.data.has_key("excel"):
            sh = book.add_sheet(u"%s" % page.proj_kod.replace("/","-").replace(" ","_"))

            tables = pd.read_html(page.data["excel"], index_col=False, header=None)
            table = tables[0].fillna("")
            columns = table.columns.size

            for i in range(0,columns):
                sh.col(i).width = 5000

            n = 0  ## Строка в листе
            for row in table.iterrows():

                for i in range(0,columns):
                    val = table.get_value(n,i)
                    sh.write(n, i, val, style=style_normal)
                n += 1



    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename="Показатели.xls"'
    book.save(response)
    return response








### Загрузка файла (остатки по складам)
def uploadfile_store(request):

    if request.method == 'POST':

        try:

            filename = request.FILES['fileupload'].name
            filedata = request.FILES['fileupload'].read()

            file_extension = os.path.splitext(filename)[-1]



            if file_extension == ".xls" or file_extension == ".xlsx":

                excel_data = ExcelFile(StringIO.StringIO(filedata))
                df = excel_data.parse(excel_data.sheet_names[0],header=None, index_col=None, na_values="")
                df=df.fillna("")
                ht = df.to_html(header=True, index=True, float_format=lambda x: '%10.2f' % x, classes="table table-bordered table-striped draggable").encode('utf-8')




                return HttpResponse("""
                <html><head><script type="text/javascript">
                window.top.ClearUploadEisup();            
                </script>
                <style>
                table {
                        border-collapse: collapse;
                        margin-left: 30px;
                }
    
                table, th, td {
                        border: 1px solid black;
                        font-family: Verdana, Arial, Helvetica, sans-serif; 
                        font-size: 8pt;  
                }
                </style>
                </head>%s</html>
                """ % ht)


            else:



                return HttpResponse("""
                <html><head><script type="text/javascript">                
                    window.top.ClearUploadEisup();            
                    alert("Формат файла не поддерживается!");
                </script></head></html>
                """)


        except:
            return HttpResponse("""
            <html><head><script type="text/javascript">                
            </script></head></html>
            """)





### Загрузка файлов АВР
def uploadfile_avr(request):

    avr_id = request.POST["avr_id"]

    avr_obj = avr.objects.get(pk=int(avr_id, 10))


    filename = request.FILES['fileuploadhdfs'].name
    filedata = request.FILES['fileuploadhdfs'].read()


    rec = avr_files.objects.create(
        avr = avr_obj,
        filename = filename,
        user = request.user
    )

    ### Запись во временный файл
    tf = tempfile.NamedTemporaryFile(delete=False)
    f = open(tf.name, 'w')
    f.write(filedata)
    f.close()


    run = 'curl -i -X PUT -T %s -L "http://10.6.0.135:50070/webhdfs/v1/avr/%s?user.name=root&op=CREATE&overwrite=true&replication=2"' % (tf.name, rec.id)

    os.system(run)


    ### Удаление временного файла
    os.remove(tf.name)

    ### Регистрация в логе
    avr_logs.objects.create(
        avr=avr_obj,
        user=request.user,
        action=u"Загружен файл: %s" % filename
    )

    return HttpResponse("""
    <html><head><script type="text/javascript">
        window.top.ClearUploadFile();
        window.top.GetListFiles();
        window.top.GetListLogs();
    </script></head></html>
    """)





### Получение файла АВР
def get_avr_file(request):

    if request.method == "GET":
        file_id = request.GET["file_id"]
        file_name = request.GET["file_name"]

        file_name = urllib.unquote(file_name).encode("utf-8")

        ### временный файл
        tfile = "/tmp/{file_id}".format(file_id=file_id)


        client = Client('10.6.0.135', 9000)
        for x in client.copyToLocal(['/avr/%s' % file_id], tfile):
            print x

        f = open(tfile, 'r')
        data = f.read()
        f.close()

        ### Удаление временного файла
        os.remove(tfile)

        content_type =  mimetypes.types_map[".%s" % file_name.split('.')[-1]]

        response = HttpResponse(data, content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
        return response






### АВР печатная форма
def get_avr_print(request,avr_id,printform):


    avr_obj = avr.objects.get(pk=avr_id)
    str_run = "doc{}(avr_obj)".format(printform)

    response = HttpResponse(eval(str_run), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    response['Content-Disposition'] = u'attachment; filename="akt_%s.docx"' % avr_id
    return response
