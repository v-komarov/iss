#coding:utf8

import json
from django.core.management.base import BaseCommand, CommandError
from iss.equipment.models import agregators,scan_iplist,devices_ip,footnodes
from iss.localdicts.models import address_city,address_street,address_house,address_companies,devices_type
from iss.inventory.models import devices



class Command(BaseCommand):
    args = '<tools ...>'
    help = 'stuff'




    def handle(self, *args, **options):

        """
        filename = args[0]
        domen = args[1]


        with open(filename, 'r') as f:
            for row in f.readlines():
                scan_iplist.objects.create(ipaddress=row[:-1],device_domen=domen)

        f.close()
        """

        """
            Заполнение агрегаторов

        fn = footnodes.objects.all()[0]

        for a in agregators.objects.all():

            ip = a.ipaddress

            if devices_ip.objects.filter(ipaddress=ip).count() == 1:
                d = devices_ip.objects.get(ipaddress=ip)
                a.footnode = fn
                a.chassisid = d.chassisid
                a.domen = d.device_domen
                a.name = d.device_name
                a.descr = d.device_descr
                a.location = d.device_location
                a.serial = d.device_serial
                a.save()

        """
        """
        import pymssql
        import tabulate


        conn=pymssql.connect(server='10.6.3.7',user='django',password='django2016',database='sibttkdb')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM address_table')
        data = cursor.fetchall()

        #print tabulate.tabulate(data)
        for r in data:
            id = r[0]
            street = address_street.objects.get(name=r[2].encode("utf-8"))
            city = address_city.objects.get(name=r[1].encode("utf-8"))
            dom = r[3].encode("utf-8")
            address_house.objects.update_or_create(house=dom,city=city,street=street,iss_address_id=id)
        """

        """
        for c in address_city.objects.all():
            for h in c.address_house_set.all():
                if h.city != None and h.street != None:
                    print h.city.name,h.street.name
                    if address_house.objects.filter(city=h.city,street=h.street,house=None).count() == 0:
                        address_house.objects.create(house=None,iss_address_id=None,city=h.city,street=h.street)

        """

        company = address_companies.objects.get(pk=2)

        with open('MP-Sibir.txt', 'r') as ip:

            for row in ip.readlines():
                ipadd = row[:-1]
                if devices.objects.filter(data__ipaddress=ipadd).count() == 1:
                    d = devices.objects.get(data__ipaddress=ipadd)
                    d.company = company
                    d.save()
                    print d.data['ipaddress']



        """
        device_type = devices_type.objects.get(pk=1)
        devices.objects.all().delete()

        for d in devices_ip.objects.all():
            #print d.data["iss_address_id"]
            if address_house.objects.filter(iss_address_id=d.data["iss_address_id"]).count() == 1:
                a = address_house.objects.get(iss_address_id=d.data["iss_address_id"])
                data = {
                    'name': d.device_name,
                    'location':d.device_location,
                    'chassisid':d.chassisid,
                    'descr':d.device_descr,
                    'domen':d.device_domen,
                    'ipaddress':d.ipaddress
                }
                #print json.dumps(data)

                devices.objects.create(
                    name = d.device_descr,
                    device_type = device_type,
                    company = company,
                    address = a,
                    serial = d.device_serial,
                    data = data
                )


                print a.city,a.street,a.house
        """