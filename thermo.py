#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import check_output
import datetime
from time import strftime,localtime,sleep
import sqlite3
import os
import sys
import re

# Reads from a linux device file the measured temperature in Celsius and creates a sqlite database entry. 
# The device file represents a 1-wire 18B20 Thermosensor. The temperatur value inside the device file is 
# measured in milli celsius.

# In order to prepare the device see https://www.kompf.de/weather/pionewiremini.html 

## globals

# the sensor UUID is associated to the table row for possible data mining
sensorUuid = "no sensor yet set"

# Database properties
# please refer to the sqlite documentation for naming conventions
databaseFilePath = "./temperatur.db"
databaseTableName = "temperatur"
databaseColumnDate = "tempDate"
databaseColumnTemperature = "temperature"
databaseColumnSensorId = "sensorId"

# ISO date format, f. e. 2016-11-12 13:14:15
isoDateFormat = "%Y-%m-%d %H:%M:%S"

debug = True

## Routines

def main(arguments):
	global sensorUuid
	
	assertUuidArgumentExists(arguments)
	assertUuidFormat(arguments[0])
	
	sensorUuid = arguments[0]

	temp = readTemp()
	if debug:
		print temp + "° C" 
	writeTempToDb(temp, sensorUuid)

def assertUuidArgumentExists(arguments):
	# check sensor UUID parameter
	if len(arguments) != 1:
		printUsageAndExit()

def printUsageAndExit():
	print "Usage synopsis: thermo.py <Thermo-sensor UUID>"
	print "example: python thermo.py 28-0316049898ae"
	sys.exit(1)

def assertUuidFormat(sensorUuidParam):
	match = re.search('\d\d-[0-9a-f]{12}', sensorUuidParam)
	if not match:
		quitWithErrorMessage("Error: Device file argument does not match expected UUID pattern: '" + pathToDriver + "'.", 2)

def readTemp():
	global sensorUuid;
	
	pathToDriver = "/sys/bus/w1/devices/" + sensorUuid + "/w1_slave"
	assertSensorDeviceExists(pathToDriver)
	
	return readTempFromFileContent(pathToDriver)
	
def assertSensorDeviceExists(pathToDriver):
	if not os.path.exists(pathToDriver):
		quitWithErrorMessage("Error: Could not find the device file '" + pathToDriver + "'.", 1)

def readTempFromFileContent(pathToDriver):
	# creates a new shell to call cat to return the file content
	out = check_output(["cat", pathToDriver])
	
	# parse the output: it's in a fixed place
	pos = out.index("t=") + 2
	tempStr =  out[pos:].replace("\n", "")
	temperaturInMilliCelsius = float(tempStr)
	temperaturInCelsius = str(temperaturInMilliCelsius / 1000)
	return temperaturInCelsius

def writeTempToDb(temperature, sensorUuid):
	global isoDateFormat, databaseFilePath, databaseTableName
	
	conn = sqlite3.connect(databaseFilePath)
	dbCursor = conn.cursor()
	
	currentDate = strftime(isoDateFormat, localtime())
	dbCursor.execute("insert into " + databaseTableName + " (tempDate,temperature,sensorId) values (?,?,?)", (currentDate, temperature, sensorUuid))
	
	conn.commit()
	conn.close()

def quitWithErrorMessage(errorMsg, exitCode):
	print errorMsg
	sys.exit(exitCode)

if __name__ == '__main__':
	cliArgumentsWithoutProgramName = sys.argv[1:]
	main(cliArgumentsWithoutProgramName)
