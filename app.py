#!/usr/bin/env python3
import os.path
import arrow
from flask import Flask, request
import sqlite3

from ipdb import set_trace

db_name = "times.db"
db_query_create = "CREATE TABLE time_tracking (action text, time text)"
db_query_insert = "INSERT INTO time_tracking (action, time) VALUES (?,?)"
db_query_select = "SELECT action, time from time_tracking"

from settings import host, port, debug, client_secret

app = Flask(__name__)
conn = None


def create_db():
    print("Creating the db")
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute(db_query_create)
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()


if not os.path.exists(db_name):
    create_db()


@app.route("/")
def index():
    return "hello my friend"


@app.route("/time/work")
@app.route("/time/free")
def set_hours():
    action = request.path.split("/")[-1]
    if action not in ('free', 'work') or client_secret != request.args['secret']:
        return "Nope", 400
    seconds = arrow.now().format("YYYY-MM-DD HH:MM:ss")
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        db_query_insert
        cur.execute(db_query_insert, (action, seconds))
        conn.commit()
    except sqlite3.Error as e:
        print(e)
        return "ERROR"
    finally:
        conn.close()

    return "OK"


@app.route("/time/data")
def data():
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        db_query_insert
        cur.execute(db_query_select)
        rows = cur.fetchall()
        for row in rows:
            t = arrow.get(row[1], "X").format("YYYY-MM-DD HH:MM:ss")
            print(t)
        return str(rows)
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()


if __name__ == '__main__':
    app.run(host, port, debug=debug)
