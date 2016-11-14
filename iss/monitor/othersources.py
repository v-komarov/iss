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

    result = {}

    zkl_list = []

    for rowid in rowid_list:
        r = events.objects.get(pk=rowid)


        if devices_ip.objects.filter(ipaddress=r.device_net_address,device_domen=r.source).count() == 1:

            a = devices_ip.objects.get(ipaddress=r.device_net_address,device_domen=r.source)
            name = a.device_name
            mac = a.chassisid
            ip = a.ipaddress
            serial = a.device_serial
            domen = a.device_domen
            #try:
                ### Запрос из ИСС
            if domen == "zenoss_krsk":

                q = """
                    SELECT ports_description.port_status_id, address_table.city_address, address_table.street_address, address_table.dom_address,
                    ports_description.port_number, equipment_info.equipment_ne_name, equipment_info.equipment_ip, mac_sn.mac_address, mac_mac.mac_address
                    FROM
                  ports_description INNER JOIN equipment_info on equipment_info.equipment_mac_id=ports_description.port_equipment_mac_id
                  INNER JOIN address_table on address_table.address_id=equipment_info.equipment_address_id
                  INNER JOIN mac_information AS mac_sn on mac_sn.mac_id=equipment_info.equipment_mac_id
                  INNER JOIN mac_information AS mac_mac on mac_mac.mac_id=equipment_info.equipment_mac_id
                  WHERE mac_sn.[description]='sn' AND mac_mac.[description]='mac' AND
                  (equipment_info.equipment_ne_name like '%s' OR equipment_info.equipment_ip like '%s' OR mac_sn.mac_address like '%s' OR mac_mac.mac_address like '%s')

                """ % (name,ip,serial,mac)
                print q
                cursor.execute(q)
                rows = cursor.fetchall()

                for row in rows:
                    zkl_list.append([row[5],row[0]])
            #except:
            #    print "iss mssql problem"

    for item in zkl_list:
        if result.has_key(item[0]) == False:
            result[item[0]] = {
                'use':0,
                'rezerv':0,
                'free':0,
                'noready':0,
                'tech':0,
                'noconnect':0
            }

        if item[1] == 2:
            result[item[0]]["use"] = result[item[0]]["use"] + 1
        elif item[1] == 3:
            result[item[0]]["rezerv"] = result[item[0]]["rezerv"] + 1
        elif item[1] == 1 or item[1] == 4:
            result[item[0]]["free"] = result[item[0]]["free"] + 1
        elif item[1] == 7:
            result[item[0]]["noready"] = result[item[0]]["noready"] + 1
        elif item[1] == 5 or item[1] == 8:
            result[item[0]]["tech"] = result[item[0]]["tech"] + 1
        elif item[1] == 9:
            result[item[0]]["noconnect"] = result[item[0]]["noconnect"] + 1

    print result
    return result