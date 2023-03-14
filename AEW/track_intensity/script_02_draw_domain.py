#!/usr/bin/python

import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

from wrf import getvar
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main = dir_GOES + '/18_2020Laura_Experiments/track_intensity'
dir_figures = dir_main + '/case_02/figures'
dir_best_track = dir_main + '/best_track'

file_d01 = dir_main + '/wrfout_and_wrfrst/wrfout_d01_2020-08-25_00:00:00'
file_d02 = dir_main + '/wrfout_and_wrfrst/wrfout_d02_2020-08-25_00:00:00'
file_best_track = dir_best_track + '/2020_Laura.csv'

data_d01 = Dataset(file_d01)
lat_d01 = data_d01.variables['XLAT'][0,:,:]
lon_d01 = data_d01.variables['XLONG'][0,:,:]
extent = [lon_d01[0,0], lon_d01[-1,-1], lat_d01[0,0], lat_d01[-1,-1]]
data_d01.close()

lat_d02  = []
lon_d02  = []
data_d02 = Dataset(file_d02)
lat_temp = data_d02.variables['XLAT'][0,:,:]
lon_temp = data_d02.variables['XLONG'][0,:,:]
n_we     = len(lat_temp[0, :])
n_sn     = len(lat_temp[:, 0])
lat_d02  = lat_d02 + list(lat_temp[0, 0:n_we-1:1])
lat_d02  = lat_d02 + list(lat_temp[0:n_sn-1, n_we-1])
lat_d02  = lat_d02 + list(lat_temp[n_sn-1, n_we-1:0:-1])
lat_d02  = lat_d02 + list(lat_temp[n_sn-1:0:-1, 0])
lon_d02  = lon_d02 + list(lon_temp[0, 0:n_we-1:1])
lon_d02  = lon_d02 + list(lon_temp[0:n_sn-1, n_we-1])
lon_d02  = lon_d02 + list(lon_temp[n_sn-1, n_we-1:0:-1])
lon_d02  = lon_d02 + list(lon_temp[n_sn-1:0:-1, 0])
lat_d02.append(lat_temp[0, 0])
lon_d02.append(lon_temp[0, 0])
data_d02.close()

fig = plt.figure(1, [6.00, 5.25])
fig.subplots_adjust(left=0.075, bottom=0.000, right=0.925, top=0.925, wspace=0.000, hspace=0.000)

ax  = fig.add_subplot(111)
m = Basemap(llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], \
            projection='lcc', lat_1=40.0, lat_2=20.0, lon_0=-80.0, resolution='i', ax=ax)
m.drawcoastlines(linewidth=0.2, color='k')
m.fillcontinents(color=[0.9375, 0.9375, 0.859375])
m.drawparallels(np.arange(0, 70, 10), labels=[1,1,0,0], fontsize=10.0, linewidth=0.5)
m.drawmeridians(np.arange(-120, -35, 10), labels=[0,0,1,1], fontsize=10.0, linewidth=0.5)

x_lon_d02, y_lat_d02 = m(lon_d02, lat_d02, inverse=False)
x_d01, y_d01 = m(-99.0, 11.0, inverse=False)
x_d02, y_d02 = m(-94.5, 14.5, inverse=False)
ax.plot(x_lon_d02, y_lat_d02, color='k', linewidth=0.75, zorder=3)
ax.text(x_d01, y_d01, 'd01: 12km', ha='center', va='center', color='black', fontsize=10.0, zorder=4)
ax.text(x_d02, y_d02, 'd02: 4km', ha='center', va='center', color='black', fontsize=10.0, zorder=4)
#ax.set_title(title, fontsize=10.0, pad=4.0)

df = pd.read_csv(file_best_track)
Latitude = list(df['Latitude'])
Longitude = list(df['Longitude'])
MWS = df['MWS (Knot)']
hh = df['Date_Time']
hh = [float(x[11:13]) for x in hh]
print(df)

x_Longitude, y_Latitude = m(Longitude, Latitude, inverse=False)
sc = ax.scatter(x_Longitude, y_Latitude, c=MWS, edgecolor='none', vmin=20, vmax=125, s=30, cmap='jet', label='NHC', zorder=5)
ax.plot(x_Longitude[2::4], y_Latitude[2::4], 'o', color='w', ms=1.50, zorder=6)
#ax.plot(x_Longitude, y_Latitude, 'o', color='white', ms=2.20, markevery=(int((4-hh[0]/6.0)%4), 4), zorder=6)

time_label = ['22', '23', '24', '25', '26', '27', '28', '29']
for idx, tlabel in enumerate(time_label):
    ax.text(x_Longitude[4*idx+2], y_Latitude[4*idx+2], tlabel, va='center', ha='center', fontsize=10.0, zorder=6)

plt.legend(loc='upper right', fontsize=10.0, scatterpoints=1, handlelength=1.0)
grade = [20, 33, 63, 82, 95, 112, 125]
cat   = ['TD', 'TS', 'Cat1', 'Cat2', 'Cat3', 'Cat4']
clb = plt.colorbar(sc, ticks=grade, orientation='horizontal', pad=0.100, aspect=30, shrink=1.00)
clb.set_ticklabels(grade)
clb.set_label('MWS (Knot)', rotation=0, fontsize=10.0)
clb.ax.tick_params(axis='both', direction='in', labelsize=10.0)
for idx, lab in enumerate(cat):
    clb.ax.text(0.5*(grade[idx+1]+grade[idx]), 175.0, lab, ha='center', va='center', color='black', fontsize=10.0)

plt.savefig(dir_figures + '/Figure_WRF_domain.pdf')
