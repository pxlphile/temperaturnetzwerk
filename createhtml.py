#!/usr/bin/env python

import datetime
from time import strftime,localtime,sleep,time
import sqlite3
import os
import sys

dbConnection = None
dbCursor = None

def main():
	currTemp = fetchTemp()
	htmlHead = createHead(currTemp)
	currDate = strftime("%Y-%m-%d %H:%M:%S", localtime())
	tempPart = createTempDiv(currTemp)
	htmlTail = createTail()
	
	writeHTMLFile(htmlHead, currDate, tempPart, htmlTail)

def createHead(currTemp):
	return """<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>""" + currTemp + """ - Willkommen zum Temperatur Netzwerk: Node: Keller</title>
		<link href="css/bootstrap.min.css" rel="stylesheet">
		<link href="style.css" rel="stylesheet" type="text/css" />
		<meta http-equiv="refresh" content="300" />
		<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
		<meta http-equiv="Pragma" content="no-cache" />
		<meta http-equiv="Expires" content="0" />
	</head>
	<body>
		<div class="container">
			<div class="col-md-6">
				<div class="panel panel-default">
					<div class="panel-heading">
						<h1 class="date" data-timestamp='""" + str(int(time())) + "'>";

def fetchTemp():
        openDb()

	tempResult = readLatestTempFromDb()
	tempString = None
	for row in tempResult:
		tempString = "{0:.1f}".format(row[0]) + " &deg;C"

	closeDb()
	return tempString

def createTempDiv(currTemp):
	return """</h1>
					</div>
					<div class="panel-body">
						<h1 class="temp">Aktuell:
							<button type="button" class="btn btn-success btn-lg currTemp">
								<span class="glyphicon glyphicon-signal" aria-hidden="true"></span>""" + currTemp + """
							</button>
						</h1>
					</div>
				</div>
			</div>
			<div class="col-md-6">
				<div class="panel panel-default system-state">
					<div class="panel-heading">
						<h1>Systemstatus</h1>
					</div>
					<div class="panel-body">
			<div class="alert alert-success" role="alert">
				<span class="glyphicon glyphicon-ok"></span>&nbsp; System l&auml;uft
			</div>
			<div class="alert alert-danger hidden" role="alert">
				<span class="glyphicon glyphicon-alert"></span>&nbsp; System l&auml;uft nicht synchron.
			</div>
		</div>
	</div>
</div>"""

def createTail():
	return """
		<div class="col-md-12">
			<img src="temperaturDay.png" class="img-responsive" />
			<img src="temperaturWeek.png" class="img-responsive" /><br />
			<img src="temperaturMonth.png" class="img-responsive" />
			<img src="temperaturAll.png" class="img-responsive"/>
		</div>
		<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
		<script src="js/jquery.min.js"></script>
		<!-- Include all compiled plugins (below), or include individual files as needed -->
		<script src="js/bootstrap.min.js"></script>
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
