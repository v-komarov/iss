#coding:utf8

import datetime
import csv

from kafka import KafkaConsumer,TopicPartition
from django.core.management.base import BaseCommand, CommandError


from iss.monitor.models import avaya_log
import iss.dbconn


kafka_server = iss.dbconn.KAFKA_SERVER

consumer = KafkaConsumer('asterisk',bootstrap_servers=kafka_server, auto_offset_reset='latest')



class Command(BaseCommand):
    args = '<log>'
    help = 'Загрузка звонков из asterisk'



    def handle(self, *args, **options):


        for m in consumer:

            cdr = m.value

            d = cdr.replace('"','').split(",")

            call_a = d[1]
            call_c = d[2]
            mode = d[3]
            d.reverse()
            duration = d[4]

            print call_a,call_c,mode,duration,len(d)

            ### Входящий или исходящий
            if len(call_a) > 4 and len(call_c) == 4:
                call_in_out = "I"
            else:
                call_in_out = "O"


            ### Внутренний или нет
            if len(call_a) == 4 and len(call_c) == 4:
                inner = 1
            else:
                inner = 0


            """
    
            :param args:
            :param options:
            :return:
            """

            if call_a != "" and call_c != "" and mode == "default":
                avaya_log.objects.create(
                    source = 1,
                    duration=int(duration,10),
                    in_out=call_in_out,
                    call_a=call_a,
                    call_c=call_c,
                    call_inner = inner
                )
                print "ok"
