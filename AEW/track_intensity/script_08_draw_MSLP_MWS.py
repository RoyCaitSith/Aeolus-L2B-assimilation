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

#cases = ['CON6h_Hybrid_082500', 'CON6h_Aeolus6h_Hybrid_082500', 'CON6h_Aeolus6h_L2B_Hybrid_082500']
#labels = ['CON_Hybrid_082500', 'Aeolus_Hybrid_082500', 'Aeolus_L2B_Hybrid_082500']
cases = ['CON6h_Hybrid_082512', 'CON6h_Aeolus6h_Hybrid_082512', 'CON6h_Aeolus6h_L2B_Hybrid_082512']
labels = ['CON_Hybrid_082512', 'Aeolus_Hybrid_082512', 'Aeolus_L2B_Hybrid_082512']
#cases = ['CON6h_Hybrid_082500', 'CON6h_Aeolus6h_Hybrid_082500', 'CON6h_Hybrid_082512', 'CON6h_Aeolus6h_Hybrid_082512']
#labels = ['CON_Hybrid_082500', 'Aeolus_Hybrid_082500', 'CON_Hybrid_082512', 'Aeolus_Hybrid_082512']
#cases = ['CON6h_082500', 'CON6h_Aeolus6h_082500']
#labels = ['CON_082500', 'Aeolus_082500']
#cases = ['CON6h_082512', 'CON6h_Aeolus6h_082512']
#labels = ['CON_082512', 'Aeolus_082512']
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
#pdfname = dir_main + '/' + time + '/figures/Aeolus_082500_intensity.pdf'
pdfname = dir_main + '/' + time + '/figures/Aeolus_082512_intensity.pdf'
#pdfname = dir_main + '/' + time + '/figures/Aeolus_Hybrid_intensity.pdf'
#pdfname = dir_main + '/' + time + '/figures/Aeolus_No1h_082412_intensity.pdf'
#pdfname = dir_main + '/' + time + '/figures/Aeolus_No1h_082512_intensity.pdf'
#pdfname = dir_main + '/' + time + '/figures/DS_Hybrid_082500_intensity.pdf'
#pdfname = dir_main + '/' + time + '/figures/DS_Hybrid_082512_intensity.pdf'
#pdfname = dir_main + '/' + time + '/figures/Aeolus_intensity.pdf'
#pdfname = dir_main + '/' + time + '/figures/DS_intensity.pdf'
#pdfname = dir_main + '/' + time + '/figures/DAWN_intensity.pdf'
#pdfname = dir_main + '/' + time + '/figures/HALO_intensity.pdf'
#pdfname = dir_main + '/' + time + '/figures/HRFD_intensity.pdf'
#pdfname = dir_main + '/' + time + '/figures/DAWN_Aeolus_intensity.pdf'
#pdfname = dir_main + '/' + time + '/figures/0412_DAWN_Aeolus_intensity.pdf'

if '20210824' in time:
    file_best_track = dir_best_track + '/2021_09L_Ida.csv'
    #forecast_start_time = datetime.datetime(2021, 8, 24,  6, 0, 0)
    #forecast_end_time   = datetime.datetime(2021, 8, 28, 12, 0, 0)
    #forecast_start_time = datetime.datetime(2021, 8, 24,  6, 0, 0)
    #forecast_end_time   = datetime.datetime(2021, 8, 26, 12, 0, 0)
    #forecast_start_time = datetime.datetime(2021, 8, 24,  6, 0, 0)
    #forecast_end_time   = datetime.datetime(2021, 8, 27, 12, 0, 0)
    forecast_start_time = datetime.datetime(2021, 8, 24,  6, 0, 0)
    forecast_end_time   = datetime.datetime(2021, 8, 28, 12, 0, 0)
if '20210828' in time:
    file_best_track = dir_best_track + '/2021_10L_Kate.csv'
    forecast_start_time = datetime.datetime(2021, 8, 28, 12, 0, 0)
    forecast_end_time   = datetime.datetime(2021, 8, 31,  0, 0, 0)
if '20210904' in time:
    file_best_track = dir_best_track + '/2021_12L_Larry.csv'
    forecast_start_time = datetime.datetime(2021, 9,  3, 18, 0, 0)
    forecast_end_time   = datetime.datetime(2021, 9,  7,  0, 0, 0)
    #forecast_start_time = datetime.datetime(2021, 9,  4, 12, 0, 0)
    #forecast_end_time   = datetime.datetime(2021, 9,  7, 18, 0, 0)

sns_cmap = sns.color_palette('bright')
colors = [sns_cmap[0], sns_cmap[1], sns_cmap[2], sns_cmap[3], sns_cmap[4], sns_cmap[5], sns_cmap[6], sns_cmap[7]]

with PdfPages(pdfname) as pdf:

    fig = plt.figure(1, [7.5, 9.0])
    fig.subplots_adjust(left=0.100, bottom=0.050, right=0.950, top=0.975, wspace=0.000, hspace=0.150)

    #Read Best Track
    df = pd.read_csv(file_best_track)
    #print(df)

    index = []
    for idx, Date_Time in enumerate(df['Date_Time']):
        time_now = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
        if time_now >= forecast_start_time and time_now <= forecast_end_time: index = index + [idx]

    MSLP_bt = list(df['MSLP (hPa)'][index])
    MWS_bt = list(df['MWS (Knot)'][index])
    idx_forecast_start_time  = int((24-float(forecast_start_time.strftime('%H')))%24/6)

    # Draw best track
    ax = fig.add_subplot(211)
    ax.plot(np.arange(len(MSLP_bt)), MSLP_bt, 'o', color='k', ls='-', ms=2.50, linewidth=1.50, label='NHC', zorder=3)
    ax.plot(np.arange(idx_forecast_start_time, len(MSLP_bt), 4), MSLP_bt[idx_forecast_start_time::4], 'o', color='w', ms=1.00, zorder=3)

    for idc, case in enumerate(cases):

        casename = time + '_' + case + '_' + domain
        filename = dir_main + '/best_track/' + casename + '.csv'

        df = pd.read_csv(filename)
        print(df)

        index = []
        for idx, Date_Time in enumerate(df['Date_Time']):
            time_now = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
            if time_now >= forecast_start_time and time_now <= forecast_end_time: index = index + [idx]
            if time_now == forecast_start_time: str_index = idx
        str_index = index[0] - str_index

        MSLP = list(df['MSLP (hPa)'][index])
        idx_forecast_start_time = int((24-float(forecast_start_time.strftime('%H')))%24/6)

        mtitle = labels[idc]
        ax.plot(np.arange(str_index, str_index + len(MSLP)), MSLP, 'o', color=colors[idc], ls='-', ms=2.00, linewidth=1.20, label=mtitle, zorder=3)
        ax.plot(np.arange(str_index + idx_forecast_start_time, str_index + len(MSLP), 4), MSLP[idx_forecast_start_time::4], 'o', color='w', ms=0.80, zorder=3)

        extent = [0, len(MSLP_bt)-1, 965.0, 1015.0]
        #extent = [3, len(MSLP_bt)-1, 965.0, 1015.0]
        #extent = [5, len(MSLP_bt)-1, 965.0, 1015.0]
        #extent = [0, len(MSLP_bt)-1, 990.0, 1015.0]
        #extent = [5, len(MSLP_bt)-1, 950.0, 1000.0]
        #extent = [2, len(MSLP_bt)-1, 950.0, 1000.0]

    ax.set_xticks(np.arange(0, len(MSLP_bt), 1))
    ax.set_xticklabels(['', '', '', \
                        '00 UTC\n25 Aug', '', '', '', \
                        '00 UTC\n26 Aug', '', '', '', \
                        '00 UTC\n27 Aug', '', '', '', \
                        '00 UTC\n28 Aug', '', ''])
    ax.set_yticks(np.arange(extent[2], extent[3]+1, 5))
    ax.set_ylabel('Time', fontsize=10.0)
    ax.set_ylabel('MSLP (hPa)', fontsize=10.0)
    ax.tick_params('both', direction='in', labelsize=10.0)
    ax.axis(extent)
    ax.grid(True, linewidth=0.5)
    ax.legend(loc='lower left', fontsize=10.0, handlelength=1.0)

    #ax.set_xticks(np.arange(0, len(MSLP_bt), 1))
    #ax.set_xticklabels(['', '', \
                        #'00 UTC\n29 Aug', '', '', '', \
                        #'00 UTC\n30 Aug', '', '', '', \
                        #'00 UTC\n31 Aug'])
    #ax.set_yticks(np.arange(extent[2], extent[3]+1, 5))
    #ax.set_ylabel('Time', fontsize=10.0)
    #ax.set_ylabel('MSLP (hPa)', fontsize=10.0)
    #ax.tick_params('both', direction='in', labelsize=10.0)
    #ax.axis(extent)
    #ax.grid(True, linewidth=0.5)
    #ax.legend(loc='lower left', fontsize=10.0, handlelength=1.0)

    #ax.set_xticks(np.arange(0, len(MSLP_bt), 1))
    #ax.set_xticklabels(['', \
                        #'00 UTC\n4 Sep', '', '', '', \
                        #'00 UTC\n5 Sep', '', '', '', \
                        #'00 UTC\n6 Sep', '', '', '', \
                        #'00 UTC\n7 Sep'])
    #ax.set_yticks(np.arange(extent[2], extent[3]+1, 10))
    #ax.set_ylabel('Time', fontsize=10.0)
    #ax.set_ylabel('MSLP (hPa)', fontsize=10.0)
    #ax.tick_params('both', direction='in', labelsize=10.0)
    #ax.axis(extent)
    #ax.grid(True, linewidth=0.5)
    #ax.legend(loc='upper left', fontsize=10.0, handlelength=1.0)

    #ax.set_xticks(np.arange(0, len(MSLP_bt), 1))
    #ax.set_xticklabels(['', '', \
                        #'00 UTC\n5 Sep', '', '', '', \
                        #'00 UTC\n6 Sep', '', '', '', \
                        #'00 UTC\n7 Sep', '', '', ''])
    #ax.set_yticks(np.arange(extent[2], extent[3]+1, 10))
    #ax.set_ylabel('Time', fontsize=10.0)
    #ax.set_ylabel('MSLP (hPa)', fontsize=10.0)
    #ax.tick_params('both', direction='in', labelsize=10.0)
    #ax.axis(extent)
    #ax.grid(True, linewidth=0.5)
    #ax.legend(loc='upper left', fontsize=10.0, handlelength=1.0)

    ax = fig.add_subplot(212)
    ax.plot(np.arange(len(MWS_bt)), MWS_bt, 'o', color='k', ls='-', ms=2.50, linewidth=1.50, label='NHC', zorder=3)
    ax.plot(np.arange(idx_forecast_start_time, len(MWS_bt), 4), MWS_bt[idx_forecast_start_time::4], 'o', color='w', ms=1.00, zorder=3)

    for idc, case in enumerate(cases):

        casename = time + '_' + case + '_' + domain
        filename = dir_main + '/best_track/' + casename + '.csv'

        df = pd.read_csv(filename)
        print(df)

        index = []
        for idx, Date_Time in enumerate(df['Date_Time']):
            time_now = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
            if time_now >= forecast_start_time and time_now <= forecast_end_time: index = index + [idx]
            if time_now == forecast_start_time: str_index = idx
        str_index = index[0] - str_index

        MWS = list(df['MWS (Knot)'][index])
        idx_forecast_start_time = int((24-float(forecast_start_time.strftime('%H')))%24/6)

        mtitle = labels[idc]
        ax.plot(np.arange(str_index, str_index + len(MWS)), MWS, 'o', color=colors[idc], ls='-', ms=2.00, linewidth=1.20, label=mtitle, zorder=3)
        ax.plot(np.arange(str_index + idx_forecast_start_time, str_index + len(MWS), 4), MWS[idx_forecast_start_time::4], 'o', color='w', ms=0.80, zorder=3)

        extent = [0, len(MWS_bt)-1, 15.0, 95.0]
        #extent = [3, len(MWS_bt)-1, 15.0, 95.0]
        #extent = [5, len(MWS_bt)-1, 15.0, 95.0]
        #extent = [0, len(MWS_bt)-1, 0.0, 55.0]
        #extent = [5, len(MWS_bt)-1, 40.0, 120.0]
        #extent = [2, len(MWS_bt)-1, 60.0, 120.0]

    ax.set_xticks(np.arange(0, len(MSLP_bt), 1))
    ax.set_xticklabels(['', '', '', \
                        '00 UTC\n25 Aug', '', '', '', \
                        '00 UTC\n26 Aug', '', '', '', \
                        '00 UTC\n27 Aug', '', '', '', \
                        '00 UTC\n28 Aug', '', ''])
    ax.set_yticks(np.arange(extent[2], extent[3]+1, 5))
    ax.set_ylabel('Time', fontsize=10.0)
    ax.set_ylabel('MWS (Knot)', fontsize=10.0)
    ax.tick_params('both', direction='in', labelsize=10.0)
    ax.axis(extent)
    ax.grid(True, linewidth=0.5)
    ax.legend(loc='upper left', fontsize=10.0, handlelength=1.0)

    #ax.set_xticks(np.arange(0, len(MWS_bt), 1))
    #ax.set_xticklabels(['', '', \
                        #'00 UTC\n29 Aug', '', '', '', \
                        #'00 UTC\n30 Aug', '', '', '', \
                        #'00 UTC\n31 Aug'])
    #ax.set_yticks(np.arange(extent[2], extent[3]+1, 5))
    #ax.set_ylabel('Time', fontsize=10.0)
    #ax.set_ylabel('MWS (Knot)', fontsize=10.0)
    #ax.tick_params('both', direction='in', labelsize=10.0)
    #ax.axis(extent)
    #ax.grid(True, linewidth=0.5)
    #ax.legend(loc='lower left', fontsize=10.0, handlelength=1.0)

    #ax.set_xticks(np.arange(0, len(MWS_bt), 1))
    #ax.set_xticklabels(['', \
                        #'00 UTC\n4 Sep', '', '', '', \
                        #'00 UTC\n5 Sep', '', '', '', \
                        #'00 UTC\n6 Sep', '', '', '', \
                        #'00 UTC\n7 Sep'])
    #ax.set_yticks(np.arange(extent[2], extent[3]+1, 10))
    #ax.set_ylabel('Time', fontsize=10.0)
    #ax.set_ylabel('MWS (Knot)', fontsize=10.0)
    #ax.tick_params('both', direction='in', labelsize=10.0)
    #ax.axis(extent)
    #ax.grid(True, linewidth=0.5)
    #ax.legend(loc='lower left', fontsize=10.0, handlelength=1.0)

    #ax.set_xticks(np.arange(0, len(MWS_bt), 1))
    #ax.set_xticklabels(['', '', \
                        #'00 UTC\n5 Sep', '', '', '', \
                        #'00 UTC\n6 Sep', '', '', '', \
                        #'00 UTC\n7 Sep', '', '', ''])
    #ax.set_yticks(np.arange(extent[2], extent[3]+1, 10))
    #ax.set_ylabel('Time', fontsize=10.0)
    #ax.set_ylabel('MWS (Knot)', fontsize=10.0)
    #ax.tick_params('both', direction='in', labelsize=10.0)
    #ax.axis(extent)
    #ax.grid(True, linewidth=0.5)
    #ax.legend(loc='lower left', fontsize=10.0, handlelength=1.0)

    pdf.savefig(fig)
    plt.cla()
    plt.clf()
    plt.close()
