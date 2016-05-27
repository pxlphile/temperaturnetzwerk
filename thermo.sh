#!/usr/bin/env bash

if [ -z ${CLIMATE_HOME+arbitraryNullCheckValue} ]; 
then
	echo "CLIMATE_HOME variable is unset. Please find a new home for it"
	exit 1
else 
	echo "CLIMATE_HOME is set to $CLIMATE_HOME."
	echo "current PID is $$"
fi

echo $$ > $CLIMATE_HOME/thermo.pid
thermDir=$CLIMATE_HOME

while [ true ]
do
(
	# acquire lock and read data
	flock -n 9 || exit 1 

	python "$thermDir/thermo.py"
) 9>/var/lock/temperaturnetzwerk

	if [ $? -gt 0 ]
	then
		echo "Fehler bei der Temperaturauslesung"
		sleep 10
		continue
	fi
	
	for i in `seq 1 10`
	do
		echo -n "T:$i..."
		sleep 6
	done
	echo "
"
done
