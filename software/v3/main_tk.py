# Written by Jacob Stasiewicz and Evan Goldstein
#
# MIT License

#import packages
import time, random, string
from time import sleep 
from picamera2 import Picamera2, Preview
from libcamera import controls
import gpsd
import os, subprocess
from PIL import ImageTk
import PIL.Image
import numpy as np
import pandas as pd
from scipy import interpolate
import matplotlib.pyplot as plt
from tkinter import *
import tkinter as tk
from tflite_runtime.interpreter import Interpreter

#DEFINE SOFTWARE VERSIONS
software_version = 0.3
model_version = 0.2


# Get the current working directory
pwd = os.getcwd()
# Create a new instance of the Picamera2 class
picam2 = Picamera2()
# Create a preview configuration for the camera
camera_config = picam2.create_preview_configuration()
# Configure the camera using the preview configuration
picam2.configure(camera_config)
# Set the autofocus mode to continuous
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
# Start the camera preview
picam2.start()
# Stop the camera preview
picam2.stop_preview()
#camera.resolution = (2048,2048)

#GPSD_connect
gpsd.connect()

path_to_model = "./models/SandCam_MNv2_QAT_notdense_aug27.tflite"

# Initialize the TF interpreter
interpreter = Interpreter(path_to_model)
interpreter.allocate_tensors()
#uncomment lines below to debug and look at expected I/O
#print(interpreter.get_input_details())
#print(interpreter.get_output_details())

#make new directory and create text file within
#random 5 letter generation fn
def random_five():
	return ''.join(random.sample(string.ascii_uppercase,5))

### BELOW IS FUNCTION CODE ###
counter = 0

#start_time = time.time()
def capture():
    """
    This function captures an image using a camera and extracts GPS data to save along with the image.
    The captured image is cropped to a size of 1024 x 1024 pixels and saved in a specified directory.

    Returns:
    None
    """

    global counter
    counter = counter + 1
    #get GNSS data
    global lat1
    global lon1
    global elev1
    lat1 = "-9999"
    lon1 = "-9999"
    elev1 = "-9999"
    time = "na"
    report = gpsd.get_current()

	
    # Print the GNSS data and save the latitude, longitude, elevation, and time values
    print(report)
    if getattr(report,'lat',0.0)!=0:
        lat1 = str(getattr(report,'lat',0.0))
    if getattr(report,'lon',0.0)!=0:
        lon1 = str(getattr(report,'lon',0.0))
    if getattr(report,'elev','nan')!= 'nan':
        elev1 = str(getattr(report,'elev','nan'))
    if getattr(report,'time','nan')!= 'nan':
        time = str(getattr(report,'time','nan'))
	
    # Capture an image using the camera, crop it to 1024 x 1024 pixels, and save it in the specified directory
    #picam2.start()
    #sleep(2)
    picam2.start_and_capture_file(newpath + '/' + str(counter) + '.jpg')
    #picam2.stop()
    im = PIL.Image.open(str(newpath + '/' + str(counter) + '.jpg'))
    crop_img = crop_center(im,1024,1024)
    crop_img.save(croppath + '/crop' + str(counter) + '.jpg')
    
    # Save the GPS data along with the image in a CSV file
    txtfile = open(newpath + '/' + direcname + '.csv', 'a')
    txtfile.write( str(counter) + ',' + str(time) +
    ',' + lat1 + ',' + lon1 + ','+ elev1 + ',')
    txtfile.close()

    print(lat1)
    print(lon1)
    print(elev1)
    
    TFlitePred(crop_img)
    print('that was picture:')
    print(counter)

def restart_gui():
    """
    Description: This function resets the GUI and creates a new session directory with a random name. 
    It also creates a new text file in the directory to store data and sets up labels and buttons for the GUI.
    """

    global counter
    counter = 0
    print(counter)
    
    global direcname
    direcname = random_five()
    global newpath
    newpath = "/home/sediment/Documents/data" + '/' + direcname
    global croppath
    croppath = "/home/sediment/Documents/data" + '/' + direcname + '/crop'
    global plotpath
    plotpath = "/home/sediment/Documents/data" + '/' + direcname + '/plot'
    os.makedirs(newpath)
    os.makedirs(croppath)
    os.makedirs(plotpath)

    print("Made a Directory for this session:")
    print(newpath)

    #Make textfile

    txtfile = open(newpath + '/' + direcname + '.csv', 'w+')
    txtfile.write('software_version ' + str(software_version) + ',' +  'model-version ' + str(model_version) + "\n")
    txtfile.write('Filename, Date/Time (UTC), Latitude (DD) , Longitude (DD), Elevation(m), D_2(mm), D_5(mm), D_10(mm), D_16(mm), D_25(mm), D_50(mm), D_75(mm), D_84(mm), D_90(mm), D_95(mm), D_98(mm) '"\n")
    txtfile.close()
    global textarg
    textarg = str(newpath + '/' + direcname + '.csv')
    #global croparg
    #croparg = str(croppath)
    
    previewbutton['state'] = NORMAL
    shutterbutton['state'] = NORMAL
    
    print("Made a txt file for this session")
    
    stats.delete(0,END)
    
    lattk = Label(master, text = "Latitude (DD): ", borderwidth=1, relief="solid",font = ("Consolas", 10),bg='#e7ac1d')
    lattk.place(relheight=0.123, relwidth=0.176, relx=0.02, rely=0.608)

    lontk = Label(master, text = "Longitude (DD): ", borderwidth=1, relief="solid",font = ("Consolas", 10),bg='#e7ac1d')
    lontk.place(relheight=0.123, relwidth=0.176, relx=0.02, rely=0.731)

    elevtk = Label(master, text = "Elevation (m): ", borderwidth=1, relief="solid",font = ("Consolas", 10),bg='#e7ac1d')
    elevtk.place(relheight=0.123, relwidth=0.176, relx=0.02, rely=0.854)
    
    preview = Label(master, text = "Instagrain", borderwidth=1, relief="solid",bg='#e7ac1d')
    preview.place(height=previewsize, width=previewsize, relx=0.216, rely=0.02)
    
    statsplot = tk.Button(master, text = "Plot",bg='#e7ac1d', state = NORMAL)
    statsplot.place(relheight=0.508, width=listsize , x=listplace, rely=0.098)
    
    session_hash = Label(master, text = direcname, font = ('Consolas', 15, 'bold'),
            background = '#e15e28',
            foreground = 'black')
    session_hash.place(x=listplace, rely=0.02, relheight=0.058, width=listsize)
    

    
def crop_center(pil_img, crop_width, crop_height):
   #start_time = time.time()
   img_width, img_height = pil_img.size
   return pil_img.crop(((img_width - crop_width) // 2,
                          (img_height - crop_height) // 2,
                          (img_width + crop_width) // 2,
                          (img_height + crop_height) // 2))
   #stop_timer = time.time() - start_time
   #stop_time = print("crop_center function: " + str(stop_timer))
                          
def TFlitePred(crop_img):
    #get image in the correct shape,size, format
    crop_img = crop_img.resize((224,224))
    converted_crop = np.array(crop_img, dtype=np.float32)
    r_crop_img = converted_crop/255
    crop_img_exp = np.expand_dims(r_crop_img, axis=0)
 
    input_index = interpreter.get_input_details()[0]["index"]
    output_index = interpreter.get_output_details()[0]["index"]
    interpreter.set_tensor(input_index, crop_img_exp)
    interpreter.invoke()
    
    global predictionstk
    predictions = interpreter.get_tensor(output_index)
    predictions = np.sort(predictions)
    #print(predictions)
    predictionstk = predictions.tolist()

    predictionstk = [round(num,3) for num in predictionstk[0]]
    
    stats = pd.DataFrame(predictions)
    statsrounded = stats.round(decimals=3)
    statsrounded.to_csv(textarg, mode='a', header = False, index = False)
    return predictions

        
grain_sizes_label= ["D_2(mm) ", "D_5(mm) ", "D_10(mm)", "D_16(mm)", "D_25(mm)", "D_50(mm)", "D_75(mm)", "D_84(mm)", "D_90(mm)", "D_95(mm)", "D_98(mm)"]  

def stats_update():

    #start_time = time.time()
    stats.delete(0,END)
    for i in range(0,len(grain_sizes_label)):
        stats.insert(i, str(grain_sizes_label[i]) + ": " + str(predictionstk[i]))
        #stats.update()
    #stop_timer = time.time() - start_time
    #stop_time = print("sed_stats function: " + str(stop_timer))
        
def make_plt():
    x = predictionstk
    cdf = [2,5,10,16,25,50,75,84,90,95,98]
    InterpF = interpolate.PchipInterpolator(cdf,x)
    ynew = np.arange(0, 101, 1)
    xnew = InterpF(ynew)   # use interpolation function
    #cdf
    fig, ax = plt.subplots(figsize=(4.5,5.5), dpi=35) 
    ax.semilogx(xnew,ynew, color="green", linewidth = 2)
    plt.grid()
    plt.xticks(size = 16)
    plt.yticks(size = 16)
    plt.title("Cumulative Grain Size, Sample " + str(counter), fontsize = 16, fontweight = "bold" )
    ax.tick_params(axis="x", rotation = 50)
    ax.set_xlim([0.01, 10])
    ax.set_ylim([0, 100])
    fig.savefig(plotpath + "/" + "CDF" + str(counter) + ".png")
    
    #CDF linear
    fig, ax = plt.subplots(figsize=(4.5,5.5), dpi=35)
    ax.plot(xnew,ynew, color="red", linewidth = 2)
    plt.grid()
    plt.xticks(size = 16)
    plt.yticks(size = 16)
    plt.title("Cumul. Grain Size (lin) Sample " + str(counter), fontsize = 16, fontweight = "bold" )
    ax.tick_params(axis="x", rotation = 50)
    #ax.set_xlim([min(x), max(x)])
    ax.set_ylim([0, 100])
    fig.savefig(plotpath + "/" + "CDF_linear_" + str(counter) + ".png")
    
current_plt = 1 
    
def change_plt():

    global current_plt
    if current_plt == 1:
        current_plt = 0
    else:
        current_plt = 1
    plot_update()

     
def plot_update():
    """
    This function updates a plot of data displayed in a tkinter GUI window. 
    It checks the value of a global variable called current_plt and based on its value, 
    it loads an image file of the plot from the specified plotpath directory. 
    It then creates a Button widget in the tkinter GUI window with the loaded 
    plot image and sets its size and position using the place() method. 
    Finally, it updates the plot widget using the update() method.
    """
    global grainplot
    if current_plt == 1:
        plotfile = plotpath + "/" + "CDF" + str(counter) + ".png"
        grainplot = tk.PhotoImage(file=plotfile)
        statsplot = tk.Button(master, image=grainplot, command=change_plt, bg='#e7ac1d')
        statsplot.place(relheight=0.508, width=listsize , x=listplace, rely=0.098)
        statsplot.update()
    else:
        plotfile = plotpath + "/" + "CDF_linear_" + str(counter) + ".png"
        grainplot = tk.PhotoImage(file=plotfile)
        statsplot = tk.Button(master, image=grainplot, command=change_plt,bg='#e7ac1d')
        statsplot.place(relheight=0.508, width=listsize , x=listplace, rely=0.098)
        statsplot.update()
    
def photo_update():
    """
    This function is responsible for updating the preview image on the screen. 
    It opens the image file saved in the 'crop' folder with the corresponding counter value. 
    Then, it resizes the image to fit the maximum square size possible in the 
    middle of the screen. Finally, it creates a new Tkinter PhotoImage object from 
    the resized image and places it in a Label widget. The widget is then positioned 
    on the screen and updated to show the new image.
    """
    #Need to add loading parameter because the computer doesnt know if it is
    #starting a new parameter or loading one 
    #place image on screen
    global img3
    sandimage = newpath + '/crop/crop' + str(counter) + '.jpg'
    img1 = PIL.Image.open(sandimage) #counter minus 1 because image hasnt been taken yet 
    previewsize = screen_height - (screen_height*0.10) #this creates the maximum square size we can have in the middle of the screen
    img2 = img1.resize((int(previewsize),int(previewsize)))
    img3 = ImageTk.PhotoImage(img2)
    preview = Label(master, image=img3)
    preview.place(height=previewsize, width=previewsize, relx=0.216, rely=0.02) #to fix so that no matter what it is square
    preview.update()
        
#Update gui function
def updategui():
    stats_update()
    coord_update()
    photo_update()
    make_plt()
    plot_update()

#Capture + update gui
def capturegui():
    subprocess.call(["./ringledon.sh"])
    capture()
    subprocess.call(["./ringledoff.sh"])
    updategui()

#preview on/off
def preview():
    subprocess.call(["./ringledon.sh"])
    picam2.start_preview(True)
    #picam2.start(show_preview=True)
    picam2.title_fields = ["ExposureTime", "AnalogueGain",]
    time.sleep(5)
    picam2.stop_preview()
    #previewon()
    #sleep(5)
    #previewoff()
    subprocess.call(["./ringledoff.sh"])

#Update Coordinates on GUI
def coord_update():
    lattk = Label(master, text = "Latitude (DD): " +"\n"+ str(lat1), borderwidth=1, relief="solid",font = ("Consolas", 10),bg='#e7ac1d')
    lattk.place(relheight=0.123, relwidth=0.176, relx=0.02, rely=0.608)
    lattk.update() #would it be better to make this global or put it in the capture function
    lontk = Label(master, text = "Longitude (DD): " +"\n"+ str(lon1), borderwidth=1, relief="solid",font = ("Consolas", 10),bg='#e7ac1d')
    lontk.place(relheight=0.123, relwidth=0.176, relx=0.02, rely=0.731)
    lontk.update()
    elevtk = Label(master, text = "Elevation (m): " +"\n"+ str(elev1), borderwidth=1, relief="solid",font = ("Consolas", 10),bg='#e7ac1d')
    elevtk.place(relheight=0.123, relwidth=0.176, relx=0.02, rely=0.854)
    elevtk.update()

def pop_up():
    """
    creates a popup window. It gets a list of directories and creates a Listbox to show these 
    directories. Additionally, it creates a button with text "Load Session" that can be clicked 
    to load a directory from the list. When the button is clicked, the load_direc() function 
    is called. The size and position of the popup window are defined using the geometry() method. 
    The function makes use of global variables direcs and popup.
    """

    global direcs
    list_of_sessions = os.listdir('/home/sediment/Documents/data')
    global popup
    popup = Toplevel(master)
    popup.geometry(str(int(screen_width/2))+'x'+str(int(screen_height/2)))
    #popup.place(relx = 0.25, rely =0.25)
    
    #Make listbox for directories
    direcs = tk.Listbox(popup, font = ("Consolas", 12),bg='#e15e28')
    direcs.place(relheight = 1, relwidth = 0.5 , x = 0, y = 0)
    
    #Make Load button
    Loadbtn = tk.Button(popup, text = "Load Session", font = ("Consolas", 12), command = load_direc,bg='#e7ac1d')
    Loadbtn.place(relheight = 1 , relwidth = 0.5, relx = 0.5, y = 0)
    
    for i in range(0,len(list_of_sessions)):
        direcs.insert(i, str(list_of_sessions[i]))
    
def load_direc():
    """
    Loads the selected session directory from the pop-up window and updates various widgets in the main window.
    It first enables certain buttons and widgets on the main window such as preview button, shutter button and stats plot. 
    Then, it gets the selected directory name from the listbox, creates the paths for crop, plot, and 
    csv files based on the selected directory name. It then reads the last line of the csv file to get the counter 
    and other values such as lat1, lon1, elev1 and predictionstk. The function updates various widgets in the main window 
    by calling other functions like coord_update(), stats_update(), photo_update() and plot_update(). 
    Finally, it destroys the pop-up window.
    """
    
    previewbutton['state'] = NORMAL
    shutterbutton['state'] = NORMAL
    statsplot['state'] = NORMAL
    
    selected_direc = direcs.curselection()
    global direcname
    direcname = direcs.get(selected_direc)
    
    global newpath
    newpath = "/home/sediment/Documents/data" + '/' + direcname
    
    global croppath
    croppath = "/home/sediment/Documents/data" + '/' + direcname + '/crop'
    
    global plotpath
    plotpath = "/home/sediment/Documents/data" + '/' + direcname + '/plot'
    
    global textarg
    textarg = str(newpath + '/' + direcname + '.csv')
    
    session_hash = Label(master, text = direcname, font = ('Consolas', 15, 'bold'),
            background = '#e15e28',
            foreground = 'black')
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
    global lon1
    global elev1
    global predictionstk
    lat1 = last_line[2]
    lon1 = last_line[3]
    elev1 =  last_line[4]
    predictionstk = last_line[5:16]
    print(predictionstk)
    
    coord_update()
    stats_update()
    photo_update()
    plot_update()
    
    popup.destroy()


### BELOW IS TKINTER CODE ###

#create main window

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
master.title('Instagrain')

#make menu options
mainmenu = Menu(master)
mainmenu.add_command(label = "Load", command = pop_up)
mainmenu.add_command(label = "New", command = restart_gui)
mainmenu.add_command(label = "Exit", command = master.destroy)

master.config(menu = mainmenu)
master.config(bg="white")

#make buttons
previewbutton = tk.Button(master, text="Preview", font = ("Consolas", 22), command=preview,bg='#e15e28', state = DISABLED) #uncomment
previewbutton.place(relheight=0.176, relwidth=0.176, relx=0.02, rely=0.216) 

shutterbutton = tk.Button(master, text="Capture", font = ("Consolas", 22), command=capturegui,background='#874ae2', state = DISABLED) #uncomment
shutterbutton.place(relheight=0.176, relwidth=0.176, relx=0.02, rely=0.412) 

statsplot = tk.Button(master, text = "Plot",bg='#e7ac1d', state = DISABLED)
statsplot.place(relheight=0.508, width=listsize , x=listplace, rely=0.098)

#make labels
sandcam = Label(master, text = "Instagrain", borderwidth=0, font = ("Consolas", 10), bg ="white")
sandcam.place(relheight=0.176, relwidth=0.088, relx=0.02, rely=0.02)

lattk = Label(master, text = "Latitude (DD): ",font = ("Consolas", 10),bg='#e7ac1d')
lattk.place(relheight=0.123, relwidth=0.176, relx=0.02, rely=0.608)

lontk = Label(master, text = "Longitude (DD): ",font = ("Consolas", 10),bg='#e7ac1d')
lontk.place(relheight=0.123, relwidth=0.176, relx=0.02, rely=0.731)

elevtk = Label(master, text = "Elevation (m): ",font = ("Consolas", 10),bg='#e7ac1d')
elevtk.place(relheight=0.123, relwidth=0.176, relx=0.02, rely=0.854)

session_hash = Label(master, text = "NONE", font = ('Consolas', 15, 'bold'),
            background = '#e15e28',
            foreground = 'black')
session_hash.place(x=listplace, rely=0.02, relheight=0.058, width=listsize)

##create height variable
preview = Label(master, text = "Sandcam", borderwidth=1, font = ("Consolas", 22), relief="solid",bg='#e7ac1d')
preview.place(height=previewsize-.02, width=previewsize, relx=0.216, rely=0.02) #to fix so that no matter what it is square

#make ListBox

stats = tk.Listbox(master, borderwidth=1, relief="solid", font = ("Consolas", 8),bg='#e7ac1d')
stats.place(relheight=(1-0.648), width=listsize , x=listplace, rely=0.628)

#create photo
logo = '/home/sediment/Documents/src/Logo.jpg'
logo1 = PIL.Image.open(logo) 
previewsize_h = screen_height * 0.176  
previewsize_w = screen_width * 0.078
logo2 = logo1.resize((int(previewsize_h),int(previewsize_w)))
logo3 = ImageTk.PhotoImage(logo2)
logoimg = Label(master, image=logo3, bg="white")
logoimg.place(relheight=0.176, relwidth=0.098, relx=0.100, rely=0.02) 

while True:
    master.mainloop()
