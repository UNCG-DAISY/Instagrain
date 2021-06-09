#import packages
from gpiozero import Button
from picamera import PiCamera
import os
import datetime
from gps import *

#define gpio pins and variables
pwd = os.getcwd()
camera = PiCamera()
previewbtn = Button(26, hold_time=2) 
counter = 1

#GPS stuff
gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) 

#make new directory and create text file within
direcname = str(input("name your file: "))
newpath = pwd + '/' + direcname
os.makedirs(newpath)
txtfile = open(newpath + '/' + direcname + '.csv', 'w+')
txtfile.write('img, date/time, lat, lon, alt(m)')
txtfile.close()

#define functions
def capture():
	global counter
	camera.capture(newpath + '/' + direcname + str(counter) + '.jpg')
	txtfile = open(newpath + '/' + direcname + '.csv', 'a')
	txtfile.write("\n")
	txtfile.write( direcname + str(counter) + ',' + str(datetime.datetime.now()) +
	',' + lat1 + ',' + lon1 + ','+ alt1)
	txtfile.close()
	counter += 1

def previewon():
	camera.start_preview()
	subprocess.call(["./ringledon.sh"])
	
def previewoff():
	camera.stop_preview()
	subprocess.call(["./ringledoff.sh"])
	
#run function
try:
	while True:
		#Setting lat,lon, and alt as variables
		report = gpsd.next() 
		if report['class'] == 'TPV':
			if getattr(report,'lat',0.0)!=0:
				lat1 = str(getattr(report,'lat',0.0))
			if getattr(report,'lon',0.0)!=0:
				lon1 = str(getattr(report,'lon',0.0))
			if getattr(report,'alt','nan')!= 'nan':
				alt1 = str(getattr(report,'alt','nan'))
		else:
			lat1 = "ERROR"
			lon1 = "ERROR"
			alt1 = "ERROR"
		#Everything else
		previewbtn.when_pressed = previewon
		previewbtn.when_held = capture
		previewbtn.when_released = previewoff 
except(KeyboardInterrupt, SystemExit):
	print("Done.\nExiting")	
	
