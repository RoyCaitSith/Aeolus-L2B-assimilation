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
from metpy.calc import divergence

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021'
dir_main = dir_CPEX + '/AEW'

time = '20210821'
domains = ['d01']

if '20210820' in time:
    cases = ['CTRL', 'MP01', 'MP02', 'MP08', 'MP10', 'MP16', 'MP26', \
             'BL02', 'BL04', 'BL06', 'BL07', 'CU02', 'CU11', 'CU14', 'CU16', 'RA03', 'RA04', 'RA05', 'RA14', \
             'GFS', 'CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_DAWN1hOE1p5', 'CON6h_HALO1h', 'CON6h_HALO1hOE0p2', \
             'CON6h_DS1h', 'CON6h_DS1h_UV', 'CON6h_DS1h_T', 'CON6h_DS1h_Q', 'CON6h_Aeolus6h', 'CON6h_DAWN1h_HALO1h_DS1h', 'CON6h_DAWN1h_HALO1h_DS1h_Aeolus6h']
if '20210821' in time:
    cases = ['GFS', 'CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_DAWN1hOE1p5', 'CON6h_HALO1h', \
             'CON6h_DS1h', 'CON6h_DS1h_UV', 'CON6h_DS1h_T', 'CON6h_DS1h_Q', 'CON6h_Aeolus6h', 'CON6h_DAWN1h_HALO1h_DS1h', 'CON6h_DAWN1h_HALO1h_DS1h_Aeolus6h']

for dom in domains:
    for case in cases:

        dir_file = dir_main + '/' + time + '/' + case
        filename = dir_file + '/ua_' + dom + '.nc'
        ncfile   = Dataset(filename)
        lat      = ncfile.variables['lat'][:,:]
        lon      = ncfile.variables['lon'][:,:]
        level    = ncfile.variables['level'][:]
        ua       = ncfile.variables['ua'][:,:,:,:]
        ncfile.close()

        filename = dir_file + '/va_' + dom + '.nc'
        ncfile   = Dataset(filename)
        va       = ncfile.variables['va'][:,:,:,:]
        ncfile.close()

        n_level = len(level)
        n_lon   = len(lon[0, :])
        n_lat   = len(lon[:, 0])
        n_time  = len(ua)

        filename = dir_file + '/div_' + dom + '.nc'
        ncfile_output = Dataset(filename, 'w', format='NETCDF4')
        ncfile_output.createDimension('n_time',  n_time)
        ncfile_output.createDimension('n_level', n_level)
        ncfile_output.createDimension('n_lat',   n_lat)
        ncfile_output.createDimension('n_lon',   n_lon)
        ncfile_output.createVariable('level',   'f8', ('n_level'))
        ncfile_output.createVariable('lat',     'f8', ('n_lat',  'n_lon'))
        ncfile_output.createVariable('lon',     'f8', ('n_lat',  'n_lon'))
        ncfile_output.createVariable('div',     'f8', ('n_time', 'n_level', 'n_lat', 'n_lon'))

        ncfile_output.variables['level'][:] = level
        ncfile_output.variables['lat'][:,:] = lat
        ncfile_output.variables['lon'][:,:] = lon
        ncfile_output.description = 'divergence'

        for idt in range(n_time):
            for idl in range(len(level)):
                ncfile_output.variables['div'][idt,idl,:,:] = divergence(ua[idt,idl,:,:], va[idt,idl,:,:], dx=12000.0, dy=12000.0)
        ncfile_output.close()
