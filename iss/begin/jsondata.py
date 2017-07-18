# coding:utf-8

import json
import random
import string

from django.http import HttpResponse, HttpResponseRedirect
from django import template
from django.contrib.auth.models import User
from django.core.mail import send_mail

from iss.begin.forms import NewUserForm




### Генерация пароля
def random_passwd():
  rid = ''
  for x in range(8): rid += random.choice(string.ascii_letters + string.digits)
  return rid





def get_json(request):


    response_data = {}

    if request.method == "GET":

        r = request.GET
        rg = request.GET.get


        ### Отображение пустой формы (добавление позиции) заказов
        if r.has_key("action") and rg("action") == 'new-user-form':
            form = NewUserForm()
            t = template.Template("{{ form.as_table }}")
            c = template.Context({'form': form})
            f = t.render(c)
            response_data = {"result": "ok", "form": f}




        ### Изменение пароля и отправка по email
        if r.has_key("action") and rg("action") == 'new-passwd':
            login = request.GET["login"]
            if User.objects.filter(username=login).exists():
                user = User.objects.get(username=login)
                ### Проверка есть ли email адрес
                if len(user.email) > 10 and user.email.find('@') != -1:
                    passwd = random_passwd()
                    user.set_password(passwd)
                    user.save()
                    send_mail('http://10.6.0.22:8000 was changed password', 'new password %s for login %s' % (passwd,login), 'GAMMA <gamma@sibttk.ru>', [user.email,])
                    response_data = {"result": "ok", "comment": u"Пароль изменен и отправлен<br>по адресу %s" % user.email }
                else:
                    response_data = {"result": "error", "comment": "Нет email адреса!"}

            else:
                response_data = {"result": "error", "comment": "Нет такой учетной записи!"}






    if request.method == "POST":


        data = eval(request.body)

        # Создание новой позиции заказа
        if data.has_key("action") and data["action"] == 'user-adding':
            login = data["login"]
            passwd = data["passwd"]
            email = data["email"]
            firstname = data["firstname"]
            lastname = data["lastname"]


            ### Проверка корректности данных
            #form = NewUserForm(initial={'login': login, 'passwd': passwd, 'email': email, 'firstname': firstname, 'lastname': lastname})

            #if form.is_valid():
            ### Валидация формы не работает - видимо форма без модели - в этом причина?
            if len(login) > 3 and len(passwd) > 7 and len(email) > 10 and email.find('@') != -1 and email.find('ttk') != -1 and len(firstname) > 2 and len(lastname) > 2:

                ### Проверка - есть ли уже такой логин
                if not User.objects.filter(username=login).exists():
                    user = User.objects.create_user(username=login, password=passwd, email=email, first_name = firstname, last_name = lastname)
                    response_data = {"result": "ok"}
                else:
                    response_data = {"result": "error", "comment": "Видимо такой пользователь уже есть!"}
            else:
                response_data = {"result": "error", "comment": "Не правильно заполнены поля формы!"}





    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response
