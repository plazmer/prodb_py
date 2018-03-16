import webbrowser
from bottle import Bottle, run, request, template, get, post
from redis import Redis
import re

HOST = '127.0.0.1'
PORT = '54321'

app = Bottle()
r = Redis(decode_responses=True)  
                                 

def protection(key):
    return re.sub(r'\W', '_', key)

@app.get('/')
def index():
    counter = r.incr("visitors") 
                                   
    vars = {'counter': counter,
           'header': 'Hi!',
            'footer': 'Bye!'}
    return template('static/index.html', vars)

@app.post('/set/')
def set_key():
    key = request.forms.get('key')
    value = request.forms.get('value')
    key = protection(key)
    r.set(key, value)
    response = "added key: %s<br /> value: %s" % (key,value)
    return template('% rebase("static/index.html")\n'+response)

@app.get('/get/<key>')
def get_key(key):
    value = r.get(key)
    response = '<strong>key</strong>: {}<br /><strong>value</strong>: {}'.format(key, value)
    return template('% rebase("static/index.html")\n'+response)

@app.get('/list')
def list_keys():
    keys_list = r.keys()
    response = ''
    for key in keys_list:
        response += '<div class="list_item"><a href="/get/%s">%s</a></div>'%(key,key)
    return  template('% rebase("static/index.html")\n'+response)
    
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
