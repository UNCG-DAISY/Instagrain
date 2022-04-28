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

There are 4 `.stl` files
- [`Camcover.stl`](./Camcover.stl)
- [`screenbracket.stl`](./screenbracket.stl)
- [`ledmountv2.stl`](./ledmountv2.stl)
- Mountingplate.stl (coming soon)

We recommend printing all of them with a SLA printer with a build volumne of 14.5 × 14.5 × 18.5 cm and using rigid resin.

Printing takes roughly 44.45hrs with a Form3/3+ printer (Look at [`BOMv2.csv`](./BOMv2.csv) for full part breakdown)

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
The Build Process is Broke down into 6 major parts:
- Soldering the Adafruit Ultimate GPS Hat and Neopixel board
- Camera Assembly 
- Mounting the Screen
- Coral mounting 
- Installing Handles
- Base Plate Assembly 

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

For the final step wwill place the Neopixel Light into the [`ledmountv2.stl`](./ledmountv2.stl) and attach the dafruit Ultimate GPS Hat to the Raspberry Pi
(will have a picture here soon) 

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
Mounting the Coral TPU uses four 10mm M2.5 Female to Female Hex Standoffs, four 12mm M2.5 Socket Head Screws, and four 6mm M2.5 Socket Head Screws.
This is a fairly starightforward step, for now we recommend it is mounted on the outside until temapture testing can be done with the Coral TPU on the inside
![IMG_6969](https://user-images.githubusercontent.com/72474059/165763053-3cdb8e88-4223-462c-98ff-5da2f3b9c861.JPG)

