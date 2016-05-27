#!/usr/bin/env bash

if [ -z ${CLIMATE_HOME+arbitraryNullCheckValue} ];
then
        echo "CLIMATE_HOME variable is unset. Please find a new home for it"
        exit 1
else
        echo "CLIMATE_HOME is set to $CLIMATE_HOME."
        echo "current PID is $$"
fi

echo $$ > $CLIMATE_HOME/publish.pid
thermDir=$CLIMATE_HOME

# make sure these .confs have 0700 permission
# ftpserver file content goes like: ftp://yourserver.com
FTP_SERVER=`cat ftpserver.conf`
# ftp credentials go like username password
FTP_CREDENTIALS=`cat ftppasswd.conf`

mkdir "$thermDir/target" 2>/dev/null

function logError() {
	echo $1
	echo `date` >> error.log
	echo ": $1" >> error.log
}

while [ true ]
do
	echo "Erzeuge Datafiles"
	python "$thermDir/createDataFile.py"
	if [ $? -gt 0 ]
	then
		logError "Fehler bei der Erzeugung der Logdatei"
	fi
	
	echo "Erzeuge Grafiken"
	gnuplot plotfile2png
	if [ $? -gt 0 ]
	then
		logError "Ein Fehler trat beim Aufruf von gnuplot auf: $result."
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
		echo -n "P:$i..."
		sleep 6
	done
	echo "
"
done
