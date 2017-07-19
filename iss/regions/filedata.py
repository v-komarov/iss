#coding:utf-8


from	django.http	import	HttpResponse

import xlwt

from iss.regions.models import orders
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


    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename="orders.xls"'
    book.save(response)
    return response
