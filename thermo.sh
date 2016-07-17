#!/usr/bin/env bash
thermDir='/home/pi/projekte/temperaturnetzwerk/'

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
