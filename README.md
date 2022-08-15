# Instagrain

<img src="./Logo" width=20% height=20%/>

[![Last Commit](https://img.shields.io/github/last-commit/UNCG-DAISY/SandCam)](
https://github.com/UNCG-DAISY/SandCam/commits/main)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/UNCG-DAISY/SandCam/graphs/commit-activity)
![GitHub](https://img.shields.io/github/license/UNCG-DAISY/SandCam)

[![Wiki](https://img.shields.io/badge/wiki-documentation-forestgreen)](https://github.com/UNCG-DAISY/SandCam/wiki)
[![Wiki](https://img.shields.io/badge/discussion-active-darkgreen)](https://github.com/UNCG-DAISY/SandCam/discussions)

![Raspberry Pi](https://img.shields.io/badge/-RaspberryPi-C51A4A?style=for-the-badge&logo=Raspberry-Pi)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white)

A camera for measuring sediment grain size in the field - 'instant grainification' (h/t D. Rubin et al., 2007)
The camera currently runs a deep learning model to estimate grain size from pictures (using tensorflow lite)

We have several working prototypes out in the field. Here at HQ we continue to refine the camera design, hardware, software, and ML model. 

Prototpye 1 (3D printed case)

<img src="./SNC.jpg" width=20% height=20%/>

Prototype 2 (current version; CNC'ed case and 3D printed parts)

<img src="./CamDB_2.jpg" width=20% height=20%/>
<img src="./CamDB._1jpg.jpg" width=20% height=20%/>

## To Build the Camera:

0. Get in touch with us, we would be happy to collaborate!

1. Read through the repository.

2. Hardware: Follow the instructions in the [hardware readme](./hardware/readme.md) to 3D print the case with an SLA or SLS printer. Wire the electronic components. Assemble the camera.

3. Software: Follow the instructions in the [software readme](./software/readme.md) to load the Raspberry Pi with the neccesary programs.

4. Test the camera. We recommend taking a picture of sand with known grain size characteristics.

## Code of Conduct

We intend to foster an inclusive and respectful environment surrounding the contribution and discussion of our project. Make sure you understand our [Code of Conduct](./CODE_OF_CONDUCT.md).

<img src="./crop2.jpg" width=50% height=50% />
