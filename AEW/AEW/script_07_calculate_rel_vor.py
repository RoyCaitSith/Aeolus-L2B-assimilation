import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import datetime
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from scipy.ndimage import gaussian_filter
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.basemap import Basemap

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021'
dir_main = dir_CPEX + '/AEW'

case = 'GFS'
time = '20210821'

if '20210820' in time:
    start_time = datetime.datetime(2021, 8, 19,  0, 0, 0)
    end_time   = datetime.datetime(2021, 8, 22,  6, 0, 0)
if '20210821' in time:
    start_time = datetime.datetime(2021, 8, 20,  0, 0, 0)
    end_time   = datetime.datetime(2021, 8, 23,  6, 0, 0)

domains = ['d01']
cycling_interval = 6
n_time = int((end_time - start_time).total_seconds()/3600/6+1)

for dom in domains:

    dir_file = dir_main + '/' + time + '/' + case
    filename = dir_file + '/avo_' + dom + '.nc'
    ncfile   = Dataset(filename)
    lat      = ncfile.variables['lat'][:,:]
    lon      = ncfile.variables['lon'][:,:]
    level    = ncfile.variables['level'][:]
    avo      = ncfile.variables['avo'][:,:,:,:]
    ncfile.close()

    n_level = len(level)
    n_lon = len(lon[0, :])
    n_lat = len(lon[:, 0])

    filename = dir_file + '/rel_vor_' + dom + '.nc'
    ncfile_output = Dataset(filename, 'w', format='NETCDF4')
    ncfile_output.createDimension('n_time',  n_time)
    ncfile_output.createDimension('n_level', n_level)
    ncfile_output.createDimension('n_lat',   n_lat)
    ncfile_output.createDimension('n_lon',   n_lon)
    ncfile_output.createVariable('level',   'f8', ('n_level'))
    ncfile_output.createVariable('lat',     'f8', ('n_lat',  'n_lon'))
    ncfile_output.createVariable('lon',     'f8', ('n_lat',  'n_lon'))
    ncfile_output.createVariable('rel_vor', 'f8', ('n_time', 'n_level', 'n_lat', 'n_lon'))

    ncfile_output.variables['level'][:] = level
    ncfile_output.variables['lat'][:,:] = lat
    ncfile_output.variables['lon'][:,:] = lon
    ncfile_output.description = 'relative vorticity'

    for idt in range(n_time):
        for idl in range(len(level)):
            ncfile_output.variables['rel_vor'][idt,idl,:,:] = avo[idt,idl,:,:] - 2.0*7.2921/100000.0*np.sin(lat*np.pi/180.0)
    rel_vor = ncfile_output.variables['rel_vor'][:,:,:,:]
    ncfile_output.close()

    filename = dir_file + '/rel_vor_gau_' + dom + '.nc'
    ncfile_output = Dataset(filename, 'w', format='NETCDF4')
    ncfile_output.createDimension('n_time',  n_time)
    ncfile_output.createDimension('n_level', n_level)
    ncfile_output.createDimension('n_lat',   n_lat)
    ncfile_output.createDimension('n_lon',   n_lon)
    ncfile_output.createVariable('level',       'f8', ('n_level'))
    ncfile_output.createVariable('lat',         'f8', ('n_lat',  'n_lon'))
    ncfile_output.createVariable('lon',         'f8', ('n_lat',  'n_lon'))
    ncfile_output.createVariable('rel_vor_gau', 'f8', ('n_time', 'n_level', 'n_lat', 'n_lon'))

    ncfile_output.variables['level'][:] = level
    ncfile_output.variables['lat'][:,:] = lat
    ncfile_output.variables['lon'][:,:] = lon
    ncfile_output.description = 'relative vorticity after gaussian filter'

    for idt in range(n_time):
        for idl in range(len(level)):
            ncfile_output.variables['rel_vor_gau'][idt,idl,:,:] = gaussian_filter(rel_vor[idt,idl,:,:], sigma=10)
    ncfile_output.close()
