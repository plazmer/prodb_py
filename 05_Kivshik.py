# -*- coding: utf-8 -*-

# Задание почти то же самое, но теперь с MongoDB
# Счетчик прячется в коллекции counters
# Данные для GET/SET в коллекции data
# Остальные правила те же.

# Базовая защита от дурака - всё, что в ключах не англоязычные буквы/цифры - заменяем на "_", что при обращении, что при записи. 
# Лучше вынести в отдельную функцию
# 1. Реализовать на главной счетчик обращений, который будет храниться в Redis и увеличиваться при каждом заходе на главную
# 2. Реализовать добавление значения
# 3. Реализовать получение значения
# 4. Реализовать вывод списка ключей
# 5. Реализовать по аналогии удаление ключей - по ссылке /del/<key>, в index() добавлены header, footer - куда можно будет писать что-то своё
# в списке выводить для каждого ключа 2 ссылки - GET / DEL


import webbrowser
from bottle import Bottle, run, request, template, get, post
from pymongo import MongoClient, ReturnDocument
import re

HOST = '127.0.0.1'
PORT = '54321'

app = Bottle()
db = MongoClient().first_database
counters = db.counters
data = db.data

@app.get('/')
def index():
    if not counters.find_one({"_id": 1}):
        counters.insert_one({"_id": 1, "VisitorNumber": 0})
    counter = counters.find_one_and_update({"_id": 1}, {"$inc": {"VisitorNumber": 1}}, return_document=ReturnDocument.AFTER)["VisitorNumber"]
    vars = {'counter':counter, 'header':'', 'footer':''}
    return template('static/index.html', vars)

def badsymbol(key):
    return re.sub(r'\W', '_', key, flags=re.ASCII)

@app.post('/set/')
def set_key():
    key = request.forms.get('key')
    key = badsymbol(key)
    value = request.forms.get('value')
    data.insert_one({"key": key, "value": value})
    response = "added key: %s<br /> value: %s" % (key,value)
    return template('% rebase("static/index.html")\n'+response)

@app.get('/get/<key>')
def get_key(key):
    value = data.find_one({"key": key})["value"]
    response = '<strong>key</strong>: %s <br /><strong>value</strong>: %s'%(key,value)
    return  template('% rebase("static/index.html")\n'+response)

@app.get('/del/<key>')
def get_key(key):
    value =  data.find_one_and_delete({"key": key})["value"]
    response = '<strong>Deleted key</strong>: %s <br /><strong>Deleted value</strong>: %s'%(key,value)
    return  template('% rebase("static/index.html")\n'+response)

@app.get('/list')
def list_keys():
    keys_list = [doc["key"] for doc in  data.find()]
    response = ''
    for key in keys_list:
        response += '''<div class="list_item"><a href="/get/%s">Get key %s</a><br />
                        <a href="/del/%s">Delete key %s</a></div>''' % (key, key, key, key)
    return  template('% rebase("static/index.html")\n'+response)


if __name__ == "__main__":
    webbrowser.open('http://%s:%s'%(HOST, PORT))
    run(app, host=HOST, port=PORT, reloader=True, debug=True)
