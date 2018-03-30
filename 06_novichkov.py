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

Ипользуемая memcached http://downloads.northscale.com/memcached-1.4.5-amd64.zip
"""

from bottle import Bottle, run, request, template, get, post
import re
import json
import zipfile
import csv
import io
import sqlite3
from pymemcache.client.base import Client

HOST = '127.0.0.1'
PORT = '20321'

app = Bottle()


class SqliteDb:
    __instance = None

    @staticmethod
    def inst(db_file="file_name"):
        if SqliteDb.__instance == None:
            SqliteDb.__instance = SqliteDb(db_file)
        return SqliteDb.__instance

    def __init__(self, db_file):
        if db_file:
            self.default_db = '../06_novichkov.db'
            self.connection = sqlite3.connect(self.default_db)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()

    def add(self, rows):
        self.cursor.executemany("INSERT INTO million_headlines (publish_date,headline_text) VALUES (?,?)", rows)
        self.connection.commit()

    def get(self, query):
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        if rows:
            return list(map(dict, rows))
        else:
            return [{"response": "error"}]

    def get_by(self, date):
        key = "SELECT * FROM million_headlines WHERE publish_date='{}'".format(date)
        cache = NoSQLCache.inst()
        return cache.get(key)

    def delete(self, rowid):
        self.cursor.execute("DELETE FROM million_headlines WHERE id=?", (rowid,))
        self.connection.commit()

    def rand(self):
        self.cursor.execute("select * from million_headlines where id = (abs(random()) % (select (select max(id) from million_headlines)+1));")
        return self.get_by(dict(self.cursor.fetchone())['publish_date'])
        # TODO return rows for random day

    def stat(self):
        # TODO sql query like:
        # SELECT date_of_news, count(*) FROM news GROUP BY date_of_news ORDER BY date_of_news
        key = "SELECT publish_date, count(*) as count FROM million_headlines GROUP BY publish_date ORDER BY publish_date"
        cache = NoSQLCache.inst()
        return cache.get(key)


class NoSQLCache:
    __instance = None
    timeout = 5

    @staticmethod
    def inst():
        if NoSQLCache.__instance == None:
            NoSQLCache.__instance = NoSQLCache(SqliteDb.inst())
        return NoSQLCache.__instance

    def __init__(self, sql_db_object):
        self.client = Client(('localhost', 11211))
        self.sql_db = sql_db_object

    def get(self, key):
        key_corrector = re.sub(r' ', '$', key)
        value = self.client.get(key_corrector)
        if value:
            return eval(value.decode('utf-8'))
        else:
            value = self.sql_db.get(key)
            self.set(key_corrector, value, self.timeout)
            return value

    def set(self, key, value, timeout):
        self.client.set(key, value, expire=timeout)


@app.get('/')
def index():
    return "ok"


@app.get('/bydate/<date>')
def bydate(date):
    cache = NoSQLCache.inst()
    j = json.dumps(cache.sql_db.get_by(date))
    return j


@app.get('/rand/')
def rand():
    cache = NoSQLCache.inst()
    j = json.dumps(cache.sql_db.rand())
    return j


@app.get('/stat/')
def stat():
    cache = NoSQLCache.inst()
    j = json.dumps(cache.sql_db.stat())
    return j


def load_to_DB(file_name="million-headlines.zip"):
    cache = NoSQLCache.inst()
    cache.sql_db.cursor.execute('DROP TABLE IF EXISTS million_headlines')
    cache.sql_db.cursor.execute('''CREATE TABLE IF NOT EXISTS million_headlines (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                                  publish_date TEXT NOT NULL, 
                                  headline_text TEXT NOT NULL)''')
    cache.sql_db.cursor.execute('''CREATE INDEX IF NOT EXISTS pubdate ON million_headlines(publish_date)''')
    cache.sql_db.connection.commit()
    with zipfile.ZipFile(file_name, 'r') as myzip:
        with myzip.open('abcnews-date-text.csv', 'r') as mycsv:
            mycsv = io.TextIOWrapper(mycsv, encoding='utf-8', newline='')
            dr = csv.DictReader(mycsv)
            to_db = [(i['publish_date'][:4]+'-'+i['publish_date'][4:6]+'-'+i['publish_date'][6:], i['headline_text']) for i in dr]
    cache.sql_db.add(to_db)


if __name__ == "__main__":
    load_to_DB()

    run(app, host=HOST, port=PORT, reloader=True, debug=True)
