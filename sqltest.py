#!/usr/bin/env python
import sqlite3
conn = sqlite3.connect('temperatur.db')
c = conn.cursor()

c.execute('''create table temperatur(datum text, temp real)''')

c.execute("insert into temperatur values ('2016-06-09 09:40',23.687)")

conn.commit()

c.execute("select * from temperatur")
print c.fetchone()


conn.close()

