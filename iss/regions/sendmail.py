#coding:utf-8

from django.core.mail import EmailMessage

from iss.regions.models import proj_stages

import logging

#logger = logging.getLogger(__name__)
#logging.basicConfig(filename='/srv/django/iss/log/projects.log',level=logging.DEBUG)




### Отправка сообщения очередным исполнитям этапа
def send_proj_worker(stages, worker):

    for stage in stages:

    ### Отправляется информация при отметке об выполнении
        for worker in stage.workers.all():


            ### Отправка сообщений по каждому этапу, каждому пользователю
            email = EmailMessage(
                subject="Управление проектами",
                body=u"""
                <a href='http://10.6.0.22:8000/regions/proj/edit/{proj_id}/'>http://10.6.0.22:8000/</a>
                <p>
                Предыдущий пункт {last_worker} отметил как выполненный<br>
                Прошу приступить к реализации пункта проекта<br>
                Проект: <b>{proj}</b><br>
                Пункт исполнения: <b>{name}</b><br>
                Срок выполнения: <b>{begin} - {end}</b>                
                </p>
                """.format(proj=stage.proj.name, name=stage.name, begin=stage.begin.strftime('%d.%m.%Y'),
                           end=stage.end.strftime('%d.%m.%Y'), proj_id=stage.proj.id, last_worker=worker.get_full_name()),
                from_email='GAMMA <gamma@baikal-ttk.ru>',
                to=[worker.email, ]
            )

            email.content_subtype = "html"
            email.send()








    return "ok"






### Отправка сообщения первым исполнителям при начале проекта (при выборе и определении ответственного исполнителя)
def send_proj_worker2(row_id,worker):


    row = proj_stages.objects.get(pk=row_id)
    depend_on = row.depend_on["stages"]
    proj = row.proj
    name = row.name



    ### Отправка для независимых пунктов
    if depend_on == [] and worker.email != "":

        ### Если этап иди шаг без зависимости - отправляем сообщение
        email = EmailMessage(
            subject="Управление проектами",
            body=u"""
            <a href='http://10.6.0.22:8000/regions/proj/edit/{proj_id}/'>http://10.6.0.22:8000/</a>
            <p>
            Вы определены как исполнитель пункта проекта<br>
            Проект: <b>{proj}</b><br>
            Пункт исполнения: <b>{name}</b><br>
            Срок выполнения: <b>{begin} - {end}</b>                
            </p>
            """.format(proj=proj.name, name=name, begin=row.begin.strftime('%d.%m.%Y'), end=row.end.strftime('%d.%m.%Y'), proj_id=proj.id),
            from_email='GAMMA <gamma@baikal-ttk.ru>',
            to=[worker.email,]
        )

        email.content_subtype = "html"
        email.send()


    return "ok"




### Отправка сообщения об отметки проблемы
def send_problem(stage):

    p = stage.proj

    if p.author.email != "":

        act = u"Отметка об установки проблемы или отказа" if stage.problem["problem"] == True else u"Снятие отметки об проблеме или отказе"

        email = EmailMessage(
            subject="Управление проектами",
            body=u"""
            <a href='http://10.6.0.22:8000/regions/proj/edit/{proj_id}/'>http://10.6.0.22:8000/</a>
            <p>
            {act}<br>
            Проект: <b>{proj}</b><br>
            Пункт исполнения: <b>{name}</b><br>
            Срок выполнения: <b>{begin} - {end}</b>                
            </p>
            """.format(act=act, proj=p.name, name=stage.name, begin=stage.begin.strftime('%d.%m.%Y'), end=stage.end.strftime('%d.%m.%Y'), proj_id=p.id),
            from_email='GAMMA <gamma@baikal-ttk.ru>',
            to=[p.author.email,]
        )

        email.content_subtype = "html"
        email.send()

    return "ok"




### Отправка оповещения из реестра проектов
def send_reestr_proj(mess,reestrproj,user):


    email = EmailMessage(
        subject="Реестр проектов [{mess_type}] {code} {name}".format(mess_type=mess.name.encode("utf-8"),code=reestrproj.proj_kod.encode("utf-8"),name=reestrproj.proj_name.encode("utf-8")),
        body=u"""
        <a href='http://10.6.0.22:8000/regions/reestrproj/edit/{id}/'>http://10.6.0.22:8000/</a>
        <p>
        Оповещение из карточки проекта
        {name}<br>
        Вид оповещения: {mess_type}<br>
        Оповещение отправил: {user}<br>
        </p>
        """.format(id=reestrproj.id, name=reestrproj.proj_name, mess_type=mess.name, user=user.get_full_name()),
        from_email='GAMMA <gamma@baikal-ttk.ru>',
        to=mess.email.split(";")
    )

    email.content_subtype = "html"
    email.send()

    return "ok"





### Отправка оповещения из реестра проектов об изменении назначенному исполнителю
def send_reestr_proj_work(task, action):

    reestrproj = task.reestr_proj

    if task.block==None:
        block_address = []
    elif task.block.email=="":
        block_address = []
    else:
        block_address = task.block.email.split(";")
    if task.worker==None:
        worker_address=[]
    elif task.worker.email=="":
        worker_address=[]
    else:
        worker_address = [task.worker.email]


    if worker_address != [] or block_address != []: # если указали ответвенного или группу, то нужно уведомление

 
        date1 = task.date1.strftime("%d.%m.%Y") if task.date1 else ""
        date2 = task.date2.strftime("%d.%m.%Y") if task.date2 else ""
        stage = task.stage.name if task.stage else ""

        if reestrproj.process == True:
            url = "<a href='http://10.6.0.22:8000/regions/processproj/edit/{id}/'>http://10.6.0.22:8000/</a>".format(id=task.reestr_proj_id)
        else:
            url = "<a href='http://10.6.0.22:8000/regions/reestrproj/edit/{id}/'>http://10.6.0.22:8000/</a>".format(id=task.reestr_proj_id)
 
        if block_address != []: # если указана группа, сплим по ;
            if action == "edit":

                email = EmailMessage(
                    subject="Реестр проектов {code} {name}".format(code=reestrproj.proj_kod.encode("utf-8"),name=reestrproj.proj_name.encode("utf-8")),
                    body=u"""
                    {url}
                    <p>
                    Оповещение: изменен этап "{stage}" проекта "{name}", по которому вы входите в ответственное подразделение
                    <br>
                    Начало этапа {date1}
                    <br>
                    Окончание этапа {date2}
                    <br>
                    </p>
                    """.format(url=url,id=reestrproj.id, name=reestrproj.proj_name, stage=stage, date1=date1, date2=date2),
                    from_email='GAMMA <gamma@baikal-ttk.ru>',
                    to=block_address
                )

            else:
                email = EmailMessage(
                    subject="Реестр проектов {code} {name}".format(code=reestrproj.proj_kod.encode("utf-8"),
                                                                   name=reestrproj.proj_name.encode("utf-8")),
                    body=u"""
                    {url}
                    <p>
                    Оповещение: вы входите в ответственное подразделение по реализации этапа "{stage}" проекта "{name}" 
                    <br>
                    Начало этапа {date1}
                    <br>
                    Окончание этапа {date2}
                    <br>
                    </p>
                    """.format(url=url, id=reestrproj.id, name=reestrproj.proj_name, stage=stage, date1=date1, date2=date2),
                    from_email='GAMMA <gamma@baikal-ttk.ru>',
                    to=block_address
                )
 
            email.content_subtype = "html"
            email.send()

        if worker_address != []: # если ответственный исполнитель
            if action == "edit":

                email = EmailMessage(
                    subject="Реестр проектов {code} {name}".format(code=reestrproj.proj_kod.encode("utf-8"),name=reestrproj.proj_name.encode("utf-8")),
                    body=u"""
                    {url}
                    <p>
                    Оповещение: изменен этап "{stage}" проекта "{name}", по которому вы назначены исполнителем 
                    <br>
                    Начало этапа {date1}
                    <br>
                    Окончание этапа {date2}
                    <br>
                    </p>
                    """.format(url=url,id=reestrproj.id, name=reestrproj.proj_name, stage=stage, date1=date1, date2=date2),
                    from_email='GAMMA <gamma@baikal-ttk.ru>',
                    to=worker_address
                )

            else:
                email = EmailMessage(
                    subject="Реестр проектов {code} {name}".format(code=reestrproj.proj_kod.encode("utf-8"),
                                                                   name=reestrproj.proj_name.encode("utf-8")),
                    body=u"""
                    {url}
                    <p>
                    Оповещение: вы назначены исполнителем этапа "{stage}" проекта "{name}" 
                    <br>
                    Начало этапа {date1}
                    <br>
                    Окончание этапа {date2}
                    <br>
                    </p>
                    """.format(url=url, id=reestrproj.id, name=reestrproj.proj_name, stage=stage, date1=date1, date2=date2),
                    from_email='GAMMA <gamma@baikal-ttk.ru>',
                    to=worker_address
                )
  
        email.content_subtype = "html"
        email.send()

        return "ok"

    else:
        return "error"


