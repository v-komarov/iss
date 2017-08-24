#coding:utf-8



from __future__ import unicode_literals


import uuid

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField


### Разделы тестирования
class sections(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Раздел')

    def __unicode__(self):
        return self.name



### Вопросы тестирования
class questions(models.Model):
    name = models.TextField(verbose_name='Вопрос')
    section = models.ForeignKey(sections, null=True, on_delete=models.PROTECT, verbose_name='Раздел')
    literature = models.CharField(max_length=250, default="", verbose_name='Литература')

    def __unicode__(self):
        return self.name


    ### Возвращает список id правильных ответов
    def get_truth_id_list(self):

        result = []
        for i in self.answers_set.all().filter(truth=True):
            result.append(i.id)

        return result


    ### Возвращает список пунктов правильных ответов
    def get_truth_html(self):

        result = "<ul>"
        for i in self.answers_set.all().filter(truth=True):
            result += "<li>{name}</li>".format(name=i.name)

        return result + "</ul>"

    ### Возвращает список вопросов
    def get_answers_html(self):

        result = ""
        for i in self.answers_set.all().order_by("?"):
            result += "<tr answer_id={id}><td width=\"10%\"><input answer type=\"checkbox\"></td><td>{name}</td></tr>".format(name=i.name, id=i.id)

        return result






### Ответы тестирования
class answers(models.Model):
    name = models.TextField(verbose_name='Ответ')
    question = models.ForeignKey(questions, null=True, on_delete=models.CASCADE, verbose_name='Связь с вопросом')
    truth = models.BooleanField(default=False, verbose_name='Правильный ответ')

    def __unicode__(self):
        return self.name





### Тесты
class tests(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название теста')
    section = models.ForeignKey(sections, null=True, on_delete=models.PROTECT, verbose_name='Раздел')
    questions = models.ManyToManyField(questions)
    testtime = models.IntegerField(default=0, verbose_name='Продолжительность теста в минутах')
    mistakes = models.IntegerField(default=0, verbose_name='Максимальное количество ошибок для сдачи')
    learning = models.BooleanField(default=False, verbose_name='Доступен для тренировки, обучения')

    def __unicode__(self):
        return self.name

    ### Возвращает словарь вопросов
    def questions_dict(self):

        questions_dict = []

        for item in self.questions.all():

            questions_dict.append({
                item.id: item.name
            })


        return questions_dict



### Результаты обучения и прохождения теста
class tests_results(models.Model):
    test = models.ForeignKey(tests, null=True, on_delete=models.PROTECT, verbose_name='Тест', db_index=True)
    begin = models.DateTimeField(null=True, verbose_name='Начало теста')
    end = models.DateTimeField(null=True, verbose_name='Окончание теста')
    passed = models.BooleanField(default=False, db_index=True, verbose_name='Тест пройден')
    job = models.CharField(max_length=100, default="", verbose_name='Должность')
    worker = models.CharField(max_length=100, default="", verbose_name='ФИО')
    department = models.CharField(max_length=100, default="", verbose_name='Место работы')
    data = JSONField(default={'questions': [], 'mistakes': []}, verbose_name='Очередь id вопросов')
    learning = models.BooleanField(default=True, db_index=True, verbose_name='Обучение или экзамен')
    mistakes = models.IntegerField(default=0, verbose_name='Количество ошибок')

    def __unicode__(self):
        return self.test.name


    ### Возвращает один id вопроса и удаляет из списка
    def get_question_id(self):

        data = self.data

        if len(data["questions"]) == 0:
            return None
        else:
            q = data["questions"].pop()
            self.data = data
            self.save()

            return q



    ### Регистрация id вопросов с ошибкой
    def set_errors(self, q):

        data = self.data

        if q not in data["mistakes"]:
            data["mistakes"].append(q)

        self.data = data
        self.save()

        return "ok"



    ### Возвращает список ip вопросов
    def get_question_list(self):

        return self.data["questions"]

