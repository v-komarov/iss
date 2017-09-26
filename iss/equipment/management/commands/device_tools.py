#coding:utf8

import json
import logging
from django.core.management.base import BaseCommand, CommandError
from iss.equipment.models import agregators,scan_iplist,devices_ip,footnodes
from iss.localdicts.models import address_city,address_street,address_house,address_companies
from iss.inventory.models import devices


logger = logging.getLogger('loadding')



class Command(BaseCommand):
    args = '<tools ...>'
    help = 'stuff'




    def handle(self, *args, **options):

        """

        :param args:
        :param options:
        :return:
        """


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
            if address_street.objects.filter(name=r[2].encode("utf-8")).count() == 0:
                address_street.objects.create(name=r[2].encode("utf-8"))
            street = address_street.objects.get(name=r[2].encode("utf-8"))
            if address_city.objects.filter(name=r[1].encode("utf-8")).count() == 0:
                address_city.objects.create(name=r[1].encode("utf-8"))
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
                        address_house.objects.update_or_create(house=None,iss_address_id=None,city=h.city,street=h.street)

                    if address_house.objects.filter(city=h.city,street=None,house=None).count() == 0:
                        address_house.objects.update_or_create(house=None,iss_address_id=None,city=h.city,street=None)
        """

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


        """
        Переадресация и изменение sysname согласно предоставленных данных Ириной Кокшаровой
        import csv
        from iss.inventory.models import logical_interfaces_prop,netelems,devices
        from iss.localdicts.models import logical_interfaces_prop_list

        prop = logical_interfaces_prop_list.objects.get(name='ipv4')


        with open('iss/equipment/csv/znodelist_4gamma.csv') as csvfile:
            spamreader = csv.reader(csvfile,delimiter=";")
            #next(spamreader, None)
            for row in spamreader:
                ip_old = row[0]
                name_old = row[1]
                ip_new = row[2]
                name_new = row[3]

                ### Поиск по ip адресу на интерфейсе manager
                if logical_interfaces_prop.objects.filter(prop=prop,val=ip_old).exists():
                    p = logical_interfaces_prop.objects.get(prop=prop,val=ip_old)
                    if p.logical_interface.name == 'manage':

                        #### Определение серевого элемента
                        ne = p.logical_interface.netelem
                        ne.name = name_new
                        ne.save()

                        p.val = ip_new
                        p.save()

                        #for d in ne.device.all():
                        #    print d.name

                    else:
                        logger.info("Интерфейс manager для адреса {ipaddress} не определен!".format(ipaddress=ip_old))
                else:

                    logger.info("IP адрес {ipaddress} не найден!".format(ipaddress=ip_old))

        """

        """
            Вывод данных ipaddress, port, номер договора

        from iss.inventory.models import logical_interfaces_prop,netelems,devices
        from iss.localdicts.models import logical_interfaces_prop_list

        f = open('gamma_onyma.csv','w')

        ipv4 = logical_interfaces_prop_list.objects.get(name='ipv4')
        onyma = logical_interfaces_prop_list.objects.get(name='onyma')

        ### Выбор всех свойств с onyma
        for p in logical_interfaces_prop.objects.filter(prop=onyma):

            ### Номер договора
            dog = p.val

            ### логический интерфейс
            li = p.logical_interface

            ### Номер порта
            port = li.name

            ### Сетевой элемент
            ne = li.netelem

            ### ip адрес
            if ne.logical_interfaces_set.all().filter(name='manage').exists():
                liip = ne.logical_interfaces_set.all().filter(name='manage').first()
                if liip.logical_interfaces_prop_set.filter(prop=ipv4).exists():
                    ip = liip.logical_interfaces_prop_set.filter(prop=ipv4).first().val

                    f.write("{ip};{port};{dog};\n".format(ip=ip,port=port,dog=dog))

        """


        """
            Вывод данных ipaddress, модель устрройства, номер договора
        """


        from iss.inventory.models import logical_interfaces_prop,netelems,devices
        from iss.localdicts.models import logical_interfaces_prop_list, address_house

        f = open('devices_dubl.csv','w')

        #ipv4 = logical_interfaces_prop_list.objects.get(name='ipv4')
        #onyma = logical_interfaces_prop_list.objects.get(name='onyma')

        ### Выбор всех устройств
        for addr in address_house.objects.filter():
            ### Выбор устройств , если на адресе более одного
            if addr.devices_set.all().count() > 1:
                for device in addr.devices_set.all():
                    str = u"{ip};{model};{address};\n".format(address=device.getaddress(), ip=u" ".join(device.get_manage_ip()), model=device.device_scheme.name)
                    f.write(str.encode("utf-8"))
