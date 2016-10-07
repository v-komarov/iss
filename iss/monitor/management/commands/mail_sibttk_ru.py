#coding:utf8

from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.db.models import Q

from iss.monitor.models import events

import pickle
import datetime
import binascii
import poplib,getpass,email
from pytz import timezone
from iss.localdicts.models import Status,Severity


tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)


class Command(BaseCommand):
    args = '<zenoss message ...>'
    help = 'saving zenoss message'




    def handle(self, *args, **options):

        now = datetime.datetime.now(timezone('UTC'))

        """
            issmail@sibttk.ru

        """

        M = poplib.POP3('10.6.0.115')
        M.user("issmail@sibttk.ru")
        M.pass_("Qwerty123")
        M.set_debuglevel(1)
        numMessages = len(M.list()[1])
        for i in range(numMessages):
            msg = M.retr(i + 1)
            raw_mail = '\n'.join(msg[1])
            mail = email.message_from_string(raw_mail)

            # subject
            subject = mail.get('Subject')
            h = email.Header.decode_header(subject)
            sub = h[0][0].decode(h[0][1]) if h[0][1] else h[0][0]
            message_id = mail.get('Message-ID')
            message_from = mail.get('From')

            d = {}
            d["mails"] = []
            d["mails"].append(pickle.dumps(mail))

            events.objects.create(
                source=message_from,
                uuid=message_id,
                datetime_evt=now,
                first_seen=now,
                update_time=now,
                last_seen=now,
                severity_id=Severity.objects.get(pk=3),
                manager="issmail@sibttk.ru",
                status_id=Status.objects.get(pk=0),
                bymail = True,
                data = d
            )
            M.dele(i + 1)

        M.quit()

        print "ok"

