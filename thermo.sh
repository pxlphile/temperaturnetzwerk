#!/usr/bin/env bash
thermDir='/home/pi/Projekte/pytest'

while [ true ]
do
	python "$thermDir/thermo.py"
	if [ $? -gt 0 ]
	then
		echo "Fehler bei der Temperaturauslesung"
		sleep 10
		continue
	fi
	
	python "$thermDir/createDataFile.py"
	if [ $? -gt 0 ]
	then
		echo "Fehler bei der Erzeugung der Logdatei"
		exit 1
	fi
	
	gnuplot plotfile2png
	if [ $? -gt 0 ]
	then
		echo "Ein Fehler trat beim Aufruf von gnuplot auf: $result."
		exit 1
	fi
	
	echo "SCP Zeug kommt hier her"
	#scp user@ssh.server-he.de:temperatur-alle.png temperatur-heute.png temperatur.html 
	if [ $? -gt 0 ]
	then
		echo "Ein Fehler trat beim Aufruf von scp auf: $result."
	fi
	
	for i in `seq 1 12`
	do
		sleep 5
		echo -n "#"
	done
	
done
