#coding:utf-8



import datetime

from django.contrib.auth.models import User

from iss.localdicts.models import blocks, init_reestr_proj, address_companies, stages
from iss.regions.models import reestr_proj_exec_date, stages_history






### Фильтрация для реестра проектов
def reestr_proj_filter(data,filter_dict):

    ### Поиск по тексту
    if filter_dict["search_text"] != "":
        data = data.filter(search_index__icontains=filter_dict["search_text"])



    ### Инициатор
    if filter_dict["initiator"] != "":
        initiator = init_reestr_proj.objects.get(pk=int(filter_dict["initiator"]))
        data = data.filter(proj_init=initiator)


    ### Реализатор
    if filter_dict["real"] != "":
        real = address_companies.objects.get(pk=int(filter_dict["real"]))
        data = data.filter(executor=real)

    ### Стадия проекта
    if filter_dict["stage"] != "":
        stage = stages.objects.get(pk=int(filter_dict["stage"]))
        data = data.filter(stage=stage)



    ### Стадию установил
    if filter_dict["stage_chif"] != "":
        chif = User.objects.get(pk=int(filter_dict["stage_chif"]))
        data = data.filter(stage_user=chif)


    ### Стадия установлена с
    if filter_dict["stage_date1"] != "":
        data = data.filter(stage_date__gte=datetime.datetime.strptime(filter_dict["stage_date1"],"%d.%m.%Y"))


    ### Стадия установлена до
    if filter_dict["stage_date2"] != "":
        data = data.filter(stage_date__lte=datetime.datetime.strptime(filter_dict["stage_date2"], "%d.%m.%Y"))


    ### Исполнитель
    if filter_dict["executor"] != "":
        executor = User.objects.get(pk=int(filter_dict["executor"]))
        data = data.filter(reestr_proj_exec_date__worker=executor)


    ### Подразделение
    if filter_dict["department"] != "":
        block = blocks.objects.get(pk=int(filter_dict["department"]))
        data = data.filter(reestr_proj_exec_date__block=block)


    ### Исполнитель с даты
    if filter_dict["executor_date1"] != "":
        data = data.filter(reestr_proj_exec_date__date1__gte=datetime.datetime.strptime(filter_dict["executor_date1"],"%d.%m.%Y"))


    ### Исполнитель по дату
    if filter_dict["executor_date2"] != "":
        data = data.filter(reestr_proj_exec_date__date2__lte=datetime.datetime.strptime(filter_dict["executor_date2"],"%d.%m.%Y"))



    ### Создан позднее чем
    if filter_dict["create_date1"] != "":
        data = data.filter(date_create__gte=datetime.datetime.strptime(filter_dict["create_date1"],"%d.%m.%Y"))


    ### Создан ранее чем
    if filter_dict["create_date2"] != "":
        data = data.filter(date_create__lte=datetime.datetime.strptime(filter_dict["create_date2"],"%d.%m.%Y"))



    ### Связь с другими системами
    if filter_dict["systems"] != "":
        data = data.filter(data__icontains=filter_dict["systems"])



    return data.distinct()