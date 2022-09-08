from blobwriter import generate_link
from flask import Flask,render_template
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger 
import atexit
import time
from csvgen import gen_data
import requests as r
import bs4

# create flask app
app = Flask(__name__)
#data generate
# def data():
#   print(time.strftime('%H:%M:%S'))
#   gen_data()

# create schedule
# scheduler = BackgroundScheduler()
# scheduler.start()
# scheduler.add_job(
#     func=data,
#     trigger=CronTrigger(hour='*',minute='52'),
#     id='gen_data_task',
#     name='gen data',
#     replace_existing=True)
# Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())

@app.route('/')
def home():
    res=generate_link()
    return render_template('home.html',res=res)
@app.route('/views')
def views():
    return render_template('views.html')
@app.route('/alive')
def alive():
    return 'alive!'
# run Flask app in debug mode
if __name__=='__main__':
    app.run(debug=True)
