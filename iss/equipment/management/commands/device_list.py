#coding:utf8


from django.core.management.base import BaseCommand, CommandError
from iss.equipment.models import devices_ip,device_access_error,scan_iplist


from iss.inventory.models import devices



class Command(BaseCommand):
    args = '<graph ...>'
    help = 'get list of device'

    """
    Формирует список устройств в формате ip, serial, model, address, количество портов, количество слотов, количество комбо, количество занятых портов, процент занятых портов
    Сохраняет в файл filename (передается как параметр)
    """

    def handle(self, *args, **options):

        filename = args[0]

        with open("iss/equipment/csv/%s" % filename, 'w') as f:

            ### Заголовок
            f.write("Адрес;Модель;Сетевой элемент;Серийный номер;ip;портов;портов используемые;портов технологических;портов в резерве;комбо портов;комбо используется;комбо технологических;комбо в резерве;слотов;слотов используется;слотов в резерве;% использования\n")

            for device in devices.objects.order_by("address__city","address__street"):
                ip = device.get_manage_ip()
                address = device.getaddress().encode("utf-8")
                netelems = []
                for nel in device.get_netelems():
                    netelems.append(nel["name"])

                ports = device.get_ports_count()
                ports_use = device.get_use_ports()
                ports_tech = device.get_tech_ports()
                ports_reserv = device.get_reserv_ports()

                combo = device.get_combo_count()
                combo_use = device.get_use_combo()
                combo_tech = device.get_tech_combo()
                combo_reserv = device.get_reserv_combo()

                slots = device.get_slots_count()
                slots_use = device.get_use_slots()
                slots_reserv = device.get_reserv_slots()


                # Процент использования
                using = 0 if ports+combo+slots == 0 else int((ports_use + combo_use + slots_use)/float(ports + combo + slots) * 100)
                print "using: {} % ports : {} ports_use : {}".format(using,ports,ports_use)

                try:
                    row = "{address};{model};{netelem};{serial};{ip};{ports};{ports_use};{ports_tech};{ports_reserv};{combo};{combo_use};{combo_tech};{combo_reserv};{slots};{slots_use};{slots_reserv};{using}\n".format(
                        ip=u" ,".join(ip), model=device.device_scheme.name, serial=device.serial, address=address, netelem=", ".join(netelems),
                        ports = ports, ports_use = ports_use, ports_tech = ports_tech, ports_reserv = ports_reserv,
                        combo = combo, combo_use = combo_use, combo_tech = combo_tech, combo_reserv = combo_reserv,
                        slots = slots, slots_use=slots_use, slots_reserv=slots_reserv,  using = using
                    )
                    f.write(row)
                except:
                    print u"%s NOT SUCCESS" % device.serial

