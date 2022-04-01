#Import Packages 
import time
import subprocess
import os
import datetime
from time import strftime
from tkinter import *
import tkinter as tk
#from tkinter.ttk import * #Not sure if this is needed for some reason, shifts all text to left align

#Latest Grain stats
#predictions = common.output_tensor(interpreter, 0)
grain_sizes = ["D_2(mm)", "D_5(mm)", "D_10(mm)", "D_16(mm)", "D_25(mm)", "D_50(mm)", "D_75(mm)", "D_84(mm)", "D_90(mm)", "D_95(mm)", "D_98(mm)"]  
print(predictions)

def stats_update():
	for i in range(1,len(grain_sizes)):
		stats.insert(i, str(grain_sizes[i]) + ": " + str(predictions[i]))
	stats.update()

#Update gui function
def update():
	stats_update()
	coord_update()

#Capture + update gui
def capturegui():
	capture()
	sleep(2)
	update()

#preview on/off
def preview():
	previewon()
	sleep(5)
	previewoff()

def coord_update():
	lattk = Label(master, text = "Lattitude (DD): " + str(lat1), borderwidth=1, relief="solid")
	lattk.place(relheight=0.058, relwidth=0.176, relx=0.02, rely=0.804)
	lattk.update()
	lontk = Label(master, text = "Longitude (DD): " + str(lon1), borderwidth=1, relief="solid")
	lontk.place(relheight=0.058, relwidth=0.176, relx=0.02, rely=0.862)
	lontk.update()
	elevtk = Label(master, text = "Altitude (m): " + str(alt1), borderwidth=1, relief="solid")
	elevtk.place(relheight=0.058, relwidth=0.176, relx=0.02, rely=0.920)
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
previewbutton = tk.Button(master, text="Preview", font = ("Times New Roman", 25))#, command=preview()) #uncomment
previewbutton.place(relheight=0.176, relwidth=0.176, relx=0.02, rely=0.216) 

shutterbutton = tk.Button(master, text="Capture", font = ("Times New Roman", 25))#,command=capturegui()) #uncomment
shutterbutton.place(relheight=0.176, relwidth=0.176, relx=0.02, rely=0.412) 
#make labels
sandcam = Label(master, text = "Sandcam + logo", borderwidth=1, relief="solid", font = ("Times New Roman", 25))
sandcam.place(relheight=0.176, relwidth=0.176, relx=0.02, rely=0.02)

latestfile = Label(master, text = "last file", borderwidth=1, relief="solid")
latestfile.place(relheight=0.176, relwidth=0.176, relx=0.02, rely=0.608)

lattk = Label(master, text = "Lattitude (DD): ", borderwidth=1, relief="solid")
lattk.place(relheight=0.058, relwidth=0.176, relx=0.02, rely=0.804)

lontk = Label(master, text = "Longitude (DD): ", borderwidth=1, relief="solid")
lontk.place(relheight=0.058, relwidth=0.176, relx=0.02, rely=0.862)

elevtk = Label(master, text = "Altitude (m): ", borderwidth=1, relief="solid")
elevtk.place(relheight=0.058, relwidth=0.176, relx=0.02, rely=0.920)

##create height variable
previewsize = screen_height- (screen_height*0.10)
print(previewsize)
preview= Label(master, text = "Sandcam", borderwidth=1, relief="solid")
preview.place(height=previewsize, width=previewsize, relx=0.216, rely=0.02) #to fix so that no matter what it is square

#make ListBox
##create variable
listsize = screen_width - (previewsize + (.08*screen_width) + (screen_width*0.176))
listplace = (previewsize + (.06*screen_width) + (screen_width*0.176))
stats = tk.Listbox(master, borderwidth=1, relief="solid")
stats.place(relheight=0.508, width=listsize , x=listplace, rely=0.098)

#make clock
def time():
    string = strftime('%H:%M:%S %p')
    lbl.config(text = string)
    lbl.after(1000, time)
    
lbl = Label(master, font = ('Times New Roman', 40, 'bold'),
            background = 'purple',
            foreground = 'white')
lbl.place(x=listplace, rely=0.02, relheight=0.058, width=listsize)

#graph
stats = tk.Listbox(master, borderwidth=1, relief="solid")
stats.place(relheight=(1-0.648), width=listsize , x=listplace, rely=0.628)

time()
#create
master.mainloop()
