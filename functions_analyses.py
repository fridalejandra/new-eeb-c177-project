#!/usr/bin/env python
# coding: utf-8

# # Function Analyses 

# ## Importing packages

# In[2]:


import netCDF4 as nf # reads in nc file
import os
import csv 
import numpy as np
import pandas as pd
#import xarray
import matplotlib.pyplot as plt
from netCDF4 import Dataset


# ## Reading in .nc files

# In[3]:


nc = nf.Dataset('air.mon.mean_1979-2015.nc')


# ### printing out the variables of the nc file

# In[4]:


variables = nc.variables
print(variables)


# ### assigning variables 

# In[5]:


lon = variables["lon"]
lat = variables["lat"]
level = variables["level"]
air = variables["air"]


print(lon)
print(lat)
print(level)
print(air)


# In[6]:


air.dimensions


# In[7]:


air.shape


# In[8]:


depth=level[:]
print(depth)


# # Part 1
# ## Extraction

# In[9]:


#data will be extracted from the current .nc format and output as .csv

import os
output_path = "data_output_new" # making the code dynamic
 
# Creating a new folder on computer to store the output data in if it doesn't already exists

if not os.path.exists(output_path): # #if it path doesnt exist (basically a safety check to not delete anything)
    os.mkdir(output_path)  #  then make the path, making a directory

# This for loop will iterate through all the surface temperature values
for ii in range(0,len(air)): #main for loop will traverse the rows
    if not os.path.exists(os.path.join(output_path,"month-"+str(ii))): #creating a new folder for each month slice
        os.mkdir(os.path.join(output_path,"month-"+str(ii))) #the join will convert to appropriate set of separators, basically not hardcoding
        for jj in range(0,len(air[ii])): # this nested for loop goes through the columns
            with open(os.path.join(output_path,"month-"+str(ii),"altitude-"+str(jj)+".csv"),"w+") as csv_out:
                csvWriter = csv.writer(csv_out, delimiter=',')
                csvWriter.writerows(air[ii][jj]) #writing the rows for the csv


# ## Analyses

# In[10]:


# Using numpy to "clean up" the lats and lons

lat =  np.arange(-90,91,2.5)
lon =  np.arange(-180,181,2.5)

print("longitudes =\n{}".format(lon[:]))

print("latitudes =\n{}".format(lat[:]))


# In[11]:


# Slicing the 'z' axis, to only get the mean surface temp at 850 hPa where most convergence occurs
air_temp_at_surf=(air[:,2,:,:])
print(air_temp_at_surf)


# In[12]:


#Finding index value of certain longitudes
print(np.where(lon==-62.5))
print(np.where(lon==-90))

air_temp_at_surf.shape

#Indexing to only get the Antarctic Circle
antcircle=air_temp_at_surf[:,36:47,:]


# In[13]:



temp_mean=[]
for ii in range(len(antcircle)):
    mean = np.mean(antcircle[ii,:,:])
    temp_mean.append(mean)


# In[14]:


ave_plot = plt.plot(temp_mean)
plt.xlabel('Timesteps')
plt.ylabel('Temperature degC')
plt.title('Surface Temp 1979-2015: Antarctic Circle')
plt.show()


# In[15]:


image = plt.imshow(air_temp_at_surf[443])
plt.show()


# In[16]:


#code to get average air per month for each row (latitude)
#air_avg_per_lat = []
#for months in range(0,len(air_new)):
    #air_avg_per_lat.append(np.mean(air_new[ii][0], axis=1))
    
#and then you can plot it whatever way you want


# # Part 2
# ## Working with nc data as dictionaries

# In[17]:


# Original data is already in dictionary form 

type(nc)
print(nc.dimensions.keys())


# ## Printing dimension keys 

# In[18]:


print(type(nc.dimensions.keys()))
for d in nc.dimensions.items():
    print(d)


# In[19]:


#organizing time with dict 
nc_time = nc.variables['time']
print(nc_time)

print(nc_time[0:7]) # printing only 6


# In[20]:


#an attempt in counting the number of items in the dictionary through indexing, here trying to do so in lon but finding it hard to wokr 
#with the several dimensions through dictionaries 

count = 0
for x in enumerate(nc.dimensions.items()): 
  
        # enumerate function returns a tuple in the form 
        # (index, (key, value)) it is a nested tuple 
        # for accessing the value we do indexing x[1][1] 
        if isinstance(x[1][1], list): 
            count += len(x[1][1]) 
print(count) 


# # Part 3 
# ## using the format() function in python 

# In[21]:


import datetime as dt
from netCDF4 import Dataset, date2index, num2date, date2num


# In[22]:


# did not necessarily use the format() function but did change the formatting of the time
#here we are just indexing the start and end of the time slices
time_start = date2index(dt.datetime(1979, 1, 1), nc_time, select="nearest")
time_end = date2index(dt.datetime(2015, 12, 31), nc_time, select="nearest")

print(time_start)
print(time_end)


# In[23]:


print(num2date(nc_time[time_end], units=nc_time.units, calendar=nc_time.calendar))


# In[24]:


#formatting all the dates using nu2date
dates=num2date(nc_time[:],nc_time.units)
time=([date.strftime('%Y-%m-%d') for date in dates[:]])


# In[ ]:


date2index()


# In[29]:


print(time[:])


# In[26]:


print(antcircle[0])


# In[27]:


get_ipython().run_cell_magic('capture', 'cap --no-stderr', 'print(time[:])\nprint(antcircle)')


# In[28]:


with open('output.txt', 'w') as f:
    f.write(cap.stdout)


# In[366]:


nc.close()


# In[ ]:




