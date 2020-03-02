#!/usr/bin/env python
# coding: utf-8

# In[122]:


#!/usr/bin/env python3
import netCDF4 as nc # handles netCDF files '.nc'
import matplotlib.pylab as plt # plots data on graphs
from mpl_toolkits.basemap import Basemap #gives basemap 
import numpy as np   # deals with arrays and allows indexing
import xarray as xr  # deals with four-dimensional arrays
import pandas as pd  # use of data in dataframe format 
from netCDF4 import Dataset  


# ## Opening the two datasets using xarray, the reason being is it handles dates more efficiently 

# In[123]:


sit_file = '/Users/fridaperez/Developer/repos/eeb-c177-project/sit.nc'
tmp_file = '/Users/fridaperez/Developer/repos/eeb-c177-project/air.nc'

dset = xr.open_dataset(sit_file)
cset = xr.open_dataset(tmp_file)

print(dset)
print(cset)


# In[124]:


sit_var = dset.variables # reading in the variables for Sea Ice Thickness 


# In[125]:


sit_att= dset.assign_attrs


# In[173]:


print(sit_att)


# ## Opening the two datasets using netCDF to assign variables to plot 

# In[127]:


tmp_data = Dataset('air.mon.mean__M-O_2002-2011.nc')
sea_data = Dataset('envisat_SIT_fb_snow-AMSR_sh_2002_2011_ease2_w50000.nc')


# In[128]:


# assinging the variables for Temperature
lon_t = tmp_data.variables["lon"][:]
lat_t = tmp_data.variables["lat"][:]
level = tmp_data.variables["level"][:]
air = tmp_data.variables["air"][:]
tmp_time = tmp_data.variables["time"]


# In[180]:


# Slicing the 'z' axis, to only get the mean surface temp at 850 hPa where most convergence occurs
air_temp_at_surf=(air[:,2,:,:])
#print(air_temp_at_surf)
#Finding index value of certain longitudes
print(np.where(lon_t==-62.5))
print(np.where(lon_t==-90))
air_temp_at_surf.shape
#Indexing to only get the Antarctic Circle
antcircle=air_temp_at_surf[:,36:47,:]
#print(antcircle)


# In[129]:


# assinging the variables for SIT
lon_sit = sea_data.variables["longitude"][:]
lat_sit = sea_data.variables["latitude"][:]
SIT = sea_data.variables["SIT"][:]
SIT_time= sea_data.variables["time"]


# In[130]:


import datetime as dt
from netCDF4 import Dataset, date2index, num2date, date2num

dates_T=num2date(SIT_time[:],SIT_time.units)


# In[131]:


dates_pd = pd.to_datetime(dates_T)
print
(dates_pd)


# In[192]:


def clim_plot(data):
    m = Basemap(projection='spstere',boundinglat=-50,lon_0=90,resolution='l')
    x, y = m(lon_sit, lat_sit )
    fig = plt.figure(figsize=(15,7))
    m.fillcontinents(color='white',lake_color='white')
    m.drawcoastlines()
    m.drawparallels(np.arange(-80.,81.,20.))
    m.drawmeridians(np.arange(-180.,181.,20.))
    m.drawmapboundary(fill_color='skyblue')
    m.contourf(x,y,data,40,cmap=plt.cm.get_cmap('jet'))
    plt.title('Sea Ice Thickness (in meters)')
    plt.colorbar()


# In[193]:


#here we use the function that was defined to plot Antarctica, calling SIT variable at the first timestep
clim_plot(SIT[44])
#plt.savefig('SITmap.png')


# In[134]:


#to get the average sea ice thickness we must go through all the values and do so with a for loop
#the reason 'np.nanmean' is used is to take an average of the array, but because values do not exist for every lat and lon for the array
sit_mean=[]
for y in range(len(SIT)):
    mean = np.nanmean(SIT[y])
    sit_mean.append(mean)


# In[135]:


print(sit_mean)


# In[116]:


ave_plot = plt.plot(sit_mean)
plt.xlabel('Timesteps')
plt.ylabel('SIT (in m)')
plt.title('Sea Ice Thickness ')
plt.show
plt.savefig('SIT_mean.png')


# In[153]:


air_mean=[]
for i in range(len(air)):
    mean = np.mean(air[i])
    air_mean.append(mean)


# In[154]:


print(air_mean)


# In[183]:


avetemp_plot = plt.plot(air_mean) #we are assinging a plot for the mean air temperature
plt.xlabel('Timesteps')           #labelling x-axis
plt.ylabel('Temperature C°')      #labelling y-axis
plt.title('Global Surface Air Temperature ') #giving the plot a title
plt.show
plt.savefig('global_tmp.png')


# In[181]:


ant_mean=[]
for i in range(len(antcircle)):
    mean = np.mean(antcircle[i])
    ant_mean.append(mean)


# In[194]:


anttemp_plot = plt.plot(ant_mean)
plt.xlabel('Timesteps')
plt.ylabel('Temperature C°')
plt.title('Antarctic Circle Surface Air Temperature ')
plt.show
#plt.savefig('ant_temp.png')


# In[ ]:




