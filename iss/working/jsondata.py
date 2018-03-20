#coding:utf-8

import json
import pickle
import datetime

import base64
from io import BytesIO

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rc


from pytz import timezone
from pprint import pformat

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login

from django.db.models import Count, Q, Avg, Sum
from django.contrib.auth.models import User




from iss.working.models import working_time, working_relax, marks, working_log, working_reports
from iss.monitor.models import Profile, avaya_log









def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip





### Определение пользователя по ip адресу
def get_ip_user(request):

    ip = get_client_ip(request)

    prof = Profile.objects.filter(ip=ip)

    if prof.exists():
        return prof.first().user
    else:
        return None








def get_json(request):

    response_data = {}

    if request.method == "GET":

        r = request.GET
        rg = request.GET.get


        ### Получение статусов пользователя
        if r.has_key("action") and rg("action") == 'get-statuses':

            user = request.user
            work = "yes" if user.profile.work_status else "no"
            relax = "yes" if user.profile.relax_status else "no"

            response_data = {"result": "ok", "work": work, "relax": relax}


        ### Начало работы (смены)
        if r.has_key("action") and rg("action") == 'work-start':

            user = request.user
            user.profile.work_status = True
            user.save()


            if not working_time.objects.filter(user=user,current=True).exists():
                ### Создание записи "Смены"
                working_time.objects.create(
                    user=user
                )

            response_data = { "result": "ok" }



        ### Завершение работы (смены)
        if r.has_key("action") and rg("action") == 'work-end':

            user = request.user
            user.profile.work_status = False
            user.save()

            if working_time.objects.filter(user=user,current=True).exists():
                ### Завершение работы (смены)
                current = working_time.objects.filter(current=True,user=user).last()
                current.current = False
                current.save()


            response_data = { "result": "ok" }



        ### Начало перерыва
        if r.has_key("action") and rg("action") == 'relax-start':

            user = request.user
            user.profile.relax_status = True
            user.save()

            if (not working_relax.objects.filter(user=user,current=True).exists()) and user.working_time_set.filter(current=True).exists():

                ### Создание перерыва
                working_relax.objects.create(
                    user=user,
                    working=user.working_time_set.filter(current=True).last()
                )

            response_data = { "result": "ok" }



        ### Завершение перерыва
        if r.has_key("action") and rg("action") == 'relax-end':

            user = request.user
            user.profile.relax_status = False
            user.save()

            if working_relax.objects.filter(user=user,current=True).exists() and user.working_time_set.filter(current=True).exists():
                ### Завершение перерыва
                for current in working_relax.objects.filter(current=True,user=user):
                    current.current = False
                    current.working = user.working_time_set.filter(current=True).last()
                    current.save()


            response_data = { "result": "ok" }



        ### Добавление действия - события
        if r.has_key("action") and rg("action") == 'plus-event':
            comment = request.GET["comment"].strip()
            mark_id = int(request.GET["mark_id"],10)
            mark = marks.objects.get(pk=mark_id)
            user = request.user
            if working_time.objects.filter(user=user,current=True).exists():
                wt = working_time.objects.filter(user=user,current=True).last()
                working_log.objects.create(
                    user=user,
                    mark=mark,
                    working=wt,
                    comment=comment

                )

                count = working_log.objects.filter(mark=mark,user=user,working=wt).count()

                response_data = { "result": "ok", "count": count, "mark_id": mark_id }
            else:
                response_data = { "result": "error" }




        ### Первоначальное отображение событий или действий в карточке
        if r.has_key("action") and rg("action") == 'showcount':
            user = request.user
            if working_time.objects.filter(user=user,current=True).exists():
                wt = working_time.objects.filter(user=user,current=True).last()

                items = working_log.objects.filter(working=wt).values('mark').annotate(count=Count('mark'))

                response_data = {"result": "ok", "items": eval(str(items))}
            else:
                response_data = {"result": "error"}




        ### Отметка строк смен для включения в отчет
        if r.has_key("action") and rg("action") == 'include-report-working':
            row_id = int(request.GET["row_id"],10)
            if request.session.has_key("include_report"):
                tmp = pickle.loads(request.session["include_report"])
                if not row_id in tmp:
                    tmp.append(row_id)
                    request.session["include_report"] = pickle.dumps(tmp)


            else:
                request.session["include_report"] = pickle.dumps([row_id])


            response_data = {"result": "ok"}




        ### Сенятие отметки строк смен для включения в отчет
        if r.has_key("action") and rg("action") == 'exclude-report-working':
            row_id = int(request.GET["row_id"], 10)
            if request.session.has_key("include_report"):
                tmp = pickle.loads(request.session["include_report"])
                if row_id in tmp:
                    tmp.remove(row_id)
                    request.session["include_report"] = pickle.dumps(tmp)


            response_data = {"result": "ok"}





        ### Отметка строк событий для включения в отчет
        if r.has_key("action") and rg("action") == 'include-report-event':
            row_id = int(request.GET["row_id"],10)
            evt = working_log.objects.get(pk=row_id)
            evt.visible = True
            evt.save()

            response_data = {"result": "ok"}




        ### Снятие отметки строк событий для включения в отчет
        if r.has_key("action") and rg("action") == 'exclude-report-event':
            row_id = int(request.GET["row_id"],10)
            evt = working_log.objects.get(pk=row_id)
            evt.visible = False
            evt.save()

            response_data = {"result": "ok"}




        ### Создание отчета
        if r.has_key("action") and rg("action") == 'create-report':
            name = request.GET["report_name"].strip()
            if request.session.has_key("include_report"):
                report_list = pickle.loads(request.session["include_report"])
                if len(report_list) > 0:

                    ### Первоначально
                    datetime_start = []
                    datetime_end = []
                    workers_count = set()
                    marks_list = {}
                    work_hour = 0
                    relax_min = 0
                    events_count = 0

                    for item in report_list:
                        work_time = working_time.objects.get(pk=item)
                        workers_count.add(work_time.user.id)
                        work_hour += work_time.get_work_hour()
                        relax_min += work_time.get_relax_min()
                        datetime_start.append(work_time.get_datetime_begin())
                        datetime_end.append(work_time.get_datetime_end())

                        for evt in work_time.working_log_set.filter(visible=True):
                            events_count += 1
                            if marks_list.has_key(evt.mark.name):
                                marks_list[evt.mark.name] += 1
                            else:
                                marks_list[evt.mark.name] = 1


                    ### Определение диапазона дат
                    datetime_start.sort()
                    datetime_start = datetime_start[0]
                    datetime_end.sort()
                    datetime_end = datetime_end[-1]

                    working_reports.objects.create(
                        name = name,
                        author = request.user,
                        datetime_begin = datetime_start,
                        datetime_end = datetime_end,
                        workers_count = len(workers_count),
                        events_count = events_count,
                        work_time = work_hour,
                        relax_time = relax_min,
                        data = marks_list

                    )

                    del request.session["include_report"]
                    response_data = {"result": "ok"}
                else:
                    response_data = {"result": "error"}


            else:
                response_data = {"result": "error"}








        ### Регистрация пользователя и ip адреса
        if r.has_key("action") and rg("action") == 'auth-desk-ip':
            ip = get_client_ip(request)
            username = request.GET["desktop_name"].strip()
            passwd = request.GET["desktop_passwd"].strip()
            phone = request.GET["desktop_phone"].strip()

            response_data = {"result": "error"}

            user = authenticate(username=username, password=passwd)
            if user is not None:
                if user.is_active:
                    login(request, user)

                    #### Регистрация ip адреса рабочей станции, номера телефона
                    Profile.objects.filter(ip=ip).update(ip=None)
                    prof = Profile.objects.filter(user=user).first()
                    prof.ip = ip
                    prof.phone = phone
                    prof.save()

                    work = "yes" if user.profile.work_status else "no"
                    relax = "yes" if user.profile.relax_status else "no"

                    ### Список доступных видов событий (действий)
                    evt_btn = []
                    for evt in marks.objects.filter(visible=True):
                        evt_btn.append(
                            {"id": evt.id, "name" : evt.name}
                        )

                    response_data = {"result": "ok", "work": work, "relax": relax, "user": user.get_full_name(), "evt_btn": evt_btn}






        ### Получение статусов пользователя для desktop (по ip адресу)
        if r.has_key("action") and rg("action") == 'get-desk-statuses':

            user = get_ip_user(request)

            if user:

                work = "yes" if user.profile.work_status else "no"
                relax = "yes" if user.profile.relax_status else "no"

                ### Список доступных видов событий (действий)
                evt_btn = []
                for evt in marks.objects.filter(visible=True):
                    evt_btn.append(
                        {"id": evt.id, "name" : evt.name}
                    )

                response_data = {"result": "ok", "work": work, "relax": relax, "user": user.get_full_name(), "evt_btn": evt_btn}

            else:

                response_data = {"result": "error"}





        ### Получение текущих данных пользователя для desktop (по ip адресу)
        if r.has_key("action") and rg("action") == 'get-desk-events':

            user = get_ip_user(request)

            if user:

                ### Определение активной сессии
                if working_time.objects.filter(user=user,current=True).exists():

                    ### текущая смена
                    wt = working_time.objects.filter(user=user,current=True).last()

                    tz = request.session['tz'] if request.session.has_key('tz') else 'UTC'
                    now = timezone(tz).localize(datetime.datetime.now())

                    ### длительность в минутах
                    dur = int((now - wt.datetime_begin).seconds / 60)

                    events = []
                    for s in working_log.objects.filter(working=wt).values('mark').annotate(Count('mark')):
                        events.append(s)

                    response_data = {"result": "ok", "dur": dur, "events": events}

                else:
                    response_data = {"result": "error"}

            else:
                response_data = {"result": "error"}



        ### Начало работы (смены) для desktop (по ip адресу)
        if r.has_key("action") and rg("action") == 'work-desk-start':

            user = get_ip_user(request)
            user.profile.work_status = True
            user.save()


            if not working_time.objects.filter(user=user,current=True).exists():
                ### Создание записи "Смены"
                working_time.objects.create(
                    user=user
                )

            response_data = { "result": "ok" }



        ### Завершение работы (смены) для desktop (по ip адресу)
        if r.has_key("action") and rg("action") == 'work-desk-end':

            user = get_ip_user(request)
            user.profile.work_status = False
            user.save()

            if working_time.objects.filter(user=user,current=True).exists():
                ### Завершение работы (смены)
                current = working_time.objects.filter(current=True,user=user).last()
                current.current = False
                current.save()


            response_data = { "result": "ok" }




        ### Начало перерыва для desktop (по ip адресу)
        if r.has_key("action") and rg("action") == 'relax-desk-start':

            user = get_ip_user(request)
            user.profile.relax_status = True
            user.save()


            if (not working_relax.objects.filter(user=user,current=True).exists()) and user.working_time_set.filter(current=True).exists():

                ### Создание перерыва
                working_relax.objects.create(
                    user=user,
                    working=user.working_time_set.filter(current=True).last()
                )

            response_data = { "result": "ok" }




        ### Завершение перерыва для desktop (по ip адресу)
        if r.has_key("action") and rg("action") == 'relax-desk-end':

            user = get_ip_user(request)
            user.profile.relax_status = False
            user.save()


            if working_relax.objects.filter(user=user,current=True).exists() and user.working_time_set.filter(current=True).exists():
                ### Завершение перерыва
                for current in working_relax.objects.filter(current=True,user=user):
                    current.current = False
                    current.working = user.working_time_set.filter(current=True).last()
                    current.save()

            response_data = { "result": "ok" }




        ### Отметка события для desktop (по ip адресу)
        if r.has_key("action") and rg("action") == 'evt-desk':

            user = get_ip_user(request)

            if user.profile.relax_status == False and user.profile.work_status == True:
                evtid = int(request.GET["evtid"], 10)
                mark = marks.objects.get(pk=evtid)
                if working_time.objects.filter(user=user,current=True).exists():
                    wt = working_time.objects.filter(user=user,current=True).last()
                    working_log.objects.create(
                        user=user,
                        mark=mark,
                        working=wt,
                        comment="desktop"

                    )

                    count = working_log.objects.filter(mark=mark,user=user,working=wt).count()
                    response_data = { "result": "ok", "name": mark.name, "count":count }

                else:
                    response_data = { "result": "error" }


            else:

                response_data = { "result": "error" }






        ### Формирование графика активности
        if r.has_key("action") and rg("action") == 'get-data-plot':

            ## Отображение кирилицы
            font = {'family': 'DejaVu Sans',
                    'weight': 'normal', 'size': 40}
            rc('font', **font)

            tz = request.session['tz'] if request.session.has_key('tz') else 'UTC'

            ### Данные из формы
            events = marks.objects.get(pk=int(request.GET["events"],10)) if request.GET["events"] != "" else None
            users = User.objects.get(pk=int(request.GET["users"],10)) if request.GET["users"] != "" else None

            date1 = timezone(tz).localize(datetime.datetime.strptime(request.GET["date1"].strip(), "%d.%m.%Y"))
            date2 = timezone(tz).localize(datetime.datetime.strptime(request.GET["date2"].strip(), "%d.%m.%Y"))

            date2 = date2 + datetime.timedelta(days=1)

            x = [] # значение по координатам
            y = [] # значение по координатам
            xl = [] ### метки

            history = {}
            history2 = {}

            if events == None and users == None:
                wl = working_log.objects.filter(datetime_create__gte=date1, datetime_create__lte=date2, visible=True)
            elif events != None and users == None:
                wl = working_log.objects.filter(datetime_create__gte=date1, datetime_create__lte=date2, visible=True, mark=events)
            elif events == None and users != None:
                wl = working_log.objects.filter(datetime_create__gte=date1, datetime_create__lte=date2, visible=True, user=users)
            else:
                wl = working_log.objects.filter(datetime_create__gte=date1, datetime_create__lte=date2, visible=True, user=users, mark=events)

            """
            Формирование словарей "строковое значение по датам или часам" и количество событий 
            """
            for a in wl:
                hour = a.datetime_create.astimezone(timezone(tz)).strftime("%d.%m.%Y %H")
                day = a.datetime_create.astimezone(timezone(tz)).strftime("%d.%m.%Y")
                if history.has_key(hour):
                    history[hour] += 1
                else:
                    history[hour] = 1
                if history2.has_key(day):
                    history2[day] += 1
                else:
                    history2[day] = 1

            """            
                Подготовка значений для графика            
            """
            date0 = date1
            while date0 < date2:
                x.append(date0)
                if (date2 - date1).days < 6: ### Если переиод 5 дней и меньше
                    if history.has_key(date0.strftime("%d.%m.%Y %H")):
                        y.append(history[date0.strftime("%d.%m.%Y %H")])
                    else:
                        y.append(0)
                    date0 = date0 + datetime.timedelta(hours=1)
                    xl.append(date0.strftime(u"%d.%m.%Y %H h"))
                else: # Если период более 5 дней
                    if history2.has_key(date0.strftime("%d.%m.%Y")):
                        y.append(history2[date0.strftime("%d.%m.%Y")])
                    else:
                        y.append(0)
                    xl.append(date0.strftime(u"%d.%m.%Y"))
                    date0 = date0 + datetime.timedelta(days=1)


            #plt.fill(x, y, zorder=10) # Рисование графика
            plt.plot(x,y, linewidth=12, color='b')
            plt.grid(True, zorder=5) # Сетка

            plt.xlim(date1, date2) # Крайние значения по х
            plt.xticks(x, xl, ha='left') # Наложение координат и меток по х

            ### Размер меток по координатам
            plt.xticks(fontsize=34, rotation=90)
            plt.yticks(fontsize=34)

            plt.ylabel(u'Количество событий') # Подпись координат

            figfile = BytesIO()
            fig = plt.gcf()
            fig.set_size_inches(60, 20)
            plt.subplots_adjust(bottom=0.2)
            plt.savefig(figfile, format='png')
            figfile.seek(0)

            ### Очистра !!!
            plt.gcf().clear()

            response_data = { "result": "ok" , "data": "data: image/png;base64,"+base64.b64encode(figfile.getvalue())}




        ### Формирование отчета из CDR логов
        if r.has_key("action") and rg("action") == 'phonequery':

            tz = request.session['tz'] if request.session.has_key('tz') else 'UTC'

            phones = request.GET["phones"].strip().split(",")
            filter = request.GET["filter"].strip()
            date1 = timezone(tz).localize(datetime.datetime.strptime(request.GET["date1"].strip(), "%d.%m.%Y")).replace(hour=0,minute=0,second=0)
            date2 = timezone(tz).localize(datetime.datetime.strptime(request.GET["date2"].strip(), "%d.%m.%Y")).replace(hour=23,minute=59,second=59)

            ### Ограничение выборки по дате
            data = avaya_log.objects.filter(datetime_call__gte=date1, datetime_call__lte=date2)

            ### Ограничение выборки по внутренним телефонам
            call_ac = []
            for ph in phones:
                call_ac.append(" Q(call_a='%s') | Q(call_c='%s') " % (ph,ph))

            data = eval("data.filter(%s)" % (" | ".join(call_ac)))

            ### Ограничение по фильтру , если есть
            if filter != "":
                data = data.filter(Q(call_a=filter) | Q(call_c=filter))


            ### Всего звонков
            calls = data.count()
            if calls == 0:
                response_data = {"result" : "zero"}
            else:
                ### Всего входяших
                calls_in = data.filter(in_out="I").count()
                ### Всего исходящих
                calls_out = data.filter(in_out="O").count()

                ### Исходящих принятых
                calls_out_ok = data.filter(in_out="O",duration__gt=0).count()

                ### Входящих принятых
                calls_in_ok = data.filter(in_out="I",duration__gt=0).count()


                ### Среднее время продолжительности разговора для входящих и исходящих
                calls_in_avg = int(data.filter(in_out="I",duration__gt=0).aggregate(Avg('duration'))["duration__avg"]) if data.filter(in_out="I",duration__gt=0).exists() else None
                calls_out_avg = int(data.filter(in_out="O",duration__gt=0).aggregate(Avg('duration'))["duration__avg"]) if data.filter(in_out="O",duration__gt=0).exists() else None

                response_data = { "result": "ok",
                                  "calls_total": calls,
                                  "calls_in": calls_in,
                                  "calls_out": calls_out,
                                  "calls_in_ok": calls_in_ok,
                                  "calls_out_ok": calls_out_ok,
                                  "calls_in_avg": calls_in_avg,
                                  "calls_out_avg": calls_out_avg,
                                  "calls_in_p": int(calls_in_ok * 100 / calls_in) if calls_in > 0 else 0,
                                  "calls_out_p": int(calls_out_ok * 100 / calls_out) if calls_out > 0 else 0,
                                  }





    if request.method == "POST":


        data = eval(request.body)



    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response


