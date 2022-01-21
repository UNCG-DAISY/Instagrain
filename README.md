# SandCam

A 3D printed camera to measure sediment grain size in the field from pictures.


<img src="./SNC.jpg" width=50% height=50%/>


---

Currently we have a working version of the camera and are refining the camera design, hardware, and software. Check out the issues if you want to follow along or contribute. 

The camera currently runs a deep learning model to estimate grain size from pictures (using tensorflow lite) — see the [ML readme](/ml/readme.md). 

(The camera can also run [pyDGS](https://github.com/dbuscombe-usgs/pyDGS) — software written by [Dan Buscombe](https://github.com/dbuscombe-usgs) that estimates grain size distribution (percent finer) of an image using the continuous wavelet transform.


## To Build the Camera:

0. Get in touch with us, we would be happy to collaborate!

1. Read through the repository.

2. Hardware: Follow the instructions in the [hardware readme](./hardware/readme.md) to 3D print the case with an SLA or SLS printer. Wire the electronic components. Assemble the camera.

3. Software: Follow the instructions in the [software readme](./software/readme.md) to load the Raspberry Pi with the neccesary programs.

4. Test the camera. We recommend taking a picture of sand with known grain size characteristics.

## Code of Conduct

We intend to foster an inclusive and respectful environment surrounding the contribution and discussion of our project. Make sure you understand our [Code of Conduct](./CODE_OF_CONDUCT.md).

<img src="./crop2.jpg" width=50% height=50% />