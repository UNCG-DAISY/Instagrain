# BOM v2

Full List of Materials can be found on the [`BOMv2.csv`](./BOMv2.csv)

---
### Major Components

- Most of the major Components can be ordered from our Adafruit wishlist http://www.adafruit.com/wishlists/543790
  - The Google Coral can be found at https://coral.ai/products/accelerator  
  - The recommended microSD card can be bought on Amazon https://www.amazon.com/SanDisk-Extreme-microSDHC-UHS-3-SDSQXAF-032G-GN6MA/dp/B06XWMQ81P/
  - Due to chip shortages in 2021 and 2022, the Raspberry Pi 4 may not be available on Adafruit
- There are two STEP files that can be sent to Polycase* to order the custom-designed, CNC-machined camera housing (expect 1 to 3 week lead time). Polycase should alread have the "setup" complete, which reduces the overall unit cost. 
  - WQ-57C_LID.stp
  - WQ-57_Body.stp

*Instructions for sending requests for custom CNC-machined parts are available at https://www.polycase.com/customized-enclosures 


---
### Hardware

The fastener hardware can be ordered from a Mcmaster-Carr cart https://www.mcmaster.com/order/rcvRtedOrd.aspx?ordid=6706876626400   

---
### 3D Parts

There are three `.stl` files
- [`Camcover.stl`](./Camcover.stl)
- [`screenbracket.stl`](./screenbracket.stl)
- [`ledmountv2.stl`](./ledmountv2.stl)

We recommend printing all of them with a SLA printer with a build volumne of 14.5 × 14.5 × 18.5 cm and using rigid resin.

Printing takes roughly 44.45hrs with a Form3/3+ printer (Look at [`BOMv2.csv`](./BOMv2.csv) for full part breakdown)

---
### CNC Part

There is only one part that needs to be custom made or hand machined
- [`WQ-57P-01.pdf`](./WQ-57P-01.pdf)

The above file has all the necessary dimensions for hand machining, feel free to make any improvements and share!

---

# Wiring Diagram

To assemble the camera, you will need the parts described in the bill of materials — [`BOMv2.csv`](./BOM.csv). 

A wiring diagram is available in Fritzing format — [`sandcamv2.fzz`](./sandcamv2.fzz).

![image](https://user-images.githubusercontent.com/72474059/165810494-b4ed2cfe-21da-4d84-8d6e-5b2b56b211d7.png)

---

# Build Instructions 

---

### Tools Needed 
- Soldering Iron
- Soldering Wire
- Flux
- Wire Strippers
- Metric Hex Bit Set
- Imperial Allen Key Set

### Components 
The Build Process is Broke down into 8 major parts:
- Soldering the Adafruit Ultimate GPS Hat and Neopixel board
- Mounting the Screen
- Coral mounting 
- Camera Assembly 
- Installing Handles
- Base Plate Assembly 
- Final assembly
- Focusing the Camera

---

 ### Step 1 --- Soldering 
First we will solder the GPIO header to the Adafruit Ultimate GPS Hat  
![IMG_6962](https://user-images.githubusercontent.com/72474059/165761674-ca67fa3f-2d08-4f01-a083-9d312f5fe1ef.JPG)

Next will cut 3, 8in male to female jumper cables in half, red for 5v, black for ground, and purple for data  
![IMG_6923](https://user-images.githubusercontent.com/72474059/164987917-60c43567-0d42-475e-9cad-d685fcdeec07.JPG)  

Once the wires are cut strip off about 5mm from each wire similar to how it is done in the above picture
and then twist the ends of the wires together and tin them  
![IMG_6963](https://user-images.githubusercontent.com/72474059/165761764-84695314-5ddc-475b-a0c2-31e72c76a57f.JPG)
 
Now we will solder the female ends to the Neopixel board, make sure solder the red wire to the middle 5v, the black wire to the middle GND, and the purple wire to the data input, so that the [`ledmountv2.stl`](./ledmountv2.stl) fits 
![IMG_6960](https://user-images.githubusercontent.com/72474059/165761863-85192372-6de5-4521-90dd-994d8c08320f.JPG)

Next solder the male ends to the Adafruit Ulimate GPS Hat, the red wire to the 5v strip, the black to the GND strip, and the purple wire to GPIO #8 
Tip: I recommend soldering the 5v and GND at different ends (Differenly then I did in the picture below)
![IMG_6964](https://user-images.githubusercontent.com/72474059/165762025-f27c6d2d-23a4-4b6b-bba1-18b4b20a6853.JPG)
![IMG_6965](https://user-images.githubusercontent.com/72474059/165762096-6dda401f-bb95-4250-9392-c413fc6de61e.JPG)

For the final step we will place the Neopixel Light into the [`ledmountv2.stl`](./ledmountv2.stl) 
![IMG_7032](https://user-images.githubusercontent.com/72474059/168943394-9fb79f5f-3cf2-4507-9d99-2d2912598311.JPG)


---

### Step 2 --- Mounting the Screen
First we will start the 4 M3 Socket Head Screws into the mounting holes in on the center of the [`screenbracket.stl`](./screenbracket.stl) 
(will have a picture here soon)

Next attach the Brackets to the polycase with 4 12mm M2 Socket Head Screws  
![IMG_6914](https://user-images.githubusercontent.com/72474059/164988811-47f7792f-20ce-47d7-869b-d1d7eb456abe.JPG)
![IMG_6915](https://user-images.githubusercontent.com/72474059/164988827-f3b6764e-d850-47ec-93c6-18f53959513b.JPG)

Once attached place the screen face down with the larger bezel on the left 
![IMG_6916](https://user-images.githubusercontent.com/72474059/164988864-5151d5f9-de15-4cfc-9e23-48e812a2f8cc.JPG)

Finish by putting the outside of the polycase lid to the backside of the Screen and tightem the M3 Socket Head screws to the screen till the screen is flush with the front of the polycase  

![IMG_6917](https://user-images.githubusercontent.com/72474059/164988931-baf984b2-621c-4751-8f05-0834f4efee7f.JPG)

---

### Step 3 --- Mounting the Coral TPU
Mounting the Coral TPU uses four 10mm M2.5 Female to Female Hex Standoffs, four 12mm M2.5 Socket Head Screws, and four 6mm M2.5 Socket Head bolts
This is a fairly starightforward step, for now we recommend it is mounted on the outside until temapture testing can be done with the Coral TPU on the inside
![IMG_6969](https://user-images.githubusercontent.com/72474059/165763053-3cdb8e88-4223-462c-98ff-5da2f3b9c861.JPG)

### Step 4 --- Camera Assembly
For this step you will need four 16mm female to male standoffs, four 2.5mm hex nuts, and four 6mm M2.5 Socket Head bolts 
For the purpose of focusing the Pi HD camera you will need to disassemble and remove this part
![IMG_7030](https://user-images.githubusercontent.com/72474059/168943662-fb838fa9-9546-4700-a3f9-a58f59eaeed3.JPG)
The removed part and pi HD camera will now look like this
![IMG_7031](https://user-images.githubusercontent.com/72474059/168943727-bb0cd277-f32c-4043-a953-0339e89d68f9.JPG)
Next attach 4 standoffs to the bottom of the camera and then 4 between the neopixel light and the top of the pi camera

![IMG_7033](https://user-images.githubusercontent.com/72474059/168943945-a6e9746f-649b-4e65-add7-d1255ba00a85.JPG)

Finally attach the the camera to the outside of the case with the four 6mm M2.5 Socket Head bolts

---

### Step 5 --- Mounting the Handles
For this step you will need 4 quarter inch bolts and 4 lock nuts  

![IMG_7060](https://user-images.githubusercontent.com/72474059/169839191-c2aee7d8-f8e0-4a46-a209-5db16d7d5323.JPG)
![IMG_7061](https://user-images.githubusercontent.com/72474059/169839233-072c267d-7c2f-48ef-b017-9032ff4848db.JPG)


---

### Step 6 --- Base Plate Assembly
For this step you will need two ribbon cables, four 10mm female to male standoffs, four 11mm female to male standoffs, a velcro strap, and four 6mm M2.5 socket head bolts   
First step is to attach the two ribbon cables to the Raspi, for the screen and the camera  
Next attach the adafruit ultimate GPS hat with the black 11mm standoffs, then attach the 10mm standoffs to the bottom of the pi    
Secure the Raspi assembly to the baseplate, and then secure the battery to the baseplate  
Finally secure the baseplate in the bottom of the case with the four screws that come with the polycase
(pictures coming soon)

---

### Step 7 --- Final Assembly
Thread the GPS antenna through the hexagonal hole in the front of the case annd attach wih double sided tape or glue to the outside of the case   
Next pull the camera ribbon through the slotted hole in the bottom of the case, and then connect the jumper cables
Connect the ground and 5v jumper cable to the screen, and connect the display ribbon to the screen
Finally connect the GPS to the adafruit ultimate GPS hat and zip tie in place to secure

(pictures coming soon)

---

### Step 8 --- Focusing the Camera 
This is by far the hardest step, it is recommended to disconnect the screen and plug the raspi into a larger screen via hdmi.
Boot up the raspi and run the [`preview.py`](./preview.py) script
Focus the camera by twisting the HD lens  (this step might take a while)
Once the camera is in focus tighten down all the camera screws and place the [`Camcover.stl`](./Camcover.stl) on the case by inserting the pegs and twisting

Finally the touch screen can be hooked back up and the Sandcam is now ready to work
(pictures coming soon)

---
