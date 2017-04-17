#!/usr/bin/env python
from subprocess import check_output
import datetime
from time import strftime
import sqlite3
import os

# Creates a gnuplot'able data file from that measured temperature data points in the database

# Database properties
# please refer to the sqlite documentation for naming conventions
databaseFilePath = "./temperatur.db"
databaseTableName = "temperatur"
databaseColumnDate = "tempDate"
databaseColumnTemperature = "temperature"
databaseColumnSensorId = "sensorId"

dbConnection = None
dbCursor = None
DELIMITER = ";"
TARGET_DIR = "target/"

def main():
    openDb()

    generateDataForAll()
    generateDataForMonth()
    generateDataForWeek()
    generateDataForLast24Hours()

    closeDb()

def generateDataForAll():
    dbResult = readAllFromDb()
    writeDateFile("datefile.txt", dbResult)

def generateDataForMonth():
    dbResult = readMonthDataFromDb()
    writeDateFile("datefileMonth.txt",dbResult)

def generateDataForWeek():
    dbResult = readWeekDataFromDb()
    writeDateFile("datefileWeek.txt", dbResult)

def generateDataForLast24Hours():
    dbResult = readLast24HoursDataFromDb()
    writeDateFile("datefileDay.txt", dbResult)

def readAllFromDb():
    return dbCursor.execute("select t.tempDate,t.temperature from `temperatur` t \
	ORDER BY t.tempDate ASC")

def readMonthDataFromDb():
    return dbCursor.execute("SELECT t.tempDate,t.temperature FROM `temperatur` t \
	where t.tempDate >= date('now', '-1 months') \
	ORDER BY t.tempDate ASC")

def readWeekDataFromDb():
    return dbCursor.execute("SELECT t.tempDate,t.temperature FROM `temperatur` t \
	where t.tempDate >= date('now', '-7 days') \
	ORDER BY t.tempDate ASC")

def readLast24HoursDataFromDb():
    return dbCursor.execute("SELECT t.tempDate,t.temperature FROM `temperatur` t \
	where t.tempDate >= date('now', '-1 days') \
	ORDER BY t.tempDate ASC")


def writeDateFile(dateFileName, dbResult):
    with open(TARGET_DIR + dateFileName,"w") as outputFile:
        for row in dbResult:
            writeDataSet(row, outputFile)

def writeDataSet(row, outputFile):
    outputFile.write('"' + row[0] +'"')
    outputFile.write(DELIMITER)
    outputFile.write(str(row[1]))
    outputFile.write("\n")

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
