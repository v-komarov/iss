# coding:utf-8

import json
import decimal
import datetime
import networkx as nx
import matplotlib.pyplot as plt

from django.http import HttpResponse, HttpResponseRedirect
from django import template
from django.contrib.auth.models import User

from iss.regions.forms import OrderForm
from iss.regions.models import orders, messages, proj, proj_stages, proj_steps
from iss.localdicts.models import regions, MessageType, proj_temp







### Уровень доступа для таблицы заказов
def get_access_order(request):
    if request.user.is_authenticated():
        ### Проверка на принадлежность группе
        if request.user.groups.filter(name='orders-admin'):
            return "admin"
        if request.user.groups.filter(name='orders'):
            return "user"

    return "anonymous"





### рассчет дат с учетом выходных дней
def date_plus(date,delta):

    ## Добавляем по одному дню и проверяем на субботу или воскресенье
    while delta != 0:
        date = date + datetime.timedelta(days=1)
        if date.weekday() < 5:
            delta = delta - 1
            print date, delta

    return date






def get_json(request):

    ### Timezone
    tz = request.session['tz'] if request.session.has_key('tz') else 'UTC'


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
            response_data = {"result": "ok", "form": f, "access": get_access_order(request)}




        ### Отображение формы с данными при редактировании заказа
        if r.has_key("action") and rg("action") == 'edit_roworder':
            row_id = int(request.GET["row_id"], 10)
            d = orders.objects.get(pk=row_id)
            form = OrderForm(instance=d)
            t = template.Template("{{ form.as_table }}")
            c = template.Context({'form': form})
            f = t.render(c)
            response_data = {"result": "ok", "row_id": row_id, "form": f, "access": get_access_order(request)}




        ### Вывод информации по заказам
        if r.has_key("action") and rg("action") == 'get-rows-order':
            region = regions.objects.get(pk=(int(request.GET["region"], 10)))



            rows = ""
            total = decimal.Decimal('0.00')

            for i in orders.objects.filter(region=region).order_by('order'):
                total += i.rowsum
                t = template.Template("""<tr id={{ id }}><td><a edit>{{ order }}</a></td>
                                      <td><a edit>{{ model }}</a></td><td><a edit>{{ name }}</a></td>
                                      <td><a edit>{{ ed }}</a></td><td><a edit>{{ count }}</a></td>
                                      <td><a edit>{{ price }}</a></td><td><a edit>{{ rowsum }}</a></td>
                                      <td><a edit>{{ b2b_b2o }}</a></td><td><a edit>{{ investment }}</a></td>
                                      <td><a edit>{{ to }}</a></td><td><a edit>{{ comment }}</a></td>
                                      <td><a edit id="tooltip" title="{{ techz }}">{{ techz|truncatechars:200 }}</a></td>
                                      <td>{% load tz %}{% timezone tz %}{{ edited|date:\"d.m.Y H:i e\" }}{% endtimezone %}</td>
                                      <td>{{ author }}</td><td><a delete title=\"Удалить\"><span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span></a></td>
                                      <tr>""")
                c = template.Context({'tz': tz, 'id': i.id, 'order': i.order,
                                      'model': i.model, 'name': i.name, 'ed': i.ed,
                                      'price': i.price, 'count': i.count, 'rowsum': i.rowsum,
                                      'comment': i.comment, 'edited': i.datetime_update,
                                      'techz': i.tz,
                                      'author': i.author, 'b2b_b2o': i.b2b_b2o,
                                      'investment': i.investment, 'to': i.to })
                row = t.render(c)
                rows += row

            t = template.Template("<tr><td></td><td></td><td></td><td></td><td></td><td>Всего</td><td>{{ total }}</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>")
            c = template.Context({'total': total})
            row = t.render(c)
            rows += row

            response_data = {"result": "ok", "rows": rows}




        ### Удаление позиции заказа
        if r.has_key("action") and rg("action") == 'delete-row-order':

            if get_access_order(request) == "admin":
                orders.objects.get(pk=(int(request.GET["row_id"], 10))).delete()
                response_data = {"result": "ok"}
            else:
                response_data = {"result": "notaccess"}




        ### Фильтр по региону для интерфейса Реестр
        if r.has_key("action") and rg("action") == 'filter-region-reestr':
            region = request.GET["region_id"]
            if region != "0":
                request.session["filter-region-reestr"] = region
            else:
                del request.session["filter-region-reestr"]

            response_data = {"result": "ok"}



        ### Фильтр по населенному пункту для интерфейса Реестр
        if r.has_key("action") and rg("action") == 'filter-city-reestr':
            region = request.GET["city_id"]
            if region != "0":
                request.session["filter-city-reestr"] = region
            else:
                del request.session["filter-city-reestr"]


            response_data = {"result": "ok"}




        ### Фильтр входящие /исходящие интерфейса Документооборот
        if r.has_key("action") and rg("action") == 'filter-docs-inout':
            inout = request.GET["inout_id"]
            if inout != "0":
                request.session["inout_value"] = inout
            else:
                del request.session["inout_value"]


            response_data = {"result": "ok"}





        ### Фильтр по виду сообщения интерфейса Документооборот
        if r.has_key("action") and rg("action") == 'filter-docs-messagetype':
            mess_type = request.GET["mess_type"]
            if mess_type != "0":
                request.session["message_type_value"] = mess_type
            else:
                del request.session["message_type_value"]


            response_data = {"result": "ok"}





        ### Фильтр по статусу сообщения интерфейса Документооборот
        if r.has_key("action") and rg("action") == 'filter-docs-messagestatus':
            mess_status = request.GET["mess_status"]
            if mess_status != "0":
                request.session["message_status_value"] = mess_status
            else:
                del request.session["message_status_value"]


            response_data = {"result": "ok"}





        ### Сохранение id сообщения интерфейса Документооборот
        if r.has_key("action") and rg("action") == 'docs-save-id':
            message_id = request.GET["message_id"]

            request.session['message_id'] = message_id


            response_data = {"result": "ok"}




        ### Сохранение id проекта
        if r.has_key("action") and rg("action") == 'proj-save-id':
            proj_id = request.GET["proj_id"]

            request.session['proj_id'] = proj_id


            response_data = {"result": "ok"}



        ### Наполнение данными формы редактирования этапа
        if r.has_key("action") and rg("action") == 'stage-get-data':
            stage_id = int(request.GET["stage_id"], 10)
            stage = proj_stages.objects.get(pk=stage_id)

            response_data = {
                "result": "ok",
                "order": stage.order,
                "name": stage.name,
                "days": stage.days,
                "depend_on": stage.depend_on["stages"]

            }



        ### Наполнение данными формы редактирования шага
        if r.has_key("action") and rg("action") == 'step-get-data':
            step_id = int(request.GET["step_id"], 10)
            step = proj_steps.objects.get(pk=step_id)

            response_data = {
                "result": "ok",
                "order": step.order,
                "name": step.name,
                "days": step.days,
                "depend_on": step.depend_on["steps"]

            }



        ### Добавление пользователя в этап или шаг
        if r.has_key("action") and rg("action") == 'stage-step-add-user':
            row_id = int(request.GET["row_id"], 10)
            row_type = request.GET["row_type"]
            user_id = int(request.GET["user_id"], 10)
            u = User.objects.get(pk=user_id)

            if row_type == "stage":
                stage = proj_stages.objects.get(pk=row_id)
                stage.workers.add(u)

            if row_type == "step":
                step = proj_steps.objects.get(pk=row_id)
                step.workers.add(u)


            response_data = { "result": "ok" }




        ### Удаление пользователя из этапа или шага
        if r.has_key("action") and rg("action") == 'stage-step-remove-user':
            row_id = int(request.GET["row_id"], 10)
            row_type = request.GET["row_type"]
            user_id = int(request.GET["user_id"], 10)
            u = User.objects.get(pk=user_id)

            if row_type == "stage":
                stage = proj_stages.objects.get(pk=row_id)
                stage.workers.remove(u)

            if row_type == "step":
                step = proj_steps.objects.get(pk=row_id)
                step.workers.remove(u)


            response_data = { "result": "ok" }




        ### Установка статуса этапа или шага
        if r.has_key("action") and rg("action") == 'stage-step-status':
            row_id = int(request.GET["row_id"], 10)
            row_type = request.GET["row_type"]
            status = request.GET["status"]

            if row_type == "stage":
                stage = proj_stages.objects.get(pk=row_id)
                stage.done = True if status == "yes" else False
                stage.save()

            if row_type == "step":
                step = proj_steps.objects.get(pk=row_id)
                step.done = True if status == "yes" else False
                step.save()


            response_data = { "result": "ok" }




        ### Рассчет дат проекта
        if r.has_key("action") and rg("action") == 'project-calculate':

            p = proj.objects.get(pk=request.session['proj_id'])

            ### Создание и наполнение графа
            DG = nx.DiGraph()
            DG.add_node(0, type='project')

            ### Создание узлов и дочерних связей шагов на этапы
            for stage in p.proj_stages_set.all():
                DG.add_node(stage.order, type='stage', id=stage.id)
                if stage.depend_on["stages"] == []:
                   ### Связи от начала проекта
                   DG.add_edge(0, stage.order, days=0)
                for step in stage.proj_steps_set.all():
                    DG.add_node(step.order, type='step', id=step.id)
                    ### Связи шагов на родительский этап если другой зависимости нет
                    if step.depend_on["steps"] == []:
                        DG.add_edge(step.order, stage.order, days=step.days)

            ### Создание зависимых связей
            for stage in p.proj_stages_set.all():
                if stage.depend_on["stages"] != []:
                    for link in stage.depend_on["stages"]:
                        ### Добавление связи
                        t = nx.get_node_attributes(DG, 'type')
                        i = nx.get_node_attributes(DG, 'id')
                        if t[link] == "stage":
                            DG.add_edge(link, stage.order, days=proj_stages.objects.get(pk=i[link]).days if proj_stages.objects.get(pk=i[link]).days else 0)
                        if t[link] == "step":
                            DG.add_edge(link, stage.order, days=proj_steps.objects.get(pk=i[link]).days)

                        ### Для шагов
                        for step in stage.proj_steps_set.all():
                            if step.depend_on["steps"] != []:
                                for link in step.depend_on["steps"]:
                                    ### Добавление связи
                                    t = nx.get_node_attributes(DG, 'type')
                                    i = nx.get_node_attributes(DG, 'id')
                                    if t[link] == "stage":
                                        DG.add_edge(link, stage.order, days=proj_stages.objects.get(pk=i[link]).days if proj_stages.objects.get(pk=i[link]).days else 0)
                                    if t[link] == "step":
                                        DG.add_edge(link, stage.order, days=proj_steps.objects.get(pk=i[link]).days)

            for n in DG.nodes():
                print DG.degree([0, n])

            nx.draw(DG)
            plt.savefig("~/123.png")

            print DG.edges()
            print "vvvvvvvvvvvvvvvvvvvvvvvvvvv"

            response_data = { "result": "ok" }






    if request.method == "POST":


        data = eval(request.body)

        # Создание новой позиции заказа
        if data.has_key("action") and data["action"] == 'order-adding':
            region = data["region"]
            order = int(data["order"], 10)
            model = data["model"]
            name = data["name"]
            ed = data["ed"]
            b2b_b2o = int(data["b2b_b2o"], 10)
            investment = int(data["investment"], 10)
            to = int(data["to"], 10)
            price = decimal.Decimal(data["price"])
            comment = data["comment"]
            count = b2b_b2o + investment + to
            tz = data["tz"]


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
                    b2b_b2o = b2b_b2o,
                    investment = investment,
                    to = to,
                    comment = comment,
                    tz = tz,
                    author=request.user.get_username() + " (" + request.user.get_full_name() + ")"
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
                        b2b_b2o=b2b_b2o,
                        investment=investment,
                        to=to,
                        comment=comment,
                        tz = tz,
                        author=request.user.get_username() + " (" + request.user.get_full_name() + ")"
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
            price = decimal.Decimal(data["price"])
            b2b_b2o = int(data["b2b_b2o"], 10)
            investment = int(data["investment"], 10)
            to = int(data["to"], 10)
            comment = data["comment"]
            count = b2b_b2o + investment + to
            tz = data["tz"]

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
            d.b2b_b2o = b2b_b2o
            d.investment = investment
            d.to = to
            d.comment = comment
            d.tz = tz
            d.author = request.user.get_username() + " (" + request.user.get_full_name() + ")"
            d.save()


            response_data = {"result": "ok"}





        ### Сохранение общих данных сообщения интерфейса Документооборот
        if data.has_key("action") and data["action"] == 'message-save-common-data':

            m = messages.objects.get(pk=int(request.session['message_id'], 10))

            head = data["head"].strip()
            message = data["message"].strip()
            message_type = data["message_type"]

            m.message = message
            m.head = head
            m.message_type = MessageType.objects.get(pk=int(message_type, 10))
            m.author_update = request.user
            m.save()

            response_data = {"result": "ok"}




        ### Создание проекта
        if data.has_key("action") and data["action"] == 'create-proj':

            ### Шаблон проекта
            t = proj_temp.objects.get(pk=int(data['temp'], 10))

            stages = eval(t.template_project)["stages"]

            ### название проекта
            name = data["name"].strip()
            ### начало проекта
            start = datetime.datetime.strptime(data["start"].strip(), "%d.%m.%Y")

            p = proj.objects.create(
                name=name, start=start, temp=t, author=request.user
            )

            for stage in stages:
                ### Создать этапы
                sg = proj_stages.objects.create(
                    order= stage["order"],
                    name= stage["name"],
                    proj= p,
                    days= stage["days"] if stage.has_key("days") else None,
                    depend_on = {'stages': stage["depend_on"]} if stage.has_key("depend_on") else {'stages':[]}
                )
                if stage.has_key("steps"):
                    for step in stage["steps"]:
                        proj_steps.objects.create(
                            order= step["order"],
                            name=step["name"],
                            stage= sg,
                            days= step["days"] if step.has_key("days") else None,
                            depend_on={'steps': step["depend_on"]} if step.has_key("depend_on") else {'steps': []}
                        )


            response_data = {"result": "ok"}



        ### Сохранение данных этапа интерфейса управления проектами
        if data.has_key("action") and data["action"] == 'save-stage-data':

            s = proj_stages.objects.get(pk=int(data['row_id'], 10))

            name = data["name"].strip()
            order = int(data["order"].strip(), 10)
            days = int(data["days"], 10) if data["days"] != "" else None
            depend_on = [int(x, 10) for x in data["depend_on"].split(",")] if data["depend_on"] != "" else []

            s.name = name
            s.order = order
            s.days = days
            s.depend_on = {"stages": depend_on}
            s.save()

            response_data = {"result": "ok"}




        ### Сохранение данных шага интерфейса управления проектами
        if data.has_key("action") and data["action"] == 'save-step-data':

            s = proj_steps.objects.get(pk=int(data['row_id'], 10))

            name = data["name"].strip()
            order = int(data["order"].strip(), 10)
            days = int(data["days"], 10) if data["days"] != "" else None
            depend_on = [int(x, 10) for x in data["depend_on"].split(",")] if data["depend_on"] != "" else []

            s.name = name
            s.order = order
            s.days = days
            s.depend_on = {"steps": depend_on}
            s.save()

            response_data = {"result": "ok"}




        ### Сохранение основных данных проекта
        if data.has_key("action") and data["action"] == 'save-proj-main-data':

            p = proj.objects.get(pk=request.session['proj_id'])

            name = data["name"].strip()
            start = datetime.datetime.strptime(data["start"].strip(), "%d.%m.%Y")

            p.name = name
            p.start = start
            p.save()

            response_data = {"result": "ok"}




    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response
