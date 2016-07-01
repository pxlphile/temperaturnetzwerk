#!/usr/bin/env python
from subprocess import check_output
import datetime
from time import strftime,gmtime
import sqlite3
import os

dbConnection = None
dbCursor = None
DELIMITER = ";"
rollingAverage = None

def initAverage(size):
	rollAvg = []
	for i in range(size):
		rollAvg.append(0.0)
	return rollAvg

def main():
	global rollingAverage
	rollingAverage = initAverage(10)
	
	openDb()
	dbResult = readFromDb()
	
	with open("datefile.txt","w") as outputFile:
		for row in dbResult:
			updateAverage(row[1])
			writeDataSet(row, outputFile)
	
	closeDb()

def readFromDb():
	result = dbCursor.execute("select datum,temp from temperatur")
	return result

def updateAverage(temp):
	global rollingAverage
	rollingAverage.pop(0)
	rollingAverage.append(temp)

def writeDataSet(row, outputFile):
		outputFile.write('"' + row[0] +'"')
		outputFile.write(DELIMITER)
		outputFile.write(str(row[1]))
		outputFile.write(DELIMITER)
		average = calculateAverage()
		outputFile.write(str(average) + "\n")

def calculateAverage():
	global rollingAverage
	result = 0.0
	for roll in rollingAverage:
		result += roll
	return result / len(rollingAverage)

def openDb():
	global dbConnection
	global dbCursor
	dbConnection= sqlite3.connect('temperatur.db')
	dbCursor = dbConnection.cursor()
	
def closeDb():
	global dbConnection
	dbConnection.close()

if __name__ == '__main__':
	main()
