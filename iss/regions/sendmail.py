#coding:utf-8

from django.core.mail import EmailMessage

from iss.regions.models import proj_stages



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
                from_email='GAMMA <gamma@sibttk.ru>',
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
            from_email='GAMMA <gamma@sibttk.ru>',
            to=[worker.email,]
        )

        email.content_subtype = "html"
        email.send()


    return "ok"