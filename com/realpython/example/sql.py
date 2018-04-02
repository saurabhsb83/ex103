# model
import sqlite3

with sqlite3.connect("blog.db") as connection:
    c = connection.cursor()
    c.execute("create table posts(title text , post text)")
    c.execute('insert into posts values("good","i am good")')
    c.execute('insert into posts values("great","i am great")')
    c.execute('insert into posts values("okay","i am okay")')
