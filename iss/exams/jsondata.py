# coding:utf-8

import json
import decimal
import datetime
import random
import logging
import pickle

from pytz import timezone

from snakebite.client import Client

from django.http import HttpResponse, HttpResponseRedirect
from django import template
from django.contrib.auth.models import User

from iss.exams.models import questions, answers, tests, tests_results
from iss.exams.forms import AnswerForm




def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip






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
            ip = get_client_ip(request)

            ### Формирование и сохранение списка номеров вопросов
            questions_lists = []
            for x in t.questions.all().order_by("?"):
                questions_lists.append(x.id)



            ### Создание записи обучения
            res = tests_results.objects.create(
                test = t,
                begin = datetime.datetime.now(),
                ip = ip,
                data = {
                    'questions': questions_lists,
                    'mistakes': []
                }

            )

            ### Вопрос и список ответов
            question_id = res.get_question_id()
            if question_id:

                qu = questions.objects.get(pk=question_id)
                response_data = {"result": "next", "result_id": res.id, "question-name": qu.name, "answers": qu.get_answers_html(), "question_id": question_id, "question_list": res.get_question_list(), "questions_count": res.get_questions_count()}
            ### Пустой тест - без вопросов
            else:
                response_data = {"result": "end"}







        ### Следующий вопрос обучения
        if r.has_key("action") and rg("action") == 'learn-next':
            result_id = request.GET["result_id"]
            res = tests_results.objects.get(pk=int(result_id, 10))
            t = res.test

            qu = questions.objects.get(pk=int(request.GET["question_id"], 10))

            ### Список id ответов
            answer_list = [int(x ,10) for x in request.GET["answer_list"].split(",")]

            ### Сравнение - на правильность ответа
            if set(sorted(answer_list)) == (set(sorted(qu.get_truth_id_list()))):

                ### Подготовка данных следующего вопроса , если этот не последний
                question_id = res.get_question_id()
                if question_id:
                    quest = questions.objects.get(pk=question_id)
                    response_data = {"result": "next", "result_id": res.id, "question-name": quest.name,
                                     "answers": quest.get_answers_html(), "question_id": question_id, "questions_count": res.get_questions_count()}
                ### Тестирование завершено
                else:
                    res.end = datetime.datetime.now()
                    res.mistakes = len(res.data["mistakes"])

                    ### Проверка пройден тест или нет
                    if t.mistakes >= len(res.data["mistakes"]):
                        res.passed = True
                        response_data = {"result": "end", "mistakes": len(res.data["mistakes"]), "passed": "yes"}
                    else:
                        response_data = {"result": "end", "mistakes": len(res.data["mistakes"]), "passed": "no"}

                    res.save()


            ### Если ответ ошибочный
            else:
                res.set_errors(qu.id)
                response_data = {"result": "error", "truth": qu.get_truth_html(), "literature": qu.literature}





        ### Начало тестирования
        if r.has_key("action") and rg("action") == 'test-begin':

            test_id = request.GET["test_id"]
            t = tests.objects.get(pk=int(test_id, 10))
            fio = request.GET["fio"].strip()
            job = request.GET["job"].strip()
            department = request.GET["department"].strip()
            ip = get_client_ip(request)


            ### Проверка была ли сдача уже сегодня
            if tests_results.objects.filter(worker__icontains=fio,begin__date=datetime.datetime.now().date(),ip=ip).exists():

                response_data = {"result": "goaway"}

            else:

                ### Формирование и сохранение списка номеров вопросов
                questions_lists = []
                for x in t.questions.all().order_by("?"):
                    questions_lists.append(x.id)

                ### Создание записи тестирования
                res = tests_results.objects.create(
                    test=t,
                    worker=fio.strip(),
                    job=job.strip(),
                    department=department.strip(),
                    learning=False,
                    begin=datetime.datetime.now(),
                    ip=ip,
                    data={
                        'questions': questions_lists,
                        'mistakes': [],
                        'questions_dict': t.questions_dict()
                    }
                )


                ### Вопрос и список ответов
                question_id = res.get_question_id()
                if question_id:

                    qu = questions.objects.get(pk=question_id)
                    response_data = {"result": "next", "result_id": res.id, "question-name": qu.name,
                                     "answers": qu.get_answers_html(), "question_id": question_id,
                                     "question_list": res.get_question_list() }
                ### Пустой тест - без вопросов
                else:
                    response_data = {"result": "end"}






        ### Следующий вопрос тестирования
        if r.has_key("action") and rg("action") == 'test-next':
            result_id = request.GET["result_id"]
            res = tests_results.objects.get(pk=int(result_id, 10))
            t = res.test

            qu = questions.objects.get(pk=int(request.GET["question_id"], 10))

            ### Список id ответов
            answer_list = [int(x, 10) for x in request.GET["answer_list"].split(",")]

            ### Сравнение - на правильность ответа
            if set(sorted(answer_list)) != (set(sorted(qu.get_truth_id_list()))):
                ### Если ответ ошибочный
                res.set_errors(qu.id)


            ### Подготовка данных следующего вопроса , если этот не последний
            question_id = res.get_question_id()
            if question_id:
                quest = questions.objects.get(pk=question_id)
                response_data = {"result": "next", "result_id": res.id, "question-name": quest.name,
                                 "answers": quest.get_answers_html(), "question_id": question_id, "questions_count": res.get_questions_count()}
            ### Тестирование завершено
            else:
                res.end = datetime.datetime.now()
                res.mistakes = len(res.data["mistakes"])


                ### Проверка пройден тест или нет по количеству ошибок
                if t.mistakes >= len(res.data["mistakes"]):
                    res.passed = True
                    response_data = {"result": "end", "mistakes": len(res.data["mistakes"]), "passed": "yes"}
                else:
                    response_data = {"result": "end", "mistakes": len(res.data["mistakes"]), "passed": "no"}
                res.save()


                ### перечитать данные записи
                res = tests_results.objects.get(pk=int(result_id, 10))
                ### Проверка превышения времени
                if t.testtime == 0:
                    ## Без лимита времени
                    response_data["overtime"] = "no"
                else:
                    ### Определение превышин ли лимит
                    if int((res.end - res.begin).total_seconds() // 60) > t.testtime:
                        ### При превышении лимита времени
                        res.passed = False
                        res.save()
                        ### Лимит времени превышен
                        response_data["overtime"] = "yes"
                        response_data["passed"] = "no"
                    else:
                        ### Превышения лимита не было
                        response_data["overtime"] = "no"






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





        ### Добавить или удалить элемент в список отчета
        if r.has_key("action") and rg("action") == 'report':

            row_id = int(request.GET["row_id"],10)
            status = request.GET["status"]

            if request.session.has_key("reportlist") and status == "yes":
                a = request.session["reportlist"]
                if row_id not in a:
                    a.append(row_id)
                    request.session["reportlist"] = a

            elif request.session.has_key("reportlist") and status == "no":
                a = request.session["reportlist"]
                if row_id in a:
                    a.remove(row_id)
                    request.session["reportlist"] = a
            elif request.session.has_key("reportlist") == False and status == "yes":
                request.session["reportlist"] = [row_id]



            response_data = {"result": "ok"}





        ### Удаление списка для вывода в отчет
        if r.has_key("action") and rg("action") == 'report-clear':

            if request.session.has_key("reportlist"):
                del request.session["reportlist"]


            response_data = {"result": "ok"}



        ### Данные результата
        if r.has_key("action") and rg("action") == 'get-data-result':
            result_id = request.GET["result_id"]
            result = tests_results.objects.get(pk=int(result_id, 10))

            response_data = {"result": "ok", "job": result.job, "department": result.department, "worker": result.worker}







    if request.method == "POST":


        data = eval(request.body)

        ### Сохранение общих данных вопроса
        if data.has_key("action") and data["action"] == 'question-save-common-data':

            q = questions.objects.get(pk=int(request.session['question_id'], 10))

            q.name = data["question"].strip()
            q.literature = data["literature"].strip()
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



        ### Сохранение должности и места работы
        if data.has_key("action") and data["action"] == 'save-result':

            result = tests_results.objects.get(pk=int(data["result_id"], 10))
            result.worker = data["worker"].strip()
            result.job = data["job"].strip()
            result.department = data["department"].strip()
            result.save()

            response_data = {"result": "ok"}





    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response

