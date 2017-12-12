# coding:utf-8

import json
import decimal
import datetime
import random
import logging
import time
import uuid

from pytz import timezone

from snakebite.client import Client

from django.http import HttpResponse, HttpResponseRedirect
from django import template
from django.contrib.auth.models import User

from iss.regions.forms import OrderForm, WorkersDatesStagesForm
from iss.regions.models import orders, proj, proj_stages, proj_notes, reestr_proj, reestr_proj_files, reestr_proj_comment, stages_history, reestr_proj_exec_date, reestr_proj_messages_history
from iss.localdicts.models import regions, proj_temp, regions, blocks, address_companies, stages as stages_list, address_house, init_reestr_proj, business, rates, passing, proj_other_system, message_type
from iss.regions.sendmail import send_proj_worker, send_proj_worker2, send_problem, send_reestr_proj




logger_proj = logging.getLogger('projects')



tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)





### Уровень доступа для таблицы заказов
def get_access_order(request):
    if request.user.is_authenticated():
        ### Проверка на принадлежность группе
        if request.user.groups.filter(name='orders-admin'):
            return "admin"
        if request.user.groups.filter(name='orders'):
            return "user"

    return "anonymous"









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





        ### Установка степени выполнения этапа в процентах
        if r.has_key("action") and rg("action") == 'stage-percent':
            row_id = int(request.GET["row_id"], 10)
            percent = int(request.GET["percent"], 10)


            stage = proj_stages.objects.get(pk=row_id)
            stage.percent = percent
            stage.save()
            proj = stage.proj



            ### Отправка email сообщение если требуется
            if percent == 100:
                ### Выбор зависимых пунктов
                stages = proj.proj_stages_set.all().filter(depend_on__stages=stage.stage_order)
                send_proj_worker(stages, request.user)

                ### Отметка статуса проекта по выполенному этапу
                proj.status = stage.name
                proj.save()


            ### Запись в лог файл
            logger_proj.info(u"Проект: {proj} - {rowname} {user} отметил {percent} процент выполнения".format(
                proj=proj.name,
                rowname=stage.name,
                percent = percent,
                user=request.user.get_username())
            )



            response_data = { "result": "ok" }





        ### список статусов по этапам проекта в процентах
        if r.has_key("action") and rg("action") == 'stage-percent-status':
            from iss.regions.models import proj

            pr = proj.objects.get(pk=request.session['proj_id'])
            status = {}
            for item in pr.proj_stages_set.all():
                row_id = "row%s" % item.id
                status[row_id] = item.percent

            response_data = {"result": "ok", "status": status}


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

            pr.calculate_dates()
            #print pr.calculate_dates().nodes()
            #print G.edges()


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




        ### Сохранение даты начала периода списка задач исполнителей
        if r.has_key("action") and rg("action") == 'workertask-begin':
            begin = request.GET["date"]

            request.session['begin_date'] = datetime.datetime.strptime(begin, "%d.%m.%Y")

            response_data = {"result": "ok"}


        ### Сохранение даты конца периода списка задач исполнителей
        if r.has_key("action") and rg("action") == 'workertask-end':
            end = request.GET["date"]

            request.session['end_date'] = datetime.datetime.strptime(end, "%d.%m.%Y")

            response_data = {"result": "ok"}


        ### Сохранение id исполнителя списка задач исполнителей
        if r.has_key("action") and rg("action") == 'workertask-worker':
            worker_id = request.GET["worker"]

            if worker_id != "":
                request.session['user_id'] = int(worker_id, 10)
            elif worker_id == "" and request.session.has_key('user_id'):
                del request.session['user_id']


            response_data = {"result": "ok"}




        ### Информация об отказе или проблеме (получение данных)
        if r.has_key("action") and rg("action") == 'stage-get-problem':
            row_id = int(request.GET["row_id"], 10)
            stage = proj_stages.objects.get(pk=row_id)

            response_data = {"result": "ok", "comment": stage.problem["comment"], "problem": 1 if stage.problem["problem"] == True else 0 }




        ### Реестр проектов : список загруженных в hdfs файлов
        if r.has_key("action") and rg("action") == 'get-reestrproj-hdfs-files':
            reestrproj_id = request.GET["reestrproj_id"]
            reestrproj = reestr_proj.objects.get(pk=int(reestrproj_id, 10))
            datafiles = []
            for row in reestr_proj_files.objects.filter(reestr_proj=reestrproj).order_by("-datetime_load"):
                datafiles.append({
                    "file_id": row.id,
                    "filename": row.filename,
                    "filetype": row.doctype.name if row.doctype else "",
                    "checked": 1 if row.checked else 0,
                    "user": row.user.get_full_name(),
                    "date": row.datetime_load.strftime("%d.%m.%Y")
                })

            response_data = {"result": "ok", "data": datafiles }






        ### Реестр проектов удаление вложеного файла
        if r.has_key("action") and rg("action") == 'reestrproj-hdfs-delete-file':
            file_id = request.GET["file_id"]

            rpf = reestr_proj_files.objects.get(pk=file_id)
            reestrproj = rpf.reestr_proj
            filename = rpf.filename
            rpf.delete()

            client = Client('10.6.0.135', 9000)
            for x in client.delete(['/projects/%s' % file_id,], recurse=True):
                print x


            reestr_proj_comment.objects.create(
                reestr_proj = reestrproj,
                user = request.user,
                comment = u"Удален документ %s" % filename
            )



            response_data = { "result": "ok" }





        ### Реестр проектов отметка об проверки вложеного файла
        if r.has_key("action") and rg("action") == 'reestrproj-doc-check-file':
            file_id = request.GET["file_id"]

            fp = reestr_proj_files.objects.get(pk=file_id)
            fp.checked = True if request.GET["checked"] == "yes" else False
            fp.save()

            ### Запись коментария
            reestr_proj_comment.objects.create(
                reestr_proj = fp.reestr_proj,
                comment = u"Документ {filename}: {check}".format(filename=fp.filename, check=u"установлена отметка проверено" if request.GET["checked"] == "yes" else u"снята отметка проверено" ),
                user = request.user
            )

            response_data = { "result": "ok" }





        ### Реестр проектов: список коментариев
        if r.has_key("action") and rg("action") == 'get-reestrproj-list-comments':
            reestrproj_id = request.GET["reestrproj_id"]
            reestrproj = reestr_proj.objects.get(pk=int(reestrproj_id, 10))
            comment_list = []
            for row in reestr_proj_comment.objects.filter(reestr_proj=reestrproj).order_by("-datetime_create"):
                comment_list.append({
                    "comment": row.comment,
                    "user": row.user.get_full_name(),
                    "date": row.datetime_create.strftime("%d.%m.%Y")
                })


            response_data = {"result": "ok", "data": comment_list }





        ### Установка стадии реестра проекта
        if r.has_key("action") and rg("action") == 'reestrproj-stage-add':
            reestrproj_id = request.GET["reestrproj_id"]
            stage_id = request.GET["stage"]
            stage = stages_list.objects.get(pk=int(stage_id, 10))
            reestrproj = reestr_proj.objects.get(pk=int(reestrproj_id, 10))

            if reestrproj.stage == stage:
                response_data = {"result": "error"}
            else:
                reestrproj.stage = stage
                reestrproj.save()

                stages_history.objects.create(
                    reestr_proj = reestrproj,
                    stage = stage,
                    user = request.user

                )


                response_data = {"result": "ok"}





        ### Реестр проектов: список стадий
        if r.has_key("action") and rg("action") == 'get-reestrproj-list-stages':
            reestrproj_id = request.GET["reestrproj_id"]
            reestrproj = reestr_proj.objects.get(pk=int(reestrproj_id, 10))
            stage_list = []
            for row in stages_history.objects.filter(reestr_proj=reestrproj).order_by("-datetime_create"):
                stage_list.append({
                    "stage": row.stage.getfullname(),
                    "user": row.user.get_full_name(),
                    "date": row.datetime_create.strftime("%d.%m.%Y")
                })


            response_data = {"result": "ok", "data": stage_list }




        ### Реестр проектов: исполнителей и дат
        if r.has_key("action") and rg("action") == 'get-reestrproj-list-tasks':
            reestrproj_id = request.GET["reestrproj_id"]
            reestrproj = reestr_proj.objects.get(pk=int(reestrproj_id, 10))
            task_list = []
            for row in reestr_proj_exec_date.objects.filter(reestr_proj=reestrproj).order_by("-datetime_edit"):
                task_list.append({
                    "id": row.id,
                    "stage": row.stage.getfullname(),
                    "user": row.user.get_full_name(),
                    "date1": row.date1.strftime("%d.%m.%Y") if row.date1 else "",
                    "date2": row.date2.strftime("%d.%m.%Y") if row.date2 else "",
                    "date3": row.datetime_edit.strftime("%d.%m.%Y"),
                    "worker" : row.worker.get_full_name() if row.worker else "",
                    "block": row.block.name if row.block else ""
                })


            response_data = {"result": "ok", "data": task_list }




        ### Реестр проектов: таблица excel
        if r.has_key("action") and rg("action") == 'get-reestrproj-table-excel':
            reestrproj_id = request.GET["reestrproj_id"]
            reestrproj = reestr_proj.objects.get(pk=int(reestrproj_id, 10))
            data = reestrproj.data
            if data.has_key('excel'):
                response_data = {"result": "ok", "table": data["excel"]}
            else:
                response_data = {"result": "empty"}





        ### Отображение формы с данными при элемента исполнители и даты реестра проектов
        if r.has_key("action") and rg("action") == 'reestrproj-task-edit':
            task_id = request.GET["task-id"]
            task = reestr_proj_exec_date.objects.get(pk=int(task_id, 10))
            form = WorkersDatesStagesForm(instance=task)
            t = template.Template("{{ form.as_p }}")
            c = template.Context({'form': form})
            f = t.render(c)

            response_data = {"result": "ok", "task-id": task_id, "form": f }




        ### Удаление элемента исполнители и даты реестра проектов
        if r.has_key("action") and rg("action") == 'reestrproj-task-delete':
            task_id = request.GET["task_id"]
            task = reestr_proj_exec_date.objects.get(pk=int(task_id, 10))
            reestrproj = task.reestr_proj
            task_stage = task.stage.name if task.stage else ""
            task.delete()

            reestr_proj_comment.objects.create(
                reestr_proj = task.reestr_proj,
                user = request.user,
                comment = u"Удален элемент исполнителей и дат %s" % task_stage
            )


            response_data = {"result": "ok"}





        ### Реестр проектов: список ссылок
        if r.has_key("action") and rg("action") == 'get-reestrproj-list-links':
            reestrproj_id = request.GET["reestrproj_id"]
            reestrproj = reestr_proj.objects.get(pk=int(reestrproj_id, 10))
            link_list = []
            data = reestrproj.data
            if data.has_key('link'):
                for row in data['link']:
                    link_list.append({
                        'id':row['id'],
                        'link':row['link'],
                        'comment':row['comment']
                    })


            response_data = {"result": "ok", "data": link_list }





        ### Удаление ссылки реестра проектов
        if r.has_key("action") and rg("action") == 'reestrproj-link-delete':
            row_id = request.GET["row-id"]
            reestrproj_id = request.GET["reestrproj_id"]
            reestrproj = reestr_proj.objects.get(pk=int(reestrproj_id, 10))

            link = ""

            data = reestrproj.data
            for row in data["link"]:
                if row['id'] == int(row_id,10):
                    link = row["link"]
                    data["link"].remove(row)

            reestr_proj_comment.objects.create(
                reestr_proj = reestrproj,
                user = request.user,
                comment = u"Удаление ссылки %s" % link
            )


            reestrproj.data = data
            reestrproj.save()

            response_data = {"result": "ok"}




        ### Добавление в адресный перечень
        if r.has_key("action") and rg("action") == 'reestrproj-address-add':
            reestrproj_id = request.GET["reestrproj_id"]
            reestrproj = reestr_proj.objects.get(pk=int(reestrproj_id, 10))
            address_id = request.GET["address_id"]
            address = address_house.objects.get(pk=int(address_id))
            addr = address.getaddress()

            data = reestrproj.data
            if data.has_key('address'):
                data['address'].append({
                    'address_id': address.id,
                    'city': address.city.name if address.city else "",
                    'street': address.street.name if address.street else "",
                    'house': address.house if address.house else ""
                })
            else:
                data['address'] = [{
                    'address_id': address.id,
                    'city': address.city.name,
                    'street': address.street.name if address.street else "",
                    'house': address.house if address.house else ""
                }]


            reestr_proj_comment.objects.create(
                reestr_proj = reestrproj,
                user = request.user,
                comment = u"Добавлен адрес %s" % addr
            )


            reestrproj.data = data
            reestrproj.save()


            response_data = {"result": "ok"}





        ### Адресный перечень
        if r.has_key("action") and rg("action") == 'get-reestrproj-list-address':
            reestrproj_id = request.GET["reestrproj_id"]
            reestrproj = reestr_proj.objects.get(pk=int(reestrproj_id, 10))

            address_list = []
            data = reestrproj.data
            if data.has_key('address'):
                for row in data['address']:
                    address_list.append({
                        'address_id':row['address_id'],
                        'city':row['city'],
                        'street':row['street'],
                        'house': row['house']
                    })



            response_data = {"result": "ok", "data": address_list }





        ### Удаление элемента из адресного перечня реестра проектов
        if r.has_key("action") and rg("action") == 'reestrproj-address-delete':
            row_id = request.GET["row-id"]
            reestrproj_id = request.GET["reestrproj_id"]
            reestrproj = reestr_proj.objects.get(pk=int(reestrproj_id, 10))

            addr = ""

            data = reestrproj.data
            for row in data["address"]:
                if row['address_id'] == int(row_id,10):
                    addr = u"{city} {street} {house}".format(city=row["city"],street=row["street"],house=row["house"])
                    data["address"].remove(row)


            reestr_proj_comment.objects.create(
                reestr_proj = reestrproj,
                user = request.user,
                comment = u"Удален адрес %s" % addr
            )



            reestrproj.data = data
            reestrproj.save()

            response_data = {"result": "ok"}





        ### Префикс инициатора проекта реестра проектов
        if r.has_key("action") and rg("action") == 'reestrproj-init-pref':
            init_id = request.GET["init_id"]
            init_ob = init_reestr_proj.objects.get(pk=int(init_id, 10))

            response_data = {"pref": init_ob.pref }





        ### Определение номера тома дочернего элемента реестра проектов
        if r.has_key("action") and rg("action") == 'reestrproj-child-level':
            reestrproj_id = request.GET["reestrproj_id"]
            reestrproj = reestr_proj.objects.get(pk=int(reestrproj_id, 10))
            level = 1
            for item in reestr_proj.objects.filter(main_proj=reestrproj):
                if int(item.proj_level,10) >= level:
                    level = int(item.proj_level,10) + 1

            response_data = {"level": ("0%s" % level)[:2] }





        ### Реестр проектов: Список дочерних проектов
        if r.has_key("action") and rg("action") == 'get-reestrproj-list-children':
            reestrproj_id = request.GET["reestrproj_id"]
            reestrproj = reestr_proj.objects.get(pk=int(reestrproj_id, 10))
            child_list = []
            for row in reestr_proj.objects.filter(main_proj=reestrproj).order_by("proj_level"):
                child_list.append({
                    "id": row.id,
                    "kod": row.proj_kod,
                    "level": row.proj_level,
                    "name": row.proj_name,
                    "stage": row.stage.name if row.stage else "",
                    "author": row.author.get_full_name(),
                    "create": row.date_create.strftime("%d.%m.%Y") if row.date_create else ""
                })


            response_data = {"result": "ok", "data": child_list }






        ### Реестр проектов: поиск
        if r.has_key("action") and rg("action") == 'reestrproj-list-search':
            search = request.GET["search"].strip()

            if search == "" and request.session.has_key("search_text"):
                del request.session["search_text"]
            else:
                request.session["search_text"] = search


            response_data = {"result": "ok"}





        ### Реестр проектов: Добавление кода связи с другими системами
        if r.has_key("action") and rg("action") == 'reestrproj-other-system-add':
            reestrproj_id = request.GET["reestrproj_id"]
            reestrproj = reestr_proj.objects.get(pk=int(reestrproj_id, 10))
            other_system = proj_other_system.objects.get(pk=int(request.GET["system_id"],10))
            other_code = request.GET["system_code"].strip()

            if reestrproj.data.has_key("other_system"):
                reestrproj.data["other_system"].append({"id": str(uuid.uuid4()), "other_id": other_system.id, "other_name": other_system.name, "other_code": other_code})
            else:
                reestrproj.data["other_system"] = [{"id": str(uuid.uuid4()), "other_id": other_system.id, "other_name": other_system.name, "other_code": other_code}]

            reestrproj.save()

            reestr_proj_comment.objects.create(
                reestr_proj = reestrproj,
                user = request.user,
                comment = u"Добавлена связь с другой системой {system} {code}".format(system=other_system.name,code=other_code)
            )


            response_data = {"result": "ok"}





        ### Реестр проектов: Получение списка связи с другими системами
        if r.has_key("action") and rg("action") == 'reestrproj-other-system-list':
            reestrproj_id = request.GET["reestrproj_id"]
            reestrproj = reestr_proj.objects.get(pk=int(reestrproj_id, 10))
            system_list = []
            if reestrproj.data.has_key("other_system"):
                for item in reestrproj.data["other_system"]:
                    system_list.append({
                        'id':item['id'],
                        'other_name':item['other_name'],
                        'other_code':item['other_code']
                    })

            response_data = {"result": "ok", "system": system_list}




        ### Реестр проектов: Удаление элемента связи с другими системами
        if r.has_key("action") and rg("action") == 'reestrproj-other-system-delete':
            reestrproj_id = request.GET["reestrproj_id"]
            reestrproj = reestr_proj.objects.get(pk=int(reestrproj_id, 10))
            system_id = request.GET["row-id"]

            for item in reestrproj.data["other_system"]:
                if item["id"] == system_id:

                    reestr_proj_comment.objects.create(
                        reestr_proj=reestrproj,
                        user=request.user,
                        comment=u"Удалена связь с другой системой {system} {code}".format(system=item["other_name"], code=item["other_code"])
                    )

                    reestrproj.data["other_system"].remove(item)
                    reestrproj.save()




            response_data = {"result": "ok"}





        ### Реестр проектов: Отправка оповещения
        if r.has_key("action") and rg("action") == 'reestrproj-message-send':
            reestrproj_id = request.GET["reestrproj_id"]
            reestrproj = reestr_proj.objects.get(pk=int(reestrproj_id, 10))
            mess = message_type.objects.get(pk=int(request.GET["message_type"],10))

            if send_reestr_proj(mess,reestrproj,request.user) == "ok":

                reestr_proj_messages_history.objects.create(
                    message_type=mess,
                    reestr_proj=reestrproj,
                    user=request.user,
                    emails=mess.email
                )


                response_data = {"result": "ok"}

            else:

                response_data = {"result": "error"}





        ### Реестр проектов: Получение списка истории отправки оповещений
        if r.has_key("action") and rg("action") == 'reestrproj-message-list':
            reestrproj_id = request.GET["reestrproj_id"]
            reestrproj = reestr_proj.objects.get(pk=int(reestrproj_id, 10))
            message_list = []
            for item in reestr_proj_messages_history.objects.filter(reestr_proj=reestrproj).order_by('-datetime_create'):
                message_list.append({
                    'message_type':item.message_type.name,
                    'date':item.datetime_create.strftime("%d.%m.%Y") if item.datetime_create else "",
                    'emails':item.emails,
                    'user': item.user.get_full_name(),
                })

            response_data = {"result": "ok", "messages": message_list}








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
                    stage_order=stage['order'],
                    name= stage["name"],
                    proj= p,
                    days= stage["days"] if stage.has_key("days") else None,
                    depend_on = {'stages': stage["depend_on"]}
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

            ### Вычисление пунктов исполнения
            rows = s.proj.make_dict()
            G = s.proj.make_graph(rows)
            G = s.proj.graph_edge_order(G, rows)
            actions = s.proj.actions(G)


            ### Если этот этап - заголовок или ссылается на заголовок - зависимость затираем
            if s.depend_on != {'stages':[]} and s.id not in actions:
                s.depend_on = {'stages':[]}
                s.save()
            if s.depend_on != {'stages':[]}:
                for dep in proj_stages.objects.filter(proj=s.proj, stage_order=s.depend_on['stages']):
                    if dep.id not in actions:
                        s.depend_on = {'stages': []}
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

            stage = proj_stages.objects.create(
                name=name,
                stage_order=order,
                days=days,
                deferment=deferment,
                depend_on={"stages": depend_on},
                proj=p
            )

            ### Вычисление пунктов исполнения
            rows = p.make_dict()
            G = p.make_graph(rows)
            G = p.graph_edge_order(G, rows)
            actions = p.actions(G)

            if stage.depend_on != {'stages':[]} and stage.id not in actions:
                stage.depend_on = {'stages':[]}
                stage.save()
            if stage.depend_on != {'stages':[]}:
                for dep in proj_stages.objects.filter(proj=p, stage_order=stage.depend_on['stages']):
                    if dep.id not in actions:
                        stage.depend_on = {'stages': []}
                        stage.save()



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
            note = data["note"]

            stage = proj_stages.objects.get(pk=row_id)
            proj_notes.objects.create(
                author=request.user,
                note=note,
                stage=stage
            )


            response_data = {"result": "ok"}





        ### Отметка отказа или проблемы
        if data.has_key("action") and data["action"] == 'stage-set-problem':
            row_id = int(data["row_id"], 10)
            problem = data["problem"]
            comment = data["comment"].strip()
            stage = proj_stages.objects.get(pk=row_id)

            stage.problem = {"problem": True if problem == 1 else False, "comment": comment}
            stage.save()

            ### Запись в лог файл
            logger_proj.info(u"Проект: {proj} - {stage} {user} отметил проблему".format(
                proj=stage.proj.name,
                stage=stage.name,
                user=request.user.get_username())
            )

            send_problem(stage)

            response_data = {"result": "ok"}







        ### Создание дочернего реестра - проекта
        if data.has_key("action") and data["action"] == 'reestrproj-create-child':

            reestrproj_id = data["reestrproj_id"]
            reestrproj = reestr_proj.objects.get(pk=int(reestrproj_id, 10))


            name = data["name"].strip()
            level = data["level"].strip()

            proj_kod = reestrproj.proj_kod.split("/")
            proj_kod[3] = level
            proj_kod = "/".join(proj_kod)

            rp = reestr_proj.objects.create(
                main_proj = reestrproj,
                proj_kod = proj_kod,
                proj_name = name,
                proj_other = reestrproj.proj_other,
                proj_level = level,
                stage = reestrproj.stage,
                proj_init = reestrproj.proj_init,
                business = reestrproj.business,
                executor = reestrproj.executor,
                author = request.user
            )


            reestr_proj_comment.objects.create(
                reestr_proj = reestrproj,
                user = request.user,
                comment = "Создан дочерний элемент %s" % name
            )


            response_data = {"result": "ok"}








        ### Создание нового реестра - проекта
        if data.has_key("action") and data["action"] == 'reestrproj-create':


            name = data["name"].strip()


            rand = random.randint(11111111,99999999)
            proj_kod = u"/{rand}/000000/00".format(rand=rand)

            rp = reestr_proj.objects.create(
                proj_kod = proj_kod,
                proj_name = name,
                proj_other = "000000",
                proj_level = "00",
                proj_init = None,
                business = None,
                executor = None,
                author = request.user
            )

            response_data = {"result": "ok", "id": rp.id}






        ### Сохранение карточки реестра - проекта
        if data.has_key("action") and data["action"] == 'reestrproj-common-save':

            reestrproj_id = data["reestrproj_id"]
            reestrproj = reestr_proj.objects.get(pk=int(reestrproj_id, 10))


            name = data["name"].strip()
            other = data["other"].strip()
            comment = data["comment"].strip()
            contragent = data["contragent"].strip()


            proj_init = None if data["proj_init"] == "" else init_reestr_proj.objects.get(pk=int(data["proj_init"],10))
            executor = None if data["executor"] == "" else address_companies.objects.get(pk=int(data["executor"],10))
            business_ob = None if data["business"] == "" else business.objects.get(pk=int(data["business"],10))
            rates_ob = None if data["rates"] == "" else rates.objects.get(pk=int(data["rates"],10))
            passing_ob = None if data["passing"] == "" else passing.objects.get(pk=int(data["passing"], 10))

            service_date = None if data["service"] == "" else datetime.datetime.strptime(data["service"],"%d.%m.%Y")

            reestrproj.proj_kod = data["proj_kod"].strip()
            reestrproj.proj_name = name
            reestrproj.proj_other = other
            reestrproj.comment = comment
            reestrproj.contragent = contragent

            reestrproj.business = business_ob
            reestrproj.executor = executor
            reestrproj.proj_init = proj_init

            reestrproj.passing = passing_ob
            reestrproj.rates = rates_ob

            reestrproj.date_service = service_date

            reestrproj.save()

            reestr_proj_comment.objects.create(
                reestr_proj = reestrproj,
                user = request.user,
                comment = u"Сохранены данные карточки проекта"
            )


            ### Формирование индекса поиска
            reestrproj.create_search_index()


            response_data = {"result": "ok"}







        ### Добавление коментария реестра проекта
        if data.has_key("action") and data["action"] == 'reestrproj-comment-add':
            reestrproj_id = data["reestrproj_id"]
            comment = data["comment"].strip()

            if comment != "":

                reestrproj = reestr_proj.objects.get(pk=int(reestrproj_id,10))

                reestr_proj_comment.objects.create(
                    reestr_proj = reestrproj,
                    user = request.user,
                    comment = comment
                )

            response_data = {"result": "ok"}






        ### Создание элемента исполнителей и дат в реестре проекта
        if data.has_key("action") and data["action"] == 'reestrproj-task-create':
            reestrproj_id = data["reestrproj_id"]
            stage = None if data["stage"] == "" else stages_list.objects.get(pk=int(data["stage"],10))
            worker = None if data["worker"] == "" else User.objects.get(pk=int(data["worker"],10))
            date1 = None if data["date1"].strip() == "" else datetime.datetime.strptime(data["date1"],"%d.%m.%Y")
            date2 = None if data["date2"].strip() == "" else datetime.datetime.strptime(data["date2"],"%d.%m.%Y")
            block_ob = None if data["block"].strip() == "" else blocks.objects.get(pk=int(data["block"],10))
            reestrproj = reestr_proj.objects.get(pk=int(reestrproj_id, 10))

            reestr_proj_exec_date.objects.create(
                reestr_proj=reestrproj,
                user=request.user,
                date1 = date1,
                date2 = date2,
                stage = stage,
                worker = worker,
                block = block_ob
            )



            response_data = {"result": "ok"}






        ### Изменение элемента исполнителей и дат в реестре проекта
        if data.has_key("action") and data["action"] == 'reestrproj-task-edit':
            stage = None if data["stage"] == "" else stages_list.objects.get(pk=int(data["stage"],10))
            worker = None if data["worker"] == "" else User.objects.get(pk=int(data["worker"],10))
            date1 = None if data["date1"].strip() == "" else datetime.datetime.strptime(data["date1"],"%d.%m.%Y")
            date2 = None if data["date2"].strip() == "" else datetime.datetime.strptime(data["date2"],"%d.%m.%Y")
            block_ob = None if data["block"].strip() == "" else blocks.objects.get(pk=int(data["block"],10))
            task = reestr_proj_exec_date.objects.get(pk=int(data["task_id"],10))

            task.user=request.user
            task.date1 = date1
            task.date2 = date2
            task.stage = stage
            task.worker = worker
            task.block = block_ob
            task.save()

            reestr_proj_comment.objects.create(
                reestr_proj = task.reestr_proj,
                user = request.user,
                comment = u"Изменен элемент исполнителей и дат %s" % task.stage.name if task.stage else ""
            )



            response_data = {"result": "ok"}





        ### Добавление ссылки в реестре проекта
        if data.has_key("action") and data["action"] == 'reestrproj-link-add':
            reestrproj_id = data["reestrproj_id"]
            reestrproj = reestr_proj.objects.get(pk=int(reestrproj_id, 10))
            link = data["link"].strip()
            comment = data["comment"].strip()

            data = reestrproj.data
            if data.has_key("link"):
                data["link"].append({
                    'id': int(time.time()),
                    'link': link,
                    'comment': comment
                })
            else:
                data["link"] = [{'id':int(time.time()),'link':link, 'comment':comment}]


            reestr_proj_comment.objects.create(
                reestr_proj = reestrproj,
                user = request.user,
                comment = u"Добавлена ссылка %s" % link
            )


            reestrproj.data = data
            reestrproj.save()

            response_data = {"result": "ok"}






    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response
