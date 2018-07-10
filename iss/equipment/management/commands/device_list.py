#coding:utf8


from django.core.management.base import BaseCommand, CommandError
from iss.equipment.models import devices_ip,device_access_error,scan_iplist


from iss.inventory.models import devices



class Command(BaseCommand):
    args = '<graph ...>'
    help = 'get list of device'

    """
    Формирует список устройств в формате ip, serial, model, address
    Сохраняет в файл filename (передается как параметр)
    """

    def handle(self, *args, **options):

        filename = args[0]

        with open("iss/equipment/csv/%s" % filename, 'w') as f:

            for device in devices.objects.order_by("device_scheme__name"):
                ip = device.get_manage_ip()
                address = device.getaddress().encode("utf-8")
                try:
                    row = "{ip};{serial};{model};{address}\n".format(ip=u" ,".join(ip), model=device.device_scheme.name, serial=device.serial, address=address)
                    f.write(row)
                except:
                    print u"%s NOT SUCCESS" % device.serial

