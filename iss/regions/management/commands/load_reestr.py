#coding:utf8

import csv
import decimal
from django.core.management.base import BaseCommand, CommandError

from iss.localdicts.models import regions, address_city
from iss.regions.models import reestr


krsk = regions.objects.get(name='Красноярск')
irk = regions.objects.get(name='Иркутск')
chi = regions.objects.get(name='Чита')




class Command(BaseCommand):
    args = '< >'
    help = 'Загрузка ререстра по регионам'


    ### Отлов из строки цифр и преобразование в Decimal
    def to_decimal(self, num_str):

        num_str.replace(",", ".")
        result = []
        for i in list(num_str):
            if i in ['0','1','2','3','4','5','6','7','8','9','.']:
                result.append(i)
        result = "".join(result)
        if len(result) > 1 and result[0] == ".":
            result = "0"+result

        return decimal.Decimal(result) if len(result) > 0 else decimal.Decimal('0.00')






    def handle(self, *args, **options):

        """

        :param args:
        :param options:
        :return:
        """

        cities = {
            'Карымская': 'Карымское',
            'Карымская-Забайкальск': 'Карымское',
            'Майская,Набережная,Нижняя': 'Майская',
            'Сковородино- Архара': 'Сковородино',
            'Сковородино - Архара  Забайкальской ж.д': 'Сковородино',
            'Забайкальская ж.д.': '',
            'Забайкальской ж. д.': '',
            'Склад': '',
            'Иркутск - Тында - Тайшет - Входная': 'Иркутск',
            'Карымская, Сковородино': 'Карымская',
            'Сковородино - Карымская': 'Сковородино',
            'Чита ЗИП': 'Чита',
            'Чита 2': 'Чита',
            'Чита (Карымская)': 'Чита',
            'Шилка ЗИП': 'Шилка',
            'Новопавловка - Забайкальск':'Новопавловка'
        }

        reestr.objects.all().delete()

        with open('iss/regions/csv/reestr.csv') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=";", quotechar='"')
            next(spamreader, None)
            for row in spamreader:
                city = row[4].strip()

                city = cities[city] if cities.has_key(city) else city



                if not address_city.objects.filter(name__icontains=city).exists():
                    print city
                    address_city.objects.create(name=city)

                c = address_city.objects.filter(name__icontains=city).first()
                #print row[13].strip()
                reestr.objects.create(
                    region = chi,
                    god_balans = row[1].strip(),
                    original = row[2].strip(),
                    net = row[3].strip(),
                    city = c,
                    invnum = row[5].strip(),
                    project_code = row[6].strip(),
                    start_date = row[7].strip(),
                    ed_os = row[8].strip(),
                    name = row[9].strip(),
                    comcode = row[10].strip(),
                    serial = row[11].strip(),
                    nomen = row[12].strip(),
                    ed = row[13].strip(),
                    count = self.to_decimal(row[14].strip()),
                    price = self.to_decimal(row[15].strip()),
                    rowsum = self.to_decimal(row[14].strip()) * self.to_decimal(row[15].strip()),
                    actos1 = row[17].strip(),
                    group = row[18].strip(),
                    age = row[19].strip(),
                    address = row[20].strip(),
                    dwdm = row[21].strip(),
                    tdm = row[22].strip(),
                    sdh = row[23].strip(),
                    ip = row[24].strip(),
                    atm = row[25].strip(),
                    emcs = row[26].strip()
                )
