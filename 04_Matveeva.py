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

import re
import webbrowser
from redis import Redis
from bottle import Bottle, run, request, template, get, post

HOST = '127.0.0.1'
PORT = '54321'


app = Bottle()
r = Redis(decode_responses=True)

def protection(key):
    return re.sub(r'\W', '_', key, flags=re.ASCII)

@app.get('/')
def index():
    vars = {'counter': r.incr('hits') , 'header': 'Hello, my friend', 'footer': 'See you soon'}
    return template('static/index.html', vars)

@app.post('/set/')
def set_key():
    key = request.forms.get('key')
    key = protection(key)
    value = request.forms.get('value') 
    r.set(key, value)
    response = "added key: %s<br /> value: %s" % (key,value)
    return template('% rebase("static/index.html")\n'+response)

@app.get('/get/<key>')
def get_key(key):    
    value = r.get(key)
    response = '<strong>key</strong>: %s <br /><strong>value</strong>: %s'%(key,value)
    return  template('% rebase("static/index.html")\n'+response)

@app.get('/list')
def list_keys():    
    keys_list = r.keys()
    response = ''
    for key in keys_list:
        response += '<div class="list_item"><a href="/get/%s">%s</a></div>'%(key,key)
    return  template('% rebase("static/index.html")\n'+response)

@app.get('/del/<key>')
def del_key(key):
    key = protection(key)
    if key in r.keys():
        r.delete(key)
        response = '<strong>The key deleted successfully! The next key<strong>: %s'%(key)
    return template('% rebase("static/index.html")\n'+response)

   

    

if __name__ == "__main__":
    webbrowser.open('http://%s:%s'%(HOST, PORT))
    run(app, host=HOST, port=PORT, reloader=True, debug=True)
