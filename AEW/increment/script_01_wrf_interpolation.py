import os, sys
import datetime
import numpy as np
from wrf import getvar, interplevel, latlon_coords
from netCDF4 import Dataset
from scipy.interpolate import griddata

dir_wrfout = []
dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021'
dir_main = dir_CPEX + '/increment'
dir_wrfout.append(dir_CPEX + '/bkg')
dir_wrfout.append(dir_CPEX + '/da')

time = '20210824'
#cases = ['CON6h', 'CON6h_DS1h', 'CON6h_DS1h_UV', 'CON6h_DS1h_T', 'CON6h_DS1h_Q', 'CON6h_Aeolus6h']
#cases = ['CON6h_082500', 'CON6h_DS1h_082500', 'CON6h_DS1h_UV_082500', 'CON6h_DS1h_T_082500', 'CON6h_DS1h_Q_082500', 'CON6h_Aeolus6h_082500']
#cases = ['CON6h_082512', 'CON6h_DS1h_082512', 'CON6h_DS1h_UV_082512', 'CON6h_DS1h_T_082512', 'CON6h_DS1h_Q_082512', 'CON6h_Aeolus6h_082512']
#cases = ['CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_HALO1h', 'CON6h_DS1h', 'CON6h_DS1h_UV', 'CON6h_DS1h_T', 'CON6h_DS1h_Q', 'CON6h_Aeolus6h', 'CON6h_DAWN1h_HALO1h_DS1h', 'CON6h_DAWN1h_HALO1h_DS1h_Aeolus6h']
#cases = ['2021090412_CON6h_DAWN1h']
#cases = ['CON6h_Hybrid_082500']
#cases = ['CON6h_Aeolus6h_Hybrid_082500']
cases = ['CON6h_DS1h_Q_Hybrid_082500']

domains = ['d01']
cycling_interval = 1

if '20210820' in time:
    anl_start_time = datetime.datetime(2021, 8, 20, 18, 0, 0)
    anl_end_time   = datetime.datetime(2021, 8, 21,  0, 0, 0)
if '20210821' in time:
    anl_start_time = datetime.datetime(2021, 8, 21, 18, 0, 0)
    anl_end_time   = datetime.datetime(2021, 8, 22,  0, 0, 0)
if '20210824' in time:
    anl_start_time = datetime.datetime(2021, 8, 24, 18, 0, 0)
    anl_end_time   = datetime.datetime(2021, 8, 25,  0, 0, 0)
if '20210828' in time:
    anl_start_time = datetime.datetime(2021, 8, 28, 18, 0, 0)
    anl_end_time   = datetime.datetime(2021, 8, 29,  0, 0, 0)
if '20210904' in time:
    anl_start_time = datetime.datetime(2021, 9,  4, 18, 0, 0)
    anl_end_time   = datetime.datetime(2021, 9,  5,  0, 0, 0)

analysis_time  = anl_end_time - anl_start_time
analysis_hours = analysis_time.days*24.0 + analysis_time.seconds/3600.0
n_time = int(analysis_hours/cycling_interval) + 1
print(n_time)

variables = {}
variables.update({'ua':     [[925, 850, 700, 500, 300, 200], 'ms-1']})
variables.update({'va':     [[925, 850, 700, 500, 300, 200], 'ms-1']})
variables.update({'temp':   [[925, 850, 700, 500, 300, 200],    'K']})
variables.update({'QVAPOR': [[925, 850, 700, 500, 300, 200], 'null']})

for dom in domains:
    for case in cases:
        for var in variables.keys():

            (levels, unit) = variables[var]
            n_level = len(levels)

            filename = dir_main + '/' + time + '/' + case + '/' + var + '_da_' + dom + '.nc'
            os.system('rm -rf ' + filename)
            print(filename)

            for idt in range(0, n_time):

                time_now = anl_start_time + datetime.timedelta(hours = idt*cycling_interval)
                print(time_now)

                wrfout_bkg = dir_wrfout[0] + '/' + time + '/' + case + '/wrfout_' + dom + '_' + time_now.strftime('%Y-%m-%d_%H:00:00')
                wrfout_anl = dir_wrfout[1] + '/' + time + '/' + case + '/wrf_inout.' + time_now.strftime('%Y%m%d%H') + '.' + dom

                if os.path.exists(wrfout_bkg) and os.path.exists(wrfout_anl):

                    ncfile = Dataset(wrfout_bkg)
                    p_bkg  = getvar(ncfile, 'pressure')
                    if unit == 'null':
                        var_bkg = getvar(ncfile, var)
                    else:
                        var_bkg = getvar(ncfile, var, units=unit)
                    ncfile.close()

                    ncfile = Dataset(wrfout_anl)
                    p_anl  = getvar(ncfile, 'pressure')
                    if unit == 'null':
                        var_anl = getvar(ncfile, var)
                    else:
                        var_anl = getvar(ncfile, var, units=unit)
                    ncfile.close()

                    lat, lon = latlon_coords(p_bkg)
                    (n_lat, n_lon) = lat.shape

                    if idt == 0:

                        ncfile_output = Dataset(filename, 'w', format='NETCDF4')
                        ncfile_output.createDimension('n_time',  n_time)
                        ncfile_output.createDimension('n_level', n_level)
                        ncfile_output.createDimension('n_wrf',   2)
                        ncfile_output.createDimension('n_lat',   n_lat)
                        ncfile_output.createDimension('n_lon',   n_lon)
                        ncfile_output.createVariable('level', 'f8', ('n_level'))
                        ncfile_output.createVariable('lat',   'f8', ('n_lat',  'n_lon'))
                        ncfile_output.createVariable('lon',   'f8', ('n_lat',  'n_lon'))
                        ncfile_output.createVariable(var,     'f8', ('n_time', 'n_level', 'n_wrf', 'n_lat', 'n_lon'))
                        ncfile_output.variables['level'][:] = levels
                        ncfile_output.variables['lat'][:,:] = lat
                        ncfile_output.variables['lon'][:,:] = lon
                        ncfile_output.description           = var

                    if 0 in levels:
                        ncfile_output.variables[var][idt,0,0,:,:] = var_bkg
                        ncfile_output.variables[var][idt,0,1,:,:] = var_anl
                    else:
                        temp_bkg = interplevel(var_bkg, p_bkg, levels)
                        temp_anl = interplevel(var_anl, p_anl, levels)
                        for idl, lev in enumerate(levels):
                            ncfile_output.variables[var][idt,idl,0,:,:] = temp_bkg[idl,:,:]
                            ncfile_output.variables[var][idt,idl,1,:,:] = temp_anl[idl,:,:]

                else:

                    ncfile_output.variables[var][idt,:,:,:,:] = 0.0

            ncfile_output.close()
