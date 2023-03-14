import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from wrf import getvar
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_pdf import PdfPages

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021'
dir_best_track = '/'.join([dir_CPEX, 'track_intensity', 'best_track'])
dir_main = dir_CPEX + '/rainfall'

time = '20210824'
domains = ['d01']
cycling_interval = 6

if '20210820' in time:
    forecast_start_time = datetime.datetime(2021, 8, 21,  3, 0, 0)
    forecast_end_time   = datetime.datetime(2021, 8, 22,  3, 0, 0)
    if_AEW = True
    idx_AEW = 9
    file_track = dir_CPEX + '/AEW/20210820/GFS/20210820.csv'
    cases = ['IMERG', 'CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_DAWN1hOE1p5', 'CON6h_HALO1h', 'CON6h_HALO1hOE0p2', \
             'CON6h_DS1h', 'CON6h_DS1h_UV', 'CON6h_DS1h_T', 'CON6h_DS1h_Q', 'CON6h_Aeolus6h', 'CON6h_DAWN1h_HALO1h_DS1h', 'CON6h_DAWN1h_HALO1h_DS1h_Aeolus6h', \
             'CTRL', 'MP01', 'MP02', 'MP08', 'MP10', 'MP16', 'MP26', 'BL02', 'BL04', 'BL06', 'BL07', \
             'CU02', 'CU11', 'CU14', 'CU16', 'RA03', 'RA04', 'RA05', 'RA14']
    labels = ['IMERG', 'CON', 'DAWN', 'DAWNOE1', 'DAWNOE1p5', 'HALO', 'HALOOE0p2', \
              'DS', 'DS_UV', 'DS_T', 'DS_Q', 'Aeolus', 'HRFD', 'HRFD_Aeolus', \
              'CTRL', 'Kessler', 'Purdue Lin', 'Thompson', 'Morrison 2-Moment', 'WDM6', 'WDM7', 'MYJ', 'QNSE', 'MYNN', 'ACM2', \
              'BMJ', 'Multi-Scale KF', 'NewSAS', 'New Tiedtke', 'CAM', 'RRTMG', 'New Goddard', 'RRTMG-K']
if '20210821' in time:
    forecast_start_time = datetime.datetime(2021, 8, 22,  3, 0, 0)
    forecast_end_time   = datetime.datetime(2021, 8, 23,  3, 0, 0)
    if_AEW = True
    idx_AEW = 9
    file_track = dir_CPEX + '/AEW/20210821/GFS/20210821.csv'
    cases = ['IMERG', 'CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_DAWN1hOE1p5', 'CON6h_HALO1h', \
             'CON6h_DS1h', 'CON6h_DS1h_UV', 'CON6h_DS1h_T', 'CON6h_DS1h_Q', 'CON6h_Aeolus6h', 'CON6h_DAWN1h_HALO1h_DS1h', 'CON6h_DAWN1h_HALO1h_DS1h_Aeolus6h']
    labels = ['IMERG', 'CON', 'DAWN', 'DAWNOE1', 'DAWNOE1p5', 'HALO', \
              'DS', 'DS_UV', 'DS_T', 'DS_Q', 'Aeolus', 'HRFD', 'HRFD_Aeolus']
if '20210824' in time:
    #forecast_start_time = datetime.datetime(2021, 8, 25, 15, 0, 0)
    #forecast_end_time   = datetime.datetime(2021, 8, 27,  9, 0, 0)
    #forecast_start_time = datetime.datetime(2021, 8, 24, 15, 0, 0)
    #forecast_end_time   = datetime.datetime(2021, 8, 27,  9, 0, 0)
    #forecast_start_time = datetime.datetime(2021, 8, 25,  3, 0, 0)
    #forecast_end_time   = datetime.datetime(2021, 8, 28,  9, 0, 0)
    forecast_start_time = datetime.datetime(2021, 8, 25, 15, 0, 0)
    forecast_end_time   = datetime.datetime(2021, 8, 28,  9, 0, 0)
    if_AEW = False
    file_best_track = dir_best_track + '/2021_09L_Ida.csv'
    #cases = ['IMERG', 'CON6h', 'CON6h_Aeolus6h', 'CON6h_DS1h', 'CON6h_DS1h_Q', 'CON6h_DS1h_T', 'CON6h_DS1h_UV', \
             #'CON6h_082500', 'CON6h_Aeolus6h_082500', 'CON6h_DS1h_082500', 'CON6h_DS1h_Q_082500', 'CON6h_DS1h_T_082500', 'CON6h_DS1h_UV_082500', \
             #'CON6h_082512', 'CON6h_Aeolus6h_082512', 'CON6h_DS1h_082512', 'CON6h_DS1h_Q_082512', 'CON6h_DS1h_T_082512', 'CON6h_DS1h_UV_082512']
    #labels = ['IMERG', 'CON', 'Aeolus', 'DS', 'DS_Q', 'DS_T', 'DS_UV', \
              #'CON_082500', 'Aeolus_082500', 'DS_082500', 'DS_Q_082500', 'DS_T_082500', 'DS_UV_082500', \
              #'CON_082512', 'Aeolus_082512', 'DS_082512', 'DS_Q_082512', 'DS_T_082512', 'DS_UV_082512']
    #cases = ['IMERG', \
             #'CON6h_082500', 'CON6h_Aeolus6h_082500', 'CON6h_DS1h_082500', 'CON6h_DS1h_Q_082500', 'CON6h_DS1h_T_082500', 'CON6h_DS1h_UV_082500', \
             #'CON6h_082512', 'CON6h_Aeolus6h_082512', 'CON6h_DS1h_082512', 'CON6h_DS1h_Q_082512', 'CON6h_DS1h_T_082512', 'CON6h_DS1h_UV_082512']
    #labels = ['IMERG', \
              #'CON_082500', 'Aeolus_082500', 'DS_082500', 'DS_Q_082500', 'DS_T_082500', 'DS_UV_082500', \
              #'CON_082512', 'Aeolus_082512', 'DS_082512', 'DS_Q_082512', 'DS_T_082512', 'DS_UV_082512']
    #cases = ['CON6h_Hybrid_082500', 'CON6h_Aeolus6h_Hybrid_082500', \
             #'CON6h_Hybrid_082512', 'CON6h_Aeolus6h_Hybrid_082512']
    #labels = ['CON_Hybrid_082500', 'Aeolus_Hybrid_082500', \
              #'CON_Hybrid_082512', 'Aeolus_Hybrid_082512']
    #cases = ['CON6h_No1h_Hybrid_082412', 'CON6h_Aeolus6h_No1h_Hybrid_082412']
    #labels = ['CON_Hybrid_082412', 'Aeolus_Hybrid_082412']
    #cases = ['CON6h_No1h_Hybrid_082512', 'CON6h_Aeolus6h_No1h_Hybrid_082512']
    #labels = ['CON_Hybrid_082512', 'Aeolus_Hybrid_082512']
    #cases = ['CON6h_Hybrid_082500', 'CON6h_Aeolus6h_Hybrid_082500', 'CON6h_DS1h_Hybrid_082500', 'CON6h_DS1h_UV_Hybrid_082500', 'CON6h_DS1h_T_Hybrid_082500', 'CON6h_DS1h_Q_Hybrid_082500']
    #labels = ['CON_Hybrid_082500', 'Aeolus_Hybrid_082500', 'DS_Hybrid_082500', 'DS_UV_Hybrid_082500', 'DS_T_Hybrid_082500', 'DS_Q_Hybrid_082500']
    cases = ['CON6h_Hybrid_082512', 'CON6h_Aeolus6h_Hybrid_082512', 'CON6h_DS1h_Hybrid_082512', 'CON6h_DS1h_UV_Hybrid_082512', 'CON6h_DS1h_T_Hybrid_082512', 'CON6h_DS1h_Q_Hybrid_082512']
    labels = ['CON_Hybrid_082512', 'Aeolus_Hybrid_082512', 'DS_Hybrid_082512', 'DS_UV_Hybrid_082512', 'DS_T_Hybrid_082512', 'DS_Q_Hybrid_082512']
if '20210828' in time:
    forecast_start_time = datetime.datetime(2021, 8, 29,  3, 0, 0)
    forecast_end_time   = datetime.datetime(2021, 8, 30, 21, 0, 0)
    if_AEW = False
    file_best_track = dir_best_track + '/2021_10L_Kate.csv'
    cases = ['IMERG', 'CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_DAWN1hOE1p5', 'CON6h_HALO1h', 'CON6h_HALO1hOE0p2', \
             'CON6h_DS1h', 'CON6h_DS1h_UV', 'CON6h_DS1h_T', 'CON6h_DS1h_Q', 'CON6h_Aeolus6h', 'CON6h_DAWN1h_HALO1h_DS1h', 'CON6h_DAWN1h_HALO1h_DS1h_Aeolus6h']
    labels = ['IMERG', 'CON', 'DAWN', 'DAWNOE1', 'DAWNOE1p5', 'HALO', 'HALOOE0p2', \
              'DS', 'DS_UV', 'DS_T', 'DS_Q', 'Aeolus', 'HRFD', 'HRFD_Aeolus']
if '20210904' in time:
    forecast_start_time = datetime.datetime(2021, 9,  5,  3, 0, 0)
    forecast_end_time   = datetime.datetime(2021, 9,  6, 21, 0, 0)
    if_AEW = False
    file_best_track = dir_best_track + '/2021_12L_Larry.csv'
    cases = ['IMERG', 'CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_DAWN1hOE1p5', 'CON6h_HALO1h', 'CON6h_HALO1hOE0p2', \
             'CON6h_DS1h', 'CON6h_DS1h_UV', 'CON6h_DS1h_T', 'CON6h_DS1h_Q', 'CON6h_Aeolus6h']
    labels = ['IMERG', 'CON', 'DAWN', 'DAWNOE1', 'DAWNOE1p5', 'HALO', 'HALOOE0p2', \
              'DS', 'DS_UV', 'DS_T', 'DS_Q', 'Aeolus']

rain_levels = [0.6, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0]
rain_labels = ['0.6', '1', '1.5', '2', '3', '4', '5', '6', '8', '10', '15', '20', '25', '30', '35', '40']
n_time = int((forecast_end_time - forecast_start_time).total_seconds()/3600/6+1)
print(len(cases))
print(len(labels))

#Read AEW track
if if_AEW:
    df = pd.read_csv(file_track)
    AEW_Date_Times = df['Date_Time']
    AEW_lats = df['Latitude']
    AEW_lons = df['Longitude']
    print(AEW_Date_Times[9])
    del df

for dom in domains:
    for idc, case in enumerate(cases):

        var = 'rainfall'
        filename = dir_main + '/' + time + '/' + case + '/rainfall_6h_' + dom + '.nc'
        ncfile   = Dataset(filename)
        rain     = ncfile.variables[var][:,:,:]*6.0
        rain_lat = ncfile.variables['lat'][:,:]
        rain_lon = ncfile.variables['lon'][:,:]
        ncfile.close()

        if not if_AEW:
            if 'IMERG' in case or 'EOL' in case:
                file_track = file_best_track
            else:
                best_track_name = '_'.join([time, case, 'd01.csv'])
                file_track = dir_best_track + '/' + best_track_name
            df = pd.read_csv(file_track)
            TC_lats = list(df['Latitude'][:])
            TC_lons = list(df['Longitude'][:])
            TC_dates = list(df['Date_Time'][:])
            del df

        for idt in range(n_time):

            label = labels[idc]
            time_now = forecast_start_time + datetime.timedelta(hours = idt*cycling_interval)
            time_now_str = time_now.strftime('%Y%m%d%H')
            pdfname = '_'.join([time_now_str, 'rainfall', case, dom+'.pdf'])
            pdfname = dir_main + '/' + time + '/figures/' + pdfname
            print(pdfname)

            with PdfPages(pdfname) as pdf:

                fig, axs = plt.subplots(1, 1, figsize=(6.0, 6.25))
                fig.subplots_adjust(left=0.075, bottom=-0.040, right=0.975, top=0.980, wspace=0.100, hspace=0.100)

                if if_AEW:
                    (AEW_lon, AEW_lat) = ((AEW_lons[idx_AEW+idt] + AEW_lons[idx_AEW+idt-1])/2, (AEW_lats[idx_AEW+idt] + AEW_lats[idx_AEW+idt-1])/2)
                    extent = [AEW_lon-5.0, AEW_lon+5.0, AEW_lat-5.0, AEW_lat+5.0]
                else:
                    time_now_end = time_now + datetime.timedelta(hours = 3.0)
                    for id_TC, TC_date in enumerate(TC_dates):
                        TC_datetime = datetime.datetime.strptime(TC_date, '%Y-%m-%d %H:%M:%S')
                        if TC_datetime == time_now_end:
                            TC_lat = 0.5*(TC_lats[id_TC] + TC_lats[id_TC-1])
                            TC_lon = 0.5*(TC_lons[id_TC] + TC_lons[id_TC-1])
                            extent = [TC_lon-5.0, TC_lon+5.0, TC_lat-5.0, TC_lat+5.0]

                ax = axs
                m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                m.drawparallels(np.arange(-10,  36, 5), labels=[1,0,0,0], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)
                m.drawmeridians(np.arange(-95, -29, 5), labels=[0,0,0,1], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)

                rain[rain<=0] = 0
                rain_lon, rain_lat = m(rain_lon, rain_lat, inverse=False)
                pcm = ax.contourf(rain_lon, rain_lat, rain[idt,:,:], locator=ticker.LogLocator(), levels=rain_levels, cmap='jet', extend='max', zorder=1)
                if if_AEW:
                    ax.plot(AEW_lon, AEW_lat, 'x', color='k', markersize=7.5, markeredgewidth=1.0)
                else:
                    ax.plot(TC_lon, TC_lat, 'x', color='k', markersize=7.5, markeredgewidth=1.0)

                clb = fig.colorbar(pcm, ax=axs, orientation='horizontal', pad=0.035, aspect=50, shrink=1.00)
                clb.set_label('6-hr Accumulated Precipitation (mm) of ' + label, fontsize=10.0, labelpad=4.0)
                clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
                clb.ax.minorticks_off()
                clb.set_ticks(rain_levels)
                clb.set_ticklabels(rain_labels)

                pdf.savefig(fig)
                plt.cla()
                plt.clf()
                plt.close()
