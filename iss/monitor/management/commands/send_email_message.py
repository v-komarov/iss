#coding:utf8

from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.db.models import Q

from iss.monitor.models import events

import pickle
import datetime
from StringIO import StringIO
import poplib,getpass,email
from email.header import decode_header

from pytz import timezone
from iss.monitor.models import messages
from iss.localdicts.models import email_templates

from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage

from transliterate import translit
from transliterate import detect_language

tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)



class Command(BaseCommand):
    args = '<mail message ...>'
    help = 'sand mail message'




    def handle(self, *args, **options):

        now = datetime.datetime.now(timezone('UTC'))

        for m in messages.objects.filter(send_done=False):
            if m.data["acc_email_templates"] == "1":

                temp_id = int(m.data["acc_email_templates"],10)
                temp = email_templates.objects.get(pk=temp_id)

                if m.accident.acc_iss_id:
                    acc_number = m.accident.acc_iss_id
                else:
                    acc_number = ""

                body = temp.template % (acc_number,m.data["acc_datetime_begin"],m.data["acc_cat_type"],m.data["acc_service_stoplist"],m.data["acc_reason"],m.data["acc_cities"],m.data["acc_address_list"],m.data["acc_zkl"],m.data["acc_repair_end"])
                sbj = "Оповещение об аварии МР-Сибирь № %s" % acc_number
                mto = m.data["acc_email_list"].split(";")

                email = EmailMessage(
                    subject=sbj,
                    body=body,
                    from_email='gamma@sibttk.ru',
                    to=mto,
                    reply_to=['ds@sibir.ttk.ru',]
                )

                email.content_subtype = "html"
                m.mail_body = pickle.dumps(email)
                email.send()

                m.send_done = True
                m.save()


        print "ok"

