# -*- coding: utf-8 -*-
# Идеи:
# Memcached, Redis, Mongo, CouchDB
# инициатива в выборе какой-то другой СУБД - приветствуется

# Source dataset:
# Rohit Kulkarni (2017), A Million News Headlines [CSV Data file], doi:10.7910/DVN/SYBGZL, Retrieved from: https://www.kaggle.com/therohk/million-headlines

"""
Механизм работы:
1. Перед стартом сервера полная очистка БД, пересоздание, загрузка всех данных ( SqliteDB.add() ). 
Можно строки передавать напрямую из архива (модуль zip). Структура БД произвольная.
2. Записи, выбираемые из БД сохраняются в промежуточный кэш на время, указанное в настройках (по умолчанию 5 000 миллисекунд)
3. Если запись не найдена в кэше, идёт обращение в БД, сохранение в кэш. 
4. Если запись в кэше устарела, в кэш сохраняется новая запись из БД
5. Если запрошенной записи в БД нет - возвращается 'error'


Тестирование:
1. Запускается на Linux сервере, даётся пауза для загрузки.
2. Apache AB: Сто тысяч запросов / - для получения минимального времени
3. Apache AB: Сто тысяч запросов /rand/ - для получения максимального времени
4. Серия из 3,5,9 секунд непрерывных запросов к 10 произвольно выбранным датам /bydate/
5. Серия из 3,5,9 секунд непрерывных запросов к /stat/
В пределах каждой СУБД победителем будет тот, чьё суммарное среднее время ответов меньше всего. Если таких двое - побеждает первый приславший.
4 СУБД (или больше) - 4 победителя (или больше).

https://ru.stackoverflow.com/questions/443608/singleton-%D0%BD%D0%B0-python
"""

from bottle import Bottle, run, request, template, get, post
import json
import sqlite3

HOST = '0.0.0.0'
PORT = '54321'

app = Bottle()

class SqliteDb:
    connection = None
    default_db = ''

    def __init__(self, db_file=None):
        if db_file:
            self.default_db = '../06.db'
        else:
            self.default_db = db_file

        self.connection = sqlite3.connect
        #todo?

    def add(self, row):        
        pass
    
    def get(self,rowid):
        pass

    def get_by(self,date):
        pass

    def delete(self,rowid):
        pass

    def rand(self):
        #TODO return rows for random day
        pass
    
    def stat(self):
        #TODO sql query like:
        # SELECT date_of_news, count(*) FROM news GROUP BY date_of_news ORDER BY date_of_news
        pass

class NoSQLCache:
    connection = None
    sql_connection = None # object of class SqliteDB
    timeout = 5000

    def __init__(self, sql_db_object):
        pass

    def get(self, key, timeout):
        """timeout in ms"""
        pass

    def set(self, key,value,timeout):
        pass


@app.get('/')
def index():
    return 'ok'

@app.get('/bydate/<date>')
def bydate(date):
    j = ''
    """JSON ENCODED: '[{"id": 1, "date": "2018-03-01", "title": "test1"}, {"id": 2, "date": "2018-03-02", "title": "test2"}]' """
    return j 

@app.get('/rand/')
def rand():
    j=''
    """JSON ENCODED: '[{"id": 1, "date": "2018-03-01", "title": "test1"}, {"id": 2, "date": "2018-03-02", "title": "test2"}]' """
    return  j

@app.get('/stat/')
def stat():
    j=''
    """JSON ENCODED: '[{"id": 1, "date": "2018-03-01", "count": 100}, {"id": 2, "date": "2018-03-02", "count": 7}]' """
    return j


def load_to_DB(file_name="million-headlines.zip"):
    pass

if __name__ == "__main__":  
    load_to_DB()

    run(app, host=HOST, port=PORT, reloader=True, debug=True)
