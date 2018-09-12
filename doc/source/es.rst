

.. contents:: Оглавление
    :depth: 3


ElasticSearch
=============



:Elasticsearch: поисковый движок с json rest api, использующий Lucene и написанный на Java


Адрес http://10.6.0.88:9200

 Ответ от сервера
 ::

    vak@dev-point:~$ curl -X GET http://10.6.0.88:9200
    {
      "status" : 200,
      "name" : "Gateway",
      "cluster_name" : "elasticsearch",
      "version" : {
        "number" : "1.5.2",
        "build_hash" : "62ff9868b4c8a0c45860bebb259e21980778ab1c",
        "build_timestamp" : "2015-04-27T09:21:06Z",
        "build_snapshot" : false,
        "lucene_version" : "4.10.4"
      },
      "tagline" : "You Know, for Search"
    }
    



Основные действия с индексом (аналог базы)
------------------------------------------

Название индекса **iss2**




Создание индекса
~~~~~~~~~~~~~~~~
 
 ::
 
    vak@dev-point:~$ curl -X POST 'http://10.6.0.88:9200/iss2'
    {"acknowledged":true} 
     

Открытие индекса
~~~~~~~~~~~~~~~~

 ::

    vak@dev-point:~$ curl -X POST 'http://10.6.0.88:9200/iss2/_open'
    {"acknowledged":true}
    

Остановка индекса перед изменениями
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
 ::
 
    vak@dev-point:~$ curl -X POST 'http://10.6.0.88:9200/iss2/_close'
    {"acknowledged":true} 
    

Удаление индекса
~~~~~~~~~~~~~~~~
 
 ::
 
    vak@dev-point:~$ curl -X DELETE 'http://10.6.0.88:9200/iss2/'
    {"acknowledged":true} 


Просмотр содержимого одного элемента
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
 ::
 
    vak@dev-point:~$ curl -X GET 'http://10.6.0.88:9200/iss2/device/1/_source?pretty'
     


Просмотр содержимого всего индекса
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
 ::
 
    vak@dev-point:~$ curl -X GET 'http://10.6.0.88:9200/iss2/_search?pretty'
     


Просмотр содержимого конкретного типа документа
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
 ::
 
    vak@dev-point:~$ curl -X GET 'http://10.6.0.88:9200/iss2/device/_search?pretty'



Пример поиска по конкретному полю **name**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
 ::
 
    vak@dev-point:~$ curl -X GET 'http://10.6.0.88:9200/iss2/device/_search?q=+name:DGS&pretty=true'

    {
      "took" : 4,
      "timed_out" : false,
      "_shards" : {
        "total" : 5,
        "successful" : 5,
        "failed" : 0
      },
      "hits" : {
        "total" : 15,
        "max_score" : 3.036022,
        "hits" : [ {
          "_index" : "iss2",
          "_type" : "device",
          "_id" : "63",
          "_score" : 3.036022,
          "_source":{"synonyms": [], "id": 63, "name": "DGS-3120-24SC"}
        }, {
          "_index" : "iss2",
          "_type" : "device",
          "_id" : "31",
          "_score" : 2.8301446,
          "_source":{"synonyms": [], "id": 31, "name": "DGS-3200-10/C1"}
        }, {
          "_index" : "iss2",
          "_type" : "device",
          "_id" : "48",
          "_score" : 2.8301446,
          "_source":{"synonyms": [], "id": 48, "name": "DGS-3610-26G"}
        }, {
          "_index" : "iss2",
          "_type" : "device",
          "_id" : "47",
          "_score" : 2.6878784,
          "_source":{"synonyms": [], "id": 47, "name": "DGS-3200-10/B1"}
        }, {
          "_index" : "iss2",
          "_type" : "device",
          "_id" : "59",
          "_score" : 2.6878784,
          "_source":{"synonyms": [], "id": 59, "name": "DGS-3420-26SC"}
        }, {
          "_index" : "iss2",
          "_type" : "device",
          "_id" : "16",
          "_score" : 2.6878784,
          "_source":{"synonyms": [], "id": 16, "name": "DGS-1100-06/ME"}
        }, {
          "_index" : "iss2",
          "_type" : "device",
          "_id" : "58",
          "_score" : 2.5763068,
          "_source":{"synonyms": [], "id": 58, "name": "DGS-3420-28SC"}
        }, {
          "_index" : "iss2",
          "_type" : "device",
          "_id" : "65",
          "_score" : 2.5763068,
          "_source":{"synonyms": [], "id": 65, "name": "DGS-3000-26TC"}
        }, {
          "_index" : "iss2",
          "_type" : "device",
          "_id" : "46",
          "_score" : 2.5763068,
          "_source":{"synonyms": [], "id": 46, "name": "DGS-3100-24TG"}
        }, {
          "_index" : "iss2",
          "_type" : "device",
          "_id" : "64",
          "_score" : 2.4882808,
          "_source":{"synonyms": [], "id": 64, "name": "DGS-3120-24TC"}
        } ]
      }
    }


Пример обновления одного поля **synonyms** в конкретном документе
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
 ::
 
     curl -X PUT 'http://10.6.0.88:9200/iss2/device/63/' -d '{ "doc": {"synonyms":["321"]}}'
    
    
Вариант формата документа 
-------------------------

 Пример для синонимов названия оборудования
 ::
 
    {
        "model": 25,
        "name": "DES-1210-10/ME",
        "synonyms": [
            "1210",
            "1210-10",
            "DES-1210-10",
            "DES1210",
            "DES-1210-10/ME",
            "DES1210-10/ME"
        ]
    
    
    }



Примеры для Python
------------------


 Пример загрузки улиц (python):
 ::

    from elasticsearch import Elasticsearch
    es = Elasticsearch(['http://10.6.0.88:9200'])
    ### Загрузка улиц        
    for street in address_street.objects.all():
        data = {
            'id': street.id,
            'name': street.name
        }
        res = es.index(index="iss2", doc_type='street', id=street.id, body=data)
        es.indices.refresh(index="iss2")





 Пример поиска улицы (python):
 ::


    q = {"query": {"fuzzy": {"name": "Телевызорная"}}}
    res = es.search(index="iss2", doc_type="street", body=q)
    for hit in res['hits']['hits']:
        print("%(name)s" % hit["_source"])







