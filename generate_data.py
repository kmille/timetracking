import arrow

from ipdb import set_trace

from app_new import Timeslot

FREE = "free"
WORK = "work"

def add_data(session):
    print("Adding data to the db")
    t1 = Timeslot(date=arrow.get("01.03.2019", "DD.MM.YYYY").format("DD.MM.YYYY"), time=arrow.get("08:00", "HH:mm").format("HH:mm"), action=WORK)
    t2 = Timeslot(date=arrow.get("01.03.2019", "DD.MM.YYYY").format("DD.MM.YYYY"), time=arrow.get("12:00", "HH:mm").format("HH:mm"), action=FREE)
    t3 = Timeslot(date=arrow.get("01.03.2019", "DD.MM.YYYY").format("DD.MM.YYYY"), time=arrow.get("13:00", "HH:mm").format("HH:mm"), action=WORK)
    t4 = Timeslot(date=arrow.get("01.03.2019", "DD.MM.YYYY").format("DD.MM.YYYY"), time=arrow.get("17:00", "HH:mm").format("HH:mm"), action=FREE)

    session.add(t1)
    session.add(t2)
    session.add(t3)
    session.add(t4)
    session.commit()

    t1 = Timeslot(date=arrow.get("02.03.2019", "DD.MM.YYYY").format("DD.MM.YYYY"), time=arrow.get("09:00", "HH:mm").format("HH:mm"), action=WORK)
    t2 = Timeslot(date=arrow.get("02.03.2019", "DD.MM.YYYY").format("DD.MM.YYYY"), time=arrow.get("14:00", "HH:mm").format("HH:mm"), action=FREE)
    t3 = Timeslot(date=arrow.get("02.03.2019", "DD.MM.YYYY").format("DD.MM.YYYY"), time=arrow.get("17:00", "HH:mm").format("HH:mm"), action=WORK)
    t4 = Timeslot(date=arrow.get("02.03.2019", "DD.MM.YYYY").format("DD.MM.YYYY"), time=arrow.get("21:00", "HH:mm").format("HH:mm"), action=FREE)

    session.add(t1)
    session.add(t2)
    session.add(t3)
    session.add(t4)
    session.commit()

