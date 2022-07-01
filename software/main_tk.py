# Written by Jacob Stasiewicz and Evan Goldstein
#
# MIT License

#Loading screen
from tkinter import *
import tkinter as tk
import threading

started = False

# def loading_screen():
	# loading = Tk()
	# screen_width = loading.winfo_screenwidth()
	# screen_height = loading.winfo_screenheight()
	# print(screen_width)
	# print(screen_height)
	# loading.geometry(str(screen_width)+'x'+str(screen_height))
	
	# loading.protocol('WM_DELETE_WINDOW', lambda: loading.destroy if started else False)
	# loading.mainloop()

# threading.Thread(target=loading_screen).start()

#import packages
import time
start_time = time.time()
from gpiozero import Button, LED
from picamera import PiCamera
import gpsd
import os
import glob
import datetime
import subprocess
#from PIL import Image#, ImageTk
from PIL import ImageTk, Image
import PIL.Image
import numpy as np
import pandas as pd
from pycoral.utils import edgetpu
from pycoral.utils import dataset
from pycoral.adapters import common
from pycoral.adapters import classify
#Import time Packages 
from time import sleep 
from time import strftime
#Import NeoPixel Commands
import board
import neopixel
import random, string
#Import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
stop_time = print("importing packages : " + str(time.time() - start_time))

#software version 
software_version = 0.1
model_version = 0.1

#define gpio pins and variables
start_time = time.time()
pwd = os.getcwd()
camera = PiCamera()
camera.resolution = (2048,2048)
counter = 1
stop_time = print("defining pins and vars: " + str(time.time() - start_time))

#GPSD_connect
start_time = time.time()
gpsd.connect()
stop_time = print("GPS connect: " + str(time.time() - start_time))

#TFLITE stuff
start_time = time.time()
path_to_model = "./models/SandCam_MNv2_QAT_notdense_edgetpu.tflite"
# Initialize the TF interpreter
interpreter = edgetpu.make_interpreter(path_to_model)
interpreter.allocate_tensors()
#uncomment lines below to debug and look at expected I/O
#print(interpreter.get_input_details())
#print(interpreter.get_output_details())
stop_time = print("TFLITE_stuff: " + str(time.time() - start_time))

#make new directory and create text file within
#random 5 letter generation fn
def random_five():
	return ''.join(random.sample(string.ascii_uppercase,5))

#Create directories
def startup():
	global direcname
	direcname = random_five()
	global newpath
	newpath = "/home/pi/Documents/sand_cam/data" + '/' + direcname
	global croppath
	croppath = "/home/pi/Documents/sand_cam/data" + '/' + direcname + '/crop'
	global plotpath
	plotpath = "/home/pi/Documents/sand_cam/data" + '/' + direcname + '/plot'
	os.makedirs(newpath)
	os.makedirs(croppath)
	os.makedirs(plotpath)

	print("Made a Directory for this session:")
	print(newpath)

	#Make textfile

	txtfile = open(newpath + '/' + direcname + '.csv', 'w+')
	txtfile.write('software_version ' + str(software_version) + ',' +  'model-version ' + str(model_version) + "\n")
	txtfile.write('Filename, Date/Time (UTC), Latitude (DD) , Longitude (DD), Altitude(m), D_2(mm), D_5(mm), D_10(mm), D_16(mm), D_25(mm), D_50(mm), D_75(mm), D_84(mm), D_90(mm), D_95(mm), D_98(mm) '"\n")
	txtfile.close()
	global textarg
	textarg = str(newpath + '/' + direcname + '.csv')
	#global croparg
	#croparg = str(croppath)

	print("Made a txt file for this session")

startup()

### BELOW IS FUNCTION CODE ###
start_time = time.time()
def capture():
	import time
	start_time = time.time()
	global counter 
	global lat1 
	global lon1 
	global alt1
	#get GNSS data
	report = gpsd.get_current()
	lat1 = "-9999"
	lon1 = "-9999"
	alt1 = "-9999"
	time = "na"
	print(report)
	if getattr(report,'lat',0.0)!=0:
		lat1 = str(getattr(report,'lat',0.0))
	if getattr(report,'lon',0.0)!=0:
		lon1 = str(getattr(report,'lon',0.0))
	if getattr(report,'alt','nan')!= 'nan':
		alt1 = str(getattr(report,'alt','nan'))
	if getattr(report,'time','nan')!= 'nan':
		time = str(getattr(report,'time','nan'))
	sleep(2)
	camera.capture(newpath + '/' + str(counter) + '.jpg')
	im = PIL.Image.open(str(newpath + '/' + str(counter) + '.jpg'))
	crop_img = crop_center(im,1024,1024)
	crop_img.save(croppath + '/crop' + str(counter) + '.jpg')
	txtfile = open(newpath + '/' + direcname + '.csv', 'a')
	txtfile.write( str(counter) + ',' + str(time) +
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
	import time
	stop_timer = time.time() - start_time
	stop_time = print("capture function: " + str(stop_timer))

def restart_gui():
	global counter
	counter = 1
	print(counter)
	
	startup()
	
	stats.delete(0,END)
	
	lattk = Label(master, text = "Latitude (DD): ", borderwidth=1, relief="solid",font = ("Consolas", 10))
	lattk.place(relheight=0.123, relwidth=0.176, relx=0.02, rely=0.608)

	lontk = Label(master, text = "Longitude (DD): ", borderwidth=1, relief="solid",font = ("Consolas", 10))
	lontk.place(relheight=0.123, relwidth=0.176, relx=0.02, rely=0.731)

	elevtk = Label(master, text = "Altitude (m): ", borderwidth=1, relief="solid",font = ("Consolas", 10))
	elevtk.place(relheight=0.123, relwidth=0.176, relx=0.02, rely=0.854)
	
	preview = Label(master, text = "Sandcam", borderwidth=1, relief="solid")
	preview.place(height=previewsize, width=previewsize, relx=0.216, rely=0.02)
	
	statsplot = tk.Button(master, text = "Plot")
	statsplot.place(relheight=0.508, width=listsize , x=listplace, rely=0.098)
	
def previewon():
	import time
	start_time = time.time()
	camera.start_preview()
	subprocess.call(["./ringledon.sh"])
	stop_timer = time.time() - start_time
	stop_time = print("preview on function: " + str(stop_timer))
	
def previewoff():
	import time
	start_time = time.time()
	camera.stop_preview()
	subprocess.call(["./ringledoff.sh"])
	stop_timer = time.time() - start_time
	stop_time = print("preview off function: " + str(stop_timer))
	
def crop_center(pil_img, crop_width, crop_height):
   import time
   start_time = time.time()
   img_width, img_height = pil_img.size
   return pil_img.crop(((img_width - crop_width) // 2,
                          (img_height - crop_height) // 2,
                          (img_width + crop_width) // 2,
                          (img_height + crop_height) // 2))
   stop_timer = time.time() - start_time
   stop_time = print("crop_center function: " + str(stop_timer))
                          
def pyDGS():
	import time
	global textarg 
	list_of_files_crop = glob.glob(croppath + '/*.jpg')
	latest_file_crop = str(max(list_of_files_crop, key=os.path.getctime))
	print("using pyDGS to get grain size")
	subprocess.call(["python3", "example_test.py", latest_file_crop, textarg])
	print("ready for next picture")

def TFlitePred(crop_img):
    import time
    start_time = time.time()
    #get image in the correct shape,size, format
    crop_img = crop_img.resize((224,224))
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
    stop_timer = time.time() - start_time
    stop_time = print("TF_Lite function: " + str(stop_timer))
    	
grain_sizes_label= ["D_2(mm) ", "D_5(mm) ", "D_10(mm)", "D_16(mm)", "D_25(mm)", "D_50(mm)", "D_75(mm)", "D_84(mm)", "D_90(mm)", "D_95(mm)", "D_98(mm)"]  

def stats_update():
	import time
	start_time = time.time()
	stats.delete(0,END)
	for i in range(0,len(grain_sizes_label)):
		stats.insert(i, str(grain_sizes_label[i]) + ": " + str(predictionstk[i]))
		#stats.update()
	stop_timer = time.time() - start_time
	stop_time = print("sed_stats function: " + str(stop_timer))
		
def make_plt():
	import time
	start_time = time.time()
	x = predictionstk
	cdf = [.02,.05,.10,.16,.25,.50,.75,.84,.90,.95,.98]
	pdf = np.gradient(cdf)
	
	#cdf
	fig, ax = plt.subplots(figsize=(4.5,5.5), dpi=35)
	ax.plot(x,cdf, color="green", linewidth = 2)
	plt.grid()
	plt.xticks(size = 16)
	plt.yticks(size = 16)
	plt.title("CDF Sample " + str(counter-1), fontsize = 16, fontweight = "bold" )
	ax.tick_params(axis="x", rotation = 50)
	ax.set_xlim([min(x), max(x)])
	ax.set_ylim([0, 1])
	fig.savefig(plotpath + "/" + "figure_cdf" + str(counter-1) + ".png")
	
	#pdf
	fig, ax = plt.subplots(figsize=(4.5,5.5), dpi=35)
	ax.plot(x,pdf, color="red", linewidth = 2)
	plt.grid()
	plt.xticks(size = 16)
	plt.yticks(size = 16)
	plt.title("PDF Sample " + str(counter-1), fontsize = 16, fontweight = "bold" )
	ax.tick_params(axis="x", rotation = 50)
	ax.set_xlim([min(x), max(x)])
	ax.set_ylim([0, 1])
	fig.savefig(plotpath + "/" + "figure_pdf" + str(counter-1) + ".png")
	stop_timer = time.time() - start_time
	stop_time = print("make_plot function: " + str(stop_timer))
	
current_plt = 1 
	
def change_plt():
	import time
	start_time = time.time()
	global current_plt
	if current_plt == 1:
		current_plt = 0
	else:
		current_plt = 1
	plot_update()
	stop_timer = time.time() - start_time
	stop_time = print("change_plt function: " + str(stop_timer))
	
def plot_update():
	import time
	start_time = time.time()
	global grainplot
	if current_plt == 1:
		plotfile = plotpath + "/" + "figure_cdf" + str(counter-1) + ".png"
		grainplot = tk.PhotoImage(file=plotfile)
		statsplot = tk.Button(master, image=grainplot, command=change_plt, bg='#e7ac1d')
		statsplot.place(relheight=0.508, width=listsize , x=listplace, rely=0.098)
		statsplot.update()
	else:
		plotfile = plotpath + "/" + "figure_pdf" + str(counter-1) + ".png"
		grainplot = tk.PhotoImage(file=plotfile)
		statsplot = tk.Button(master, image=grainplot, command=change_plt,bg='#e7ac1d')
		statsplot.place(relheight=0.508, width=listsize , x=listplace, rely=0.098)
		statsplot.update()
	stop_timer = time.time() - start_time
	stop_time = print("plot_update function: " + str(stop_timer))
	
def photo_update():
	import time
	start_time = time.time()
	#place image on screen
	global img3
	sandimage = newpath + '/' + str(counter-1) + '.jpg'
	img1 = PIL.Image.open(sandimage) #counter minus 1 because image hasnt been taken yet 
	previewsize = screen_height - (screen_height*0.10) #this creates the maximum square size we can have in the middle of the screen
	img2 = img1.resize((int(previewsize),int(previewsize)))
	img3 = ImageTk.PhotoImage(img2)
	preview = Label(master, image=img3)
	preview.place(height=previewsize, width=previewsize, relx=0.216, rely=0.02) #to fix so that no matter what it is square
	preview.update()
	stop_timer = time.time() - start_time
	stop_time = print("photo_update function: " + str(stop_timer))
		
#Update gui function
def updategui():
	import time
	start_time = time.time()
	stats_update()
	coord_update()
	photo_update()
	make_plt()
	plot_update()
	stop_timer = time.time() - start_time
	stop_time = print("updategui function: " + str(stop_timer))

#Capture + update gui
def capturegui():
	import time
	start_time = time.time()
	subprocess.call(["./ringledon.sh"])
	capture()
	subprocess.call(["./ringledoff.sh"])
	#make_plt()
	updategui()
	stop_timer = time.time() - start_time
	stop_time = print("capturegui function: " + str(stop_timer))

#preview on/off
def preview():
	import time
	start_time = time.time()
	previewon()
	sleep(5)
	previewoff()
	stop_timer = time.time() - start_time
	stop_time = print("preview function: " + str(stop_timer))

def coord_update():
	import time
	start_time = time.time()
	lattk = Label(master, text = "Latitude (DD): " +"\n"+ str(lat1), borderwidth=1, relief="solid",font = ("Consolas", 10),bg='#e7ac1d')
	lattk.place(relheight=0.123, relwidth=0.176, relx=0.02, rely=0.608)
	lattk.update() #would it be better to make this global or put it in the capture function
	lontk = Label(master, text = "Longitude (DD): " +"\n"+ str(lon1), borderwidth=1, relief="solid",font = ("Consolas", 10),bg='#e7ac1d')
	lontk.place(relheight=0.123, relwidth=0.176, relx=0.02, rely=0.731)
	lontk.update()
	elevtk = Label(master, text = "Altitude (m): " +"\n"+ str(alt1), borderwidth=1, relief="solid",font = ("Consolas", 10),bg='#e7ac1d')
	elevtk.place(relheight=0.123, relwidth=0.176, relx=0.02, rely=0.854)
	elevtk.update()
	stop_timer = time.time() - start_time
	stop_time = print("coord_update function: " + str(stop_timer))

def pop_up():
	global direcs
	list_of_sessions = os.listdir('/home/pi/Documents/sand_cam/data')
	global popup
	popup = Toplevel(master)
	popup.geometry(str(int(screen_width/2))+'x'+str(int(screen_height/2)))
	
	#Make listbox for directories
	direcs = tk.Listbox(popup, font = ("Consolas", 12),bg='#e15e28')
	direcs.place(relheight = 1, relwidth = 0.5 , x = 0, y = 0)
	
	#Make Load button
	Loadbtn = tk.Button(popup, text = "Load Session", font = ("Consolas", 12), command = load_direc,bg='#e7ac1d')
	Loadbtn.place(relheight = 1 , relwidth = 0.5, relx = 0.5, y = 0)
	
	for i in range(0,len(list_of_sessions)):
		direcs.insert(i, str(list_of_sessions[i]))
	
def load_direc():
	selected_direc = direcs.curselection()
	global direcname
	direcname = direcs.get(selected_direc)
	
	global newpath
	newpath = "/home/pi/Documents/sand_cam/data" + '/' + direcname
	
	global croppath
	croppath = "/home/pi/Documents/sand_cam/data" + '/' + direcname + '/crop'
	
	global plotpath
	plotpath = "/home/pi/Documents/sand_cam/data" + '/' + direcname + '/plot'
	
	global textarg
	textarg = str(newpath + '/' + direcname + '.csv')
	
	# files = os.listdir(croppath)
	# global counter
	# counter = max([int(sub[4]) for sub in files]) + 1
	# print(counter)
	
	session_hash = Label(master, text = direcname, font = ('Consolas', 15, 'bold'),
            background = 'black',
            foreground = 'green')
	session_hash.place(x=listplace, rely=0.02, relheight=0.058, width=listsize)
	
	txtfile = open(newpath + '/' + direcname + '.csv', 'r')
	for line in txtfile:
		pass
	last_line = line.split(",")
	txtfile.close()
	
	global counter
	counter = int(last_line[0])
	print(counter)
	global lat1
	lat1 = last_line[2]
	global lon1
	lon1 = last_line[3]
	global alt1
	alt1 =  last_line[4]
	global predictionstk
	predictionstk = last_line[5:16]
	print(predictionstk)
	
	coord_update()
	stats_update()
	photo_update()
	plot_update()
	
	counter = counter + 1
	popup.destroy()

stop_time = print("Create functions: " + str(time.time() - start_time))

### BELOW IS TKINTER CODE ###

#create main window
start_time = time.time()
master = tk.Tk()

#define ratios
screen_width = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()
print(screen_width)
print(screen_height)
master.geometry(str(screen_width)+'x'+str(screen_height))

previewsize = screen_height- (screen_height*0.10)
listsize = screen_width - (previewsize + (.08*screen_width) + (screen_width*0.176))
listplace = (previewsize + (.06*screen_width) + (screen_width*0.176))

#make title
master.title('SandCam')

#make menu options
mainmenu = Menu(master)
mainmenu.add_command(label = "Load", command = pop_up)
mainmenu.add_command(label = "New", command = restart_gui)
mainmenu.add_command(label = "Exit", command = master.destroy)

master.config(menu = mainmenu)
master.config(bg="white")

#make buttons
previewbutton = tk.Button(master, text="Preview", font = ("Consolas", 22), command=preview,bg='#e15e28') #uncomment
previewbutton.place(relheight=0.176, relwidth=0.176, relx=0.02, rely=0.216) 

shutterbutton = tk.Button(master, text="Capture", font = ("Consolas", 22), command=capturegui,background='#874ae2') #uncomment
shutterbutton.place(relheight=0.176, relwidth=0.176, relx=0.02, rely=0.412) 

statsplot = tk.Button(master, text = "Plot",bg='#e7ac1d')
statsplot.place(relheight=0.508, width=listsize , x=listplace, rely=0.098)

#make labels
sandcam = Label(master, text = "Sandcam", borderwidth=0, font = ("Consolas", 10), bg ="white")
sandcam.place(relheight=0.176, relwidth=0.088, relx=0.02, rely=0.02)

lattk = Label(master, text = "Latitude (DD): ",font = ("Consolas", 10),bg='#e7ac1d')
lattk.place(relheight=0.123, relwidth=0.176, relx=0.02, rely=0.608)

lontk = Label(master, text = "Longitude (DD): ",font = ("Consolas", 10),bg='#e7ac1d')
lontk.place(relheight=0.123, relwidth=0.176, relx=0.02, rely=0.731)

elevtk = Label(master, text = "Altitude (m): ",font = ("Consolas", 10),bg='#e7ac1d')
elevtk.place(relheight=0.123, relwidth=0.176, relx=0.02, rely=0.854)

session_hash = Label(master, text = direcname, font = ('Consolas', 15, 'bold'),
            background = '#e15e28',
            foreground = 'black')
session_hash.place(x=listplace, rely=0.02, relheight=0.058, width=listsize)

##create height variable
preview = Label(master, text = "Sandcam", borderwidth=1, font = ("Consolas", 22), relief="solid",bg='#e7ac1d')
preview.place(height=previewsize-.02, width=previewsize, relx=0.216, rely=0.02) #to fix so that no matter what it is square

#make ListBox

stats = tk.Listbox(master, borderwidth=1, relief="solid", font = ("Consolas", 8),bg='#e7ac1d')
stats.place(relheight=(1-0.648), width=listsize , x=listplace, rely=0.628)

stop_time = print("make tk widgets function: " + str(time.time() - start_time))

#create photo
logo = '/home/pi/Documents/sand_cam/scripts/sandcam_logo_white-01.png'
logo1 = PIL.Image.open(logo) 
previewsize_h = screen_height * 0.176  
previewsize_w = screen_width * 0.078
logo2 = logo1.resize((int(previewsize_h),int(previewsize_w)))
logo3 = ImageTk.PhotoImage(logo2)
logoimg = Label(master, image=logo3, bg="white")
logoimg.place(relheight=0.176, relwidth=0.098, relx=0.100, rely=0.02) 

#destroy loading screen
started = True
while True:
	master.mainloop()
