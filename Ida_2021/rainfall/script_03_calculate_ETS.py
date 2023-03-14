import os
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from wrf import getvar
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_pdf import PdfPages

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS'
dir_best_track = '/'.join([dir_CPEX, 'track_intensity', 'best_track'])
dir_main = dir_CPEX + '/rainfall'

domains = ['d01']
cycling_interval = 6
n_time = 9
box = 500.0
thresholds = [1.0, 5.0, 10.0, 15.0]

#cases = ['CON6h_082406_Hybrid_C05', 'CON6h_082406_Hybrid_C06', 'CON6h_082406_Hybrid_C07', 'CON6h_082406_Hybrid_C08']
#cases = ['CON6h_Aeolus6h_082406_Hybrid_C05', 'CON6h_Aeolus6h_082406_Hybrid_C06', 'CON6h_Aeolus6h_082406_Hybrid_C07', 'CON6h_Aeolus6h_082406_Hybrid_C08']
#cases = ['CON6h_082412_Hybrid_C05', 'CON6h_082412_Hybrid_C06', 'CON6h_082412_Hybrid_C07', 'CON6h_082412_Hybrid_C08']
#cases = ['CON6h_Aeolus6h_082412_Hybrid_C05', 'CON6h_Aeolus6h_082412_Hybrid_C06', 'CON6h_Aeolus6h_082412_Hybrid_C07', 'CON6h_Aeolus6h_082412_Hybrid_C08']
#cases = ['CON6h_082418_Hybrid_C05', 'CON6h_082418_Hybrid_C06', 'CON6h_082418_Hybrid_C07', 'CON6h_082418_Hybrid_C08']
#cases = ['CON6h_Aeolus6h_082418_Hybrid_C05', 'CON6h_Aeolus6h_082418_Hybrid_C06', 'CON6h_Aeolus6h_082418_Hybrid_C07', 'CON6h_Aeolus6h_082418_Hybrid_C08']
#cases = ['CON6h_082500_Hybrid_C05', 'CON6h_082500_Hybrid_C06', 'CON6h_082500_Hybrid_C07', 'CON6h_082500_Hybrid_C08']
#cases = ['CON6h_Aeolus6h_082500_Hybrid_C05', 'CON6h_Aeolus6h_082500_Hybrid_C06', 'CON6h_Aeolus6h_082500_Hybrid_C07', 'CON6h_Aeolus6h_082500_Hybrid_C08']
#cases = ['CON6h_Aeolus6h_082500_H2_Hybrid_C05', 'CON6h_Aeolus6h_082500_H2_Hybrid_C06', 'CON6h_Aeolus6h_082500_H2_Hybrid_C07', 'CON6h_Aeolus6h_082500_H2_Hybrid_C08']
#cases = ['CON6h_Aeolus6h_082500_V1_Hybrid_C05', 'CON6h_Aeolus6h_082500_V1_Hybrid_C06', 'CON6h_Aeolus6h_082500_V1_Hybrid_C07', 'CON6h_Aeolus6h_082500_V1_Hybrid_C08']
cases = ['CON6h_Aeolus6h_082500_V2_Hybrid_C05', 'CON6h_Aeolus6h_082500_V2_Hybrid_C06', 'CON6h_Aeolus6h_082500_V2_Hybrid_C07', 'CON6h_Aeolus6h_082500_V2_Hybrid_C08']

#forecast_start_time = datetime.datetime(2021, 8, 25, 15, 0, 0)
#forecast_start_time = datetime.datetime(2021, 8, 25, 21, 0, 0)
#forecast_start_time = datetime.datetime(2021, 8, 26,  3, 0, 0)
forecast_start_time = datetime.datetime(2021, 8, 26,  9, 0, 0)
file_best_track = dir_best_track + '/2021_09L_Ida.csv'

for dom in domains:
    for idc, case in enumerate(cases):

        filename1 = dir_main + '/' + case + '/IMERG_6h_' + dom + '.nc'
        filename2 = dir_main + '/' + case + '/rainfall_6h_' + dom + '.nc'

        best_track_name = '_'.join([case, 'd01.csv'])
        file_track1 = file_best_track
        file_track2 = dir_best_track + '/' + best_track_name

        var = 'rainfall'
        ncfile1 = Dataset(filename1)
        rain1 = ncfile1.variables[var][:,:,:]*6.0
        lat1 = ncfile1.variables['lat'][:,:]
        lon1 = ncfile1.variables['lon'][:,:]
        ncfile1.close()

        ncfile2 = Dataset(filename2)
        rain2 = ncfile2.variables[var][:,:,:]*6.0
        lat2 = ncfile2.variables['lat'][:,:]
        lon2 = ncfile2.variables['lon'][:,:]
        ncfile2.close()

        df_track1 = pd.read_csv(file_track1)
        TC_lats1 = list(df_track1['Latitude'][:])
        TC_lons1 = list(df_track1['Longitude'][:])
        TC_dates1 = list(df_track1['Date_Time'][:])
        del df_track1

        df_track2 = pd.read_csv(file_track2)
        TC_lats2 = list(df_track2['Latitude'][:])
        TC_lons2 = list(df_track2['Longitude'][:])
        TC_dates2 = list(df_track2['Date_Time'][:])
        del df_track2

        ETS_df = pd.DataFrame(0.0, index=np.arange(n_time), columns=['Time', 'Box_Size', 'IMERG_Lat', 'IMERG_Lon', 'Simulation_Lat', 'Simulation_Lon', \
                              'ETS_Threshold1', 'ETS_Threshold2', 'ETS_Threshold3', 'ETS_Threshold4', 'ETS1', 'ETS2', 'ETS3', 'ETS4'])

        initial_time = forecast_start_time + datetime.timedelta(hours = idc*cycling_interval)
        for idt in range(n_time):

            time_now = initial_time + datetime.timedelta(hours = idt*cycling_interval)
            time_now_end = time_now + datetime.timedelta(hours = 3.0)
            time_now_str = time_now.strftime('%Y-%m-%d %H:%M:%S')
            ETS_df.loc[idt, 'Time'] = time_now_str
            ETS_df.loc[idt, 'Box_Size'] = box

            for iddate, TC_date in enumerate(TC_dates1):
                TC_datetime = datetime.datetime.strptime(TC_date, '%Y-%m-%d %H:%M:%S')
                if TC_datetime == time_now_end:
                    TC_lat1 = 0.5*(TC_lats1[iddate] + TC_lats1[iddate-1])
                    TC_lon1 = 0.5*(TC_lons1[iddate] + TC_lons1[iddate-1])
            ETS_df.loc[idt, 'IMERG_Lat'] = TC_lat1
            ETS_df.loc[idt, 'IMERG_Lon'] = TC_lon1

            for iddate, TC_date in enumerate(TC_dates2):
                TC_datetime = datetime.datetime.strptime(TC_date, '%Y-%m-%d %H:%M:%S')
                if TC_datetime == time_now_end:
                    TC_lat2 = 0.5*(TC_lats2[iddate] + TC_lats2[iddate-1])
                    TC_lon2 = 0.5*(TC_lons2[iddate] + TC_lons2[iddate-1])
            ETS_df.loc[idt, 'Simulation_Lat'] = TC_lat2
            ETS_df.loc[idt, 'Simulation_Lon'] = TC_lon2

            id_TC_lat1 = np.argmin(np.abs(np.array(lat1[:,0])-TC_lat1))
            id_TC_lon1 = np.argmin(np.abs(np.array(lon1[0,:])-TC_lon1))
            id_TC_lat2 = np.argmin(np.abs(np.array(lat2[:,0])-TC_lat2))
            id_TC_lon2 = np.argmin(np.abs(np.array(lon2[0,:])-TC_lon2))
            TC_rain1 = rain1[idt, id_TC_lat1-42:id_TC_lat1+42, id_TC_lon1-42:id_TC_lon1+42]
            TC_rain2 = rain2[idt, id_TC_lat2-42:id_TC_lat2+42, id_TC_lon2-42:id_TC_lon2+42]

            for idth, thres in enumerate(thresholds):

                Hit         = (TC_rain1 >= thres) & (TC_rain2 >= thres)
                False_Alarm = (TC_rain1  < thres) & (TC_rain2 >= thres)
                Miss        = (TC_rain1 >= thres) & (TC_rain2  < thres)
                Correct_Neg = (TC_rain1  < thres) & (TC_rain2  < thres)

                N_H   = len(TC_rain2[Hit])
                N_FA  = len(TC_rain2[False_Alarm])
                N_M   = len(TC_rain2[Miss])
                N_CN  = len(TC_rain2[Correct_Neg])
                Total = N_H + N_FA + N_M + N_CN

                ref = (N_H + N_FA)*(N_H + N_M)/Total
                ETS_df.loc[idt, 'ETS_Threshold'+str(idth+1)] = thres
                ETS_df.loc[idt, 'ETS'+str(idth+1)] = (N_H - ref)/(N_H + N_FA + N_M - ref)

        ETS_df.to_csv(dir_main + '/' + case + '/ETS_' + dom + '.csv', index=False)
