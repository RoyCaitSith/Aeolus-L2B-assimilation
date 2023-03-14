import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import re
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.basemap import Basemap

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN'
dir_main = dir_CPEX + '/08_CPEX_AW_2021/track_intensity'
dir_best_track = dir_main + '/best_track'

time = '20210824'
domain = 'd01'

#cases = ['CON6h_082500', 'CON6h_Aeolus6h_082500']
#labels = ['CON_082500', 'Aeolus_082500']
#cases = ['CON6h_Hybrid_082500', 'CON6h_Aeolus6h_Hybrid_082500', 'CON6h_Aeolus6h_L2B_Hybrid_082500']
#labels = ['CON_Hybrid_082500', 'Aeolus_Hybrid_082500', 'Aeolus_L2B_Hybrid_082500']
#cases = ['CON6h_082512', 'CON6h_Aeolus6h_082512']
#labels = ['CON_082512', 'Aeolus_082512']
#cases = ['CON6h_Hybrid_082512', 'CON6h_Aeolus6h_Hybrid_082512', 'CON6h_Aeolus6h_L2B_Hybrid_082512']
#labels = ['CON_Hybrid_082512', 'Aeolus_Hybrid_082512', 'Aeolus_L2B_Hybrid_082512']
cases = ['CON6h_Hybrid_082500', 'CON6h_Aeolus6h_Hybrid_082500', 'CON6h_Hybrid_082512', 'CON6h_Aeolus6h_Hybrid_082512']
labels = ['CON_Hybrid_082500', 'Aeolus_Hybrid_082500', 'CON_Hybrid_082512', 'Aeolus_Hybrid_082512']
#cases = ['CON6h_No1h_Hybrid_082412', 'CON6h_Aeolus6h_No1h_Hybrid_082412']
#labels = ['CON_Hybrid_082412', 'Aeolus_Hybrid_082412']
#cases = ['CON6h_No1h_Hybrid_082512', 'CON6h_Aeolus6h_No1h_Hybrid_082512']
#labels = ['CON_Hybrid_082512', 'Aeolus_Hybrid_082512']
#cases = ['CON6h_082500', 'CON6h_082512', 'CON6h_Aeolus6h_082500', 'CON6h_Aeolus6h_082512']
#labels = ['CON_082500', 'CON_082512', 'Aeolus_082500', 'Aeolus_082512']
#cases = ['CON6h_Hybrid_082500', 'CON6h_DS1h_Hybrid_082500', 'CON6h_DS1h_UV_Hybrid_082500', 'CON6h_DS1h_T_Hybrid_082500', 'CON6h_DS1h_Q_Hybrid_082500']
#labels = ['CON_Hybrid_082500', 'DS_Hybrid_082500', 'DS_UV_Hybrid_082500', 'DS_T_Hybrid_082500', 'DS_Q_Hybrid_082500']
#cases = ['CON6h_Hybrid_082512', 'CON6h_DS1h_Hybrid_082512', 'CON6h_DS1h_UV_Hybrid_082512', 'CON6h_DS1h_T_Hybrid_082512', 'CON6h_DS1h_Q_Hybrid_082512']
#labels = ['CON_Hybrid_082512', 'DS_Hybrid_082512', 'DS_UV_Hybrid_082512', 'DS_T_Hybrid_082512', 'DS_Q_Hybrid_082512']
#cases = ['CON6h', 'CON6h_Aeolus6h']
#labels = ['CON', 'Aeolus']
#cases = ['CON6h', 'CON6h_DS1h', 'CON6h_DS1h_UV', 'CON6h_DS1h_T', 'CON6h_DS1h_Q']
#labels = ['CON', 'DS', 'DS_UV', 'DS_T', 'DS_Q']
#cases = ['CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_DAWN1hOE1p5']
#labels = ['CON', 'DAWN', 'DAWN1hOE1', 'DAWN1hOE1p5']
#cases = ['CON6h', 'CON6h_HALO1h', 'CON6h_HALO1hOE0p2']
#labels = ['CON', 'HALO', 'HALO1hOE0p2']
#cases = ['CON6h', 'CON6h_DAWN1h_HALO1h_DS1h', 'CON6h_DAWN1h_HALO1h_DS1h_Aeolus6h']
#labels = ['CON', 'HRFD', 'HRFD_Aeolus']
#cases = ['CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_DAWN1hOE1p5', 'CON6h_Aeolus6h', 'CON6h_DAWN1h_Aeolus6h', 'CON6h_DAWN1hOE1_Aeolus6h', 'CON6h_DAWN1hOE1p5_Aeolus6h']
#labels = ['CON', 'DAWN', 'DAWNOE1', 'DAWNOE1p5', 'Aeolus', 'DAWN_Aeolus', 'DAWNOE1_Aeolus', 'DAWNOE1p5_Aeolus']
#cases = ['2021090412_CON6h', '2021090412_CON6h_DAWN1h', '2021090412_CON6h_DAWN1hOE1', '2021090412_CON6h_DAWN1hOE1p5', '2021090412_CON6h_Aeolus6h', \
         #'2021090412_CON6h_DAWN1h_Aeolus6h', '2021090412_CON6h_DAWN1hOE1_Aeolus6h', '2021090412_CON6h_DAWN1hOE1p5_Aeolus6h']
#labels = ['0412_CON', '0412_DAWN', '0412_DAWNOE1', '0412_DAWNOE1p5', '0412_Aeolus', '0412_DAWN_Aeolus', '0412_DAWNOE1_Aeolus', '0412_DAWNOE1p5_Aeolus']
#cases = ['CON6h',  'CON6h_Aeolus6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_DAWN1h_Aeolus6h', 'CON6h_DAWN1hOE1_Aeolus6h']
#labels = ['CON', 'Aeolus', 'DAWN', 'DAWNOE1', 'DAWN_Aeolus', 'DAWNOE1_Aeolus']
#cases = ['2021090412_CON6h', '2021090412_CON6h_Aeolus6h', '2021090412_CON6h_DAWN1h', '2021090412_CON6h_DAWN1hOE1', \
         #'2021090412_CON6h_DAWN1h_Aeolus6h', '2021090412_CON6h_DAWN1hOE1_Aeolus6h']
#labels = ['CON_090518', 'Aeolus_090518', 'DAWN_090518', 'DAWNOE1_090518', 'DAWN_Aeolus_090518', 'DAWNOE1_Aeolus_090518']

#pdfname = dir_main + '/' + time + '/figures/' + time + '_track_' + domain + '.pdf'
#pdfname = dir_main + '/' + time + '/figures/Aeolus_082500_track.pdf'
#pdfname = dir_main + '/' + time + '/figures/Aeolus_082512_track.pdf'
pdfname = dir_main + '/' + time + '/figures/Aeolus_Hybrid_track.pdf'
#pdfname = dir_main + '/' + time + '/figures/Aeolus_No1h_082412_track.pdf'
#pdfname = dir_main + '/' + time + '/figures/Aeolus_No1h_082512_track.pdf'
#pdfname = dir_main + '/' + time + '/figures/DS_Hybrid_082500_track.pdf'
#pdfname = dir_main + '/' + time + '/figures/DS_Hybrid_082512_track.pdf'
#pdfname = dir_main + '/' + time + '/figures/Aeolus_track.pdf'
#pdfname = dir_main + '/' + time + '/figures/DS_track.pdf'
#pdfname = dir_main + '/' + time + '/figures/DAWN_track.pdf'
#pdfname = dir_main + '/' + time + '/figures/HALO_track.pdf'
#pdfname = dir_main + '/' + time + '/figures/HRFD_track.pdf'
#pdfname = dir_main + '/' + time + '/figures/DAWN_Aeolus_track.pdf'
#pdfname = dir_main + '/' + time + '/figures/0412_DAWN_Aeolus_track.pdf'

if '20210824' in time:
    file_best_track = dir_best_track + '/2021_09L_Ida.csv'
    forecast_start_time = datetime.datetime(2021, 8, 24,  6, 0, 0)
    forecast_end_time   = datetime.datetime(2021, 8, 28, 12, 0, 0)
    #forecast_start_time = datetime.datetime(2021, 8, 25,  0, 0, 0)
    #forecast_end_time   = datetime.datetime(2021, 8, 28, 12, 0, 0)
    #forecast_start_time = datetime.datetime(2021, 8, 25, 12, 0, 0)
    #forecast_end_time   = datetime.datetime(2021, 8, 28, 12, 0, 0)
    #forecast_start_time = datetime.datetime(2021, 8, 24,  6, 0, 0)
    #forecast_end_time   = datetime.datetime(2021, 8, 26, 12, 0, 0)
    #forecast_start_time = datetime.datetime(2021, 8, 24,  6, 0, 0)
    #forecast_end_time   = datetime.datetime(2021, 8, 27, 12, 0, 0)
    extent = [-95.0, -50.0, 5.0, 30.0]
if '20210828' in time:
    file_best_track = dir_best_track + '/2021_10L_Kate.csv'
    forecast_start_time = datetime.datetime(2021, 8, 28, 12, 0, 0)
    forecast_end_time   = datetime.datetime(2021, 8, 31,  0, 0, 0)
    extent = [-65.0, -45.0, 12.5, 27.5]
if '20210904' in time:
    file_best_track = dir_best_track + '/2021_12L_Larry.csv'
    forecast_start_time = datetime.datetime(2021, 9,  5,  0, 0, 0)
    forecast_end_time   = datetime.datetime(2021, 9,  7,  0, 0, 0)
    #forecast_start_time = datetime.datetime(2021, 9,  5, 18, 0, 0)
    #forecast_end_time   = datetime.datetime(2021, 9,  7, 18, 0, 0)
    extent = [-60.0, -45.0, 15.0, 30.0]

sns_cmap = sns.color_palette('bright')
colors = [sns_cmap[0], sns_cmap[1], sns_cmap[2], sns_cmap[3], sns_cmap[4], sns_cmap[5], sns_cmap[6], sns_cmap[7]]

with PdfPages(pdfname) as pdf:

    fig = plt.figure(1, [4.0, 4.0])
    fig.subplots_adjust(left=0.100, bottom=0.050, right=0.950, top=0.980, wspace=0.000, hspace=0.000)

    #Read Best Track
    df = pd.read_csv(file_best_track)
    #print(df)

    index = []
    for idx, Date_Time in enumerate(df['Date_Time']):
        time_now = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
        if time_now >= forecast_start_time and time_now <= forecast_end_time: index = index + [idx]

    lat = list(df['Latitude'][index])
    lon = list(df['Longitude'][index])
    idx_forecast_start_time = int((24-float(forecast_start_time.strftime('%H')))%24/6)

    # Draw best track
    ax = fig.add_subplot(111)
    m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='h', ax=ax)
    m.drawcoastlines(linewidth=0.2, color='k')
    ax.plot(lon, lat, 'o', color='k', ls='-', ms=2.50, linewidth=1.50, label='NHC', zorder=3)
    ax.plot(lon[idx_forecast_start_time::4], lat[idx_forecast_start_time::4], 'o', color='w', ms=1.00, zorder=3)

    for idc, case in enumerate(cases):

        casename = time + '_' + case + '_' + domain
        filename = dir_main + '/best_track/' + casename + '.csv'

        df = pd.read_csv(filename)
        print(df)

        index = []
        for idx, Date_Time in enumerate(df['Date_Time']):
            time_now = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
            if time_now >= forecast_start_time and time_now <= forecast_end_time: index = index + [idx]

        lat = list(df['Latitude'][index])
        lon = list(df['Longitude'][index])
        idx_forecast_start_time = int((24-float(forecast_start_time.strftime('%H')))%24/6)

        ax.plot(lon, lat, 'o', color=colors[idc], ls='-', ms=1.00, linewidth=0.60, label=labels[idc], zorder=3)
        ax.plot(lon[idx_forecast_start_time::4], lat[idx_forecast_start_time::4], 'o', color='w', ms=0.40, zorder=3)

    ax.set_xticks(np.arange(-95, -49, 5))
    ax.set_xticklabels(['95W', '90W', '85W', '80W', '75W', '70W', '65W', '60W', '55W', '50W'])
    ax.set_yticks(np.arange(5, 31, 5))
    ax.set_yticklabels(['5N', '10N', '15N', '20N', '25N', '30N'])
    ax.tick_params('both', direction='in', labelsize=10.0)
    ax.axis(extent)
    ax.grid(True, linewidth=0.5)
    ax.text(-64.0, 10.0, '06 UTC 24 Aug', fontsize=10.0)
    ax.text(-85.0, 25.5, '12 UTC 28 Aug', fontsize=10.0)
    ax.legend(loc='lower left', fontsize=5.0, handlelength=1.0)

    #ax.set_xticks(np.arange(-95, -49, 5))
    #ax.set_xticklabels(['95W', '90W', '85W', '80W', '75W', '70W', '65W', '60W', '55W', '50W'])
    #ax.set_yticks(np.arange(5, 31, 5))
    #ax.set_yticklabels(['5N', '10N', '15N', '20N', '25N', '30N'])
    #ax.tick_params('both', direction='in', labelsize=10.0)
    #ax.axis(extent)
    #ax.grid(True, linewidth=0.5)
    #ax.text(-75.0,  9.0, '00 UTC 25 Aug', fontsize=10.0)
    #ax.text(-90.0, 25.5, '12 UTC 28 Aug', fontsize=10.0)
    #ax.legend(loc='lower left', fontsize=5.0, handlelength=1.0)

    #ax.set_xticks(np.arange(-95, -49, 5))
    #ax.set_xticklabels(['95W', '90W', '85W', '80W', '75W', '70W', '65W', '60W', '55W', '50W'])
    #ax.set_yticks(np.arange(5, 31, 5))
    #ax.set_yticklabels(['5N', '10N', '15N', '20N', '25N', '30N'])
    #ax.tick_params('both', direction='in', labelsize=10.0)
    #ax.axis(extent)
    #ax.grid(True, linewidth=0.5)
    #ax.text(-75.0, 10.0, '12 UTC 25 Aug', fontsize=10.0)
    #ax.text(-90.0, 25.5, '12 UTC 28 Aug', fontsize=10.0)
    #ax.legend(loc='lower left', fontsize=5.0, handlelength=1.0)

    #ax.set_xticks(np.arange(-65, -39, 5))
    #ax.set_xticklabels(['65W', '60W', '55W', '50W', '45W', '40W'])
    #ax.set_yticks(np.arange(5, 31, 5))
    #ax.set_yticklabels(['5N', '10N', '15N', '20N', '25N', '30N'])
    #ax.tick_params('both', direction='in', labelsize=10.0)
    #ax.axis(extent)
    #ax.grid(True, linewidth=0.5)
    #ax.text(-53.0, 13.0, '12 UTC 28 Aug', fontsize=10.0)
    #ax.text(-57.5, 23.0, '00 UTC 31 Aug', fontsize=10.0)
    #ax.legend(loc='lower left', fontsize=5.0, handlelength=1.0)

    #ax.set_xticks(np.arange(-60, -34, 5))
    #ax.set_xticklabels(['60W', '55W', '50W', '45W', '40W', '35W'])
    #ax.set_yticks(np.arange(5, 31, 5))
    #ax.set_yticklabels(['5N', '10N', '15N', '20N', '25N', '30N'])
    #ax.tick_params('both', direction='in', labelsize=10.0)
    #ax.axis(extent)
    #ax.grid(True, linewidth=0.5)
    #ax.text(-50.0, 16.0, '00 UTC 05 Sep', fontsize=10.0)
    #ax.text(-57.5, 24.0, '00 UTC 07 Sep', fontsize=10.0)
    #ax.legend(loc='lower left', fontsize=5.0, handlelength=1.0)

    #ax.set_xticks(np.arange(-60, -34, 5))
    #ax.set_xticklabels(['60W', '55W', '50W', '45W', '40W', '35W'])
    #ax.set_yticks(np.arange(5, 31, 5))
    #ax.set_yticklabels(['5N', '10N', '15N', '20N', '25N', '30N'])
    #ax.tick_params('both', direction='in', labelsize=10.0)
    #ax.axis(extent)
    #ax.grid(True, linewidth=0.5)
    #ax.text(-52.0, 18.5, '18 UTC 05 Sep', fontsize=10.0)
    #ax.text(-57.5, 26.0, '18 UTC 07 Sep', fontsize=10.0)
    #ax.legend(loc='lower left', fontsize=5.0, handlelength=1.0)

    pdf.savefig(fig)
    plt.cla()
    plt.clf()
    plt.close()
