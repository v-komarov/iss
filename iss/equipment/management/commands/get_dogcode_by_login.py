#coding:utf8

import json

from django.core.management.base import BaseCommand, CommandError

from iss.equipment.models import client_login_log
from iss.onyma.apidata import get_dogcodebylogin


class Command(BaseCommand):
    args = '<onyma data ...>'
    help = 'getting dogcode by login'





    def handle(self, *args, **options):

        dogcode_list = []
        for item in client_login_log.objects.filter(onyma_dogid=0).order_by("?")[:100]:
            dogcode_list.append(item.login)


        for d in json.loads(get_dogcodebylogin("#".join(dogcode_list))):
            if d["dogid"]:
                client_login_log.objects.filter(onyma_dogid=0,login=d["login"]).update(onyma_dogid=d["dogid"],onyma_dogcode=d["dogcode"])

