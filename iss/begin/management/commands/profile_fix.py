#coding:utf8

from django.core.management.base import BaseCommand, CommandError
from iss.monitor.models import Profile
from django.contrib.auth.models import User




class Command(BaseCommand):
    args = '<>'
    help = 'checking and fixing profile'



    def handle(self, *args, **options):

        for u in User.objects.all():
            try:
                print u.profile
            except:
                Profile.objects.create(user=u)
                print "Создан профиль - %s" % u

        print "ok"




