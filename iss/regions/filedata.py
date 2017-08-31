#coding:utf-8


from	django.http	import	HttpResponse, HttpResponseRedirect


import xlwt
import tempfile
import os
import StringIO

from operator import itemgetter

from snakebite.client import Client

from iss.regions.models import orders, load_proj_files, proj_stages, proj
from iss.localdicts.models import regions





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


    run = 'curl -i -X PUT -T %s -L "http://10.6.0.135:50070/webhdfs/v1/projects/%s?user.name=root&op=CREATE&overwrite=true&replication=4"' % (tf.name, rec.id)
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


        response = HttpResponse(data, content_type="application/octet-stream")
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
def projgant(request, project):
    pass