#coding:utf8

from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.db.models import Q

from iss.monitor.models import events

import pickle
import datetime
import binascii
from StringIO import StringIO
import poplib,getpass,email
from email.header import decode_header

from pytz import timezone
from iss.localdicts.models import Status,Severity


from transliterate import translit
from transliterate import detect_language

tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)


class Command(BaseCommand):
    args = '<mail message ...>'
    help = 'saving mail message'




    def handle(self, *args, **options):

        now = datetime.datetime.now(timezone('UTC'))

        """
            gamma@sibttk.ru

        """

        M = poplib.POP3('10.6.0.115')
        M.user("gamma@sibttk.ru")
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
            message_id = mail.get('Message-ID').replace("<","").replace(">","")
            message_from = mail.get('From')
            message_from = message_from[message_from.find("<"):message_from.find(">")+1]


            ### Тело письма
            body = ""
            if mail.is_multipart():
                for part in mail.walk():
                    ctype = part.get_content_type()
                    cdispo = str(part.get('Content-Disposition'))

                    # skip any text/plain (txt) attachments
                    if ctype == 'text/plain' and 'attachment' not in cdispo:
                        body = part.get_payload(decode=True)  # decode
                        break
            # not multipart - i.e. plain text, no attachments, keeping fingers crossed
            else:
                body = mail.get_payload(decode=True)

            # Почтовое сообщение для хранения
            m = {
                'mail_id':message_id,
                'mail_date':mail.get('Date'),
                'mail_from':message_from,
                'subject':sub,
                'mail_body':body,
                'attachment':[]

            }

            ## Вложение файлов
            if mail.is_multipart():
                for part in mail.walk():
                    ctype = part.get_content_type()

                    if ctype in ['image/jpeg', 'image/png', 'application/pdf', 'application/zip', 'application/gzip', 'application/msword', 'application/vnd.ms-excel']:
                        file_data = StringIO(part.get_payload(decode=True))
                        file_name = part.get_filename()
                        if decode_header(file_name)[0][1] is not None:
                            file_name = str(decode_header(file_name)[0][0]).decode(decode_header(file_name)[0][1]).replace(" ","_")
                            if detect_language(file_name) == "ru":
                                file_name = translit(file_name,reversed=True)
                        m["attachment"].append({
                            'file_name':file_name,
                            'mime_type':ctype,
                            'file_data':pickle.dumps(file_data)
                        })

            # Поиск в теле письма ISS-ID:
            start = body.find("ISS-ID:")
            if start > 0:
                end = body.find(">",start)
                mail_iss_id = body[start+7:end+1]

                ### Поиск сообщения
                if events.objects.filter(uuid=mail_iss_id).count() == 1:
                    e = events.objects.get(uuid=mail_iss_id)
                    d = e.data
                    d["mails"].append(m)
                    e.data = d
                    e.save()


            else:
                d = {}
                d["mails"] = []
                d["mails"].append(m)

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

