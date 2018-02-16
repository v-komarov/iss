#coding:utf8

import datetime

from django.core.management.base import BaseCommand, CommandError


from iss.monitor.models import avaya_log






class Command(BaseCommand):
    args = '<log>'
    help = 'Загрузка звонков из avaya'



    def handle(self, *args, **options):


        cdr = args[0]
        #print cdr

        """

        :param args:
        :param options:
        :return:
        """

        st = cdr.split(",")

        duration_str = st[1].split(":")
        h = int(duration_str[0],10)
        m = int(duration_str[1],10)
        s = int(duration_str[2],10)

        sec = datetime.timedelta(hours=h, minutes=m, seconds=s)


        call_a = st[3]
        call_b = st[6]
        call_c = st[5]
        call_in_out = st[4]
        inner = st[8]

        avaya_log.objects.create(
            duration=int(sec.total_seconds()),
            in_out=call_in_out,
            call_a=call_a,
            call_b=call_b,
            call_c=call_c,
            call_inner = int(inner,10)
        )


