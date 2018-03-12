# -*- coding: utf-8 -*-
# https://bottlepy.org/docs/dev/tutorial.html
# https://habrahabr.ru/post/221659/
# https://habrahabr.ru/post/250831/
# https://github.com/MicrosoftArchive/redis/releases


# Базовая защита от дурака - всё, что в ключах не англоязычные буквы/цифры - заменяем на "_", что при обращении, что при записи.
# Лучше вынести в отдельную функцию
# 1. Реализовать на главной счетчик обращений, который будет храниться в Redis и увеличиваться при каждом заходе на главную
# 2. Реализовать добавление значения
# 3. Реализовать получение значения
# 4. Реализовать вывод списка ключей
# 5. Реализовать по аналогии удаление ключей - по ссылке /del/<key>, в index() добавлены header, footer - куда можно будет писать что-то своё


import webbrowser
import re
from bottle import Bottle, run, request, template, get, post
from redis import Redis

HOST = '127.0.0.1'
PORT = '54321'

app = Bottle()
r = Redis(decode_responses=True)  # указанный параметр необходим, чтобы redis не возвращал байтовые строки типа b'key'
if not r.exists('visit_counter'):
    r.set('visit_counter', 0)


def protection(key):
    return re.sub(r'\W+', '_', key, flags=re.ASCII)  # флаг, чтобы заменять и кириллицу, без него она не заменяется


@app.get('/')
def index():
    #todo
    counter = r.incr("visit_counter")
    #/todo
    vars = {'counter': counter, 'header': 'Hello, my friend', 'footer': 'Goodluck, my friend'}
    return template('static/index_novichkov.html', vars)


@app.post('/set/')
def set_key():
    key = request.forms.get('key')
    value = request.forms.get('value')
    #todo
    key = protection(key)
    r.set(key, value)
    #/todo
    response = "added key: %s<br /> value: %s" % (key,value)
    return template('% rebase("static/index_novichkov.html")\n'+response)


@app.get('/get/<key>')
def get_key(key):
    # todo
    value = r.get(key)
    response = '<strong>key</strong>: %s <br /><strong>value</strong>: %s'%(key,value)
    #/todo
    return template('% rebase("static/index_novichkov.html")\n'+response)


@app.get('/list')
def list_keys():
    #todo
    keys_list = r.keys()
    #/todo
    response = ''
    for key in keys_list:
        response += '<div class="list_item"><a href="/get/%s">%s</a></div>'%(key,key)
    return template('% rebase("static/index_novichkov.html")\n'+response)


@app.post('/del/')
def delete_key():
    key = request.forms.get('key2')
    key = protection(key)
    if r.exists(key):
        r.delete(key)
        response = "deleted key: %s" % key
    else:
        response = "deleted key: there is no such key in the database"
    return template('% rebase("static/index_novichkov.html")\n'+response)


if __name__ == "__main__":
    webbrowser.open('http://%s:%s'%(HOST, PORT))
    run(app, host=HOST, port=PORT, reloader=True, debug=True)
