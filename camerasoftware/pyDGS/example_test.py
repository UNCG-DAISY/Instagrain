# Written by Dr Daniel Buscombe, Marda Science LLC
#
# MIT License
#
# Copyright (c) 2020, Marda Science LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from dgs import *
import os, glob
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
#========================================
# single image
def dotest1(image, with_plot=False):
   # if this is 1, it means "give me the results in pixels - I'll apply my own scaling"
   # otherwise, it is mm/pixel (if you want your results in mm) or um/pixel for microns
   resolution = .02073052

   #the maximum scale (grain size) considered by the wavelet is the horizontal width dimension divided by this number
   #so if your image is 1000 pixels wide and maxscale=4, only grains up to 1000/4 = 250 pixels are considered
   maxscale=5

   # if 1, prints grain size statistics to screen
   verbose=1

   #this is the area to volume conversion coefficient. See Cuttler et al (provided)
   #you could also use it as an empirical tuning coefficient against field data (recommended)
   x = -.47

   #I recommend you compute in pixels (resolution=1) then apply your resolution scaling afterwards
   data_out = dgs(image, 1, maxscale, verbose, x)

   ## parse out dict into three separate dictionaries
   stats = dict(list(data_out.items())[:4])
   percentiles = dict(list(data_out.items())[4:6])
   freqs_bins = dict(list(data_out.items())[6:])

   if resolution!=1:
       freqs_bins['grain size bins']*=resolution
       percentiles['percentile_values']*=resolution

       for k in stats.keys():
           stats[k] = stats[k]*resolution

   # write each to csv file
   # newarray = np.reshape(percentiles["percentile_values"], (1,10))
   # print(newarray)
   # newDF = pd.DataFrame(newarray)
   # print(newDF)
   # newDF.to_csv(textarg, mode = 'a', header = False)
   # statsarray = [[stats['mean grain size'], stats['grain size sorting'],stats['grain size skewness'], stats['grain size kurtosis']]]
   # print(statsarray)
   # newarray.extend(statsarray)
   # statsDF = pd.DataFrame(statsarray)
   # print(statsDF)
   # statsDF.to_csv(textarg, mode = 'a', header = False, index = False)
   
   percarray = np.reshape(percentiles["percentile_values"], (1,10))
   statsarray = [[stats['mean grain size'], stats['grain size sorting'],stats['grain size skewness'], stats['grain size kurtosis']]]
   both = np.append(percarray, statsarray)
   newarray = np.reshape(both,(1,14))
   stats = pd.DataFrame(newarray)
   stats.to_csv(textarg, mode = 'a', header = False, index = False)
   
#====================================
if __name__ == '__main__':
   image= str(sys.argv[1])
   textarg = str(sys.argv[2])
   dotest1(image)
