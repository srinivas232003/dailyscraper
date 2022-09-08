import csv
from bs4 import BeautifulSoup
import requests as r
from datetime import date
import sqlite3 as sql
import os
import re
import pyodbc
from blobwriter import append_data_to_blob
import psycopg2
import os
uri = os.getenv('DATABASE_URL')

header=["id","url","headline","author","date"]
#AZURE connections



#get date if not found in link
def get_date(div,link):
    date=div.find(name='time',class_="c-byline__item")
    if date==None:
        res=r.get(link).text
        soup=BeautifulSoup(res,"html.parser")
        date=soup.find(name='time',class_="c-byline__item")
    date=date.get('datetime').split("T")[0]
    date='/'.join(date.split('-'))
    return date

def csv_gen(row,writer):
    writer.writerow(row)
def gen_data():
    res=r.get("https://www.theverge.com/").text
    soup=BeautifulSoup(res,'html.parser')
    required_div=soup.find_all(name="div",class_="c-entry-box--compact__body")
    data=[]
    for i in required_div:
        cont=i.find(name="h2",class_="c-entry-box--compact__title")
        head=cont.text
        link=cont.find(name="a").get('href')
        #author
        try:
            author=i.find(name="span",class_="c-byline__author-name").text
        except:
            try:
                author=i.find(name="span",class_="c-byline__item").text
            except:
                author=i.find(name="span",class_="c-byline__item")
        #date
        try:
            if author!=None:
                dt=re.findall('\d+/\d+/\d+',link)[0]
            else:
                continue
        except:
            dt=get_date(i,link)
        
        if author!=None:
            data.append([link,head,author,dt])
    print(data)
    return save_to_db(data) 

def save_to_db(data):
    append_data=[]
    needs_header=None
    f=open('ddmmyyy_verge.csv','a+',newline="")
    writer=csv.writer(f)
    conn=psycopg2.connect(uri,sslmode='require')
    # conn=pyodbc.connect(f"Driver={driver};Server={server};Database={db_name};Uid={user};Pwd={pwd};Connection Timeout=30;")
    c=conn.cursor()
   
    c.execute('''CREATE TABLE IF NOT EXISTS news (

       id INTEGER PRIMARY KEY , 
       link varchar(200) NOT NULL UNIQUE ,
       title TEXT NOT NULL ,
       author TEXT NOT NULL,
       date TEXT         
)''')
    conn.commit()
    id=0
    #set id
    c.execute("select * from news")
    if c.fetchone()==None:
        needs_header=True
        id=0
        print(id)
    else:
        c.execute(f'Select MAX(id) from news')
        id=c.fetchone()[0]
        id+=1
        print(id)

    for i in data:
        try:
            cmd=f"INSERT INTO news VALUES({id},'{i[0]}','{i[1]}','{i[2]}','{i[3]}')"
            c.execute(cmd)
            conn.commit()
        except Exception as e:
            continue
        else:
            if needs_header:
                csv_gen(header,writer)
                append_data.append(header)
                needs_header=False   
            i.insert(0,str(id))
            i[2]=f'"{i[2]}"'
            append_data.append(i)
            csv_gen(i,writer)
            id+=1
    conn.close()
    f.close()
    print(append_data)
    append_data_to_blob(append_data) 

