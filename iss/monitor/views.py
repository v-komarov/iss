#coding:utf-8

from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db import connections
import datetime
import binascii


def event_list(request):

    data = []

    cursor = connections["zenoss_krsk"].cursor()
    cursor.execute("""
            SELECT
            first_seen,
            update_time,
            last_seen,
            summary,
            message,
            details_json,
            event_class.name,
            severity_id,
            uuid,
            element_identifier,
            element_sub_identifier,
            status_id
            FROM event_archive
            LEFT JOIN event_class ON event_archive.event_class_id=event_class.id
            LIMIT 100

            """)
    d = cursor.fetchall()


    for row in d:

        manager = ""
        device_class = ""
        device_group = ""
        device_net_address = ""
        device_location = ""
        device_system = ""


        arrayjson = eval(row[5])
        print arrayjson
        for item in arrayjson:
            if item['name'] == 'manager':
                manager = item['value']
            elif item['name'] == 'zenoss.device.ip_address':
                device_net_address = item['value']
            elif item['name'] == 'zenoss.device.location':
                device_location = item['value']
            elif item['name'] == 'zenoss.device.device_class':
                device_class = item['value']
            elif item['name'] == 'zenoss.device.groups':
                device_group = item['value']
            elif item['name'] == 'zenoss.device.systems':
                device_system = item['value']

        #.strftime('%d.%m.%Y %H:%M:%S')
        data.append(
            {
                'first_seen':datetime.datetime.fromtimestamp(int(row[0])/1000),
                'update_time':datetime.datetime.fromtimestamp(int(row[1])/1000),
                'last_seen':datetime.datetime.fromtimestamp(int(row[2])/1000),
                'event_class':row[6],
                'severity_id':row[7],
                'manager':manager,
                'device_net_address':device_net_address,
                'device_location':device_location,
                'device_class':device_class,
                'device_group':device_group,
                'device_system':device_system,
                'uuid':binascii.b2a_hex(row[8]),
                'element_identifier':row[9],
                'element_sub_identifier':row[10],
                'status_id':row[11],
            }

        )

    template_name = "monitor/event_list.html"

    c = RequestContext(request,locals())
    return render_to_response(template_name, c)

