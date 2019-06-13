#!/usr/bin/env python3
from collections import OrderedDict
import arrow
import os.path

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from settings import host, port, debug, WORK, FREE, log_file

from ipdb import set_trace


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class Timeslot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    time = db.Column(db.String)
    action = db.Column(db.String)

    def __repr__(self):
        return f"Timeslot {self.date} {self.time} {self.action}"

if not os.path.exists("/tmp/test.db"):
    print("Creating the db")
    db.create_all()
    from generate_data import add_data
    add_data(db.session)


def get_current_state():
    now = arrow.now().format("DD.MM.YYYY")
    i = db.session.query(Timeslot).filter(Timeslot.date == now).order_by(Timeslot.time).all()
    if len(i) % 2  == 0:
        return FREE
    else:
        return WORK

def load_data():
    data = OrderedDict()
    timeslots = db.session.query(Timeslot).order_by(Timeslot.date.desc()).order_by(Timeslot.time).all()
    #i = db.session.query(Timeslot).filter(Timeslot.date < '13.06.2019').all()
    for t in timeslots:
        data[t.date] = {} 
        data[t.date]['time_records'] = []
        data[t.date]['total_time_seconds'] = 0
    for t in timeslots:
        data[t.date]['time_records'].append({'time': t.time, 'action': t.action})
    now = arrow.now().format("DD.MM.YYYY")
    if now in data.keys():
        if len(data[now]['time_records']) % 2 == 1:
            data[now]['time_records'].append({'time': arrow.now().format("HH:mm"), 'action': FREE})
    return data

def make_seconds_pretty(seconds):
    hours = seconds // 3600
    remaining_seconds = seconds % 3600
    minutes = remaining_seconds // 60
    nice = f"{hours}:{minutes:02d}"
    return nice


def test_data(data):
    now = arrow.now().format("DD.MM.YYYY")
    for date, data_of_day in data.items():
        time_records = data_of_day['time_records']
        if date != now:
            assert len(time_records) % 2 == 0, "amount of records shoud be an even number"
        for i in range(0, len(time_records), 2):
            if date != now:
                assert time_records[i]['action'] == WORK, "expecting WORK here"
                assert time_records[i+1]['action'] == FREE, "expecting FREE here"
            begin = arrow.get(time_records[i]['time'], "HH:mm")
            try:
                end = arrow.get(time_records[i+1]['time'], "HH:mm")
            except IndexError: 
                print("kann nicht auf i+1 zugreifen. sind daten von heute und wir sind noch am arbeiten")
                now = arrow.now()
                end = now
                data[date]['time_records'].append({ 'time': now.format("HH:mm") })

            diff = end - begin
            data[date]['total_time_seconds'] += diff.seconds
        data[date]['total_time_nice'] = make_seconds_pretty(data[date]['total_time_seconds'])
    return data


@app.route("/")
def index():
    data = load_data()
    data = test_data(data)
    state = get_current_state()
    return render_template("index", data=data, state=state)


@app.route("/work")
@app.route("/free")
def set_hours():
    action = request.path.split("/")[-1]
    if action not in ('free', 'work'):
        return "Nope", 400
    now = arrow.now()
    
    if get_current_state() == action:
        with open(log_file, "a") as f:
            f.write(f"Prevent DB Write: {action} {now.format('DD.MM.YYYY')} {now.format('HH:mm')}\n")
            return "That's not possible now.", 400

    t = Timeslot(date=now.format("DD.MM.YYYY"),
                 time=now.format("HH:mm"),
                 action=action)
    db.session.add(t)
    db.session.commit()
    return redirect("/")

if __name__ == '__main__':
    app.run(host, port, debug=debug)
