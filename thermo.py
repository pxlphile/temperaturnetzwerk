#!/usr/bin/env python
from subprocess import check_output
import datetime
from time import strftime,gmtime,sleep
import sqlite3
import os
import sys

# Liest aus einer Devicedatei einen Integer, der ein tausendfaches der gemessenen Temperatur
# betraegt. Dieser Wert wird zurueckgerechnet und dann sowohl auf STDOU ausgegeben als auch
# in eine SQLite DB geschrieben.

def readTemp():
# to prepare the device see https://www.kompf.de/weather/pionewiremini.html
	path_to_driver = "/sys/bus/w1/devices/28-0316049898ff/w1_slave"
	if not os.path.exists(path_to_driver):
		quitWithErrorMessage(path_to_driver)
	out = check_output(["cat", path_to_driver])
	pos = out.index("t=")+2
	numberStr =  out[pos:].replace("\n","")
	number = float(numberStr)
	return str(number/1000)

def writeTempToDb(temp):
	conn = sqlite3.connect('temperatur.db')
	c = conn.cursor()
	currDate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
	c.execute("insert into temperatur (datum,temp) values (?,?)", (currDate, temp))
	conn.commit()
	conn.close()

def quitWithErrorMessage(filePath):
	print "Die Datei" + filePath + " wurde nicht gefunden."
	sys.exit(1)

temp = readTemp()
print temp + " C" 
writeTempToDb(temp)
