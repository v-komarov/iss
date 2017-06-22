#coding:utf-8

"""

    Модуль взаимодействия с ИСС и другими источниками c целью расчета ЗКЛ

"""


from django.db import connections

from iss.monitor.models import events
from iss.equipment.models import devices_ip
from iss.inventory.models import logical_interfaces_prop
from iss.localdicts.models import logical_interfaces_prop_list

#import pymssql


#conn=pymssql.connect(server='10.6.3.77',user='django',password='django2016',database='sibttkdb')
#cursor = conn.cursor()


prop = logical_interfaces_prop_list.objects.get(name='ipv4')


def get_zkl(rowid_list):

    result = []

    for rowid in rowid_list:
        r = events.objects.get(pk=rowid)

        ### Поиск по ip адресу на интерфейсе manager
        if logical_interfaces_prop.objects.filter(prop=prop, val=r.device_net_address, logical_interface__name='manage').exists():
            p = logical_interfaces_prop.objects.get(prop=prop, val=r.device_net_address)
            ### Добавление строк с зкл
            result.extend(p.logical_interface.get_zkl(r.device_net_address))

    return result