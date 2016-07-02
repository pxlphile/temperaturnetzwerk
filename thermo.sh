#!/usr/bin/env bash
thermDir='/home/pi/Projekte/pytest'
# make sure these .confs have 0700 permission
FTP_SERVER=`cat ftpserver.conf`
FTP_CREDENTIALS=`cat ftppasswd.conf`

while [ true ]
do
	python "$thermDir/thermo.py"
	if [ $? -gt 0 ]
	then
		echo "Fehler bei der Temperaturauslesung"
		sleep 10
		continue
	fi
	
	echo "Erzeuge Datafiles"
	python "$thermDir/createDataFile.py"
	if [ $? -gt 0 ]
	then
		echo "Fehler bei der Erzeugung der Logdatei"
	fi
	
	echo "Erzeuge Grafiken"
	gnuplot plotfile2png
	if [ $? -gt 0 ]
	then
		echo "Ein Fehler trat beim Aufruf von gnuplot auf: $result."
	fi
	
	echo "Erzeuge HTML-Datei"
	python createhtml.py
	
	echo "FTP upload"
	lftp $FTP_SERVER << FTPEND

	user $FTP_CREDENTIALS
	mput target/*.png
	mput target/*.html
	mput target/*.css

	bye
FTPEND

	if [ $? -gt 0 ]
	then
		echo "Ein Fehler trat beim Aufruf von lftp auf: $result."
	fi
	# sicherheitshalber lftp queue files löschen
	rm -rf .local/share/lftp/*
	
	for i in `seq 1 10`
	do
		echo -n "$i..."
		sleep 6
	done
	echo "
"
	
done
