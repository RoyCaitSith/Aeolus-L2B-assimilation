import os
import h5py
import datetime
import numpy as np
import pandas as pd
from wrf import getvar, latlon_coords
from netCDF4 import Dataset
from scipy.interpolate import griddata

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS'
dir_main = dir_CPEX + '/rainfall'

domains = ['d01']
accumulation_hour = 6

#cases = ['IMERG', 'CON6h_082406_Hybrid_C08']
#cases = ['IMERG', 'CON6h_082412_Hybrid_C08']
#cases = ['IMERG', 'CON6h_082418_Hybrid_C08']
#cases = ['IMERG', 'CON6h_082500_Hybrid_C08']
#cases = ['IMERG', 'CON6h_Aeolus6h_082406_Hybrid_C08']
#cases = ['IMERG', 'CON6h_Aeolus6h_082412_Hybrid_C08']
cases = ['IMERG', 'CON6h_Aeolus6h_082418_Hybrid_C05']
#cases = ['IMERG', 'CON6h_Aeolus6h_082500_Hybrid_C08']

anl_end_time = datetime.datetime(2021, 8, 26,  0, 0, 0)
forecast_start_time = datetime.datetime(2021, 8, 26,  6, 0, 0)
forecast_end_time = datetime.datetime(2021, 8, 28,  6, 0, 0)
n_time = int((forecast_end_time - forecast_start_time).total_seconds()/3600/6+1)

print(len(cases))

for dom in domains:
    for case in cases:

        dir_case = dir_main + '/' + case
        dir_wrfout = '/'.join([dir_CPEX, 'cycling_da', 'Data', case, 'bkg'])
        filename = dir_case + '/rainfall_6h_' + dom + '.nc'
        if 'IMERG' in case:
            dir_case = dir_main + '/' + cases[-1]
            dir_wrfout = '/'.join([dir_CPEX, 'cycling_da', 'Data', cases[-1], 'bkg'])
            filename = dir_case + '/IMERG_6h_' + dom + '.nc'
        os.system('mkdir ' + dir_case)
        print(filename)

        time_now = forecast_start_time

        wrfout = dir_wrfout + '/wrfout_' + dom + '_' + time_now.strftime('%Y-%m-%d_%H:%M:00')
        ncfile = Dataset(wrfout)
        RAINNC = getvar(ncfile, 'RAINNC')
        ncfile.close()

        lat, lon = latlon_coords(RAINNC)
        (n_lat, n_lon) = lat.shape

        ncfile_output = Dataset(filename, 'w', format='NETCDF4')
        ncfile_output.createDimension('n_time', n_time)
        ncfile_output.createDimension('n_lat',  n_lat)
        ncfile_output.createDimension('n_lon',  n_lon)
        ncfile_output.createVariable('lat',      'f8', ('n_lat', 'n_lon'))
        ncfile_output.createVariable('lon',      'f8', ('n_lat', 'n_lon'))
        ncfile_output.createVariable('rainfall', 'f8', ('n_time', 'n_lat', 'n_lon'))

        ncfile_output.variables['lat'][:,:] = lat
        ncfile_output.variables['lon'][:,:] = lon
        ncfile_output.variables['rainfall'][:,:,:] = 0.0

        for idt in range(0, n_time):

            time_now = forecast_start_time + datetime.timedelta(hours = idt*6.0)
            print(time_now)

            if 'IMERG' in case:

                IMERG_prep = np.zeros((3600, 1800), dtype=float)

                for dh in np.arange(-6.0, 0.0, 0.5):

                    time_IMERG = time_now + datetime.timedelta(hours=dh)
                    YYMMDD     = time_IMERG.strftime('%Y%m%d')
                    HHMMSS     = time_IMERG.strftime('%H%M%S')

                    dir_IMERG  = dir_GOES + '/Data/IMERG'
                    info       = os.popen('ls ' + dir_IMERG + '/' + YYMMDD + '/3B-HHR.MS.MRG.3IMERG.' + YYMMDD + '-S' + HHMMSS + '*').readlines()
                    file_IMERG = info[0].replace('\n', '')
                    print(file_IMERG)

                    f          = h5py.File(file_IMERG)
                    IMERG_prep = IMERG_prep + 0.5*f['Grid']['precipitationCal'][0,:,:]

                IMERG_prep  = IMERG_prep/6.0
                IMERG_lat   = np.tile(f['Grid']['lat'][:], (3600, 1))
                IMERG_lon   = np.transpose(np.tile(f['Grid']['lon'][:], (1800, 1)))
                IMERG_index = (IMERG_lat < np.array(lat[-1, -1]) + 15.0) & (IMERG_lat > np.array(lat[0, 0]) - 15.0) & \
                              (IMERG_lon < np.array(lon[-1, -1]) + 15.0) & (IMERG_lon > np.array(lon[0, 0]) - 15.0)

                IMERG_prep_1d = IMERG_prep[IMERG_index]
                IMERG_lat_1d  = IMERG_lat[IMERG_index]
                IMERG_lon_1d  = IMERG_lon[IMERG_index]

                ncfile_output.variables['rainfall'][idt,:,:] = griddata((IMERG_lon_1d, IMERG_lat_1d), IMERG_prep_1d, (lon, lat), method='linear')
                print(np.nanmax(ncfile_output.variables['rainfall'][idt,:,:]))
                print(np.nanmin(ncfile_output.variables['rainfall'][idt,:,:]))

            else:

                cycling_interval = 6

                for idx in range(0, accumulation_hour, cycling_interval):

                    time_0 = time_now - datetime.timedelta(hours = idx+cycling_interval)
                    time_1 = time_now - datetime.timedelta(hours = idx)

                    wrfout_0 = dir_wrfout + '/wrfout_' + dom + '_' + time_0.strftime('%Y-%m-%d_%H:%M:00')
                    wrfout_1 = dir_wrfout + '/wrfout_' + dom + '_' + time_1.strftime('%Y-%m-%d_%H:%M:00')
                    print(wrfout_0)
                    print(wrfout_1)

                    ncfile   = Dataset(wrfout_0)
                    RAINNC_0 = getvar(ncfile, 'RAINNC')
                    RAINC_0  = getvar(ncfile, 'RAINC')
                    ncfile.close()

                    ncfile   = Dataset(wrfout_1)
                    RAINNC_1 = getvar(ncfile, 'RAINNC')
                    RAINC_1  = getvar(ncfile, 'RAINC')
                    ncfile.close()

                    if time_0 == anl_end_time:
                        RAINNC_0 = 0.0
                        RAINC_0 = 0.0

                    rainfall = RAINNC_1 + RAINC_1 - RAINNC_0 - RAINC_0
                    ncfile_output.variables['rainfall'][idt,:,:] = ncfile_output.variables['rainfall'][idt,:,:] + rainfall

                ncfile_output.variables['rainfall'][idt,:,:] = ncfile_output.variables['rainfall'][idt,:,:]/6.0
                print(np.nanmax(ncfile_output.variables['rainfall'][idt,:,:]))
                print(np.nanmin(ncfile_output.variables['rainfall'][idt,:,:]))

        ncfile_output.close()
