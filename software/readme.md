# Setting up the camera software on the Pi

After assembling the case and wiring the electronics for the RPi (see the ['hardware directory'](../hardware)), it's time to get the Software and configurations set. 


## Update Pi 

Boot up Raspberry Pi and connect to internet  
Update raspberry Pi with commands
```
sudo apt-get update
sudo apt-get upgrade
sudo reboot
```

## Configure Pi

Applications menu -> Preferences -> Raspberry Pi Configuration -> Interfaces -> ENABLE; Camera, SPI,(SSH, VNC are optional)  
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
interfacing options (3) -> Serial Port (P6) -> No -> Yes -> Finish   
then reboot   

Install, gpsd, gpsmon and cgps  
`sudo apt-get install gpsd-clients gpsd -y`

config GPS to work with correct serial device  
`sudo nano /etc/default/gpsd`  
Look for  `DEVICES=""`  
Change to `DEVICES="/dev/serial0"`  
Now save file (control X, Y) 
`sudo pip3 install gps` to download gps for python3
<img width="500" alt="Screen Shot 2021-07-02 at 12 17 02 PM" src="https://user-images.githubusercontent.com/72474059/124324670-6350b680-db51-11eb-8d51-c88c321e43b6.png">

## set up RTC

`sudo raspi-config` Interface options (3) -> (P5) I2C -> yes -> finish  
<img width="502" alt="Screen Shot 2021-07-02 at 12 03 23 PM" src="https://user-images.githubusercontent.com/72474059/124324683-651a7a00-db51-11eb-9ab6-369bd1b30153.png">
<img width="502" alt="Screen Shot 2021-07-02 at 12 03 43 PM" src="https://user-images.githubusercontent.com/72474059/124324681-651a7a00-db51-11eb-83ec-318309767175.png">
<img width="502" alt="Screen Shot 2021-07-02 at 12 04 38 PM" src="https://user-images.githubusercontent.com/72474059/124324680-6481e380-db51-11eb-9981-be4f91f25073.png">
<img width="501" alt="Screen Shot 2021-07-02 at 12 04 50 PM" src="https://user-images.githubusercontent.com/72474059/124324679-6481e380-db51-11eb-8cdc-9e692816c19a.png">
<img width="501" alt="Screen Shot 2021-07-02 at 12 05 08 PM" src="https://user-images.githubusercontent.com/72474059/124324677-6481e380-db51-11eb-91b4-3a1fd8bbbb47.png">  
`sudo reboot`  
Now use i2cdetect to see if the RTC is working   
`sudo i2cdetect -y 1` will show mounted drives, you should see a 68  
<img width="502" alt="Screen Shot 2021-07-02 at 12 06 21 PM" src="https://user-images.githubusercontent.com/72474059/124324676-63e94d00-db51-11eb-8588-0b36c7acb4bb.png">  
`sudo nano /boot/config.txt`        
Add to the end    
`#rtc`   
`dtoverlay=i2c-rtc,ds3231`     
save and exit (control x, y, enter)   
<img width="501" alt="Screen Shot 2021-07-02 at 12 07 14 PM" src="https://user-images.githubusercontent.com/72474059/124324675-63e94d00-db51-11eb-94cc-bf6d3439c419.png">  
Now that we have the RTC ready to work on boot, restart your pi and..
`sudo i2cdetect -y 1` a mounted drive will have a "UU" ID  
<img width="499" alt="Screen Shot 2021-07-02 at 12 09 07 PM" src="https://user-images.githubusercontent.com/72474059/124324672-63e94d00-db51-11eb-9099-01946bae5407.png">   
Setting up RTC to be the main clock  
First disable the fake "hwclock"   
`sudo apt-get -y remove fake-hwclock`   
`sudo update-rc.d -f fake-hwclock remove`      
`sudo systemctl disable fake-hwclock`     

Second make the RTC to the main clock   
Run `sudo nano /lib/udev/hwclock-set` and comment out the following lines with `#`   
`if [-e/run/systemd/system];then`   
`exit 0`    
`fi`     
<img width="497" alt="Screen Shot 2022-02-01 at 1 30 48 PM" src="https://user-images.githubusercontent.com/72474059/152029207-bcb3e759-0c84-4c40-9294-703016023e37.png">   
`/sbin/hwclock --rtc=$dev --systz --badyear`   

`/sbin/hwclock --rtc=$dev --systz`   
<img width="498" alt="Screen Shot 2022-02-01 at 1 31 12 PM" src="https://user-images.githubusercontent.com/72474059/152029235-122ef9c5-87ff-4331-acd7-c8182d23dccd.png">    

Make sure there is an internet connection so that the clocks can sync

## set up Neopixel Lite   
`sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel`   

## set up Tensorflow Lite

Follow instructions to `pip install` the tflite runtime on the Raspberry Pi
https://www.tensorflow.org/lite/guide/python

create a `/models/` directory on the desktop and place the `*.tflite` file (the tflite model) in that directory.

## set up Google Coral TPU   
Run the commands   
`echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list`   
`curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -`   
`sudo apt-get update`   

Next Install Edge TPU Runtime
`sudo apt-get install libedgetpu1-std`   

Now Install the Pycoral Library   
`sudo apt-get install python3-pycoral`   

The Google Coral is ready to be plugged in now  
To test use the code below   
`mkdir coral && cd coral`   
`git clone https://github.com/google-coral/pycoral.git`   
`cd pycoral`   

`bash examples/install_requirements.sh classify_image.py`   

`python3 examples/classify_image.py \
--model test_data/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite \
--labels test_data/inat_bird_labels.txt \
--input test_data/parrot.jpg`   


## set up pyDGS (optional)
visit https://github.com/dbuscombe-usgs/pyDGS to look pyDGS or download to pi with `git clone --depth 1 https://github.com/dbuscombe-usgs/pyDGS.git`  
once downloaded edit test.py script to look like example code in SandCam --> camerasoftware --> pyDGS --> example_test.py  
next copy the __pycahce__ folder, dgs.pyc, and dgs.py to your SandCam folder 

--- 

Helpful instructions to get packages for Ring LED, GPS, Coral TPU, and RTC  
https://www.thegeekpub.com/16187/controlling-ws2812b-leds-with-a-raspberry-pi/  
https://ozzmaker.com/berrygps-setup-guide-raspberry-pi/  
https://coral.ai/docs/accelerator/get-started#1-install-the-edge-tpu-runtime   
https://maker.pro/raspberry-pi/tutorial/how-to-add-an-rtc-module-to-raspberry-pi  

## Usage
When Pi computer is booted up, double click on the RUN.sh script, to see a preview press button and to take a picture hold the button for 2 seconds  
Photos and a text file will be stored in a new folder name of your choosing, the text file will have every photo with the time taken, corresponding GPS coordinates, altitude, grain size percentiles, d50, mean size, stddev, skewness, and kurtosis.  

NOTE: -9999 under lat, lon, and alt means the GPS can not get a lock on coordinates. For best GPS result use external GPS.  

photos  
<img width="718" alt="Screen Shot 2021-07-21 at 11 56 56 AM" src="https://user-images.githubusercontent.com/72474059/126538800-ce039c6b-e40f-4c60-90d1-a071767147ba.png"> 
cropped photos  
<img width="717" alt="Screen Shot 2021-07-21 at 2 11 52 PM" src="https://user-images.githubusercontent.com/72474059/126538848-ac084483-d7b8-41e1-9a25-d67f0b4ee5e7.png">  
Example text file  
<img width="1370" alt="Screen Shot 2021-07-21 at 2 16 31 PM" src="https://user-images.githubusercontent.com/72474059/126542683-53ad00b9-8314-4e10-8d9b-7ab32bca3c4f.png">

