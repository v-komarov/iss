.. contents:: Оглавление
    :depth: 3


kafka
=====



:kafka: Брокер сообщений (для организации взаимодействия Gamma Акты АВР - КИС ТМЦ, Gamma - zenoss по спискам сетевых устройств)


Кластер реализован на 10.6.0.88, 10.6.0.22, 10.6.0.135


Порядок запуска кластера
------------------------

#. На всех хостах кластера **systemctl start zookeeper**
#. Затем на всех хостах кластера **systemctl start kafka**

Два процесса должны быть в работе (zookeeper, kafka)
----------------------------------------------------

 Диагностика zookeeper
 ::
 
   root@iss:~# netstat -an|grep 2181
   tcp        0      0 0.0.0.0:2181            0.0.0.0:*               LISTEN     
   tcp        0      0 10.6.0.22:53850         10.6.0.88:2181          ESTABLISHED
   tcp        0      0 10.6.0.22:2181          10.6.0.135:35744        ESTABLISHED

 Диагностика kafka
 ::
 
    root@iss:~# netstat -an|grep 9092
    tcp        0      0 10.6.0.22:9092          0.0.0.0:*               LISTEN     


 Время жизни сообщений в топике определяется параметром:
 ::
 
    # The minimum age of a log file to be eligible for deletion due to age
    log.retention.hours=24
     


Topic devices
-------------

Назначение: обмен информацимей по zenoss сетевым устройствам

 Пример записи
 :: 
 
    {'vendor': 'D-Link', 'name': 'zlg-4-sa1x120-65t10t21p1', 'ip': '55.65.10.21', 'location': '/Zelenogorsk/Parkovaya/72', 'model': 'DES-3028', 'serial': 'PVCM1A1001605'}
    

Запись в топик
~~~~~~~~~~~~~~

Запись ведется с 10.6.0.88 из **AirFlow** DAG **zenoss**

 Пишущий скрипт /root/device-topic.py
 ::
 
    #!/usr/bin/python
    #coding:utf-8
    
    import argparse
    import csv
    import json
    from kafka import KafkaProducer
    
    ### kafka
    ka_host = ['10.6.0.88:9092']
    producer = KafkaProducer(bootstrap_servers=ka_host)
    queue = 'devices'
    
    parser = argparse.ArgumentParser()
    parser.add_argument("csvfile", type=str, help=u"Файл в формате csv данных")
    args = parser.parse_args()
    
    
    def SendRec(rec):
        
        """ 
        Запись в топик kafka данных по устройствам zenoss 
    
        """
        producer.send(queue, rec)
        producer.flush()
    
    
    
    
    if __name__ == '__main__':
    
        if args:
            csvfile = args.csvfile
    
            with open(csvfile,'r') as f:
                next(f)
                spamreader = csv.reader(f, delimiter=";")
                for row in spamreader:
                    if len(row) > 9:
                        ip = row[1]
                        name = row[2]
                        location = row[5]
                        model_full = row[6]
                        serial = row[10]
                        m = model_full.split("/")
                        if m[1] == "Network" and m[2] == "Switch" and len(m)>5:
                            vendor = m[3]
                            model = m[4]
                            rec = {
                                "ip":ip,
                                "name":name,
                                "location":location,
                                "vendor":vendor,
                                "model":model,
                                "serial":serial
                            }
                            SendRec(json.dumps(rec))
    
 
 
 Проверить записи в топике можно консольной командой
 ::
 
    /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server 10.6.0.88:9092 --from-beginning --topic devices

    
Topic avaya
-----------

Назначение: обмен информацией CDR

 Пример записей
 ::

    2018/09/07 11:06:53,00:00:27,0,9145661757@172.16.2.10,I,4209,2160492,,0,1949529,1,T9017,Line 17.1,V9513,VM Channel 13,0,0,,,,,,,,,,,,,
    2018/09/07 11:06:53,00:00:00,0,9145661757@172.16.2.10,I,4666,2160492,,0,1949529,0,T9017,Line 17.1,V9513,VM Channel 13,0,0,,,,,,,,,,,,,
    2018/09/07 11:07:20,00:00:00,0,,O,78007750775,78007750775,,1,1949565,0,E3776,VIRTUAL SPP 3,,,0,0,,,,,,,,,,,,,
    2018/09/07 11:06:19,00:00:38,0,4731,O,69145869202,69145869202,,0,1949480,0,E4731,Тароватова М,T9017,Line 17.4,0,0,,,,,,,,,,,U,Тароватова М,
    2018/09/07 11:07:21,00:00:00,0,,O,78007750775,78007750775,,1,1949566,0,E3779,VIRTUAL SPP 4,,,0,0,,,,,,,,,,,,,
    2018/09/07 11:07:22,00:00:00,0,,O,78007750775,78007750775,,1,1949567,0,E3777,VIRTUAL SPP,,,0,0,,,,,,,,,,,,,
    2018/09/07 11:07:22,00:00:00,0,,O,78007750775,78007750775,,1,1949568,0,E3778,VIRTUAL SPP 1,,,0,0,,,,,,,,,,,,,
    2018/09/07 11:07:23,00:00:00,0,,O,78007750775,78007750775,,1,1949569,0,E3775,VIRTUAL SPP 2,,,0,0,,,,,,,,,,,,,
    2018/09/07 11:07:24,00:00:00,0,,O,78007750775,78007750775,,1,1949570,0,E3776,VIRTUAL SPP 3,,,0,0,,,,,,,,,,,,,
     
 
 Просмотр сообщений топика
 ::
 
    /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server 10.6.0.88:9092 --from-beginning --topic avaya
    
    



Topic asterisk
--------------

Назначение: обмен информацией CDR

 Пример записей
 ::

    2018-09-07 11:05:20","2018-09-07 11:05:20",0,0,"ANSWERED","DOCUMENTATION","1536293101.12461",""
    "","2889","09243820431","pre-rec","""2889"" <2889>","SIP/2889-0000098e","Local/09243820431@default-000005a6;1","Dial","Local/09243820431@default,30,t","2018-09-07 11:05:01","2018-09-07 11:05:20","2018-09-07 11:05:20",19,0,"ANSWERED","DOCUMENTATION","1536293101.12458",""
    "","2889","09243820431","pre-rec","""2889"" <2889>","SIP/2889-0000098e","OOH323/avayaG700-1919","Dial","Local/09243820431@default,30,t","2018-09-07 11:05:20","2018-09-07 11:05:20","2018-09-07 11:08:24",183,183,"ANSWERED","DOCUMENTATION","1536293101.12458",""
    "","9996837840","1","IVR88007757800_tree","""New User"" <9996837840>","SIP/KTTK-000009ae","Local/2998@default-000005b6;1","Dial","Local/2998@default","2018-09-07 11:07:30","2018-09-07 11:07:30","2018-09-07 11:07:39",9,9,"ANSWERED","DOCUMENTATION","1536293250.12602",""
    "","9996837840","1","IVR88007757800_tree","""New User"" <9996837840>","SIP/KTTK-000009ae","SIP/2910-000009b0","Dial","Local/2998@default","2018-09-07 11:07:39","2018-09-07 11:07:39","2018-09-07 11:08:29",50,50,"ANSWERED","DOCUMENTATION","1536293250.12602",""
    "","2863","09083258557","pre-rec","""2863"" <2863>","SIP/2863-000009bf","Local/09083258557@default-000005b8;1","Dial","Local/09083258557@default,30,t","2018-09-07 11:08:04","2018-09-07 11:08:14","2018-09-07 11:08:14",10,0,"ANSWERED","DOCUMENTATION","1536293284.12655",""
    "","2863","09083258557","pre-rec","""2863"" <2863>","SIP/2863-000009bf","OOH323/avayaG700-1946","Dial","Local/09083258557@default,30,t","2018-09-07 11:08:14","2018-09-07 11:08:14","2018-09-07 11:08:31",16,16,"ANSWERED","DOCUMENTATION","1536293284.12655",""
    "ast_h323","09083258557","","default",""""" <09083258557>","OOH323/avayaG700-1946","Local/09083258557@default-000005b8;1","AppDial","(Outgoing Line)","2018-09-07 11:08:14","2018-09-07 11:08:14","2018-09-07 11:08:14",0,0,"ANSWERED","DOCUMENTATION","1536293284.12658",""
    "ast_h323","3711","1110","default","""Bryl A"" <3711>","OOH323/avayaipo-1945","SIP/1110-000009be","Dial","SIP/1110","2018-09-07 11:08:03",,"2018-09-07 11:08:31",28,0,"NO ANSWER","DOCUMENTATION","1536293283.12653",""
    "","1111","1314","default","""1111 Krasnoperov S."" <1111>","SIP/1111-000009c0","SIP/1314-000009c1","Dial","SIP/1314","2018-09-07 11:08:40",,"2018-09-07 11:08:52",12,0,"NO ANSWER","DOCUMENTATION","1536293320.12674",""
    


 Просмотр сообщений топика
 ::
 
    /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server 10.6.0.88:9092 --from-beginning --topic asterisk



Topic circuit
-------------

Назначение: обмен информацией с инвентори gamma о занятых портах абонентами на оборудовании абонентского доступа на основании тега **circuit**.

 Пример записей
 ::
 
    AC:F1:DF:D3:44:73::55.34.3.66::12
    C8:D3:A3:28:21:75::55.20.5.43::1
    10:7B:44:E1:1D:78::55.66.2.37::18
    C4:A8:1D:44:15:8F::55.50.4.55::8
    64:5A:04:98:73:0E::55.49.4.16::7


 Просмотр сообщений топика
 ::
 
    /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server 10.6.0.88:9092 --from-beginning --topic circuit
    
 Наполнение топика: 10.6.0.88 (скрипты по сбору информации с радиус серверов - cron)


Топик port-mac
--------------

Назначение: обмен информацией с инвентори gamma о занятых портах абонентами на оборудовании абонентского доступа на основании активности mac адресов на портах.

 Пример записей
 ::
 
    {"ip": "33.80.9.86", "port": "7", "mode": "use"}
    {"ip": "33.80.9.87", "port": "0", "mode": "use"}
    {"ip": "33.80.9.87", "port": "16", "mode": "use"}
    {"ip": "33.80.9.87", "port": "17", "mode": "use"}
    {"ip": "33.80.9.87", "port": "18", "mode": "use"}
    {"ip": "33.80.9.87", "port": "2", "mode": "use"}
    {"ip": "33.80.9.87", "port": "22", "mode": "use"}
    {"ip": "33.80.9.87", "port": "23", "mode": "use"}
    {"ip": "33.80.9.87", "port": "24", "mode": "use"}
    {"ip": "33.80.9.87", "port": "25", "mode": "tech"}
    {"ip": "33.80.9.87", "port": "26", "mode": "tech"}
    {"ip": "33.80.9.87", "port": "6", "mode": "use"}

 Просмотр сообщений топика
 ::
 
    /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server 10.6.0.88:9092 --from-beginning --topic port-mac



Топик zenoss-krsk
-----------------

Наполнение топика на 10.6.0.22 - получение данных с zenoss Красноярска

Назначенние: обмен записями событий zenoss Красноярска


 Просмотр сообщений топика
 ::
 
    /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server 10.6.0.88:9092 --from-beginning --topic zenoss-krsk




Топик zenoss-irk
----------------

Наполнение топика на 10.6.0.22 - получение данных с zenoss Иркутска

Назначенние: обмен записями событий zenoss Иркутска


 Просмотр сообщений топика
 ::
 
    /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server 10.6.0.88:9092 --from-beginning --topic zenoss-irk


Топик zenoss-chi
----------------

Наполнение топика на 10.6.0.22 - получение данных с zenoss Читы

Назначенние: обмен записями событий zenoss Читы


 Просмотр сообщений топика
 ::
 
    /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server 10.6.0.88:9092 --from-beginning --topic zenoss-chi




Ключевый изменения в server.properties
--------------------------------------

 ::
 
    num.network.threads=16
    num.io.threads=32
