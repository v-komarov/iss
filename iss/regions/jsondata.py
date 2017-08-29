# coding:utf-8

import json
import decimal
import datetime
import random
import logging

from pytz import timezone

from snakebite.client import Client

from django.http import HttpResponse, HttpResponseRedirect
from django import template
from django.contrib.auth.models import User

from iss.regions.forms import OrderForm
from iss.regions.models import orders, proj, proj_stages, proj_notes
from iss.localdicts.models import regions, proj_temp
from iss.regions.sendmail import send_proj_worker, send_proj_worker2



logger_proj = logging.getLogger('projects')








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







        ### Наполнение данными формы редактирования этапа
        if r.has_key("action") and rg("action") == 'stage-get-data':
            stage_id = int(request.GET["stage_id"], 10)
            stage = proj_stages.objects.get(pk=stage_id)

            response_data = {
                "result": "ok",
                "order": ".".join(["%s" % x for x in stage.stage_order]),
                "name": stage.name,
                "days": stage.days,
                "deferment": stage.deferment,
                "depend_on": ".".join(["%s" % x for x in stage.depend_on["stages"]])

            }





        ### Добавление пользователя в этап
        if r.has_key("action") and rg("action") == 'stage-step-add-user':
            row_id = int(request.GET["row_id"], 10)
            user_id = int(request.GET["user_id"], 10)
            u = User.objects.get(pk=user_id)

            stage = proj_stages.objects.get(pk=row_id)
            stage.workers.add(u)
            proj = stage.proj
            rowname = stage.name


            ### Отправка email сообщение если требуется
            send_proj_worker2(row_id, u)

            ### Запись в лог файл
            logger_proj.info(u"Проект: {proj} - {rowname} {user} добавил исполнителя {worker}".format(
                proj=proj.name,
                rowname=rowname,
                worker=u.get_username(),
                user=request.user.get_username())
            )

            response_data = { "result": "ok" }




        ### Удаление пользователя из этапа
        if r.has_key("action") and rg("action") == 'stage-step-remove-user':
            row_id = int(request.GET["row_id"], 10)
            user_id = int(request.GET["user_id"], 10)
            u = User.objects.get(pk=user_id)

            stage = proj_stages.objects.get(pk=row_id)
            stage.workers.remove(u)
            proj = stage.proj
            rowname = stage.name


            ### Запись в лог файл
            logger_proj.info(u"Проект: {proj} - {rowname} {user} удалил исполнителя {worker}".format(
                proj=proj.name,
                rowname=rowname,
                worker=u.get_username(),
                user=request.user.get_username())
            )


            response_data = { "result": "ok" }





        ### Удаление этапа
        if r.has_key("action") and rg("action") == 'stage-delete':
            row_id = int(request.GET["row_id"], 10)

            stage = proj_stages.objects.get(pk=row_id)
            proj = stage.proj
            rowname = stage.name
            stage.delete()


            ### Запись в лог файл
            logger_proj.info(u"Проект: {proj} - {rowname} {user} удалил строку этапа".format(
                proj=proj.name,
                rowname=rowname,
                user=request.user.get_username())
            )


            response_data = { "result": "ok" }





        ### Установка статуса этапа
        if r.has_key("action") and rg("action") == 'stage-step-status':
            row_id = int(request.GET["row_id"], 10)
            row_type = request.GET["row_type"]
            status = request.GET["status"]


            stage = proj_stages.objects.get(pk=row_id)
            stage.done = True if status == "yes" else False
            stage.save()
            proj = stage.proj
            rowname = stage.name
            status = stage.done



            ### Отправка email сообщение если требуется
            send_proj_worker(row_type, row_id, request.user)

            ### Запись в лог файл
            logger_proj.info(u"Проект: {proj} - {rowname} {user} отметил как {done}".format(
                proj=proj.name,
                rowname=rowname,
                done = status,
                user=request.user.get_username())
            )



            response_data = { "result": "ok" }





        ### Удаление вложеного файла
        if r.has_key("action") and rg("action") == 'stage-step-delete-file':
            row_id = int(request.GET["row_id"], 10)
            file_id = request.GET["file_id"]

            from iss.regions.models import load_proj_files

            f = load_proj_files.objects.get(pk=file_id)
            filename = f.filename
            f.delete()

            stage = proj_stages.objects.get(pk=row_id)
            proj = stage.proj
            rowname = stage.name


            client = Client('10.6.0.135', 9000)
            for x in client.delete(['/projects/%s' % file_id,], recurse=True):
                print x

            ### Запись в лог файл
            logger_proj.info(u"Проект: {proj} - {rowname} {user} удалил файл {fname}".format(
                proj=proj.name,
                rowname=rowname,
                fname = filename,
                user=request.user.get_username())
            )



            response_data = { "result": "ok" }








        ### Рассчет дат проекта
        if r.has_key("action") and rg("action") == 'project-calculate':

            from iss.regions.models import proj

            pr = proj.objects.get(pk=request.session['proj_id'])

            """
            ### Формирование id записей этапов
            stage_id = [s.id for s in pr.proj_stages_set.all()]


            while len(stage_id) > 0:

                ### Расчет дат по-этапно
                ### Первоначально для этапов и шагов с зависимостью от начала проекта
                stage = proj_stages.objects.get(pk=random.choice(stage_id))


                if stage.depend_on["stages"] == []:
                    ### Для этапов с пустым полем зависимости начало этапа - начало проекта
                    stage.begin = pr.start
                    stage.save()
                    ### Этап обработан - убираем id из списка
                    stage_id.remove(stage.id)
                    ### Обрабатывать вложенные шаги
                    steps_run = "ok"



                ### Для этапов с зависимостью от других
                else:

                    stage_id2 = []  # id этапов, от которых есть зависимость
                    stage_enddate = []
                    ### Нужно проставить начало этапа в зависимости от предыдущих
                    for st in stage.depend_on["stages"]:
                        stg = pr.proj_stages_set.all().filter(order=st)[0]
                        stage_id2.append(stg.id)
                        stage_enddate.append(stg.end)
                    ### Если этапы, от которых зависимость уже обработаны
                    if list(set(stage_id2).intersection(set(stage_id))) == []:
                        ### Выбрать дату начала от самой поздней даты предшествующих пунктов
                        stage.begin = date_plus(sorted(stage_enddate)[-1], 1)
                        stage.save()
                        ### Этап обработан - убираем id из списка
                        stage_id.remove(stage.id)
                        ### Обрабатывать вложенные шаги
                        steps_run = "ok"
                    else:
                        ### Обрабатывать вложенные шаги
                        steps_run = "no"

                #### Обрабатывать шаги или нет
                if steps_run == "ok":

                    ### Формирование id записей шагов
                    step_id = [s.id for s in stage.proj_steps_set.all()]


                    while len(step_id) > 0:
                        step = proj_steps.objects.get(pk=random.choice(step_id))
                        ### Обрабатываем только если есть в списке необработанных id
                        if step.id in step_id:
                            ### Обрабатываем шаг, если зависимости нет или зависимые строки шаги обработаны
                            if step.depend_on["steps"] == []:
                                step.begin = stage.begin
                                step.end = date_plus(stage.begin, step.days)
                                step.save()
                                ### Шаг обработан - убираем id из списка
                                step_id.remove(step.id)
                            else:
                                ### Проверка обработаны ли шаги от которых есть зависимость
                                step_id2 = [] # id шагов, от которых есть зависимость
                                step_enddate = [] # Список дат, завершения шага
                                for p in step.depend_on["steps"]:
                                    stp = stage.proj_steps_set.all().get(order=p)
                                    step_id2.append(stp.id)
                                    step_enddate.append(stp.end)
                                if list(set(step_id2).intersection(set(step_id))) == []:
                                    ### Выбрать дату начала от самой поздней даты предшествующих пунктов
                                    step.begin = date_plus(sorted(step_enddate)[-1], 1)
                                    step.end = date_plus(step.begin, step.days)
                                    step.save()
                                    ### Шаг обработан - убираем id из списка
                                    step_id.remove(step.id)

                    ### расчет даты окончания этапа и длительность в днях
                    step_enddate = []  # Список дат, завершения шага
                    for step in stage.proj_steps_set.all():
                        step_enddate.append(step.end)

                    ### Самая поздняя дата
                    stage.end = sorted(step_enddate)[-1]
                    ### Вычисление длительности этапа
                    stage.days = working_days(stage.begin, stage.end)
                    stage.save()


            ### Запись в лог файл
            logger_proj.info(u"Проект: {proj} {user} Запустил расчет дат".format(
                proj=pr.name,
                user=request.user.get_username())
            )

            """
            G = pr.calculate_dates()
            #print pr.calculate_dates().nodes()
            print G.edges()


            response_data = { "result": "ok" }






        ### Отображение данных коментариев по этапам
        if r.has_key("action") and rg("action") == 'get-proj-notes':
            tz = request.session['tz']
            row_id = int(request.GET["row_id"], 10)

            stage = proj_stages.objects.get(pk=row_id)
            rowname = stage.name
            notes = []
            for note in  stage.proj_notes_set.order_by('-datetime'):
                notes.append({
                    'datetime': note.datetime.astimezone(timezone(tz)).strftime("%d.%m.%Y"),
                    'author':note.author.get_username() + " (" + note.author.get_full_name() + ")",
                    'note': note.note
                })





            response_data = {
                "result": "ok",
                "name": rowname,
                "notes_list": notes
            }








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







        ### Создание проекта
        if data.has_key("action") and data["action"] == 'create-proj':

            ### Шаблон проекта
            t = proj_temp.objects.get(pk=int(data['temp'], 10))

            stages = eval(t.template_project)["stages"]

            ### название проекта
            name = data["name"].strip()
            ### начало проекта
            start = datetime.datetime.strptime(data["start"].strip(), "%d.%m.%Y")

            from iss.regions.models import proj
            p = proj.objects.create(
                name=name, start=start, temp=t, author=request.user
            )

            for stage in stages:
                ### Создать этапы
                sg = proj_stages.objects.create(
                    order= 0,
                    stage_order=stage['order'],
                    name= stage["name"],
                    proj= p,
                    days= stage["days"] if stage.has_key("days") else None,
                    depend_on = {'stages': stage["depend_on"]} if stage.has_key("depend_on") else {'stages':[]}
                )


            response_data = {"result": "ok"}






        ### Сохранение данных этапа интерфейса управления проектами
        if data.has_key("action") and data["action"] == 'save-stage-data':

            s = proj_stages.objects.get(pk=int(data['row_id'], 10))

            name = data["name"].strip()
            order = [int(x, 10) for x in data["order"].strip().split(".")]
            days = int(data["days"], 10) if data["days"] != "" else None
            deferment = int(data["deferment"], 10) if data["deferment"] != "" else 0
            depend_on = [int(x, 10) for x in data["depend_on"].split(".")] if data["depend_on"] != "" else []

            s.name = name
            s.stage_order = order
            s.days = days
            s.deferment = deferment
            s.depend_on = {"stages": depend_on}
            s.save()

            ### Запись в лог файл
            logger_proj.info(u"Проект: {proj} - {stage} {user} сохранил данные этапа".format(
                proj=s.proj.name,
                stage=s.name.decode("utf-8"),
                user=request.user.get_username())
            )


            response_data = {"result": "ok"}




        ### Создание нового этапа интерфейса управления проектами
        if data.has_key("action") and data["action"] == 'create-stage-data':

            from iss.regions.models import proj

            p = proj.objects.get(pk=int(request.session['proj_id'], 10))

            name = data["name"].strip()
            order = [int(x, 10) for x in data["order"].strip().split(".")]
            days = int(data["days"], 10) if data["days"] != "" else None
            deferment = int(data["deferment"], 10) if data["deferment"] != "" else 0
            depend_on = [int(x, 10) for x in data["depend_on"].split(".")] if data["depend_on"] != "" else []

            proj_stages.objects.create(
                name=name,
                stage_order=order,
                days=days,
                deferment=deferment,
                depend_on={"stages": depend_on},
                proj=p
            )


            ### Запись в лог файл
            logger_proj.info(u"Проект: {proj} - {stage} {user} создал новый этап".format(
                proj=p.name,
                stage=name.decode("utf-8"),
                user=request.user.get_username())
            )


            response_data = {"result": "ok"}





        ### Сохранение основных данных проекта
        if data.has_key("action") and data["action"] == 'save-proj-main-data':

            from iss.regions.models import proj

            p = proj.objects.get(pk=int(request.session['proj_id'], 10))

            name = data["name"].strip()
            start = datetime.datetime.strptime(data["start"].strip(), "%d.%m.%Y")

            p.name = name
            p.start = start
            p.save()

            ### Запись в лог файл
            logger_proj.info(u"Проект: {proj} {user} сохранил основные данные".format(
                proj=p.name.decode("utf-8"),
                user=request.user.get_username())
            )


            response_data = {"result": "ok"}




        ### Добавление коментария к этапу или шагу
        if data.has_key("action") and data["action"] == 'proj-adding-note':
            row_id = int(data["row_id"], 10)
            row_type = data["row_type"]
            note = data["note"]

            if row_type == "stage":
                stage = proj_stages.objects.get(pk=row_id)
                proj_notes.objects.create(
                    author=request.user,
                    note=note,
                    stage=stage
                )

            if row_type == "step":
                step = proj_steps.objects.get(pk=row_id)
                proj_notes.objects.create(
                    author=request.user,
                    note=note,
                    step=step
                )



            response_data = {"result": "ok"}





    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response
