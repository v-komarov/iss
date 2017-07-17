#coding:utf-8


from	django.http	import	HttpResponse

from iss.regions.models import orders
from iss.localdicts.models import regions



### Данные по заказам выбранного региона
def get_orders_region(request):

    if request.GET.has_key("action") and request.GET["action"] == "getorders":
        region_id = request.GET["region"]

        region = regions.objects.get(pk=int(region_id, 10))


        response_data = u"№п/п;Артикул/марка;Наименование товара;Ед.изм.;Кол-во;Начальная цена за единицу товара, в руб. без НДС с учетов всех расходов;Начальная цена договора, в руб. без НДС с учетов всех расходов;Подключения B2B+B2O;Инвестпроекты;ТО сетей связи;Коментарий;\n"

        for row in orders.objects.filter(region=region).order_by('order'):
            price = ("%s" % row.price).replace(".", ",")
            rowsum = ("%s" % row.rowsum).replace(".", ",")
            response_data += u"{order};{model};{name};{ed};{count};{price};{rowsum};{b2b_b2o};{investment};{to};{comment};\n".format(order=row.order, model=row.model, name=row.name, ed=row.ed, count=row.count, price=price, rowsum=rowsum, b2b_b2o=row.b2b_b2o, investment=row.investment, to=row.to, comment=row.comment)





    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'
    response.write(response_data.encode("cp1251"))
    return response
