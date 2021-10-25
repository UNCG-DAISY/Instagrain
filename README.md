# SandCam

A 3D printed camera to measure sediment grain size from pictures.

<img src="./SNC.jpg" width=50% height=50%>

---

Currently we have a working version of the camera and are refining the camera design, hardware, and software. Check out the Issues if you want to follow along or contribute. 

The camera currently runs a [pyDGS](https://github.com/dbuscombe-usgs/pyDGS) — software written by [Dan Buscombe](https://github.com/dbuscombe-usgs) that estimates grain size distribution of an image using the continuous wavelet transform.

We are actively working on a new machine learning method (that will run on the camera) to estimate grain size — see the [ML readme](/ml/readme.md). 

## To Build the Camera:

0. Get in touch with us, we would be happy to collaborate!

1. Read through the repository.

2. Follow the instructions in the [hardware readme](./hardware/readme.md) to 3D print the case, wire the electronic components, and build the camera.

3. Follow the instructions in the [software readme](./software/readme.md) to load the Raspberry Pi with the neccesary programs.

4. Field test the camera. 

## Code of Conduct

We intend to foster an inclusive and respectful environment surrounding the contribution and discussion of our project. Make sure you understand our [Code of Conduct](./codeofconduct.md).
