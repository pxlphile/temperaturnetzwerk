#!/usr/bin/env python

import datetime
from time import strftime,gmtime,sleep
import sqlite3
import os
import sys

dbConnection = None
dbCursor = None

def main():
	currTemp = fetchTemp()
	htmlHead = createHead(currTemp)
	currDate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
	tempPart = createTempDiv(currTemp)
	htmlTail = createTail()
	
	writeHTMLFile(htmlHead, currDate, tempPart, htmlTail)

def createHead(currTemp):
	return """<!DOCTYPE html>
<html>
	<head>
		<title>""" + currTemp + """ - Willkommen zum Temperatur Netzwerk: Node: Keller</title>
		<link href="style.css" rel="stylesheet" type="text/css" />
		<meta http-equiv="refresh" content="300" />
		<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
		<meta http-equiv="Pragma" content="no-cache" />
		<meta http-equiv="Expires" content="0" />
	</head>
	<body>
		<h1 class='temp'>"""

def fetchTemp():
        openDb()

	tempResult = readLatestTempFromDb()
	tempString = None
	for row in tempResult:
		tempString = "{0:.1f}".format(row[0]) + " &deg;C"

	closeDb()
	return tempString

def createTempDiv(currTemp):
	return "<div class='currTemp'>" + currTemp + "</div>"

def createTail():
	return """
		</h1>
		<img src="temperaturDay.png" /><br />
		<img src="temperaturWeek.png" /><br />
		<img src="temperaturMonth.png" /><br />
		<img src="temperaturAll.png" />
	</body>
</html>"""

def readLatestTempFromDb():
        return dbCursor.execute("SELECT t.temp FROM `temperatur` t \
        ORDER BY t.datum DESC Limit 1")


def openDb():
        global dbConnection
        global dbCursor
        dbConnection= sqlite3.connect('temperatur.db')
        dbCursor = dbConnection.cursor()

def closeDb():
        global dbConnection
        dbConnection.close()

def writeHTMLFile(head, currDate, currTemp, tail):
	with open("target/index.html","w") as outputFile:
		outputFile.write(head)
		outputFile.write(currDate)
		outputFile.write(currTemp)
		outputFile.write(tail)

if __name__ == '__main__':
	main()
