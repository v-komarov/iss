#coding:utf8

import datetime
import iss.settings

from django.core.management.base import BaseCommand, CommandError


from iss.monitor.models import Profile
from iss.working.models import marks, working_time, working_log


### Входящие звонки
callin = marks.objects.get(pk=3)
### Исходящие звонки
callout = marks.objects.get(pk=4)




class Command(BaseCommand):
    args = '<log>'
    help = 'Загрузка звонков'



    def handle(self, *args, **options):



        cdr = args[0]
        #print cdr


        ### Отладка
        #if iss.settings.DEBUG == False:
        #    f = open("/srv/django/iss/log/calls.log","a")
        #    f.write(cdr.replace("_"," ")+"\n")
        #    f.close()


        """

        :param args:
        :param options:
        :return:
        """


        st = cdr.split(",")
        #print st
        call_a = st[3]
        call_c = st[6]
        call_b = st[5]
        comment = ""
        call_type = st[4]


        ### Для групповых номеров
        if call_type == "I" and call_b == "4888" and call_c == "2160410":
            call_c = st[11][1:]


        duration_str = st[1].split(":")
        h = int(duration_str[0],10)
        m = int(duration_str[1],10)
        s = int(duration_str[2],10)

        sec = datetime.timedelta(hours=h, minutes=m, seconds=s)


        user = None

        ### Если вызов исходящий
        if call_type == "O":
            ### Поиск пользователя
            if call_a != "" and Profile.objects.filter(phone=call_a,work_status=True,relax_status=False).exists():
                prof = Profile.objects.filter(phone=call_a,work_status=True,relax_status=False).first()
                user = prof.user



        ### Если вызов входящий
        if call_type == "I":
            ### Поиск пользователя
            if call_c != "" and Profile.objects.filter(phone=call_c,work_status=True,relax_status=False).exists():
                prof = Profile.objects.filter(phone=call_c,work_status=True,relax_status=False).first()
                user = prof.user




        if user == None or user.is_active == False:
            exit()
        elif call_type == "I":
            mark = callin
            comment = "%s -> %s" % (call_a,call_c)
        elif call_type == "O":
            mark =callout
            comment = "%s -> %s" % (call_a,call_c)
        else:
            exit()


        if working_time.objects.filter(user=user, current=True).exists():
            wt = working_time.objects.filter(user=user, current=True).last()
            working_log.objects.create(
                user=user,
                mark=mark,
                working=wt,
                comment=comment,
                duration = int(sec.total_seconds())

            )




