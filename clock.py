from apscheduler.schedulers.blocking import BlockingScheduler
from csvgen import gen_data
from apscheduler.triggers.cron import CronTrigger 
import atexit
import time
import requests as r
sched = BlockingScheduler()
import os
import psycopg2
def keep_alive():
  res=r.get("https://automate-scraper.herokuapp.com/alive")
  print("alive",res.text)


def data():
  print(time.strftime('%H:%M:%S'))
  gen_data()


sched.add_job(
    func=data,
    trigger=CronTrigger(hour='2,14',minute='30'),#utc time
    id='gen_data_task',
    name='gen data',
    replace_existing=True)
sched.add_job(
  func=keep_alive,
  trigger=CronTrigger(hour='*',minute='*/3'),
  id='keep_alive',
  name='keep alive',
  replace_existing=True)

sched.start()
