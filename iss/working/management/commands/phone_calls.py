#coding:utf8

import datetime
from multiprocessing import Process
from kafka import KafkaConsumer

from django.core.management.base import BaseCommand, CommandError


from iss.monitor.models import Profile
from iss.working.models import marks, working_time, working_log
import iss.dbconn


kafka_server = iss.dbconn.KAFKA_SERVER
consumer = KafkaConsumer('avaya',bootstrap_servers=kafka_server, auto_offset_reset='latest')


### Входящие звонки
callin = marks.objects.get(pk=3)
### Исходящие звонки
callout = marks.objects.get(pk=4)




class Command(BaseCommand):
    args = '<log>'
    help = 'Загрузка звонков, привязка звонка к сотруднику'





    def senddb(self, user, mark, comment, sec):

        if working_time.objects.filter(user=user, current=True).exists():
            wt = working_time.objects.filter(user=user, current=True).last()
            working_log.objects.create(
                user=user,
                mark=mark,
                working=wt,
                comment=comment,
                duration=int(sec.total_seconds())

            )






    def handle(self, *args, **options):


        """

        :param args:
        :param options:
        :return:
        """

        for m in consumer:

            cdr = m.value

            st = cdr.split(",")
            #print st
            call_a = st[3]
            call_c = st[6]
            call_b = st[5]
            comment = ""
            call_type = st[4]


            ### Для групповых номеров
            #if call_type == "I" and call_b == "4888" and call_c == "2160410":
            if call_type == "I" and (call_b == "4888" or call_b == "4666" or call_b == "4664" or call_b == "3773"):
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
                mark = None
            elif call_type == "I":
                mark = callin
                comment = "%s -> %s" % (call_a,call_c)
            elif call_type == "O":
                mark =callout
                comment = "%s -> %s" % (call_a,call_c)
            else:
                mark = None

            print "call_a = {} call_b = {} call_c = {} mark = {} user = {} comment = {}".format(call_a, call_b, call_c, mark, user, comment)

            ### Запись в базу
            self.senddb(user, mark, comment, sec)

            #p = Process(target=self.senddb, arg=(user, mark, comment, sec,))
            #p.start()
