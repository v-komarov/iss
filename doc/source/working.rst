.. contents:: Оглавление
    :depth: 3


Учет рабочего времени (working) и сбор логов CDR
================================================



Схема поступления CDR данных
----------------------------

.. figure:: _static/cdr.jpeg
       :scale: 30 %
       :align: center
       :alt: Схема поступления CDR данных


Описание компонентов схемы
--------------------------


AVAYA
~~~~~

Отпраляет CDR данные на конкретный ip адрес и порт (10.6.0.88:11111)
Настраивается из интерфейса управления.


Asterisk
~~~~~~~~

Запущен отдельный процесс из командной строки для чтения логов asterisk-а и отправки CDR данных на конкретный адрес и порт (10.6.0.88:11112)

 Команда
 ::
 
    tail -f /var/log/asterisk/cdr-csv/Master.csv|nc 10.6.0.22 11112
    
Модуль 1    
~~~~~~~~

Служба реализована как компонент **xinetd** (10.6.0.88)

 phone
 ::
 
    [root@memcache ~]# cat /etc/xinetd.d/phone
    service phone
    {
        disable = no
        type = UNLISTED
        socket_type = stream
        port = 11111
        wait = no
        user = root
        server = /srv/phone.py
    }
        


 phone.py
 ::
 
    #!/usr/bin/python
    #coding:utf-8
    
    import sys
    import json
    from kafka import KafkaProducer
    
    ### kafka
    ka_host = ['10.6.0.88:9092']
    producer = KafkaProducer(bootstrap_servers=ka_host)
    queue = 'avaya'
    
    
    while True:
        line = sys.stdin.readline().strip()
        if line == "":
            break
        else:
    
            producer.send(queue, line)
            producer.flush()
    


Модуль 2    
~~~~~~~~

Служба реализована как компонент **xinetd** (10.6.0.88)

 phone2
 ::
 
    [root@memcache ~]# cat /etc/xinetd.d/phone2
    service phone2
    {
        disable = no
        type = UNLISTED
        socket_type = stream
        port = 11112
        wait = no
        user = root
        server = /srv/phone2.py
    }
    
 phone2.py
 ::
 
    #!/usr/bin/python
    #coding:utf-8
    
    import sys
    import json
    from kafka import KafkaProducer
    
    ### kafka
    ka_host = ['10.6.0.88:9092']
    producer = KafkaProducer(bootstrap_servers=ka_host)
    queue = 'asterisk'
    
    
    while True:
        line = sys.stdin.readline().strip()
        if line == "":
            break
        else:
    
            producer.send(queue, line)
            producer.flush()
    

Модуль 3
~~~~~~~~

Кластер брокера сообщений - kafka (10.6.0.88, 10.6.0.22, 10.6.0.135)


Модуль 4
~~~~~~~~

 Процесс
 ::
 
    root@iss:~# cat /srv/django/iss/get_avaya_log.sh
    #!/bin/sh
    
    cd /srv/django/iss
    
    /usr/bin/python manage.py get_avaya_log

 Команда запуска
 ::
 
    systemctl start screen-avaya
    

Модуль 5
~~~~~~~~

 Процесс
 ::
 
    root@iss:~# cat /srv/django/iss/get_asterisk_log.sh
    #!/bin/sh
    
    cd /srv/django/iss
    
    /usr/bin/python manage.py get_asterisk_log

 Команда запуска
 ::
 
    systemctl start screen-asterisk
    
Модуль 6
~~~~~~~~

 Процесс
 ::
 
    root@iss:~# cat /srv/django/iss/calls_worker.sh 
    #!/bin/sh
    
    cd /srv/django/iss
    
    /usr/bin/python manage.py phone_calls
    

 Команда запуска
 ::
 
    systemctl start screen-worker
    

