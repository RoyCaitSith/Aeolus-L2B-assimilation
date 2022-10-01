import os, sys
import pygrib
import datetime
import numpy as np
from wrf import getvar, interplevel, latlon_coords
from netCDF4 import Dataset
from scipy.interpolate import griddata

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS'
dir_data = '/'.join([dir_GOES, 'Data'])
dir_main = '/'.join([dir_CPEX, 'forecasts'])

cases = ['GFS']
start_time = datetime.datetime(2021, 8, 24, 18, 0, 0)
end_time   = datetime.datetime(2021, 8, 29,  0, 0, 0)

domains = ['d01']
cycling_interval = 6
n_time = int((end_time - start_time).total_seconds()/3600/6+1)

variables = {}
variables.update({'ua':      [[925, 850, 700, 600, 500, 300, 200], 'ms-1', 'U component of wind']})
variables.update({'va':      [[925, 850, 700, 600, 500, 300, 200], 'ms-1', 'V component of wind']})
variables.update({'avo':     [[925, 850, 700, 600, 500, 300, 200], 's-1',  'Absolute vorticity']})
variables.update({'rh':      [[925, 850, 700, 600, 500, 300, 200], '%',    'Relative humidity']})
variables.update({'geopt':   [[925, 850, 700, 600, 500, 300, 200], 'gpm',  'Geopotential height']})

for dom in domains:
    for case in cases:
        for var in variables.keys():

            (levels, unit, GFS_var) = variables[var]
            n_level = len(levels)

            dir_file = '/'.join([dir_main, 'gfs', 'CON6h_Aeolus6h_082418_Hybrid_C08'])
            filename = dir_file + '/' + var + '_' + dom + '.nc'
            os.system('mkdir '  + dir_file)
            os.system('rm -rf ' + filename)
            print(filename)

            dir_wrfout = '/'.join([dir_CPEX, 'cycling_da', 'Data', 'CON6h_Aeolus6h_082418_Hybrid_C08', 'bkg'])
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

                YYMMDD   = time_now.strftime('%Y%m%d')
                YYMMDDHH = time_now.strftime('%Y%m%d%H')

                dir_GFS  = '/'.join([dir_GOES, 'Data', 'GFS'])
                GFS_name = '.'.join(['gfs', '0p25', YYMMDDHH, 'f000', 'grib2'])
                info = os.popen('ls ' + dir_GFS + '/' + GFS_name).readlines()
                file_GFS = info[0].replace('\n', '')
                print(file_GFS)

                GFS_file = pygrib.open(file_GFS)

                for idl, lev in enumerate(levels):
                    print(lev)
                    GFS_temp = GFS_file.select(name=GFS_var, typeOfLevel='isobaricInhPa', level=lev)[0]
                    GFS_lat, GFS_lon = GFS_temp.latlons()
                    GFS_lon[GFS_lon>180.0] = GFS_lon[GFS_lon>180.0] - 360.0
                    GFS_index = (GFS_lat < max_lat + 15.0) & (GFS_lat > min_lat - 15.0) & \
                                (GFS_lon < max_lon + 15.0) & (GFS_lon > min_lon - 15.0)
                    GFS_lat_1d = GFS_lat[GFS_index]
                    GFS_lon_1d = GFS_lon[GFS_index]
                    GFS_temp_1d = GFS_temp.values[GFS_index]
                    ncfile_output.variables[var][idt,idl,:,:] = griddata((GFS_lon_1d, GFS_lat_1d), GFS_temp_1d, (lon, lat), method='linear')

                GFS_file.close()

                time_now += datetime.timedelta(hours = cycling_interval)
                idt += 1

            ncfile_output.close()
