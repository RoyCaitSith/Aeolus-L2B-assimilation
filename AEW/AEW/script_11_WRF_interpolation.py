import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import Nio
import os, sys
import datetime
import numpy as np
from wrf import getvar, interplevel, latlon_coords
from netCDF4 import Dataset
from scipy.interpolate import griddata

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021'
dir_data = '/'.join([dir_GOES, 'Data'])
dir_main = '/'.join([dir_CPEX, 'AEW'])

time = '20210820'
domains = ['d01']

if '20210820' in time:
    start_time = datetime.datetime(2021, 8, 20, 18, 0, 0)
    end_time   = datetime.datetime(2021, 8, 22,  6, 0, 0)
    cases = ['CTRL', 'MP01', 'MP02', 'MP08', 'MP10', 'MP16', 'MP26', \
             'BL02', 'BL04', 'BL06', 'BL07', 'CU02', 'CU11', 'CU14', 'CU16', 'RA03', 'RA04', 'RA05', 'RA14', \
             'CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_DAWN1hOE1p5', 'CON6h_HALO1h', 'CON6h_HALO1hOE0p2', \
             'CON6h_DS1h', 'CON6h_DS1h_UV', 'CON6h_DS1h_T', 'CON6h_DS1h_Q', 'CON6h_Aeolus6h', 'CON6h_DAWN1h_HALO1h_DS1h', 'CON6h_DAWN1h_HALO1h_DS1h_Aeolus6h']
if '20210821' in time:
    start_time = datetime.datetime(2021, 8, 21, 18, 0, 0)
    end_time   = datetime.datetime(2021, 8, 23,  6, 0, 0)
    cases = ['CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_DAWN1hOE1p5', 'CON6h_HALO1h', \
             'CON6h_DS1h', 'CON6h_DS1h_UV', 'CON6h_DS1h_T', 'CON6h_DS1h_Q', 'CON6h_Aeolus6h', 'CON6h_DAWN1h_HALO1h_DS1h', 'CON6h_DAWN1h_HALO1h_DS1h_Aeolus6h']

print(len(cases))

cycling_interval = 6
n_time = int((end_time - start_time).total_seconds()/3600/6+1)

variables = {}
variables.update({'ua':     [[925, 850, 700, 600, 500, 300, 200], 'ms-1']})
variables.update({'va':     [[925, 850, 700, 600, 500, 300, 200], 'ms-1']})
variables.update({'avo':    [[925, 850, 700, 600, 500, 300, 200], 'null']})
variables.update({'pvo':    [[925, 850, 700, 600, 500, 300, 200], 'null']})
variables.update({'eth':    [[925, 850, 700, 600, 500, 300, 200],    'K']})
variables.update({'rh':     [[925, 850, 700, 600, 500, 300, 200], 'null']})
variables.update({'slp':    [[0],                                  'hPa']})

for dom in domains:
    for case in cases:
        for var in variables.keys():

            (levels, unit) = variables[var]
            n_level = len(levels)

            dir_file = '/'.join([dir_main, time, case])
            filename = var + '_' + dom + '.nc'
            filename = '/'.join([dir_file, filename])
            #os.system('mkdir '  + dir_file)
            os.system('rm -rf ' + filename)
            print(filename)

            dir_wrfout = '/'.join([dir_CPEX, 'bkg', time, case])
            wrf_file   = '_'.join(['wrfout', dom, end_time.strftime('%Y-%m-%d_%H:00:00')])
            wrfout     = '/'.join([dir_wrfout, wrf_file])

            ncfile         = Dataset(wrfout)
            p              = getvar(ncfile, 'pressure')
            lat, lon       = latlon_coords(p)
            (n_lat, n_lon) = lat.shape
            ncfile.close()

            max_lat = np.array(np.max(np.max(lat)))
            min_lat = np.array(np.min(np.min(lat)))
            max_lon = np.array(np.max(np.max(lon)))
            min_lon = np.array(np.min(np.min(lon)))

            ncfile_output = Dataset(filename, 'w', format='NETCDF4')
            ncfile_output.createDimension('n_time',  n_time)
            ncfile_output.createDimension('n_level', n_level)
            ncfile_output.createDimension('n_lat',   n_lat)
            ncfile_output.createDimension('n_lon',   n_lon)
            ncfile_output.createVariable('level', 'f8', ('n_level'))
            ncfile_output.createVariable('lat',   'f8', ('n_lat',  'n_lon'))
            ncfile_output.createVariable('lon',   'f8', ('n_lat',  'n_lon'))
            ncfile_output.createVariable(var,     'f8', ('n_time', 'n_level', 'n_lat', 'n_lon'))

            ncfile_output.variables['level'][:] = levels
            ncfile_output.variables['lat'][:,:] = lat
            ncfile_output.variables['lon'][:,:] = lon
            ncfile_output.description = var

            idt = 0
            time_now = start_time
            while time_now <= end_time:

                dir_wrfout = '/'.join([dir_CPEX, 'bkg', time, case])
                wrf_file   = '_'.join(['wrfout', dom, time_now.strftime('%Y-%m-%d_%H:00:00')])
                wrfout     = '/'.join([dir_wrfout, wrf_file])

                ncfile = Dataset(wrfout)
                p = getvar(ncfile, 'pressure')
                if unit == 'null': var_value = getvar(ncfile, var)
                else: var_value = getvar(ncfile, var, units=unit)
                ncfile.close()

                lat, lon = latlon_coords(p)
                (n_lat, n_lon) = lat.shape

                if 0 in levels:
                    ncfile_output.variables[var][idt,0,:,:] = var_value
                else:
                    temp_value = interplevel(var_value, p, levels)
                    for idl, lev in enumerate(levels):
                        ncfile_output.variables[var][idt,idl,:,:] = temp_value[idl,:,:]

                time_now += datetime.timedelta(hours = cycling_interval)
                idt += 1

            ncfile_output.close()
