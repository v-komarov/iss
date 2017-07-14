# coding:utf-8

import json
import decimal

from django.http import HttpResponse, HttpResponseRedirect
from django import template

from iss.regions.forms import OrderForm
from iss.regions.models import orders
from iss.localdicts.models import regions


def get_json(request):
    response_data = {}

    if request.method == "GET":

        r = request.GET
        rg = request.GET.get


        ### Отображение пустой формы (добавление позиции) заказов
        if r.has_key("action") and rg("action") == 'new_roworder':
            form = OrderForm()
            t = template.Template("{{ form.as_table }}")
            c = template.Context({'form': form})
            f = t.render(c)
            response_data = {"result": "ok", "form": f}




        ### Отображение формы с данными при редактировании заказа
        if r.has_key("action") and rg("action") == 'edit_roworder':
            row_id = int(request.GET["row_id"], 10)
            d = orders.objects.get(pk=row_id)
            form = OrderForm(instance=d)
            t = template.Template("{{ form.as_table }}")
            c = template.Context({'form': form})
            f = t.render(c)
            response_data = {"result": "ok", "row_id": row_id, "form": f}




        ### Вывод информации по заказам
        if r.has_key("action") and rg("action") == 'get-rows-order':
            region = regions.objects.get(pk=(int(request.GET["region"], 10)))

            tz = request.session['tz'] if request.session.has_key('tz') else 'UTC'

            rows = ""
            total = decimal.Decimal('0.00')

            for i in orders.objects.filter(region=region).order_by('order'):
                total += i.rowsum
                updatetime = ""
                t = template.Template("<tr id={{ id }}><td><a edit>{{ order }}</a></td><td><a edit>{{ model }}</a></td><td><a edit>{{ name }}</a></td><td><a edit>{{ ed }}</a></td><td><a edit>{{ count }}</a></td><td><a edit>{{ price }}</a></td><td><a edit>{{ rowsum }}</a></td><td><a>{% load tz %}{% timezone tz %}{{ update|date:\"d.m.Y H:i e\" }}{% endtimezone %}</a></td><td><a>{{ author }}</a></td><td><a delete title=\"Удалить\"><span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span></a></td><tr>")
                c = template.Context({'tz': tz, 'id': i.id, 'order': i.order, 'model': i.model, 'name': i.name, 'ed': i.ed, 'price': i.price, 'count': i.count, 'rowsum': i.rowsum, 'edited': updatetime, 'author': i.author })
                row = t.render(c)
                rows += row

            t = template.Template("<tr><td></td><td></td><td></td><td></td><td></td><td>Всего</td><td>{{ total }}</td><td></td><td></td><td</td></tr>")
            c = template.Context({'total': total})
            row = t.render(c)
            rows += row

            response_data = {"result": "ok", "rows": rows}




        ### Удаление позиции заказа
        if r.has_key("action") and rg("action") == 'delete-row-order':
            orders.objects.get(pk=(int(request.GET["row_id"], 10))).delete()

            response_data = {"result": "ok"}




    if request.method == "POST":


        data = eval(request.body)

        # Создание новой позиции заказа
        if data.has_key("action") and data["action"] == 'order-adding':
            region = data["region"]
            order = int(data["order"], 10)
            model = data["model"]
            name = data["name"]
            ed = data["ed"]
            count = int(data["count"], 10)
            price = decimal.Decimal(data["price"])
            comment = data["comment"]


            ### Для конкретного региона
            if region != "":
                reg = regions.objects.get(pk=int(region, 10))
                orders.objects.create(
                    region = reg,
                    order = order,
                    model = model,
                    name = name,
                    ed = ed,
                    count = count,
                    price = price,
                    rowsum = count * price,
                    comment = comment
                )
            else:
                ### Создание для каждого региона
                for reg in regions.objects.all():
                    orders.objects.create(
                        region=reg,
                        order=order,
                        model=model,
                        name=name,
                        ed=ed,
                        count=count,
                        price=price,
                        rowsum=count * price,
                        comment=comment
                    )


            response_data = {"result": "ok"}




        # Изменение позиции заказа
        if data.has_key("action") and data["action"] == 'order-editing':
            row_id = data["row_id"]
            region = data["region"]
            order = int(data["order"], 10)
            model = data["model"]
            name = data["name"]
            ed = data["ed"]
            count = int(data["count"], 10)
            price = decimal.Decimal(data["price"])
            comment = data["comment"]

            reg = regions.objects.get(pk=int(region, 10))

            d = orders.objects.get(pk=int(row_id, 10))
            d.region = reg
            d.order = order
            d.model = model
            d.name = name
            d.ed = ed
            d.count = count
            d.price = price
            d.rowsum = price*count
            d.comment = comment
            d.save()


            response_data = {"result": "ok"}



    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response
