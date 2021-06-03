#import packages
from gpiozero import Button, LED
from picamera import PiCamera
import os
import datetime
from gps import *

#define gpio pins and variables
pwd = os.getcwd()
camera = PiCamera()
led = LED(13)
previewbtn = Button(26, hold_time=2) 
counter = 1

#GPS stuff
gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) 

#make new directory and create text file within
direcname = str(raw_input("name your file: "))
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
		#Everything else
		led.source = previewbtn
		previewbtn.when_pressed = camera.start_preview
		previewbtn.when_held = capture
		previewbtn.when_released = camera.stop_preview
	
except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "Done.\nExiting."
	
