#coding:utf8

import datetime


from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now

from iss.monitor.models import Profile
from iss.working.models import working_time, working_relax






class Command(BaseCommand):
    args = '<checking and closing>'
    help = 'Проверка и принудительное завершение смены'



    def handle(self, *args, **options):

        """

        :param args:
        :param options:
        :return:
        """


        for s in working_time.objects.filter(current=True, datetime_begin__lte=(now() - datetime.timedelta(hours=12))):
            prof = s.user.profile
            prof.work_status = False
            prof.relax_status = False
            prof.save()

            s.datetime_end = now()
            s.current = False
            s.save()

            working_relax.objects.filter(user=s.user, current=True).update(current=False, datetime_end=now())


