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
r = Redis(decode_responses=True)


def protection(key):
    return re.sub(r'\W', '_', key, flags=re.ASCII)


@app.get('/')
def index():
    #todo
    counter = r.incrby("visit_counter")
    #/todo
    vars = {'counter': counter,
            'header': 'Удаление производится по ссылке /del/<key>',
            'footer': 'Goodluck'}
    return template('static/index.html', vars)


@app.post('/set/')
def set_key():
    key = request.forms.get('key')
    value = request.forms.get('value')
    #todo
    key = protection(key)
    r.set(key, value)
    #/todo
    response = "<strong>added key</strong>: {}<br /><strong>value</strong>: {}".format(key, value)
    return template('% rebase("static/index.html")\n'+response)


@app.get('/get/<key>')
def get_key(key):
    # todo
    value = r.get(key)
    response = '<strong>key</strong>: {}<br /><strong>value</strong>: {}'.format(key, value)
    #/todo
    return template('% rebase("static/index.html")\n'+response)


@app.get('/list')
def list_keys():
    response = ''
    for key in r.scan_iter():
        response += '<div class="list_item"><a href="/get/{}">{}</a></div>'.format(key, key)
    return template('% rebase("static/index.html")\n'+response)


@app.get('/del/<key>')
def delete_key(key):
    key = protection(key)
    if r.exists(key):
        r.delete(key)
        response = "deleted key: {}".format(key)
    else:
        response = "no key"
    return template('% rebase("static/index.html")\n'+response)


if __name__ == "__main__":
    webbrowser.open('http://%s:%s'%(HOST, PORT))
    run(app, host=HOST, port=PORT, reloader=True, debug=True)
