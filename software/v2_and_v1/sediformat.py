#This script is repsonable for taking sieve data and creating a excel file with the correct format for SediNet

import os
import numpy as np
import math

def sediformat(input, unit, weights, l_s, u_s, img, pixel):
	# input =  a list of sieve values
	# units = specifiy if list is "mm", "phi", "in"
	# weights = cumulative weights for corresponding sieve values
	# l_s = lower sieve value (ASTM)
	# u_s = upper sieve value (ASTM)
	# img = list of images of sieved sand
	# pixel = pixels per mm in photo 
	
	avg = (l_s + u_s)/2
	# change input from to correct output
	if str(unit) == "phi":
		invaluestomm = [2**-i for i in phi]
	elif str(unit) == "in":
		invaluestomm = [25.4*i for i in inch]
	elif str(unit) == "mm":
		invaluetomm == mm
		
		
	#figure out values
	lst = np.interp([95,84,75,50,25,16,10,5],cumulative_weights,invaluestomm)

	# create csv file
	pwd = os.getcwd()
	txtfile = open(pwd + '/' + 'sediformat.csv', 'w+')
	txtfile.write('file, min_sieve, max_sieve, average_sieve, p5, p10, p16, p25, p50, p75, p84, p95')
	for i in range(len(img)):
		pxllst = [pixels[i]*k for k in lst]
		per = map(str, pxllst)
		txtfile.write("\n")
		txtfile.write(img[i] + ',' + str(l_s) + ',' + str(u_s) + ',' + str(avg) + ',' + per[0] + ',' + per[1] + ',' + per[2] + ',' + per[3] + ',' + per[4] + ',' + per[5]+ ',' + per[6] + ',' + per[7])
	txtfile.close()

# Example parameters and code, output put is sediformat.csv
phi = [-1,0,.5002,1.000,1.4982,2,2.4982,3.000,3.9885,4.7563]
cumulative_weights= [ 1.57, 5.97, 12.63, 21.68, 32.97, 53.94, 90.41, 99.35, 99.97, 100.00]
units = "phi"
lowersieve = 10
uppersieve = 230
img = ['3in.jpg','4in.jpg','5in.jpg', '6in.jpg', '7in.jpg']
pixels = [19.775, 14.832, 11.865, 9.914, 8.514]

sediformat(phi, units, cumulative_weights, lowersieve, uppersieve, img, pixels)
