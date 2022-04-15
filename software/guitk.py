# Written by Jacob Stasiewicz and Evan Goldstein
#
# MIT License

#import packages
from gpiozero import Button, LED
from picamera import PiCamera
import gpsd
import os
import glob
import datetime
import subprocess
#from PIL import Image#, ImageTk
import PIL.Image
#import PIL.ImageTK
import numpy as np
import pandas as pd
from pycoral.utils import edgetpu
from pycoral.utils import dataset
from pycoral.adapters import common
from pycoral.adapters import classify
#Import tk Packages 
import time
from time import sleep 
from time import strftime
from tkinter import *
import tkinter as tk
#Import NeoPixel Commands
import board
import neopixel
#Import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt

#define gpio pins and variables
pwd = os.getcwd()
camera = PiCamera()
camera.resolution = (2048,2048)
led = LED(13)
#previewbtn = Button(4, hold_time=2) #screwed up program for some reason
counter = 1

#New GPS trial
gpsd.connect()

#TFLITE stuff
path_to_model = "./models/SandCam_QAT_notdense_edgetpu.tflite"
# Initialize the TF interpreter
interpreter = edgetpu.make_interpreter(path_to_model)
interpreter.allocate_tensors()
#uncomment lines below to debug and look at expected I/O
#print(interpreter.get_input_details())
#print(interpreter.get_output_details())

#make new directory and create text file within

#direcname = str(input("name your file: "))
time = datetime.datetime.now()
direcname = time.strftime("%m_%d_%Y_%H_%M_%S")
newpath = pwd + '/' + direcname
croppath = pwd + '/' + direcname + '/crop'
os.makedirs(newpath)
os.makedirs(croppath)

print("Made a Directory for this session:")
print(newpath)

txtfile = open(newpath + '/' + direcname + '.csv', 'w+')
txtfile.write('Filename, Date/Time (UTC), Latitude (DD) , Longitude (DD), Altitude(m), D_2(mm), D_5(mm), D_10(mm), D_16(mm), D_25(mm), D_50(mm), D_75(mm), D_84(mm), D_90(mm), D_95(mm), D_98(mm) '"\n")
txtfile.close()
textarg = str(newpath + '/' + direcname + '.csv')
croparg = str(croppath)

print("Made a txt file for this session")

#define functions
def capture():
	global counter 
	global lat1 
	global lon1 
	global alt1
	#get GNSS data
	report = gpsd.get_current()
	lat1 = "-9999"
	lon1 = "-9999"
	alt1 = "-9999"
	print(report)
	if getattr(report,'lat',0.0)!=0:
		lat1 = str(getattr(report,'lat',0.0))
	if getattr(report,'lon',0.0)!=0:
		lon1 = str(getattr(report,'lon',0.0))
	if getattr(report,'alt','nan')!= 'nan':
		alt1 = str(getattr(report,'alt','nan'))

	camera.capture(newpath + '/' + str(counter) + '.jpg')
	camera.capture(newpath + '/' + str(counter) + '.png')
	im = PIL.Image.open(str(newpath + '/' + str(counter) + '.jpg'))
	crop_img = crop_center(im,1024,1024)
	crop_img.save(croppath + '/crop' + str(counter) + '.jpg')
	txtfile = open(newpath + '/' + direcname + '.csv', 'a')
	txtfile.write( str(counter) + ',' + str(datetime.datetime.now()) +
	',' + lat1 + ',' + lon1 + ','+ alt1 + ',')
	txtfile.close()
	
	print(lat1)
	print(lon1)
	print(alt1)
	
	#prediction step
	#with pyDGS
	#pyDGS()
	#with TFLite:
	
	TFlitePred(crop_img)
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

def TFlitePred(crop_img):
    #get image in the correct shape,size, format
    converted_crop = np.array(crop_img, dtype=np.float32)
    r_crop_img = converted_crop/255
    crop_img_exp = np.expand_dims(r_crop_img, axis=0)
 
    common.set_input(interpreter, crop_img_exp)
    interpreter.invoke()
    
    global predictionstk
    predictions = common.output_tensor(interpreter, 0)
    predictionstk = predictions.tolist()
    predictionstk = [round(num,3) for num in predictionstk[0]]
    print(predictions)
    
    stats = pd.DataFrame(predictions)
    statsrounded = stats.round(decimals=3)
    statsrounded.to_csv(textarg, mode='a', header = False, index = False)
    return predictions
    	
grain_sizes_label= ["D_2(mm) ", "D_5(mm) ", "D_10(mm)", "D_16(mm)", "D_25(mm)", "D_50(mm)", "D_75(mm)", "D_84(mm)", "D_90(mm)", "D_95(mm)", "D_98(mm)"]  
def stats_update():
	stats.delete(0,END)
	for i in range(0,len(grain_sizes_label)):
		stats.insert(i, str(grain_sizes_label[i]) + ": " + str(predictionstk[i]))
		#stats.update()
		
def make_plt():
	x = predictionstk
	y = [2,5,10,16,25,50,75,84,90,95,98]

	fig, ax = plt.subplots(figsize=(4.5,5.5), dpi=35)
	ax.plot(x,y, color="green")
	#ax.text(size=1.2)
	# plt.xlabel("Grain Size (mm)")
	# plt.ylabel("% Finer")
	plt.grid()
	fig.savefig("figure" + str(counter-1) + ".png")

def photo_update():
	#place image on screen
	global img
	sandimage = newpath + '/' + str(counter-1) + '.png'
	img = tk.PhotoImage(file=sandimage) #counter minus 1 because image hasnt been taken yet 
	preview = Label(master, image=img)
	preview.place(height=previewsize, width=previewsize, relx=0.216, rely=0.02) #to fix so that no matter what it is square
	preview.update()

def plot_update():
	global grainplot
	plotfile = "/home/pi/Desktop/figure" + str(counter-1) + ".png"
	grainplot = tk.PhotoImage(file=plotfile)
	statsplot = Label(master, image=grainplot)
	statsplot.place(relheight=0.508, width=listsize , x=listplace, rely=0.098)
	statsplot.update()
		
#Update gui function
def updategui():
	stats_update()
	coord_update()
	photo_update()
	plot_update()

#Capture + update gui
def capturegui():
	subprocess.call(["./ringledon.sh"])
	capture()
	subprocess.call(["./ringledoff.sh"])
	make_plt()
	updategui()

#preview on/off
def preview():
	previewon()
	sleep(5)
	previewoff()

def coord_update():
	lattk = Label(master, text = "Latitude (DD): " +"\n"+ str(lat1), borderwidth=1, relief="solid",font = ("Consolas", 10))
	lattk.place(relheight=0.123, relwidth=0.176, relx=0.02, rely=0.608)
	lattk.update() #would it be better to make this global or put it in the capture function
	lontk = Label(master, text = "Longitude (DD): " +"\n"+ str(lon1), borderwidth=1, relief="solid",font = ("Consolas", 10))
	lontk.place(relheight=0.123, relwidth=0.176, relx=0.02, rely=0.731)
	lontk.update()
	elevtk = Label(master, text = "Altitude (m): " +"\n"+ str(alt1), borderwidth=1, relief="solid",font = ("Consolas", 10))
	elevtk.place(relheight=0.123, relwidth=0.176, relx=0.02, rely=0.854)
	elevtk.update()

### BELOW IS TKINTER CODE ###

#create main window

master = tk.Tk()

#screen height and width

screen_width = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()
print(screen_width)
print(screen_height)
master.geometry(str(screen_width)+'x'+str(screen_height))

#make title
master.title('SandCam')

#make buttons
previewbutton = tk.Button(master, text="Preview", font = ("Consolas", 22), command=preview,background='yellow') #uncomment
previewbutton.place(relheight=0.176, relwidth=0.176, relx=0.02, rely=0.216) 

shutterbutton = tk.Button(master, text="Capture", font = ("Consolas", 22), command=capturegui,background='green') #uncomment
shutterbutton.place(relheight=0.176, relwidth=0.176, relx=0.02, rely=0.412) 

#make labels
sandcam = Label(master, text = "Sandcam", borderwidth=1, relief="solid", font = ("Consolas", 22))
sandcam.place(relheight=0.176, relwidth=0.176, relx=0.02, rely=0.02)

# latestfile = Label(master, text = "last file", borderwidth=1, relief="solid")
# latestfile.place(relheight=0.176, relwidth=0.176, relx=0.02, rely=0.608)

lattk = Label(master, text = "Latitude (DD): ", borderwidth=1, relief="solid",font = ("Consolas", 10))
lattk.place(relheight=0.123, relwidth=0.176, relx=0.02, rely=0.608)

lontk = Label(master, text = "Longitude (DD): ", borderwidth=1, relief="solid",font = ("Consolas", 10))
lontk.place(relheight=0.123, relwidth=0.176, relx=0.02, rely=0.731)

elevtk = Label(master, text = "Altitude (m): ", borderwidth=1, relief="solid",font = ("Consolas", 10))
elevtk.place(relheight=0.123, relwidth=0.176, relx=0.02, rely=0.854)

##create height variable
previewsize = screen_height- (screen_height*0.10)
print(previewsize)
preview = Label(master, text = "Sandcam", borderwidth=1, relief="solid")
preview.place(height=previewsize, width=previewsize, relx=0.216, rely=0.02) #to fix so that no matter what it is square

#make ListBox
##create variable
listsize = screen_width - (previewsize + (.08*screen_width) + (screen_width*0.176))
listplace = (previewsize + (.06*screen_width) + (screen_width*0.176))

# statsplot = Label(master, borderwidth=1, relief="solid")
# statsplot.place(relheight=0.508, width=listsize , x=listplace, rely=0.098)
#larger font size in the font

#
#make clock
def time():
    string = strftime('%H:%M:%S')
    lbl.config(text = string)
    lbl.after(1000, time)
    
lbl = Label(master, font = ('Consolas', 15, 'bold'),
            background = 'black',
            foreground = 'green')
lbl.place(x=listplace, rely=0.02, relheight=0.058, width=listsize)

#graph
stats = tk.Listbox(master, borderwidth=1, relief="solid", font = ("Consolas", 8))
stats.place(relheight=(1-0.648), width=listsize , x=listplace, rely=0.628)

time()
#create
while True:
	master.mainloop()
