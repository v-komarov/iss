#coding:utf8

from django.core.management.base import BaseCommand, CommandError
from iss.equipment.models import devices_ip
import pymssql


class Command(BaseCommand):
    args = '<get iss data ...>'
    help = "getting iss's data"




    def handle(self, *args, **options):


        conn = pymssql.connect(server='10.6.3.7', user='django', password='django2016', database='sibttkdb')
        cursor = conn.cursor()


        for device in devices_ip.objects.filter(device_domen="zenoss_krsk"):

            a = devices_ip.objects.get(ipaddress=device.ipaddress, device_domen="zenoss_krsk")
            name = a.device_name
            mac = a.chassisid.replace(":","")
            ip = a.ipaddress
            serial = a.device_serial

            mac = "%s-%s-%s" % (mac[0:4],mac[4:9],mac[8:13])

            # try:
            ### Запрос из ИСС

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

            """ % (name, ip, serial, mac)

            print q

            cursor.execute(q)
            rows = cursor.fetchall()

            ports_info = {
                'used': 0,
                'reservation': 0,
                'free': 0,
                'defective': 0,
                'tech': 0,
                'unconnected': 0
            }

            for row in rows:
                #print row
                # except:
                #    print "iss mssql problem"

                if row[0] == 2:
                    ports_info["used"] = ports_info["used"] + 1
                elif row[0] == 3:
                    ports_info["reservation"] = ports_info["reservation"] + 1
                elif row[0] == 1 or row[1] == 4:
                    ports_info["free"] = ports_info["free"] + 1
                elif row[0] == 7:
                    ports_info["defective"] = ports_info["defective"] + 1
                elif row[0] == 5 or row[1] == 8:
                    ports_info["tech"] = ports_info["tech"] + 1
                elif row[0] == 9:
                    ports_info["unconnected"] = ports_info["unconnected"] + 1


            data = a.data
            data["ports_info"] = ports_info
            a.data = data
            a.save()

            print data
