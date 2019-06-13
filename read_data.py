from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from collections import OrderedDict

import arrow
from ipdb import set_trace

from db_test import Timeslot

FREE = "free"
WORK = "work"

def load_data():
    data = OrderedDict()
    engine = create_engine('sqlite:////tmp/test.db')
    session = sessionmaker(bind=engine)()
    timeslots = session.query(Timeslot).order_by(Timeslot.date).order_by(Timeslot.time).all()
    for t in timeslots:
        data[t.date] = {} 
        data[t.date]['time_records'] = []
        data[t.date]['total_time_seconds'] = 0
    for t in timeslots:
        data[t.date]['time_records'].append({'time': t.time, 'action': t.action})
    session.close()
    return data

def make_seconds_pretty(seconds):
    hours = seconds // 3600
    remaining_seconds = seconds % 3600
    minutes = remaining_seconds // 60
    nice = f"{hours}:{minutes:02d}"
    return nice


def test_data(data):
    for date, data_of_day in data.items():
        time_records = data_of_day['time_records']
        assert len(time_records) % 2 == 0, "amount of records shoud be an even number"
        for i in range(0, len(time_records), 2):
            assert time_records[i]['action'] == WORK, "expecting WORK here"
            assert time_records[i+1]['action'] == FREE, "expecting FREE here"
            begin = arrow.get(time_records[i]['time'], "HH:mm:SS")
            end = arrow.get(time_records[i+1]['time'], "HH:mm:SS")
            diff = end - begin
            data[date]['total_time_seconds'] += diff.seconds
        data[date]['total_time_nice'] = make_seconds_pretty(data[date]['total_time_seconds'])

data = load_data()
test_data(data)
    
set_trace()
