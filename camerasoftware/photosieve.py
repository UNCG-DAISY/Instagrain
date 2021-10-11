# Written by Jacob Stasiewicz
#
# MIT License

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#import packages
from gpiozero import Button, LED
from picamera import PiCamera
import os
import glob
import datetime
from gps import *
import subprocess
from PIL import Image 

#define gpio pins and variables
pwd = os.getcwd()
camera = PiCamera()
led = LED(13)
previewbtn = Button(4, hold_time=2) 
counter = 1

#GPS stuff
gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) 

#make new directory and create text file within

	#direcname = str(input("name your file: "))
direcname = str(datetime.datetime.now())
newpath = pwd + '/' + direcname
croppath = pwd + '/' + direcname + '/crop'
os.makedirs(newpath)
os.makedirs(croppath)

print("Made a Directory for this session:")
print(newpath)

txtfile = open(newpath + '/' + direcname + '.csv', 'w+')
txtfile.write('img, date/time (UTC), lat, lon, alt(m), 0.05, 0.10, 0.16, 0.15, 0.30, 0.50, 0.75, 0.84, 0.90, 0.95, d50, std dev, skewness, kurtosis '"\n")
txtfile.close()
textarg = str(newpath + '/' + direcname + '.csv')
croparg = str(croppath)

print("Made a txt file for this session")

#define functions
def capture():
	global counter
	#get GNSS data
	report = gpsd.next() 
	if report['class'] == 'TPV':
		if getattr(report,'lat',0.0)!=0:
			lat1 = str(getattr(report,'lat',0.0))
		if getattr(report,'lon',0.0)!=0:
			lon1 = str(getattr(report,'lon',0.0))
		if getattr(report,'alt','nan')!= 'nan':
			alt1 = str(getattr(report,'alt','nan'))
	else:
			lat1 = "-9999"
			lon1 = "-9999"
			alt1 = "-9999" 	

	camera.capture(newpath + '/' + str(counter) + '.jpg')
	im = Image.open(str(newpath + '/' + str(counter) + '.jpg'))
	crop_img = crop_center(im,512,512)
	crop_img.save(croppath + '/crop' + str(counter) + '.jpg')
	txtfile = open(newpath + '/' + direcname + '.csv', 'a')
	txtfile.write( str(counter) + ',' + str(datetime.datetime.now()) +
	',' + lat1 + ',' + lon1 + ','+ alt1 + ',')
	txtfile.close()
	print(lat1)
	print(lon1)
	print(alt1)
	pyDGS()
	print('that was picture:')
	print(counter)
	counter = counter + 1
	

def previewon():
	camera.start_preview()
	subprocess.call(["./ringledon.sh"])
	
def previewoff():
	camera.stop_preview()
	subprocess.call(["./ringledoff.sh"])

def crop_center(pil_img, crop_width, crop_height):
   img_width, img_height = pil_img.size
   return pil_img.crop(((img_width - crop_width) // 2,
                          (img_height - crop_height) // 2,
                          (img_width + crop_width) // 2,
                          (img_height + crop_height) // 2))
                          
def pyDGS():
	global textarg 
	list_of_files_crop = glob.glob(croppath + '/*.jpg')
	latest_file_crop = str(max(list_of_files_crop, key=os.path.getctime))
	print("using pyDGS to get grain size")
	subprocess.call(["python3", "example_test.py", latest_file_crop, textarg])
	print("ready for next picture")
	
	
print("ready for a picture. Press trigger to preview, hold for 2 seconds for a picture.")

#While function to just run

while True:
				
	#Everything else
	led.source = previewbtn
	previewbtn.when_pressed = previewon
	previewbtn.when_held = capture
	previewbtn.when_released = previewoff 
		
#except(KeyboardInterrupt, SystemExit):
#	print ("Done.\nExiting")
