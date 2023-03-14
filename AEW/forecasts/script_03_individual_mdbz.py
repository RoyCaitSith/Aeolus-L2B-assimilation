import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from wrf import getvar
from netCDF4 import Dataset
from cpt_convert import loadCPT
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_pdf import PdfPages

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021'
dir_best_track = '/'.join([dir_CPEX, 'track_intensity', 'best_track'])
dir_main = dir_CPEX + '/forecasts'

time = '20210824'
domains = ['d01']

if '20210820' in time:
    draw_times = [datetime.datetime(2021, 8, 21,  2, 0, 0), datetime.datetime(2021, 8, 21, 16, 0, 0), datetime.datetime(2021, 8, 22,  3, 0, 0)]
    if_AEW = True
    AEW_locations = [(-71.81, 14.95), (-77.03, 16.72), (-81.235, 17.74)]
    cases = ['CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_DAWN1hOE1p5', 'CON6h_HALO1h', 'CON6h_HALO1hOE0p2', \
             'CON6h_DS1h', 'CON6h_DS1h_UV', 'CON6h_DS1h_T', 'CON6h_DS1h_Q', 'CON6h_Aeolus6h', 'CON6h_DAWN1h_HALO1h_DS1h', 'CON6h_DAWN1h_HALO1h_DS1h_Aeolus6h', \
             'CTRL', 'MP01', 'MP02', 'MP08', 'MP10', 'MP16', 'MP26', 'BL02', 'BL04', 'BL06', 'BL07', \
             'CU02', 'CU11', 'CU14', 'CU16', 'RA03', 'RA04', 'RA05', 'RA14']
    labels = ['CON', 'DAWN', 'DAWNOE1', 'DAWNOE1p5', 'HALO', 'HALOOE0p2', \
              'DS', 'DS_UV', 'DS_T', 'DS_Q', 'Aeolus', 'HRFD', 'HRFD_Aeolus', \
              'CTRL', 'Kessler', 'Purdue Lin', 'Thompson', 'Morrison 2-Moment', 'WDM6', 'WDM7', 'MYJ', 'QNSE', 'MYNN', 'ACM2', \
              'BMJ', 'Multi-Scale KF', 'NewSAS', 'New Tiedtke', 'CAM', 'RRTMG', 'New Goddard', 'RRTMG-K']
if '20210821' in time:
    draw_times = [datetime.datetime(2021, 8, 22,  1, 0, 0), datetime.datetime(2021, 8, 22, 15, 0, 0), \
                  datetime.datetime(2021, 8, 23,  0, 0, 0), datetime.datetime(2021, 8, 23,  2, 0, 0)]
    if_AEW = True
    AEW_locations = [(-50.42, 12.26), (-53.93, 12.34), (-56.97, 12.39), (-57.85, 12.35)]
    cases = ['CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_DAWN1hOE1p5', 'CON6h_HALO1h', \
             'CON6h_DS1h', 'CON6h_DS1h_UV', 'CON6h_DS1h_T', 'CON6h_DS1h_Q', 'CON6h_Aeolus6h', 'CON6h_DAWN1h_HALO1h_DS1h', 'CON6h_DAWN1h_HALO1h_DS1h_Aeolus6h']
    labels = ['CON', 'DAWN', 'DAWNOE1', 'DAWNOE1p5', 'HALO', \
              'DS', 'DS_UV', 'DS_T', 'DS_Q', 'Aeolus', 'HRFD', 'HRFD_Aeolus']
if '20210824' in time:
    draw_times = [datetime.datetime(2021, 8, 25,  0, 0, 0), datetime.datetime(2021, 8, 25, 12, 0, 0), datetime.datetime(2021, 8, 25, 18, 0, 0), \
                  datetime.datetime(2021, 8, 26,  0, 0, 0), datetime.datetime(2021, 8, 26, 12, 0, 0), datetime.datetime(2021, 8, 27,  0, 0, 0), \
                  datetime.datetime(2021, 8, 27, 18, 0, 0), datetime.datetime(2021, 8, 28,  0, 0, 0), datetime.datetime(2021, 8, 28, 12, 0, 0)]
    #draw_times = [datetime.datetime(2021, 8, 24, 18, 0, 0), datetime.datetime(2021, 8, 25,  0, 0, 0), datetime.datetime(2021, 8, 25, 12, 0, 0), \
                  #datetime.datetime(2021, 8, 25, 18, 0, 0), datetime.datetime(2021, 8, 26,  0, 0, 0), datetime.datetime(2021, 8, 26, 12, 0, 0)]
    #draw_times = [datetime.datetime(2021, 8, 26,  0, 0, 0), datetime.datetime(2021, 8, 26, 12, 0, 0), datetime.datetime(2021, 8, 27,  0, 0, 0)]
    #draw_times = [datetime.datetime(2021, 8, 24, 18, 0, 0)]
    if_AEW = False
    #cases = ['CON6h_082500', 'CON6h_Aeolus6h_082500', 'CON6h_DS1h_082500', 'CON6h_DS1h_Q_082500', 'CON6h_DS1h_T_082500', 'CON6h_DS1h_UV_082500', 'CON6h_Hybrid_082500', 'CON6h_Aeolus6h_Hybrid_082500', \
             #'CON6h_082512', 'CON6h_Aeolus6h_082512', 'CON6h_DS1h_082512', 'CON6h_DS1h_Q_082512', 'CON6h_DS1h_T_082512', 'CON6h_DS1h_UV_082512', 'CON6h_Hybrid_082512', 'CON6h_Aeolus6h_Hybrid_082512']
    #labels = ['CON_082500', 'Aeolus_082500', 'DS_082500', 'DS_Q_082500', 'DS_T_082500', 'DS_UV_082500', 'CON_Hybrid_082500', 'Aeolus_Hybrid_082500', \
              #'CON_082512', 'Aeolus_082512', 'DS_082512', 'DS_Q_082512', 'DS_T_082512', 'DS_UV_082512', 'CON_Hybrid_082512', 'Aeolus_Hybrid_082512']
    #cases = ['CON6h_No1h_Hybrid_082412', 'CON6h_Aeolus6h_No1h_Hybrid_082412']
    #labels = ['CON_Hybrid_082412', 'Aeolus_Hybrid_082412']
    #cases = ['CON6h_No1h_Hybrid_082512', 'CON6h_Aeolus6h_No1h_Hybrid_082512']
    #labels = ['CON_Hybrid_082512', 'Aeolus_Hybrid_082512']
    #cases = ['CON6h_Hybrid_082500', 'CON6h_Aeolus6h_Hybrid_082500', 'CON6h_DS1h_Hybrid_082500', 'CON6h_DS1h_UV_Hybrid_082500', 'CON6h_DS1h_T_Hybrid_082500', 'CON6h_DS1h_Q_Hybrid_082500']
    #labels = ['CON_Hybrid_082500', 'Aeolus_Hybrid_082500', 'DS_Hybrid_082500', 'DS_UV_Hybrid_082500', 'DS_T_Hybrid_082500', 'DS_Q_Hybrid_082500']
    cases = ['CON6h_Hybrid_082512', 'CON6h_Aeolus6h_Hybrid_082512', 'CON6h_DS1h_Hybrid_082512', 'CON6h_DS1h_UV_Hybrid_082512', 'CON6h_DS1h_T_Hybrid_082512', 'CON6h_DS1h_Q_Hybrid_082512']
    labels = ['CON_Hybrid_082512', 'Aeolus_Hybrid_082512', 'DS_Hybrid_082512', 'DS_UV_Hybrid_082512', 'DS_T_Hybrid_082512', 'DS_Q_Hybrid_082512']
if '20210828' in time:
    draw_times = [datetime.datetime(2021, 8, 29,  0, 0, 0), datetime.datetime(2021, 8, 29, 12, 0, 0), datetime.datetime(2021, 8, 30,  0, 0, 0), \
                  datetime.datetime(2021, 8, 30, 12, 0, 0), datetime.datetime(2021, 8, 31,  0, 0, 0)]
    if_AEW = False
    cases = ['CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_DAWN1hOE1p5', 'CON6h_HALO1h', 'CON6h_HALO1hOE0p2', \
             'CON6h_DS1h', 'CON6h_DS1h_UV', 'CON6h_DS1h_T', 'CON6h_DS1h_Q', 'CON6h_Aeolus6h', 'CON6h_DAWN1h_HALO1h_DS1h', 'CON6h_DAWN1h_HALO1h_DS1h_Aeolus6h']
    labels = ['CON', 'DAWN', 'DAWNOE1', 'DAWNOE1p5', 'HALO', 'HALOOE0p2', \
              'DS', 'DS_UV', 'DS_T', 'DS_Q', 'Aeolus', 'HRFD', 'HRFD_Aeolus']
if '20210904' in time:
    draw_times = [datetime.datetime(2021, 9,  5,  0, 0, 0), datetime.datetime(2021, 9,  5, 12, 0, 0), datetime.datetime(2021, 9,  5, 18, 0, 0), \
                  datetime.datetime(2021, 9,  6, 12, 0, 0), datetime.datetime(2021, 9,  7,  0, 0, 0)]
    if_AEW = False
    cases = ['CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_DAWN1hOE1p5', 'CON6h_HALO1h', 'CON6h_HALO1hOE0p2', \
             'CON6h_DS1h', 'CON6h_DS1h_UV', 'CON6h_DS1h_T', 'CON6h_DS1h_Q', 'CON6h_Aeolus6h']
    labels = ['CON', 'DAWN', 'DAWNOE1', 'DAWNOE1p5', 'HALO', 'HALOOE0p2', \
              'DS', 'DS_UV', 'DS_T', 'DS_Q', 'Aeolus']

cpt = loadCPT('./colormaps/PU_Rain_rate.rgb')
cpt_convert = LinearSegmentedColormap('cpt', cpt)
levs = np.array([-5, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70])

for dom in domains:
    for idc, case in enumerate(cases):

        if not if_AEW:
            best_track_name = '_'.join([time, case, 'd01.csv'])
            file_best_track = dir_best_track + '/' + best_track_name
            df = pd.read_csv(file_best_track)
            TC_lats = list(df['Latitude'][:])
            TC_lons = list(df['Longitude'][:])
            TC_dates = list(df['Date_Time'][:])
            del df

        for idt, time_now in enumerate(draw_times):

            label = labels[idc]
            time_now_str = time_now.strftime('%Y%m%d%H')
            pdfname = '_'.join([time_now_str, 'mdbz', case, dom+'.pdf'])
            pdfname = dir_main + '/' + time + '/mdbz/' + pdfname
            print(pdfname)

            with PdfPages(pdfname) as pdf:

                fig, axs = plt.subplots(1, 1, figsize=(6.0, 6.25))
                fig.subplots_adjust(left=0.075, bottom=-0.040, right=0.975, top=0.980, wspace=0.100, hspace=0.100)

                dir_wrfout = dir_CPEX + '/bkg/' + time + '/' + case
                file_wrf = dir_wrfout + '/wrfout_' + dom + '_' + time_now.strftime('%Y-%m-%d_%H:00:00')
                print(file_wrf)

                ncfile = Dataset(file_wrf)
                lat = ncfile.variables['XLAT'][0,:,:]
                lon = ncfile.variables['XLONG'][0,:,:]
                mdbz = getvar(ncfile, 'mdbz')
                slp = getvar(ncfile, 'slp', units='hPa')
                (u10, v10) = getvar(ncfile, 'uvmet10', units='kt')
                ncfile.close()

                if if_AEW:
                    (AEW_lon, AEW_lat) = AEW_locations[idt]
                    extent = [AEW_lon-5.0, AEW_lon+5.0, AEW_lat-5.0, AEW_lat+5.0]
                else:
                    for id_TC, TC_date in enumerate(TC_dates):
                        TC_datetime = datetime.datetime.strptime(TC_date, '%Y-%m-%d %H:%M:%S')
                        if TC_datetime == time_now:
                            TC_lat = TC_lats[id_TC]
                            TC_lon = TC_lons[id_TC]
                            extent = [TC_lon-5.0, TC_lon+5.0, TC_lat-5.0, TC_lat+5.0]

                ax = axs
                m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                m.drawparallels(np.arange(-10,  36, 5), labels=[1,0,0,0], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)
                m.drawmeridians(np.arange(-95, -29, 5), labels=[0,0,0,1], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)

                pcm = ax.contourf(lon, lat, mdbz, levels=levs, cmap=cpt_convert, extend='max', zorder=1)
                if if_AEW:
                    ax.plot(AEW_lon, AEW_lat, 'x', color='k', markersize=7.5, markeredgewidth=1.0)
                else:
                    ax.plot(TC_lon, TC_lat, 'x', color='k', markersize=7.5, markeredgewidth=1.0)

                clb = fig.colorbar(pcm, ax=axs, ticks=levs, orientation='horizontal', pad=0.035, aspect=50, shrink=1.00)
                clb.set_label('MdBZ of ' + label, fontsize=10.0, labelpad=4.0)
                clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

                pdf.savefig(fig)
                plt.cla()
                plt.clf()
                plt.close()
