#coding:utf-8

"""

    Модуль взаимодействия с ИСС и другими источниками c целью расчета ЗКЛ

"""


from django.db import connections

from iss.monitor.models import events
from iss.equipment.models import devices_ip

import pymssql


conn=pymssql.connect(server='10.6.3.7',user='django',password='django2016',database='sibttkdb')
cursor = conn.cursor()


def get_zkl(rowid_list):

    result = []

    for rowid in rowid_list:
        r = events.objects.get(pk=rowid)


        if devices_ip.objects.filter(ipaddress=r.device_net_address,device_domen=r.source).count() == 1:

            a = devices_ip.objects.get(ipaddress=r.device_net_address,device_domen=r.source)
            name = a.device_name
            location = a.device_location
            ip = a.ipaddress
            data = a.data
            if data.has_key("ports_info"):

                result.append(
                    {
                        'name':name,
                        'address':location,
                        'ip':ip,
                        'ports_info':data["ports_info"]
                    }
                )


    return result