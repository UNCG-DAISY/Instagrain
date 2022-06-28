import numpy as np
import pandas
import csv
import matplotlib

#Sieve Sizes
x = [2,1,.5,.250,.125,.063,0] #might need to be changed based on sieve methods
#change sieve sizes to phi
phis = -(np.log2(x)) 


def SedStats(phi,type,per):

  if str(type) == "weight":
  # Compute percentages of total weight
    per = np.divide(per,sum(per)) * 100
  elif str(type) == "percent":
  # Ensure values are greater than 1 if 'percent' was specified
    if max(per) < 1:
        per = per*100

  #Sort from smallest to largest
  tmp = np.zeros((len(phi),2));
  tmp[:,0] = phi
  tmp[:,1] = per
  phi = tmp[:,0].T
  per = tmp[:,1].T

  cdf = np.cumsum(per)

  x = [98,95,90,84,75,50,25,16,10,5,2]
  interp_phis= np.interp(x,cdf,phi)
  interp_mm = 2**(-interp_phis)
  return interp_mm

#reading sieve csv file
with open('Wilmington_Percentages_1.csv', 'rt') as f:
    reader = csv.reader(f)
    data_as_list = list(reader)

#reading sandcam csv file
with open('wb_17FEB2022.csv', 'rt') as g:
    reader1 = csv.reader(g)
    data_as_list1 = list(reader1)

#parsing sieve data
data = np.array(data_as_list)
new_data = data[1:21,13:20]
x = new_data.astype(np.float)
#0s must be changed to a small number or interp will not work 
x[x == 0] = 0.0001
measured = []
range1 = list(range(0,len(x)))

#parsing sandcam data
sc_data = np.array(data_as_list1)
sc_new_data = sc_data[1:21,5:16]
sc = sc_new_data.astype(np.float)


for i in range1:
  sed = SedStats(phis,"percent",x[i])
  measured.append(sed)

MAPE = (abs(sc-measured)/measured)*100
matplotlib.pyplot.boxplot(MAPE)
