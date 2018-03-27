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

from iss.regions.models import orders, load_proj_files, proj_stages, proj, reestr_proj_files, reestr_proj, reestr_proj_comment, store_list, store_rest
from iss.localdicts.models import regions, ProjDocTypes




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

        dic={1049:'Й',1062:'Ц',1059:'У',1050:'К',1045:'Е',1053:'Н',1043:'Г',1064:'Ш',1065:'Щ',1047:'З',1061:'Х',1066:'Ъ',1060:'Ф',1067:'Ы',1042:'В',1040:'А',1055:'П',1056:'Р',1054:'О',1051:'Л',1044:'Д',1046:'Ж',1069:'Э',1071:'Я',1063:'Ч',1057:'С',1052:'М',1048:'И',1058:'Т',1068:'Ь',1041:'Б',1070:'Ю', \
            1081:'й',1094:'ц',1091:'у',1082:'к',1077:'е',1085:'н',1075:'г',1096:'ш',1097:'щ',1079:'з',1093:'х',1098:'ъ',1092:'ф',1099:'ы',1074:'в',1072:'а',1087:'п',1088:'р',1086:'о',1083:'л',1076:'д',1078:'ж',1101:'э',1103:'я',1095:'ч',1089:'с',1084:'м',1080:'и',1090:'т',1100:'ь',1073:'б',1102:'ю', \
            32:' ',33:'!',34:'"',35:'#',36:'$',37:'%',38:'&',40:'(',41:',',42:'*',43:'+',44:',',45:'-',46:'.',47:'/',48:'0',49:'1',50:'2',51:'3',52:'4',53:'5',54:'6',55:'7',56:'8',57:'9',58:':',59:';',60:'<',61:'=',62:'>',63:'?',64:'@',65:'A',66:'B',67:'C',68:'D',69:'E',70:'F',71:'G',72:'H',73:'I',74:'J', \
            75:'K',76:'L',77:'M',78:'N',79:'O',80:'P',81:'Q',82:'R',83:'S',84:'T',85:'U',86:'V',87:'W',88:'X',89:'Y',90:'Z',91:'[',93:']',94:'^',95:'_',96:'`',97:'a',98:'b',99:'c',100:'d',101:'e',102:'f',103:'g',104:'h',105:'i',106:'j',107:'k',108:'l',109:'m',110:'n',111:'o',112:'p',113:'q',114:'r',115:'s', \
            116:'t',117:'u',118:'v',119:'w',120:'x',121:'y',122:'z',123:'{',124:'|',125:'}',126:'~'}
        i=0
        n=len(file_name)
        sp=[]
        while (i<n) :
            sp.append(dic[ord(file_name[i])])
            i=i+1
        file_name=''.join(sp)


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
def reestrprojexcel(request):


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
    if request.session.has_key("search_text"):
        data = reestr_proj.objects.filter(search_index__icontains=request.session["search_text"]).order_by("-id")
    else:
        data = reestr_proj.objects.order_by("-id")


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
            worker_list = worker_list + u"{worker} ({stage} {date1} - {date2}); ".format(worker=w.worker.get_full_name(), stage=w.stage.name if w.stage else "", date1=w.date1.strftime("%d.%m.%Y") if w.date1 else "", date2=w.date2.strftime("%d.%m.%Y") if w.date2 else "")

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
def reestrprojexcelall(request):


    book = xlwt.Workbook()

    style_bold = xlwt.easyxf('font: bold 1;')
    style_normal = xlwt.easyxf('')

    style_wrap = xlwt.easyxf('align: wrap yes')


    ### Получение данных
    if request.session.has_key("search_text"):
        data = reestr_proj.objects.filter(search_index__icontains=request.session["search_text"]).order_by("-id")
    else:
        data = reestr_proj.objects.order_by("-id")


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

        filename = request.FILES['fileupload'].name
        filedata = request.FILES['fileupload'].read()

        file_extension = os.path.splitext(filename)[-1]

        if file_extension != ".xls" and file_extension != ".xlsx":

            return HttpResponse("""
            <html><head><script type="text/javascript">
                window.top.ClearUploadEisup();
                alert("Формат файла не поддерживается!");
            </script></head></html>
            """)

        else:

            excel_data = ExcelFile(StringIO.StringIO(filedata))
            df = excel_data.parse(excel_data.sheet_names[0],skiprows=9,header=None, na_values="", dtype={2:str,16:str})

            df=df.fillna("")
            df[1] = df[1].replace("nan","")
            df[2] = df[2].replace("nan","")
            df[4] = df[4].replace("nan","")
            df[16] = df[16].replace("nan","")
            data = []
            for index, row in df.iterrows():
                name = row[1].strip()
                eisup = row[2].strip()
                store = row[4].strip()
                rest = row[16].strip()
                if name != "" and eisup != "" and store != "" and rest != "":

                    user = request.user

                    ### Поиск среди складов
                    if store_list.objects.filter(name=store).exists():
                        st = store_list.objects.get(name=store)
                    else:
                        st = store_list.objects.create(name=store)

                    ### Поиск записей остатков
                    if store_rest.objects.filter(eisup=eisup,store=st,mol=user).exists():
                        st_rest = store_rest.objects.filter(eisup=eisup,store=st,mol=user).first()
                        data.append({
                            'id': st_rest.id,
                            'name': name,
                            'eisup': eisup,
                            'store': store,
                            'rest': rest,
                            'load': "no"
                        })

                    else:
                        store_rest.objects.create(eisup=eisup,store=st,mol=user,name=name,rest=Decimal(rest))
                        data.append({
                            'id': "",
                            'name': name,
                            'eisup': eisup,
                            'store': store,
                            'rest': rest,
                            'load': "yes"
                        })



            return HttpResponse("""
            <html><head><script type="text/javascript">
            window.top.ClearUploadEisup();
            window.top.DiffUpload(%s);
            </script></head></html>
            """ % json.dumps(data))


