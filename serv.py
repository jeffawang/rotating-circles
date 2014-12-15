import psycopg2 as pg
import psycopg2.extras
import json
import traceback
import time
from bottle import route, run, template, static_file

def json_is_dumb(dt):
    import datetime
    if isinstance(dt, datetime.datetime):
        return dt.strftime("%Y-%m-%d %X")

# postgres connection stuff
conn_hash = {
        "dbname":   "mrs_sar",
        }
conn_string = " ".join(map(lambda x: "=".join(x), conn_hash.items()))

print "Connecting to postgres (%s)" % conn_string
conn = pg.connect(conn_string)
print "Connected to postgres!"

@route('/sar/<query>')
def sar(query):
    cur = conn.cursor(cursor_factory=pg.extras.RealDictCursor)
    try:
        cur.execute(query)
        conn.commit()
    except pg.ProgrammingError as e:
        conn.commit()
        jm = {"message": "you suck at sql", "heres_why": e.diag.message_primary }
        return json.dumps(jm)
    result = cur.fetchall()
    return json.dumps(result, default=json_is_dumb)

@route('/')
def index():
    return static_file("index.html", root='.')

@route('/hexweb')
def index():
    return static_file("index.html", root='.')

@route('/asset/<name>')
def data(name):
    return static_file(name, root='asset')

@route('/data/json/<name>')
def data(name):
    return static_file(name, root='data/json')

@route('/data/bed/<name>')
def data(name):
    return static_file(name, root='data/bed')

@route('/data/<name>')
def data(name="index.json"):
    return static_file(name, root='data')

@route('/style/<file>')
def style(file="main.css"):
    return static_file(file, root='style')

@route('/js/<file>')
def lib(file):
    return static_file(file, root="js")

run(host='localhost', port=8080)
