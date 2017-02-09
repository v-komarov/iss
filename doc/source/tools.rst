.. contents:: Оглавление
    :depth: 2



Вспомогательные утилиты
=======================


zenapitool
----------

.. index:: zenoss

Утилита формирования запросов командной строки к базе zenoss

`github : zenapitool <https://github.com/k-vinogradov/zenapitool/>`_

Пример: выборка всех сетевых устройств
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 ::

    python zenapitool.py device-list -p "/Devices/Network" -c icCV -f table  -w device_list.txt


 ::

    IP Address       Device Class                                        SNMP Community         SNMP Version
    ---------------  --------------------------------------------------  ---------------------  --------------
    10.207.2.28      /Network/VoIP                                       sibttklocal            v2c
    10.207.5.84      /Network/VoIP                                       private                v2c
    10.207.5.91      /Network/VoIP                                       sibttklocal            v2c
    10.8.1.1         /Network/VoIP                                       private                v2c
    10.8.1.3         /Network/VoIP                                       sibttklocal            v2c
    10.8.1.4         /Network/VoIP                                       private                v2c
    10.8.1.9         /Network/VoIP                                       sibttklocal            v2c
    10.8.1.16        /Network/VoIP                                       sibttklocal            v2c
    10.8.1.34        /Network/VoIP                                       private                v2c
    10.8.1.41        /Network/VoIP                                       sibttklocal            v2c
    10.8.1.45        /Network/VoIP                                       sibttklocal            v2c
    10.8.1.47        /Network/VoIP                                       sibttklocal            v2c
    10.8.1.48        /Network/VoIP                                       sibttklocal            v2c
    10.8.1.50        /Network/VoIP                                       sibttklocal            v2c
    10.8.1.51        /Network/VoIP                                       sibttklocal            v2c
    10.8.1.52        /Network/VoIP                                       sibttklocal            v2c
    10.8.1.114       /Network/VoIP                                       private                v2c
    10.208.8.35      /Network/VoIP                                       private                v2c
    10.208.9.11      /Network/VoIP                                       private                v2c
    10.208.9.84      /Network/VoIP                                       private                v2c
    10.208.10.202    /Network/VoIP                                       sibttklocal            v2c
    10.208.28.23     /Network/VoIP                                       sibttklocal            v2c
    10.208.130.15    /Network/Switch/D-Link/DES 3028 Series/FTTB Access  sibttklocal            v2c
    10.208.130.16    /Network/Switch/D-Link/DES 3028 Series/FTTB Access  sibttklocal            v2c
    10.208.130.17    /Network/Switch/D-Link/DES 3028 Series/FTTB Access  sibttklocal            v2c
    10.208.130.11    /Network/Switch/D-Link/DES 3028 Series/FTTB Access  sibttklocal            v2c
    10.208.130.12    /Network/Switch/D-Link/DES 3028 Series/FTTB Access  sibttklocal            v2c
    10.208.130.13    /Network/Switch/D-Link/DES 3028 Series/FTTB Access  sibttklocal            v2c
    10.208.130.18    /Network/Switch/D-Link/DES 3028 Series/FTTB Access  sibttklocal            v2c
    10.208.130.14    /Network/Switch/D-Link/DES 3028 Series/FTTB Access  sibttklocal            v2c
    10.208.130.22    /Network/Switch/D-Link/DES 3028 Series/FTTB Access  sibttklocal            v2c
    10.208.130.21    /Network/Switch/D-Link/DES 3028 Series/FTTB Access  sibttklocal            v2c
    10.208.130.23    /Network/Switch/D-Link/DES 3028 Series/FTTB Access  sibttklocal            v2c




Пример: выборка всех TV устройств
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 ::

    python zenapitool.py device-list -p "/Devices/TV" -c icCV -f table  -w device_list.txt

 ::

    IP Address       Device Class                SNMP Community    SNMP Version
    ---------------  --------------------------  ----------------  --------------
    10.247.0.146     /TV/TrCATV/220-60-C         sibttk            v2c
    10.247.0.147     /TV/TrCATV/220-60-C         sibttk            v2c
    192.168.18.91    /TV/Anevia Flamingo 660     sibttklocal       v2c
    192.168.18.92    /TV/Anevia Flamingo 660     sibttklocal       v2c
    192.168.17.91    /TV/Anevia Flamingo 660     sibttklocal       v2c
    192.168.17.92    /TV/Anevia Flamingo 660     sibttklocal       v2c
    192.168.17.93    /TV/Anevia Flamingo 660     sibttklocal       v2c
    192.168.16.91    /TV/Anevia Flamingo 660     sibttklocal       v2c
    192.168.16.92    /TV/Anevia Flamingo 660     sibttklocal       v2c
    192.168.16.93    /TV/Anevia Flamingo 660     sibttklocal       v2c
    192.168.117.91   /TV/Anevia Flamingo 660     sibttklocal       v2c
    192.168.117.92   /TV/Anevia Flamingo 660     sibttklocal       v2c
    9.208.131.45     /TV/ONTF20-A10/Pin 1        sibttk            v2c
