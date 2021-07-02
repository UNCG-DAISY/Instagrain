# SediNetCam
---
## Installation

###### Update Pi 
Boot up raspberry pi 
Connect raspberry pi to internet

Update raspberry pi with commands
```
sudo apt-get update
sudo apt-get upgrade
```

###### Configure Pi

Applications menu -> Preferences -> Raspberry Pi Configuration -> Interfaces -> ENABLE; Camera, SPI, I2C (SSH, VNC are optional)
Reboot Raspberry Pi  

###### Add Hardware
After reboot  
Power Raspi off and add header extension, attach GPS to UART pins. Place RTC on I2C.
Connect Pi HQ camera to raspberry pi  

Connect Button to GPIO26 and to GND 
Connect Flash to GPIO18, 5v (back of RTC), and GND  
Power Raspberry pi on   

###### set up GPS
`sudo raspi-config`  
interfacing options -> Serial -> No -> Yes   
then reboot  
`pip3 install gps`  

config GPS to work with correct serial device  
`sudo nano /etc/default/gpsd`  
Look for  `DEVICES=""`  
Change to `DEVICES="/dev/serial0"`  
Now save file (control X, Y)  

###### set up RTC

###### set up LED Ring Flash

Helpful instructions to get packages for flash, GPS, and RTC  
https://www.thegeekpub.com/16187/controlling-ws2812b-leds-with-a-raspberry-pi/ 
https://ozzmaker.com/berrygps-setup-guide-raspberry-pi/  
https://maker.pro/raspberry-pi/tutorial/how-to-add-an-rtc-module-to-raspberry-pi  



