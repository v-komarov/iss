#coding:utf8

from django.core.management.base import BaseCommand, CommandError


from iss.monitor.models import Profile
from iss.working.models import marks, working_time, working_log


### Входящие звонки
callin = marks.objects.get(pk=1)
### Исходящие звонки
callout = marks.objects.get(pk=2)




class Command(BaseCommand):
    args = '<log>'
    help = 'Загрузка звонков'



    def handle(self, *args, **options):


        cdr = args[0]

        """

        :param args:
        :param options:
        :return:
        """

        st = cdr.split(",")
        sec = st[2]
        call_from = st[3]
        call_to = st[6]
        call_type = ""
        comment = ""

        user = None

        ### Поиск пользователя - входящие
        if call_to != "" and Profile.objects.filter(phone=call_to,work_status=True,relax_status=False).exists():
            prof = Profile.objects.filter(phone=call_to,work_status=True,relax_status=False).first()
            user = prof.user
            call_type = "in"


        ### Поиск пользователя - исходящие
        if call_from != "" and Profile.objects.filter(phone=call_from,work_status=True,relax_status=False).exists():
            prof = Profile.objects.filter(phone=call_from,work_status=True,relax_status=False).first()
            user = prof.user
            call_type = "out"


        if user == None or user.is_active() == False:
            exit()
        elif call_type == "in":
            mark = callin
            comment = "%s -> %s" % (call_from,call_to)
        elif call_type == "out":
            mark =callout
            comment = "%s -> %s" % (call_to,call_from)
        else:
            exit()


        if working_time.objects.filter(user=user, current=True).exists():
            wt = working_time.objects.filter(user=user, current=True).last()
            working_log.objects.create(
                user=user,
                mark=mark,
                working=wt,
                comment=comment

            )




