# temperaturnetzwerk
A tool chain for climate/temperature publishing on a Raspberry Pi and a ds18s20-Thermosensor

1. Read temperature and write into SQLite DB
2. Read data from DB and create gnuplot'able CSV files
3. Gnuplot the CSV files to different graphics: today, week, month, all
4. Generate HTML file which accommodates temperatur, date and graphics
5. Publish the deliverables via FTP to a webspace
repeat

# Setup

## Kernel games
A major precondition is the usage of the w1-therm kernel module. You can install it by adding
the corresponding modules in the */etc/modules* file:

>w1-gpio pullup=1

Once started (either by reboot or by the modprobe command) there should exist a new special file per 
thermosensor in the directory */sys/bus/w1/devices*

> ls -l /sys/bus/w1/devices

> insgesamt 0

> lrwxrwxrwx 1 root root 0 Sep 13 21:18 28-0316049898ff -> ../../../devices/w1_bus_master1/28-0316049898ff

> lrwxrwxrwx 1 root root 0 Sep 13 21:18 w1_bus_master1 -> ../../../devices/w1_bus_master1

Files that contain long numbers uniquely identify a single sensor. 

## Dependencies to other software
Since this is a Raspberry Pi project, Python should already be installed. But of course there is 
other software needed:
- Python SQLite module
- git
- lftp
	Install this one with `sudo apt-get install lftp`. Please note that the Rasbian package is not compiled
	with SSH-support so you can't use SFTP.	If you want to have SFTP support you have to 
	[compile it yourself](http://lftp.yar.ru/get.html)
- gnuplot
	Install this one with `sudo apt-get install gnuplot`

Now we're good to start.

## Get the code
This is just an example. Just take care that the project directory which is referenced here is consistently replace ;)
> cd

> mkdir projects && cd projects

> get clone https://github.com/pxlphile/temperaturnetzwerk```

## Initialize SQLite database
To create the climate database just call in the project directory where you cloned the project:
>python createDb.py

## Set environment variables
In order to remove duplicate directy references in different scripts, set the `CLIMATE_HOME` variable to your 
project directory, for example
>export CLIMATE_HOME=/home/pi/projects/temperaturnetzwerk

## Create remote credential files
These are needed for the constant upload of files to your remote server. Both files are one-liners:

The content of `ftpserver.conf` should look like this: ftp://yourserver.com

The content of `ftppasswd.conf` should look like this: username passphrase

## Give it a go

Time to start the engines. 
- Start `./thermo.sh <YOUR_SENSOR_UUID_GOES_HERE>` to create a temperature reading every minute.
- Start `./publish.sh` to generate graphics, HTML files and upload all artifacts to a remote server.
