# SediNetCam
Installation

Boot up raspberry pi 
Connect raspberry pi to internet

Applications menu -> Preferences -> Raspberry Pi Configuration -> Interfaces -> ENABLE; Camera, SPI, I2C (SSH, VNC are optional)
Reboot Raspberry pi

Update raspberry pi with commands
`sudo apt-get update`
`sudo apt-get upgrade`

After reboot 
Power Raspi off and add header extension, attach GPS to UART pins. Place RTC on I2C. 
Connect Pi HQ camera to raspberry pi 

Connect Button to GPIO26 and to GND
Connect Flash to GPIO18, 5v (back of RTC), and GND
Power Raspberry pi on 

Follow instructions to get packages for flash, GPS, and RTC
https://www.thegeekpub.com/16187/controlling-ws2812b-leds-with-a-raspberry-pi/
https://ozzmaker.com/berrygps-setup-guide-raspberry-pi/
https://maker.pro/raspberry-pi/tutorial/how-to-add-an-rtc-module-to-raspberry-pi



