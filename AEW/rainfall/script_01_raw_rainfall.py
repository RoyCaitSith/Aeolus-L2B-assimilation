import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import h5py
import datetime
import numpy as np
import pandas as pd
from wrf import getvar, latlon_coords
from netCDF4 import Dataset
from scipy.interpolate import griddata

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021'
dir_main = dir_CPEX + '/rainfall'

time = '20210824'
domains = ['d01']
accumulation_hour = 6

if '20210820' in time:
    flight_start_time   = datetime.datetime(2021, 8, 20, 18, 0, 0)
    flight_end_time     = datetime.datetime(2021, 8, 21,  0, 0, 0)
    anl_end_time        = datetime.datetime(2021, 8, 21,  0, 0, 0)
    forecast_start_time = datetime.datetime(2021, 8, 21,  6, 0, 0)
    forecast_end_time   = datetime.datetime(2021, 8, 22,  6, 0, 0)
    cases = ['IMERG', 'EOL', 'CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_DAWN1hOE1p5', 'CON6h_HALO1h', 'CON6h_HALO1hOE0p2', \
             'CON6h_DS1h', 'CON6h_DS1h_UV', 'CON6h_DS1h_T', 'CON6h_DS1h_Q', 'CON6h_Aeolus6h', 'CON6h_DAWN1h_HALO1h_DS1h', 'CON6h_DAWN1h_HALO1h_DS1h_Aeolus6h', \
             'CTRL', 'MP01', 'MP02', 'MP08', 'MP10', 'MP16', 'MP26', 'BL02', 'BL04', 'BL06', 'BL07', 'CU02', 'CU11', 'CU14', 'CU16', 'RA03', 'RA04', 'RA05', 'RA14']
if '20210821' in time:
    flight_start_time   = datetime.datetime(2021, 8, 21, 18, 0, 0)
    flight_end_time     = datetime.datetime(2021, 8, 22,  0, 0, 0)
    anl_end_time        = datetime.datetime(2021, 8, 22,  0, 0, 0)
    forecast_start_time = datetime.datetime(2021, 8, 22,  6, 0, 0)
    forecast_end_time   = datetime.datetime(2021, 8, 23,  6, 0, 0)
    cases = ['IMERG', 'EOL', 'CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_DAWN1hOE1p5', 'CON6h_HALO1h', \
             'CON6h_DS1h', 'CON6h_DS1h_UV', 'CON6h_DS1h_T', 'CON6h_DS1h_Q', 'CON6h_Aeolus6h', 'CON6h_DAWN1h_HALO1h_DS1h', 'CON6h_DAWN1h_HALO1h_DS1h_Aeolus6h']
if '20210824' in time:
    #082412
    #anl_end_time        = datetime.datetime(2021, 8, 24, 12, 0, 0)
    #forecast_start_time = datetime.datetime(2021, 8, 24, 18, 0, 0)
    #forecast_end_time   = datetime.datetime(2021, 8, 26, 18, 0, 0)
    #082500
    #flight_start_time   = datetime.datetime(2021, 8, 24, 18, 0, 0)
    #flight_end_time     = datetime.datetime(2021, 8, 25,  0, 0, 0)
    #anl_end_time        = datetime.datetime(2021, 8, 25,  0, 0, 0)
    #forecast_start_time = datetime.datetime(2021, 8, 25,  6, 0, 0)
    #forecast_end_time   = datetime.datetime(2021, 8, 28, 18, 0, 0)
    #082512
    flight_start_time   = datetime.datetime(2021, 8, 24, 18, 0, 0)
    flight_end_time     = datetime.datetime(2021, 8, 25,  0, 0, 0)
    anl_end_time        = datetime.datetime(2021, 8, 25, 12, 0, 0)
    forecast_start_time = datetime.datetime(2021, 8, 25,  6, 0, 0)
    forecast_end_time   = datetime.datetime(2021, 8, 28, 18, 0, 0)
    #082512
    #anl_end_time        = datetime.datetime(2021, 8, 25, 12, 0, 0)
    #forecast_start_time = datetime.datetime(2021, 8, 25, 12, 0, 0)
    #forecast_end_time   = datetime.datetime(2021, 8, 27, 18, 0, 0)
    #IMERG
    #anl_end_time        = datetime.datetime(2021, 8, 24, 12, 0, 0)
    #forecast_start_time = datetime.datetime(2021, 8, 24, 18, 0, 0)
    #forecast_end_time   = datetime.datetime(2021, 8, 27, 18, 0, 0)
    #cases = ['IMERG', 'EOL', 'CON6h', 'CON6h_Aeolus6h', 'CON6h_DS1h', 'CON6h_DS1h_Q', 'CON6h_DS1h_T', 'CON6h_DS1h_UV']
    #cases = ['IMERG', 'EOL', 'CON6h_082500', 'CON6h_Aeolus6h_082500', 'CON6h_DS1h_082500', 'CON6h_DS1h_Q_082500', 'CON6h_DS1h_T_082500', 'CON6h_DS1h_UV_082500']
    #cases = ['IMERG', 'EOL', 'CON6h_082512', 'CON6h_Aeolus6h_082512', 'CON6h_DS1h_082512', 'CON6h_DS1h_Q_082512', 'CON6h_DS1h_T_082512', 'CON6h_DS1h_UV_082512']
    #cases = ['CON6h_Hybrid_082500', 'CON6h_Aeolus6h_Hybrid_082500']
    #cases = ['CON6h_Hybrid_082512', 'CON6h_Aeolus6h_Hybrid_082512']
    #cases = ['CON6h_No1h_Hybrid_082412', 'CON6h_Aeolus6h_No1h_Hybrid_082412']
    #cases = ['CON6h_No1h_Hybrid_082512', 'CON6h_Aeolus6h_No1h_Hybrid_082512']
    #cases = ['IMERG']
    #cases = ['CON6h_Hybrid_082500', 'CON6h_Aeolus6h_Hybrid_082500', 'CON6h_DS1h_Hybrid_082500', 'CON6h_DS1h_UV_Hybrid_082500', 'CON6h_DS1h_T_Hybrid_082500', 'CON6h_DS1h_Q_Hybrid_082500']
    cases = ['CON6h_Hybrid_082512', 'CON6h_Aeolus6h_Hybrid_082512', 'CON6h_DS1h_Hybrid_082512', 'CON6h_DS1h_UV_Hybrid_082512', 'CON6h_DS1h_T_Hybrid_082512', 'CON6h_DS1h_Q_Hybrid_082512']
if '20210828' in time:
    flight_start_time   = datetime.datetime(2021, 8, 28, 18, 0, 0)
    flight_end_time     = datetime.datetime(2021, 8, 29,  0, 0, 0)
    anl_end_time        = datetime.datetime(2021, 8, 29,  0, 0, 0)
    forecast_start_time = datetime.datetime(2021, 8, 29,  6, 0, 0)
    forecast_end_time   = datetime.datetime(2021, 8, 31,  6, 0, 0)
    cases = ['IMERG', 'EOL', 'CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_DAWN1hOE1p5', 'CON6h_HALO1h', 'CON6h_HALO1hOE0p2', \
             'CON6h_DS1h', 'CON6h_DS1h_UV', 'CON6h_DS1h_T', 'CON6h_DS1h_Q', 'CON6h_Aeolus6h', 'CON6h_DAWN1h_HALO1h_DS1h', 'CON6h_DAWN1h_HALO1h_DS1h_Aeolus6h']
if '20210904' in time:
    #flight_start_time   = datetime.datetime(2021, 9,  4, 18, 0, 0)
    #flight_end_time     = datetime.datetime(2021, 9,  5,  0, 0, 0)
    #anl_end_time        = datetime.datetime(2021, 9,  5,  0, 0, 0)
    #forecast_start_time = datetime.datetime(2021, 9,  5,  6, 0, 0)
    #forecast_end_time   = datetime.datetime(2021, 9,  7,  6, 0, 0)
    #cases = ['IMERG', 'EOL', 'CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_DAWN1hOE1p5', 'CON6h_HALO1h', 'CON6h_HALO1hOE0p2', \
             #'CON6h_DS1h', 'CON6h_DS1h_UV', 'CON6h_DS1h_T', 'CON6h_DS1h_Q', 'CON6h_Aeolus6h']
    flight_start_time   = datetime.datetime(2021, 9,  4, 18, 0, 0)
    flight_end_time     = datetime.datetime(2021, 9,  5,  0, 0, 0)
    anl_end_time        = datetime.datetime(2021, 9,  5, 18, 0, 0)
    forecast_start_time = datetime.datetime(2021, 9,  6,  0, 0, 0)
    forecast_end_time   = datetime.datetime(2021, 9,  8,  0, 0, 0)
    cases = ['0412_IMERG', '0412_CON6h', '0412_CON6h_DAWN1h', '0412_CON6h_DAWN1hOE1', '0412_CON6h_DAWN1hOE1p5', '0412_CON6h_Aeolus6h', \
             '0412_CON6h_DAWN1h_Aeolus6h', '0412_CON6h_DAWN1hOE1_Aeolus6h', '0412_CON6h_DAWN1hOE1p5_Aeolus6h']
n_time = int((forecast_end_time - forecast_start_time).total_seconds()/3600/6+1)

print(len(cases))

for dom in domains:
    for case in cases:

        dir_case = dir_main + '/' + time + '/' + case
        dir_wrfout = dir_CPEX + '/bkg/' + time + '/' + case
        if 'IMERG' in case: dir_wrfout = dir_CPEX + '/bkg/' + time + '/CON6h'
        filename = dir_case + '/rainfall_6h_' + dom + '.nc'
        os.system('mkdir ' + dir_case)
        print(filename)

        time_now = forecast_start_time

        if 'EOL' in case:

            time_EOL = time_now
            YYMMDD   = time_EOL.strftime('%Y%m%d')
            YYMMDDHH = time_EOL.strftime('%Y%m%d%H')

            dir_EOL  = dir_GOES + '/Data/EOL'
            info     = os.popen('ls ' + dir_EOL + '/' + YYMMDD + '/st4_pr.' + YYMMDDHH + '.06h.grb2').readlines()
            file_EOL = info[0].replace('\n', '')
            print(file_EOL)

            hfile = Nio.open_file(file_EOL)
            lat   = hfile.variables['gridlat_0'][:,:]
            lon   = hfile.variables['gridlon_0'][:,:]
            n_lat = len(lat[:,0])
            n_lon = len(lat[0,:])

        else:

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

            if 'EOL' in case:

                time_EOL = time_now
                YYMMDD   = time_EOL.strftime('%Y%m%d')
                YYMMDDHH = time_EOL.strftime('%Y%m%d%H')

                dir_EOL  = dir_GOES + '/Data/EOL'
                info     = os.popen('ls ' + dir_EOL + '/' + YYMMDD + '/st4_pr.' + YYMMDDHH + '.06h.grb2').readlines()
                file_EOL = info[0].replace('\n', '')
                print(file_EOL)

                hfile    = Nio.open_file(file_EOL)
                EOL_prep = hfile.variables['APCP_P8_L1_GST0_acc'][:,:]/6.0
                EOL_lat  = hfile.variables['gridlat_0'][:,:]
                EOL_lon  = hfile.variables['gridlon_0'][:,:]
                n_lat    = len(EOL_lat[:,0])
                n_lon    = len(EOL_lat[0,:])

                ncfile_output.variables['lat'][:,:]          = EOL_lat
                ncfile_output.variables['lon'][:,:]          = EOL_lon
                ncfile_output.variables['rainfall'][idt,:,:] = EOL_prep

                print(np.nanmax(ncfile_output.variables['rainfall'][idt,:,:]))
                print(np.nanmin(ncfile_output.variables['rainfall'][idt,:,:]))

            elif 'IMERG' in case:

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

                #if time_now == flight_end_time:
                    #cycling_interval = 1
                #else:
                    #cycling_interval = 6
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

                    #if (time_0 <= flight_end_time or time_0 <= anl_end_time) and time_0 >= flight_start_time:
                        #RAINNC_0 = 0.0
                        #RAINC_0  = 0.0
                    if time_0 <= anl_end_time:
                        RAINNC_0 = 0.0
                        RAINC_0  = 0.0

                    rainfall = RAINNC_1 + RAINC_1 - RAINNC_0 - RAINC_0
                    ncfile_output.variables['rainfall'][idt,:,:] = ncfile_output.variables['rainfall'][idt,:,:] + rainfall

                ncfile_output.variables['rainfall'][idt,:,:] = ncfile_output.variables['rainfall'][idt,:,:]/6.0
                print(np.nanmax(ncfile_output.variables['rainfall'][idt,:,:]))
                print(np.nanmin(ncfile_output.variables['rainfall'][idt,:,:]))

        ncfile_output.close()
