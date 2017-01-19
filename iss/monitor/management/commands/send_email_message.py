#coding:utf8

from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.db.models import Q

from iss.monitor.models import events

import pickle
import datetime
import urllib2
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




### Ключ для iss
day = "eed3eis9quei7ga9avievaegaaNieHui"



### Отправка ДРП в ИСС
def send_iss_drp(iss_work_id,action_text):

    """

    iss_work_id - идентификатор работ
    action_text - суть ДРП

    """

    value = ""
    value = value + "type_query(%s)create_drp[%s]" % (day, day)
    value = value + "iss_work_id(%s)%s[%s]" % (day, iss_work_id ,day)
    value = value + "action_text(%s)%s[%s]" % (day, action_text ,day)

    req = urllib2.Request(url='http://10.6.3.7/departs/rcu/works/create_work_mss_post.php', data=value, headers={'Content-Type': 'text/plain; charset=cp1251'})
    f = urllib2.urlopen(req)








class Command(BaseCommand):
    args = '<mail message ...>'
    help = 'sand mail message'

    """
    Отправка email сообщений согласно шаблона

    """


    def handle(self, *args, **options):

        now = datetime.datetime.now(timezone('UTC'))

        ### Поиск неотправленных сообщений в очереди (в таблице)
        for m in messages.objects.filter(send_done=False):

            ### Выбор сообщений с оповещение об аварии на МСС
            if m.data["acc_email_templates"] == "1":

                temp_id = int(m.data["acc_email_templates"],10)
                temp = email_templates.objects.get(pk=temp_id)

                if m.accident.acc_iss_id:
                    acc_number = m.accident.acc_iss_id
                else:
                    acc_number = ""

                acc_type_cat = "%s,%s" % (m.data["acc_cat_type"].split(",")[1],m.data["acc_cat_type"].split(",")[0])

                body = temp.template % (acc_number,m.data["acc_datetime_begin"],acc_type_cat,m.data["acc_service_stoplist"],m.data["acc_reason"],m.data["acc_cities"],m.data["acc_address_list"],m.data["acc_zkl"],m.data["acc_repair_end"])
                sbj = "Оповещение об аварии МР-Сибирь № %s" % acc_number
                mto = m.data["acc_email_list"].split(";")

                issid = "<p style=\"color:white;\">ISS-ID:%s:ISS-ID</p>" % (m.accident.acc_event.uuid)

                email = EmailMessage(
                    subject=sbj,
                    body=body+issid,
                    from_email='gamma@sibttk.ru',
                    to=mto,
                    reply_to=['ds@sibir.ttk.ru',]
                )

                email.content_subtype = "html"
                m.mail_body = pickle.dumps(email)
                email.send()

                m.send_done = True
                m.save()

                ### Отправка сообщения в ИСС для создания ДРП
                send_iss_drp(acc_number,sbj)

        print "ok"

