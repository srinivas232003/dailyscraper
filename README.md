# dailyscraper
This is an assignment given by the Shack ;labs for an internship.
the Daily scraper is a flask app that scrapes the https://www.theverge.com/ for headlines,it's link,author,and date everyday at 7:30 am and 9:00 pm(for testing purposes )
and stores it in a SQL database and generates a csv file.I've used sqlite3 for prototyping and changed to heroku Postgres SQL.The csv file is stored in Microsoft 
Azure storage Blob.the DB and csv file is free from duplicates.The flask application is stored in heroku.the tasks are scheduled in python Using Apscheduler as 'cron' jobs

please do check out the app at 
https://automate-scraper.herokuapp.com/
