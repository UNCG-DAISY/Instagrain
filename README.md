# SediNetCam
---
# Installation

## Update Pi 

Boot up Raspberry Pi and connect to internet  
Update raspberry Pi with commands
```
sudo apt-get update
sudo apt-get upgrade
sudo reboot
```

## Configure Pi

Applications menu -> Preferences -> Raspberry Pi Configuration -> Interfaces -> ENABLE; Camera, SPI, I2C (SSH, VNC are optional)  
`sudo reboot` 

## Add Hardware

After reboot  
Power Raspi off and add header extension, attach GPS to UART pins. Place RTC on I2C.
Connect Pi HQ camera to raspberry pi  

Connect Button to GPIO26 and to GND 
Connect LED light to GPIO18, 5v (back of RTC), and GND  
Power Raspberry pi on   

## set up GPS

`sudo raspi-config`    
interfacing options -> Serial -> No -> Yes   
then reboot   

config GPS to work with correct serial device  
`sudo nano /etc/default/gpsd`  
Look for  `DEVICES=""`  
Change to `DEVICES="/dev/serial0"`  
Now save file (control X, Y) 
`sudo pip3 install gps` to download gps for python3
<img width="500" alt="Screen Shot 2021-07-02 at 12 17 02 PM" src="https://user-images.githubusercontent.com/72474059/124324670-6350b680-db51-11eb-8d51-c88c321e43b6.png">

## set up RTC

`sudo raspi-config` Interface options -> P5 I2C -> yes -> finish  
<img width="502" alt="Screen Shot 2021-07-02 at 12 03 23 PM" src="https://user-images.githubusercontent.com/72474059/124324683-651a7a00-db51-11eb-9ab6-369bd1b30153.png">
<img width="502" alt="Screen Shot 2021-07-02 at 12 03 43 PM" src="https://user-images.githubusercontent.com/72474059/124324681-651a7a00-db51-11eb-83ec-318309767175.png">
<img width="502" alt="Screen Shot 2021-07-02 at 12 04 38 PM" src="https://user-images.githubusercontent.com/72474059/124324680-6481e380-db51-11eb-9981-be4f91f25073.png">
<img width="501" alt="Screen Shot 2021-07-02 at 12 04 50 PM" src="https://user-images.githubusercontent.com/72474059/124324679-6481e380-db51-11eb-8cdc-9e692816c19a.png">
<img width="501" alt="Screen Shot 2021-07-02 at 12 05 08 PM" src="https://user-images.githubusercontent.com/72474059/124324677-6481e380-db51-11eb-91b4-3a1fd8bbbb47.png">  
`sudo reboot`  
Now install this package to see if the raspberry pi recognizes the RTC  
`sudo apt-get install python-smbus i2c-tools`   
`sudo i2cdetect -y 1` will show mounted drives, you should see a 68  
<img width="502" alt="Screen Shot 2021-07-02 at 12 06 21 PM" src="https://user-images.githubusercontent.com/72474059/124324676-63e94d00-db51-11eb-8588-0b36c7acb4bb.png">  
`sudo nano /boot/config.txt`        
Add to the end    
`#rtc 
dtoverlay=i2c-rtc,ds3231`  
save and exit (control x, y, enter)   
<img width="501" alt="Screen Shot 2021-07-02 at 12 07 14 PM" src="https://user-images.githubusercontent.com/72474059/124324675-63e94d00-db51-11eb-94cc-bf6d3439c419.png">  
Now that we have the RTC ready to work on boot, restart your pi and..
`sudo i2cdetect -y 1` a mounted drive will have a "UU" ID  
<img width="499" alt="Screen Shot 2021-07-02 at 12 09 07 PM" src="https://user-images.githubusercontent.com/72474059/124324672-63e94d00-db51-11eb-9099-01946bae5407.png">

## set up pyDGS
visit https://github.com/dbuscombe-usgs/pyDGS to look pyDGS or download to pi with `git clone --depth 1 https://github.com/dbuscombe-usgs/pyDGS.git`  
once downloaded edit test.py script to look like example code in SediNetCam --> camerasoftware --> pyDGS --> examplecode.py  
next copy the __pycahce__ folder, dgs.pyc, and dgs.py to your SediNetCam folder 

Helpful instructions to get packages for flash, GPS, and RTC  
https://www.thegeekpub.com/16187/controlling-ws2812b-leds-with-a-raspberry-pi/  
https://ozzmaker.com/berrygps-setup-guide-raspberry-pi/  
https://maker.pro/raspberry-pi/tutorial/how-to-add-an-rtc-module-to-raspberry-pi  

## Usage
When Pi computer is booted up, open terminal and change directory to location of photosieve.py  
Enter command `python3 photosieve.py` in terminal to run photosieve, to see a preview press button and to take a picture hold the button for 2 seconds  
Photos and a text file will be stored in a new folder name of your choosing, the text file will have every photo with the time taken, corresponding GPS coordinates, altitude, and grain size percentiles
<img width="699" alt="Screen Shot 2021-07-02 at 12 30 42 PM" src="https://user-images.githubusercontent.com/72474059/124324666-62b82000-db51-11eb-9946-f49eceb3640a.png">
<img width="717" alt="Screen Shot 2021-07-02 at 12 30 16 PM" src="https://user-images.githubusercontent.com/72474059/124324668-6350b680-db51-11eb-8f29-a62ef0759309.png">
