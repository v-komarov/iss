

.. contents:: Оглавление
    :depth: 3


Spark
=====


:spark:  фреймворк с открытым исходным кодом для реализации распределённой обработки неструктурированных и слабоструктурированных данных, входящий в экосистему проектов Hadoop


В настоящее время настроен только один экземпляр spark (в режиме **standalone**) на **10.6.0.88**


 Пример чтения файла из hdfs хранилища (в оболочке pyspark)
 ::
 
    >>> lines = sc.textFile("/krasnoyarsk/device-last-full.csv")
    >>> list = lines.collect()
    >>> for line in list:
    >>>     print line
    2018-08-21;55.18.11.31;krsk-4-sa1x209-18t11t31p1;krsk-4-sa1x209-18t11t31p1;Krasnoyarsk, Miroshnichenko, 4;/Krasnoyarsk/    
    Miroshnichenko/4;/Network/Switch/D-Link/DES-3200-10_C1/Any Ports;['/TMA 02/Segment 209/Ring 03'];['/Switch
    Access'];IV;R3J11E6000840;Production;DES-3200-10/C1 Fast Ethernet Switch
    2018-08-21;55.33.70.46;abk-4-ctvr1x57-33t70t46p8;abk-4-ctvr1x57-33t70t46p8;Abakan, Torosova, 2;/Abakan/Torosova/2;/TV/ONTF20-  
    A10/Pin 1;['/TMA 08/Segment 057/Ring 04'];['/CTVr'];IV;104K-41109350;Production;ONTF20-A10.14
    2018-08-21;55.34.66.55;cher-4-ctvr1x143-34t66t55p6;cher-4-ctvr1x143-34t66t55p6;Chernogorsk, Kosmonavtov, 3;/Chernogorsk/    
    Kosmonavtov/3;/TV/ONTF20-A10/Pin 1;['/TMA 09/Segment 143/Ring 05'];['/CTVr'];IV;104K-41120824;Production;ONTF20-A10.14
    2018-08-21;192.168.117.101;les-1-ctvh2x619-appear;les-1-ctvh2x619-appear;;/Lesosibirsk/Entuziastov/12a;/TV/AppearTV;['/TMA  
    11'];['/CTVh'];I;123100387;Production
