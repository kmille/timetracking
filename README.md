# Tracking working hours with nfc tags
- Use a nfc tag to send requests to a flask backend which tracks your working hours


# Workflow
1. write a nfc tag to open a url: https://mydomain/time/work?secret=123123 (I used NFCtools on Android)
2. GET /time/work will respond with javascript (1. calc current time, 2. send post request)
3. POST /time/work the backend will save the action (work/free) and the time into a sqlite db
4. you work
5. write a nfc tag to open a url: https://mydomain/time/free?secret=123123 (free instead of work this time; this will save in the db when you stopped working)
6. https://mydomain/time/data shows your hours

# how to use it
```
git clone git@github.com:kmille/timetracking.git
cd timetracking
cp settings.py.dummy settings.py
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
or: gunicorn --bind 127.0.0.1:5001 app:app 
```

# todo
- automatically close the window (javascript is not allowed to do)
- nice format for /data
- calc: how long have I been worked?
- timezone fuckup
