#coding:utf-8

import json
import ipaddress
import csv

import datetime
from pytz import timezone

from django.http import HttpResponse, HttpResponseRedirect

from iss.localdicts.models import address_city, address_house, logical_interfaces_prop_list
from iss.monitor.models import accidents
from iss.inventory.models import logical_interfaces_prop, devices



prop = logical_interfaces_prop_list.objects.get(name='ipv4')
tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)

start = datetime.datetime(2017, 7, 9, 12, 0, 0, 0, timezone(tz))


devices_ports = {}


### Чтение данных по портам устройств из csv файла
with open('iss/maps/csv/ports.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';')
    next(spamreader, None)
    for row in spamreader:
        devices_ports[row[0]] = {'oldports': row[1], 'olddate': row[2], 'newports': row[3], 'newdate': row[4]}




def get_json(request):

    response_data = {}

    if request.method == "GET":

        r = request.GET
        rg = request.GET.get








        ### Получение координат городов и населенных пунктов
        if r.has_key("action") and rg("action") == 'get_city_geo':
            city_id = int(request.GET["city_id"],10)

            city = address_city.objects.get(pk=city_id)
            rec = address_house.objects.filter(city=city,house=None,street=None).first()

            data = {
                "lat": rec.geo["lat"],
                "lng": rec.geo["lng"]
            }

            response_data = data




        ### Получение координат по аварии
        if r.has_key("action") and rg("action") == 'get_accident_geo':
            acc_id = int(request.GET["acc_id"],10)

            acc = accidents.objects.get(pk=acc_id)
            data = {}

            data["acc_id"] = acc.id
            data["acc_name"] = acc.acc_name
            data["acc_reason"] = acc.acc_reason
            data["address_list"] = []


            ### Список id адресов
            if acc.acc_addr_dict.has_key("address_list"):
                addr_id_list = [a["address_id"] for a in acc.acc_addr_dict["address_list"]["address_list"]]
            else:
                addr_id_list = []


            for add_id in addr_id_list:
                add = address_house.objects.get(pk=add_id)
                ### Проверка является ли адрес групповым
                if add.house == None and add.street == None:
                    for a in address_house.objects.filter(city=add.city).exclude(street=None).exclude(house=None):
                        ### Добавление всех домов города или населенного пункта
                        if a.geo["result"] == "ok":
                            data["address_list"].append({
                                "city": a.city.name,
                                "street": a.street.name,
                                "house": a.house,
                                "lat": a.geo["lat"],
                                "lng": a.geo["lng"]
                            })

                elif add.house == None and add.street:
                    for b in address_house.objects.filter(city=add.city,street=add.street).exclude(house=None):
                        ### Добавление всех домов на улице
                        if b.geo["result"] == "ok":
                            data["address_list"].append({
                                "city": b.city.name,
                                "street": b.street.name,
                                "house": b.house,
                                "lat": b.geo["lat"],
                                "lng": b.geo["lng"]
                            })

                else:
                ### Для обычных адресов домов
                    if add.geo["result"] == "ok":
                        data["address_list"].append({
                            "city": add.city.name,
                            "street": add.street.name,
                            "house": add.house,
                            "lat": add.geo["lat"],
                            "lng": add.geo["lng"]
                        })

            


            response_data = data





        ### Поиск устройств по ip адресам
        if r.has_key("action") and rg("action") == 'find_devices_ip':
            ip_list = request.GET["ip_list"].split(",")



            if len(ip_list) > 0 and len(request.GET["ip_list"])>=7:

                ip_checked = []
                ### Проверка является ли адрес сетью
                for i in ip_list:
                    ### Адрес хоста
                    if i.find("/") == -1:
                        if i not in ip_checked:
                            ip_checked.append(i)
                    ### Адрес сети
                    else:
                        for ii in list(ipaddress.ip_network(i).hosts()):
                            host = str(ii).encode("utf-8")
                            if host not in ip_checked:
                                ip_checked.append(host)

                ### Список устройств
                d = []

                #print ip_checked

                ### Поиск оборудования по ip адресу
                for ip in ip_checked:

                    ### Поиск по ip адресу на интерфейсе manager
                    if logical_interfaces_prop.objects.filter(prop=prop, val=ip,
                                                              logical_interface__name='manage').exists():
                        p = logical_interfaces_prop.objects.get(prop=prop, val=ip, logical_interface__name='manage')
                        #### Определение логического интерфейса
                        li = p.logical_interface

                        ### Поиск связанных устройств
                        for dev_id in li.get_dev_list():
                            dev = devices.objects.get(pk=dev_id)
                            ### Если определены координаты адреса
                            if dev.address.geo["result"] == "ok":
                                d.append({
                                    'ip': ip,
                                    'model': dev.device_scheme.name,
                                    'address': dev.getaddress(),
                                    'status': dev.getstatus(),
                                    'netelems': dev.get_netelems(),
                                    'zkl': dev.getzkl(),
                                    'lat': dev.address.geo["lat"],
                                    'lng': dev.address.geo["lng"]
                                })



                ### Подведение итогов по поиску
                if len(d) > 0:
                    response_data["result"] = "ok"
                    response_data["devices"] = d

                    ### Определение аварийных ip адресов
                    accidents_ip = []
                    for acc in accidents.objects.filter(acc_end=None, acc_start__gt=start):
                        for ip in acc.get_event_ip_list():
                            if ip not in accidents_ip:
                                accidents_ip.append(ip)

                    response_data["accidents_ip"] = accidents_ip


                else:
                    response_data = {"result": "empty"}

            else:
                response_data = {"result": "empty"}





        ### Получение списка координат устройств, удаленных от центра не более км.
        if r.has_key("action") and rg("action") == 'get-devices-distance':

            city_id = int(request.GET["city_id"],10)

            city = address_city.objects.get(pk=city_id)
            rec = address_house.objects.filter(city=city,house=None,street=None).first()

            devices_list = []
            for item in address_house.objects.all():
                if item.check_distance(rec.geo["lat"],rec.geo["lng"], 20):
                    for dev in item.devices_set.all():
                        ips = dev.get_manage_ip()

                        ports_information = {}

                        if devices_ports.has_key(ips[0]):
                            ports_information['result'] = "ok"
                            ports_information['oldports'] = devices_ports[ips[0]]['oldports']
                            ports_information['newports'] = devices_ports[ips[0]]['newports']
                            ports_information['olddate'] = devices_ports[ips[0]]['olddate']
                            ports_information['newdate'] = devices_ports[ips[0]]['newdate']
                        else:
                            ports_information['result'] = "empty"


                        devices_list.append({
                            'lat': item.geo['lat'],
                            'lng': item.geo['lng'],
                            'ip': " ".join(ips),
                            'device': dev.device_scheme.name,
                            'address': item.getaddress(),
                            'ports_information': ports_information
                        })

            data = {
                "lat": rec.geo["lat"],
                "lng": rec.geo["lng"],
                "devices": devices_list
            }


            response_data = data





    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response
