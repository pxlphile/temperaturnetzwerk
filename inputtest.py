#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

def main():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(18, GPIO.IN)
	
	superLoop()
	
	return 0

def superLoop():
	while True:
		print GPIO.input(18)

if __name__ == '__main__':
	main()

