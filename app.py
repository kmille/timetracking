#!/usr/bin/env python3
import os.path
import arrow
from flask import Blueprint, Flask, request
import sqlite3

from ipdb import set_trace

db_name = "times.db"
db_query_create = "CREATE TABLE time_tracking (action text, time text)"
db_query_insert = "INSERT INTO time_tracking (action, time) VALUES (?,?)"
db_query_select = "SELECT action, time from time_tracking"

from settings import host, port, debug, client_secret

html = """

    <script>

        var now = new Date().getTime() /1000;

        var xhr = new XMLHttpRequest();
        xhr.open('POST', window.location.pathname)
        xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        xhr.send('now=' + now);
        xhr.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                     //eval(xhr.responseText);
                     //window.close();
            }
        };
    </script>


"""


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


@app.route("/time/work", methods=['POST', 'GET'])
@app.route("/time/free", methods=['POST', 'GET'])
def work():
    if request.method == "GET":
        if "secret" not in request.args.keys() or request.args['secret'] != client_secret:
            return "YOU SHALL NOT PASS", 403
        return html
    if request.method == "POST":
        action = request.path.split("/")[-1]
        if action not in ('free', 'work') or 'now' not in request.form.keys():
            return "Nope", 400
        seconds = arrow.get(request.form['now'], "X").format("YYYY-MM-DD HH:MM:ss")
        try:
            conn = sqlite3.connect(db_name)
            cur = conn.cursor()
            db_query_insert
            cur.execute(db_query_insert, (action, seconds))
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    
        return "window.close()"


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
