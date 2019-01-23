#coding:utf8


import datetime
from django.utils import timezone

from django.core.management.base import BaseCommand, CommandError


from django.db.models import Func, F, Value, IntegerField
from django.db.models.functions import Length, Upper, Lower

from iss.working.models import working_log




start = timezone.now().replace(year=2019,month=1,day=1,hour=0,minute=0)



class Command(BaseCommand):
    args = '< >'
    help = 'Выгрузка данных детализации событий по сотрудникам'




    def handle(self, *args, **options):

        """

        :param args:
        :param options:
        :return:
        """

        filename = args[0]




        with open("iss/working/csv/%s" % filename, 'w') as f:

            f.write("ПОЛЬЗОВАТЕЛЬ;ДАТА И ВРЕМЯ;ДЕЙСТВИЕ;ДЛИТЕЛЬНОСТЬ;ДЕТАЛИЗАЦИЯ\n")
            for w in working_log.objects.filter(datetime_create__gte=start).order_by('datetime_create'):
                print w.user.get_full_name(), w.datetime_create, w.mark.name, w.duration, w.comment
                data = "{};{};{};{};{}\n".format(w.user.get_full_name().encode('utf-8'),(w.datetime_create+datetime.timedelta(hours=7)).strftime("%d.%m.%Y %H:%M"),w.mark.name.encode('utf-8'),w.duration if w.duration else "",w.comment.encode('utf-8'))
                f.write(data)
