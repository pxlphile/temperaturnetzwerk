#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

def main():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(18, GPIO.OUT)
	
	superLoop()
	
	return 0

def superLoop():
	while True:
		time.sleep(1)
		print "high"
		GPIO.output(18, 1)
		time.sleep(1)
		print "low"
		GPIO.output(18, 0)

if __name__ == '__main__':
	main()

