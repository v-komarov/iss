#coding:utf8

import logging
import json
from elasticsearch import Elasticsearch
from kafka import KafkaConsumer,TopicPartition
from transliterate import translit, get_available_language_codes

from django.core.management.base import BaseCommand, CommandError
from django.db.models.functions import Upper

from iss.inventory.models import devices, devices_scheme, netelems, logical_interfaces_prop_list, device_status, logical_interfaces, logical_interfaces_prop, devices_removal
from iss.localdicts.models import address_house, address_city, address_street, address_companies

import iss.dbconn

logger = logging.getLogger('devices')



kafka_server = iss.dbconn.KAFKA_SERVER
elsearch_server = iss.dbconn.ELASTICSEARCH


consumer = KafkaConsumer('devices',bootstrap_servers=kafka_server, auto_offset_reset='earliest')
es = Elasticsearch(elsearch_server)


company = address_companies.objects.get(name="МР-Сибирь")
prop = logical_interfaces_prop_list.objects.get(name='ipv4')
device_use = device_status.objects.get(name='Используется')


def find_model(d):

    """
     Поиск модели

    """
    q = {"query": {"match_phrase": {"synonyms": d["model"]}}}
    res = es.search(index="iss2", doc_type="device", body=q)
    for hit in res['hits']['hits']:
        result = "%(id)s" % hit["_source"]
        return result
        #break
    else:
        print u"ElasticSearch Не найден: %s" % d["model"]
        logger.info(u"ElasticSearch Не найден {} {}".format(d["model"], d["ip"]))

        return False




def find_city(city):

    """
    Поиск города в ElasticSearch

    :param d:
    :return:
    """

    q = {"query": {"match_phrase": {"synonyms": city}}}
    res = es.search(index="iss2", doc_type="city", body=q)
    for hit in res['hits']['hits']:
        result = "%(id)s" % hit["_source"]

        print "city_id %s" % result
        return address_city.objects.get(pk=int(result,10))

    else:
        print u"ElasticSearch Не найден: %s" % city
        logger.info(u"ElasticSearch Не найден город {}".format(city))

        return False






def find_street(street):

    """
    Поиск улицы в ElasticSearch

    :param d:
    :return:
    """

    q = {"query": {"match_phrase": {"synonyms": street}}}
    res = es.search(index="iss2", doc_type="street", body=q)
    for hit in res['hits']['hits']:
        result = "%(id)s" % hit["_source"]
        print "street_id %s" % result
        return address_street.objects.get(pk=int(result,10))

    else:
        print u"ElasticSearch Не найден: %s" % street
        logger.info(u"ElasticSearch Не найдена улица {}".format(street))

        return False




def find_address(d):

    """
    Поиск адреса

    :param d:
    :return:
    """

    address = d["location"].split("/")
    city_obj = False
    street_obj = False
    house = ""

    ### Случай полного адреса
    if len(address) == 4:

        city_obj = find_city(address[1])
        street_obj = find_street(address[2])
        """
        Символ разделения номера дома и литеры (например Хабаровская 4б-1) 
        необходимо привести к единому виду с символом разделениея /
        пример: Хабаровская 4б/1
        """
        house = translit(address[3], 'ru').upper().replace("-","/").replace(" ","/").replace("_","/")

        if not city_obj == False and not street_obj == False:

            if address_house.objects.all().annotate(house_upper=Upper("house")).filter(city=city_obj, street=street_obj, house_upper=house).exists():
                address = address_house.objects.all().annotate(house_upper=Upper("house")).filter(city=city_obj, street=street_obj, house_upper=house).first()

                return address





    ### Адрес из города и улицы
    elif len(address) == 3:

        city_obj = find_city(address[1])
        street_obj = find_street(address[2])

        if not city_obj == False and not street_obj == False:

            if address_house.objects.filter(city=city_obj, street=street_obj, house=None).exists():
                address = address_house.objects.filter(city=city_obj, street=street_obj, house=None).first()

                return address





    ### Адрес из города
    elif len(address) == 2:

        city_obj = find_city(address[1])

        if not city_obj == False:

            if address_house.objects.filter(city=city_obj, street=None, house=None).exists():
                address = address_house.objects.filter(city=city_obj, street=None, house=None).first()

                return address



    print u"Не найден адрес: %s" % d["location"]
    logger.info(u"Не найден адрес {} (city:{} street:{} house:{})".format(d["location"],city_obj, street_obj, house))

    return False






### Создание нового элемента оборудования
def CreateDevice(model, address, serial):

    """
    Создание устройства по заданным модели и адресу
    :param model:
    :param address:
    :return:
    """
    ### Создание элемента устройства
    dev = devices.objects.create(
        name = model.name,
        company = company,
        address = address,
        serial = serial,
        device_scheme=model,
        author="device_check",
        status=device_use
    )

    ### Создание элементов портов, слотов, свойств
    dev.mkports(author="device_check")
    dev.mkslots(author="device_check")
    dev.mkcombo(author="device_check")
    dev.mkprop(author="device_check")


    logger.info(u"Создано устройство: {} серийный номер: {} адрес: {}".format(dev.name, dev.serial, dev.getaddress()))








### Перемещение устройства на другой адрес
def MoveDevice(dev, address):

    ### Регистрация перемещения
    devices_removal.objects.create(
        device = dev,
        address = address,
        author = "device_check",
        comment = u"перемещено автоматически"
    )


    logger.info(u"Перемещено устройство {} с адреса {} на адрес {}".format(dev.device_scheme, dev.getaddress(), address.getaddress()))

    dev.address = address
    dev.status = device_use
    dev.save()








### Поиск сетевого элемента по IP адресу
def FindNetIp(ip):

    """
    Происходит поиск сетевого элемента по ip адресу
    в случае успеха - возвращается сам сетевой элемент
    в случае неудачи возвращается False
    """

    if logical_interfaces_prop.objects.filter(val=ip, prop=prop).exists():

        ### Логический интерфейс c необходимым ip адресом
        logintr = logical_interfaces_prop.objects.filter(val=ip, prop=prop).first()

        ### Проверка названия интерфейса
        if logintr.logical_interface.name == "manage":

            #### Необходимый сетевой элемент найден
            netel = logintr.logical_interface.netelem

            return netel

        else:

            return False

    else:

        return False






### Установка ip адреса на управляющий интерфейс сетевого элемента
def NetIntrIp(net,ip):
    """
    Проверяет наличие интерфейса manager, если необходимо - создает,
    Устанавливает ip адрес на интерфейс manager
    :param net:
    :param ip:
    :return:
    """
    ### Проверка наличия интерфейса manage
    if not net.logical_interfaces_set.all().filter(name="manage").exists():
        ### Интерфейса manager нет
        logical_interfaces.objects.create(
            name = "manage",
            netelem = net,
            comment = "created by device_check"
        )

    ### Поиск логического интерфейса
    logintr = net.logical_interfaces_set.all().filter(name="manage").first()

    ### Есть ли необходимое свойство интерфейса
    if logintr.logical_interfaces_prop_set.all().filter(prop=prop).exists():
        ip_prop = logintr.logical_interfaces_prop_set.all().filter(prop=prop).first()
        ip_prop.val = ip
        ip_prop.comment = "saved by device_check"
        ip_prop.save()
    else:
        ### Создание свойства для интерфейса manage
        logical_interfaces_prop.objects.create(
            logical_interface = logintr,
            prop = prop,
            val = ip,
            comment = "device_check"
        )


    logger.info(u"Установлен ip адрес управления {} для сетевого элемента {}".format(ip, net.name))

    return net







### Создание сетевого элемента
def CreateNet(name,ip):
    """
    Создание сетевого элемента по заданному имени,
    добавление интерфейса управления manage с ip адресом
    """
    net = netelems.objects.create(
        name = name,
        author = "device_check"
    )

    logger.info(u"Создан сетевой элемент {}".format(name))


    return NetIntrIp(net,ip)







### Удаление всех связей сетевого элемента и устройств
def NetDeleteLinks(net):
    net.device.clear()





### Удаление всех связей устройства и сетевых элементов
def DevDeleteLinks(dev):
    dev.netelems_set.clear()






### Проверка есть ли связность многие ко многим между устройством и сетевым элементом
def DevNetCheck(dev,net):
    if dev.netelems_set.filter(pk=net.pk).exists():
        return True
    else:
        return False







class Command(BaseCommand):
    args = '<devices ...>'
    help = 'check data of device'

    """
    Читает топик devices с данными zenoss устройств,
    проверяет соответствие в базе данных инвентори 
    """

    def handle(self, *args, **options):

        for m in consumer:
            d = json.loads(m.value)
            model = find_model(d)
            address = find_address(d)

            ### Модель и адрес определены
            if model and address:

                ### Проверка есть ли в инвенторе такая модель по такому адресу и с таким серийным номером
                dev_schema = devices_scheme.objects.get(pk=model)
                if devices.objects.filter(device_scheme=dev_schema, address=address, serial=d["serial"]).exists():
                    ### такое оборудование есть
                    dev = devices.objects.filter(device_scheme=dev_schema, address=address, serial=d["serial"]).first()
                    ### Поиск сетевого элемента
                    net = d["name"]
                    if netelems.objects.filter(name=net).exists():

                        ### Сетевой элемент найден по названию
                        netel = netelems.objects.filter(name=net).first()

                        ### Установка ip адреса на управляющий интерфейс
                        NetIntrIp(netel,d["ip"])

                        ### Проверка есть ли связанность между устройством и сетевым элементом
                        if not DevNetCheck(dev, netel):
                            ### Создание связи между элементами
                            DevDeleteLinks(dev)
                            netel.device.add(dev)
                            logger.info(u"Создание связи устройства {} и сетевого элемента {}".format(dev.name, netel.name))


                    else:
                        """
                        Сетевой элемент по названию не найден
                        Поиск сентевого элемента по ip
                        """
                        netel = FindNetIp(d["ip"])

                        ### Сетевой элемент найден по ip адресу
                        if netel:

                            ### Перезапись названия сетевого элемента
                            netel.name = d["name"]
                            netel.save()

                            ### Проверка есть ли связанность между устройством и сетевым элементом
                            if not DevNetCheck(dev,netel):
                                ### Создание связи между элементами
                                DevDeleteLinks(dev)
                                netel.device.add(dev)
                                logger.info(u"Создание связи устройства {} и сетевого элемента {}".format(dev.name, netel.name))


                        else:
                            """
                            Сетевой элемент по ip адресу не найден
                            Создание сетевого элемента
                            """
                            net = CreateNet(d["name"],d["ip"])
                            ### Создание связи между элементами
                            DevDeleteLinks(dev)
                            net.device.add(dev)
                            logger.info(u"Создание связи устройства {} и сетевого элемента {}".format(dev.name, net.name))





                else:
                    ### Такого оборудования нет

                    ### Попытка найти по ip адресу
                    netel = FindNetIp(d["ip"])


                    ###  если сетевой элемент найден по ip адресу
                    if netel:

                        ### Проверка есть ли привязанное к данному сетевому элементу оборудование с соответствующей моделью, но с другим адресом размещения
                        if netel.device.filter(device_scheme=dev_schema, serial=d["serial"]).exclude(address=address).exists():

                            ### Выбор первого элемента , совпадающего по модели
                            dev = netel.device.filter(device_scheme=dev_schema, serial=d["serial"]).exclude(address=address).first()

                            ### Перемещение устройства на другой адрес
                            MoveDevice(dev, address)

                        else:
                            """
                            на данном сетевом элементе нет оборудования требуемой модели
                            Создание устройства требуемой модели 
                            """
                            CreateDevice(dev_schema, address, d["serial"])



                    else:
                        """
                        По ip адресу найти оборудрование не удалось
                        Создание нового элемента оборудования
                        """
                        CreateDevice(dev_schema, address, d["serial"])


