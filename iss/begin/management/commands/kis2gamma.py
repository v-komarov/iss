#coding:utf8

from django.core.management.base import BaseCommand, CommandError
from iss.monitor.models import Profile
from django.contrib.auth.models import User

import csv
import random
import string




### Генерация пароля
def random_passwd():
  rid = ''
  for x in range(8): rid += random.choice(string.ascii_letters + string.digits)
  return rid


class Command(BaseCommand):
    args = '<>'
    help = 'Миграция учетных записей из КИС (центр авторизации) в gamma'



    def handle(self, *args, **options):

        filename = args[0]

        with open('iss/begin/csv/%s' % filename) as csvfile:
            spamreader = csv.reader(csvfile,delimiter=";")
            next(spamreader, None)
            for row in spamreader:
                userkiscode = row[0].strip()
                lastname = row[1].strip()
                firstname = row[2].strip()
                surname = row[3].strip()
                phone = row[4].strip()
                email = row[5].strip()
                login = row[6].strip()
                job = row[7].strip()

                if login != "" and email != "":
                    print "{} {} {}".format(lastname,firstname,surname)
                    if User.objects.filter(username=login).exists():
                        u = User.objects.filter(username=login).first()
                        prof = u.profile
                        prof.userkiscode = userkiscode
                        prof.save()

                        print "%s записан" % userkiscode

                    else:
                        passwd = random_passwd()

                        u = User.objects.create_user(
                            username=login,
                            password=passwd,
                            email=email,
                            first_name=firstname,
                            last_name=lastname
                        )
                        prof = u.profile
                        prof.userkiscode = userkiscode
                        prof.surname = surname
                        prof.phone = phone[:10]
                        prof.email = email
                        prof.job = job[:100]
                        prof.save()

                        print "Создана учетная запись %s" % login

