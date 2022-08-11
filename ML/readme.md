# ML model for grain size detection from SandCam images

All notebooks are in the `/src/` directory. For retraining, users will need to make a `/data/` directory as a companion to `/src/`. Data will be released on Zenodo. 

The training notebook takes the data, trains a model, quantizes the model, and saves it as a tensorflow lite file `.tflite`. 

This tflite file can then be loaded onto the camera.