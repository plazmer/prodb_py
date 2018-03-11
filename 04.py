# -*- coding: utf-8 -*-
# https://bottlepy.org/docs/dev/tutorial.html
# https://habrahabr.ru/post/221659/
# https://habrahabr.ru/post/250831/
# https://github.com/MicrosoftArchive/redis/releases


# Никакой защиты от дурака, ключи подразумеваем, что только англоязычные, без слэшей и прочего, что поломает логику.
# Добавить на главную счетчик обращений, который будет храниться в Redis и увеличиваться при каждом заходе на главную
#
#
#


import webbrowser
from bottle import Bottle, run, request, template
from redis import Redis

HOST = '127.0.0.1'
PORT = '54321'

app = Bottle()
r = Redis()

@app.post('/set/')
def set_key():
    key = request.forms.get('key')
    value = request.forms.get('value')
    #todo

    #/todo
    response = "added key: %s<br /> value: %s" % (key,value)
    return template('% rebase("static/index.html")\n'+response)

@app.get('/get/<key>')
def get_key(key):
    #todo
    value = 'for testing only, replace real code'
    response = '<strong>key</strong>: %s <br /><strong>value</strong>: %s'%(key,value)
    #/todo
    return  template('% rebase("static/index.html")\n'+response)

@app.route('/list')
def list_keys():
    #todo
    keys_list = ['1','2','3']
    #/todo
    response = ''
    for key in keys_list:
        response += '<div class="list_item"><a href="/get/%s">%s</a></div>'%(key,key)
    return  template('% rebase("static/index.html")\n'+response)



@app.route('/')
def index():
    #todo
    counter=5
    #/todo
    vars = {'counter':counter}
    return template('static/index.html', vars)

#warning: firewall, used ports!!!
webbrowser.open('http://%s:%s'%(HOST, PORT))
run(app, host=HOST, port=PORT, reloader=True, debug=True)