#coding:utf8

import csv


from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User


from iss.monitor.models import Profile






class Command(BaseCommand):
    args = '<>'
    help = 'Рассылква сообщений пользователям КИС'



    def handle(self, *args, **options):

        filename = args[0]
        msg = args[1]


        f = open("iss/begin/msg/%s" % msg,"r")
        text = f.read()
        f.close()


        with open('iss/begin/csv/%s' % filename) as csvfile:
            spamreader = csv.reader(csvfile,delimiter=";")
            next(spamreader, None)
            for row in spamreader:
                email = row[5].strip()

                if len(email) > 8:

                    print email

                    send_mail(
                        'http://10.6.0.22:8000 kis\'s user informaition',
                        '%s' % (text),
                        'GAMMA <gamma@baikal-ttk.ru>',
                        [email, ])
