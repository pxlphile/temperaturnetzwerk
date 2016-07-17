#!/usr/bin/env python
import sqlite3

dbName = 'temperatur.db'

def create():
	conn = sqlite3.connect(dbName)
	c = conn.cursor()
	print "Create sqlite database" + dbName
	
	c.execute("""
CREATE TABLE `temperatur` (
`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
`datum`	text, 
`temp`	real 
);""")
	conn.commit()	
	conn.close()

create()
