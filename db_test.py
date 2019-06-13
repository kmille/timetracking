#!/usr/bin/env python3
from flask import Flask, request
import arrow
from flask_sqlalchemy import SQLAlchemy
import os.path
import os
from ipdb import set_trace

from settings import host, port, debug, db_name
db_name = "/tmp/test.db"

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(os.getcwd(), db_name)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Timeslot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    time = db.Column(db.String)
    action = db.Column(db.String)

if not os.path.exists(db_name):
    print("Creating the db")
    db.create_all()
    from generate_data import add_data
    add_data(db.session)


@app.route("/")
def index():
    return "hello my friend"

@app.route("/work")
@app.route("/free")
def set_hours():
    action = request.path.split("/")[-1]
    if action not in ('free', 'work'):
        return "Nope", 400
    now = arrow.now()
    t = Timeslot(date=now.format("DD.MM.YYYY"),
                 time=now.format("HH:MM:SS"),
                 action=action)
    db.session.add(t)
    db.session.commit()
    return "OK"

if __name__ == '__main__':
    app.run(host, port, debug=debug)
