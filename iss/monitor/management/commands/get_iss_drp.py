#coding:utf8

import pymssql
import pickle
import hashlib

from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.db.models import Q

from iss.monitor.models import accidents,drp_list

import datetime
from pytz import timezone


tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)



class Command(BaseCommand):
    args = '<getting grp ...>'
    help = 'refresh & saving drp'


    def handle(self, *args, **options):

        conn = pymssql.connect(server='10.6.3.7', user='django', password='django2016', database='sibttkdb')
        cursor = conn.cursor()

        ### Выбор аварий без acc_iss_id
        for ac in accidents.objects.exclude(acc_iss_id=None):

            ## Для отладки 30081 вложенных файлов
            q = """
                SELECT
                  work_actions.work_id as accident,
                  work_actions.work_action_date as datetime_drp,
                  work_actions.work_action as message_drp,
                  users.user_name as author,
                  work_actions.work_action_num as num_drp
                FROM
                  dbo.work_actions INNER JOIN users on users.user_id=work_actions.user_id where work_actions.work_id={iss_id}
            """.format(iss_id=ac.acc_iss_id)

            #print q

            cursor.execute(q)
            rows = cursor.fetchall()

            for row in rows:

                datetime_drp = krsk_tz.localize(row[1])
                message_drp = row[2]
                author_drp = row[3]
                num_drp = row[4]

                print datetime_drp,row[1]

                if drp_list.objects.filter(num_drp=num_drp,accident=ac).count() == 0:
                    drp_list.objects.create(
                        datetime_drp = datetime_drp,
                        message_drp = message_drp,
                        num_drp = num_drp,
                        accident=ac,
                        author = author_drp
                    )

            q = """
                SELECT
                 work_docs.work_id as accident,
                  work_docs.work_doc_edit_date as datetime_file,
                  work_docs.work_doc_name as data_files_name,
                  work_docs.work_doc as data_files,
                  users.user_name as author
                FROM
                  dbo.work_docs INNER JOIN users on users.user_id=work_docs.user_id where work_docs.work_id={iss_id}
            """.format(iss_id=ac.acc_iss_id)

            #print q

            cursor.execute(q)
            rows = cursor.fetchall()


            for row in rows:

                datetime_file_drp = krsk_tz.localize(row[1])
                file_name = row[2]
                file_data = pickle.dumps(row[3])
                author_file = row[4]
                file_hash = hashlib.md5(file_data).hexdigest()


                if drp_list.objects.filter(num_drp=0, accident=ac, data_files__hash=file_hash).count() == 0:
                    drp_list.objects.create(
                        datetime_drp=datetime_file_drp,
                        data_files={
                            'filename':file_name,
                            'filedata':file_data,
                            'hash':file_hash
                        },
                        num_drp=0,
                        accident=ac,
                        author=author_file
                    )
