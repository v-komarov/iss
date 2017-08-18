# coding:utf-8

import json
import decimal
import datetime
import random
import logging

from pytz import timezone

from snakebite.client import Client

from django.http import HttpResponse, HttpResponseRedirect
from django import template
from django.contrib.auth.models import User

from iss.exams.models import questions, answers, tests, tests_results
from iss.exams.forms import AnswerForm




def get_json(request):

    ### Timezone
    tz = request.session['tz'] if request.session.has_key('tz') else 'UTC'


    response_data = {}

    if request.method == "GET":

        r = request.GET
        rg = request.GET.get


        ### Фильтр по разделу
        if r.has_key("action") and rg("action") == 'choice-section':
            section = request.GET["section"]
            if section != "0":
                request.session["exams-section"] = section
            else:
                del request.session["exams-section"]

            print section

            response_data = {"result": "ok"}




        ### Передача формы для создания нового варианта ответа
        if r.has_key("action") and rg("action") == 'get-data-create-answer':

            form = AnswerForm()
            t = template.Template("{{ form.as_table }}")
            c = template.Context({'form': form})
            f = t.render(c)

            response_data = {"result": "ok", "form":f}




        ### Передача формы редактирования варианта ответа
        if r.has_key("action") and rg("action") == 'get-data-edit-answer':
            a = answers.objects.get(pk=int(request.GET['answer_id'], 10))

            form = AnswerForm(instance=a)
            t = template.Template("{{ form.as_table }}")
            c = template.Context({'form': form})
            f = t.render(c)

            response_data = {"result": "ok", "form":f}




        ### Удаление вопроса
        if r.has_key("action") and rg("action") == 'delete-question':
            question_id = request.GET["question_id"]

            questions.objects.get(pk=int(question_id, 10)).delete()

            response_data = {"result": "ok"}




        ### Удаление теста
        if r.has_key("action") and rg("action") == 'delete-test':
            test_id = request.GET["test_id"]

            tests.objects.get(pk=int(test_id, 10)).delete()

            response_data = {"result": "ok"}





        ### Удаление варианта ответа
        if r.has_key("action") and rg("action") == 'delete-answer':
            answer_id = request.GET["answer_id"]

            answers.objects.get(pk=int(answer_id, 10)).delete()

            response_data = {"result": "ok"}




        ### Добавление или удаление вопроса из теста
        if r.has_key("action") and rg("action") == 'test-adding-remove-question':
            test_id = request.GET["test_id"]
            question_id = request.GET["question_id"]
            act = request.GET["act"]

            q = questions.objects.get(pk=int(question_id, 10))
            t = tests.objects.get(pk=int(test_id, 10))

            ### Добавление
            if act == "yes":
                t.questions.add(q)

            if act == "no":
                t.questions.remove(q)

            response_data = {"result": "ok"}




        ### Начало обучения
        if r.has_key("action") and rg("action") == 'learn-begin':
            test_id = request.GET["test_id"]
            t = tests.objects.get(pk=int(test_id, 10))

            ### Формирование и сохранение списка номеров вопросов
            questions_lists = [x.id for x in t.questions.order_by("?")]

            ### Создание записи обучения
            res = tests_results.objects.create(
                test = t,
                begin = datetime.datetime.now(),
                data = {
                    'questions': questions_lists,
                    'mistakes': []
                }

            )

            ### Вопрос и список ответов
            data = res.data
            quests_list = data["questions"]

            q = quests_list.pop()
            data["questions"] = quests_list
            res.data = data
            res.save()

            qu = questions.objects.get(pk=q)


            response_data = {"result": "next", "tests_result_id": res.id, "question-name": qu.name, "answers": qu.get_answers_html()}



        ### Следующий вопрос обучения
        if r.has_key("action") and rg("action") == 'learn-next':
            test_id = request.GET["test_id"]

            response_data = {"result": "next"}





        ### Отображение списка ответов по вопросу
        if r.has_key("action") and rg("action") == 'get-question-answers-list':
            question_id = request.GET["question_id"]

            q = questions.objects.get(pk=int(question_id, 10))

            rows = ""

            order = 1

            for i in q.answers_set.all().order_by('name'):
                t = template.Template("""<tr row_id={{ id }}>
                                        <td><a ans>{{ order }}</a></td>
                                        <td><a ans><input type=\"checkbox\" disabled {{ truth }} /></a></td>
                                        <td><a ans>{{ name }}</a></td>
                                        <td><a delete title=\"Удалить\"><span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span></a></td>
                                        <tr>""")
                c = template.Context({'id': i.id, 'order': order,
                                      'name': i.name,
                                      'truth': 'checked' if i.truth == True else ''
                                      })
                row = t.render(c)
                rows += row
                order += 1


            response_data = {"result": "ok", "rows": rows}






    if request.method == "POST":


        data = eval(request.body)

        ### Сохранение общих данных вопроса
        if data.has_key("action") and data["action"] == 'question-save-common-data':

            q = questions.objects.get(pk=int(request.session['question_id'], 10))

            q.name = data["question"].strip()
            q.save()

            response_data = {"result": "ok"}



        ### Создание варианта ответа
        if data.has_key("action") and data["action"] == 'create-answer-data':


            q = questions.objects.get(pk=int(data['question_id'], 10))
            name = data['name'].strip()
            truth = True if data['truth'] == "yes" else False
            answers.objects.create(name=name, question=q, truth=truth)


            response_data = {"result": "ok"}



        ### Редактирование варианта ответа
        if data.has_key("action") and data["action"] == 'edit-answer-data':

            a = answers.objects.get(pk=int(data['answer_id'], 10))

            a.name = data['name'].strip()
            a.truth = True if data['truth'] == "yes" else False
            a.save()

            response_data = {"result": "ok"}



        ### Сохранение общих данных теста
        if data.has_key("action") and data["action"] == 'test-save-common-data':

            t = tests.objects.get(pk=int(request.session['test_id'], 10))


            t.name = data["test"].strip()
            t.testtime = data["testtime"]
            t.mistakes = data["mistakes"]
            t.learning = True if data['learning'] == "yes" else False
            t.save()

            response_data = {"result": "ok"}



    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response

