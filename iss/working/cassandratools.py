#coding:utf-8

import datetime
import pandas as pd
from cassandra.cluster import Cluster

import iss.dbconn



cluster = Cluster(iss.dbconn.CASSANDRA_SERVER,iss.dbconn.CASSANDRA_PORT)
session = cluster.connect()
session.set_keyspace(iss.dbconn.CASSANDRA_KEYSPACE)


def createdate(year,month,day):
    """Формирование даты"""
    return datetime.date(year=year, month=month, day=day)


def phone1history():
    """Отчетные данные телефонных вызовов группы 1"""

    query = """SELECT year,month,day,city,phone,calls,calls_in,calls_out,calls_in_ok,calls_out_ok,calls_in_per,calls_out_per,talk_in_avg,talk_out_avg FROM phone_report WHERE group=1 AND mode='day' ALLOW FILTERING;"""


    df = pd.DataFrame(list(session.execute(query)),columns=["year","month","day","city","phone","calls","calls_in","calls_out","calls_in_ok","calls_out_ok","calls_in_per","calls_out_per","talk_in_avg","talk_out_avg"])
    df['phone']= df['phone'].astype(str)

    df.sort_values(by=["year","month","day","city","phone"], ascending=False, inplace=True)
    #df["date"] = datetime.datetime.today()
    df["date"] = df.apply(lambda row: createdate(year=row.year, month=row.month, day=row.day), axis=1)


    return df

