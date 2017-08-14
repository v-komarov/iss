#coding:utf-8

from django.core.mail import EmailMessage

from iss.regions.models import proj_stages, proj_steps



### Отправка сообщения очередному исполнителю этапа или шага проекта
def send_proj_worker(row_type,row_id, worker):

    ### Отправляется информация при отметке об выполнении

    if row_type == "stage":
        row = proj_stages.objects.get(pk=row_id)


        ### Определение этапа, зависимого от этого
        p = row.proj # Проект
        ###По всем этапам проекта
        for stage in p.proj_stages_set.all():
            if stage != row and row.order in stage.depend_on["stages"]:
                ### Определение выполенны ли пункты

                ### Изначально все пункты выполнены
                done = True
                for item in stage.depend_on["stages"]:
                    for a in p.proj_stages_set.filter(order=item):
                        if a.done == False:
                            done = False

                ### Если пункт можно выполнять
                if done == True:
                    ### Определение первого или первых шагов к выполнению внутри этапа
                    for step in stage.proj_steps_set.all():
                        if step.depend_on["steps"] == []:
                            for w in step.workers.all():
                                if worker != w and w.email != "":
                                    #workers.append(w)

                                    ### Отправка сообщений по каждому этапу, каждому пользователю
                                    email = EmailMessage(
                                        subject="Управление проектами http://10.6.0.22:8000",
                                        body=u"""
                                        <p>
                                        Прошу приступить к реализации пункта проекта<br>
                                        Проект: <b>{proj}</b><br>
                                        Пункт исполнения: <b>{name}</b><br>
                                        Срок выполнения: <b>{begin} - {end}</b>                
                                        </p>
                                        """.format(proj=p.name, name=step.name, begin=step.begin.strftime('%d.%m.%Y'),
                                                   end=step.end.strftime('%d.%m.%Y')),
                                        from_email='GAMMA <gamma@sibttk.ru>',
                                        to=[w.email, ]
                                    )

                                    email.content_subtype = "html"
                                    email.send()




    if row_type == "step":
        row = proj_steps.objects.get(pk=row_id)
        stage = row.stage
        p = stage.proj

        ### Обход шагов
        for step in stage.proj_steps_set.all():
            if step != row and row.order in step.depend_on["steps"]:
                ### Определение выполенны ли пункты
                ### Изначально все пункты выполнены
                done = True
                for item in step.depend_on["steps"]:
                    for a in stage.proj_steps_set.filter(order=item):
                        if a.done == False:
                            done = False

                ### Если пункт можно выполнять
                if done == True:
                    for w in step.workers.all():
                        if worker != w and w.email != "":

                            ### Отправка сообщений по каждому шагу, каждому пользователю
                            email = EmailMessage(
                                subject="Управление проектами http://10.6.0.22:8000",
                                body=u"""
                                <p>
                                Прошу приступить к реализации пункта проекта<br>
                                Проект: <b>{proj}</b><br>
                                Пункт исполнения: <b>{name}</b><br>
                                Срок выполнения: <b>{begin} - {end}</b>                
                                </p>
                                """.format(proj=p.name, name=step.name, begin=step.begin.strftime('%d.%m.%Y'),
                                           end=step.end.strftime('%d.%m.%Y')),
                                from_email='GAMMA <gamma@sibttk.ru>',
                                to=[w.email, ]
                            )

                            email.content_subtype = "html"
                            email.send()




    return "ok"






### Отправка сообщения первым исполнителям при начале проекта (при выборе и определении ответственного исполнителя)
def send_proj_worker2(row_type,row_id,worker):


    if row_type == "stage":
        row = proj_stages.objects.get(pk=row_id)
        depend_on = row.depend_on["stages"]
        proj = row.proj
        name = row.name

    if row_type == "step":
        row = proj_steps.objects.get(pk=row_id)
        depend_on = row.depend_on["steps"]
        proj = row.stage.proj
        name = row.name


    ### Отправка для независимых пунктов
    if ((row_type == "stage" and depend_on == []) or (row_type == "step" and depend_on == [] and row.stage.depend_on["stages"] == [])) and worker.email != "":

        ### Если этап иди шаг без зависимости - отправляем сообщение
        email = EmailMessage(
            subject="Управление проектами http://10.6.0.22:8000",
            body=u"""
            <p>
            Вы определены как исполнитель пункта проекта<br>
            Проект: <b>{proj}</b><br>
            Пункт исполнения: <b>{name}</b><br>
            Срок выполнения: <b>{begin} - {end}</b>                
            </p>
            """.format(proj=proj.name, name=name, begin=row.begin.strftime('%d.%m.%Y'), end=row.end.strftime('%d.%m.%Y')),
            from_email='GAMMA <gamma@sibttk.ru>',
            to=[worker.email,]
        )

        email.content_subtype = "html"
        email.send()


    return "ok"