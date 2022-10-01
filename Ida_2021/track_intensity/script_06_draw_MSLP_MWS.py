import os
import re
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.basemap import Basemap

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN'
dir_main = dir_CPEX + '/15_ENS/track_intensity'
dir_best_track = dir_main + '/best_track'

#cases  = ['CON6h_082406_Hybrid_C05', 'CON6h_082406_Hybrid_C06', 'CON6h_082406_Hybrid_C07', 'CON6h_082406_Hybrid_C08']
#labels = ['CON_082406_Hybrid_C05', 'CON_082406_Hybrid_C06', 'CON_082406_Hybrid_C07', 'CON_082406_Hybrid_C08']
#cases  = ['CON6h_082412_Hybrid_C05', 'CON6h_082412_Hybrid_C06', 'CON6h_082412_Hybrid_C07', 'CON6h_082412_Hybrid_C08']
#labels = ['CON_082412_Hybrid_C05', 'CON_082412_Hybrid_C06', 'CON_082412_Hybrid_C07', 'CON_082412_Hybrid_C08']
#cases  = ['CON6h_082418_Hybrid_C05', 'CON6h_082418_Hybrid_C06', 'CON6h_082418_Hybrid_C07', 'CON6h_082418_Hybrid_C08']
#labels = ['CON_082418_Hybrid_C05', 'CON_082418_Hybrid_C06', 'CON_082418_Hybrid_C07', 'CON_082418_Hybrid_C08']
#cases  = ['CON6h_082500_Hybrid_C05', 'CON6h_082500_Hybrid_C06', 'CON6h_082500_Hybrid_C07', 'CON6h_082500_Hybrid_C08']
#labels = ['CON_082500_Hybrid_C05', 'CON_082500_Hybrid_C06', 'CON_082500_Hybrid_C07', 'CON_082500_Hybrid_C08']
#cases  = ['CON6h_Aeolus6h_082406_Hybrid_C05', 'CON6h_Aeolus6h_082406_Hybrid_C06', 'CON6h_Aeolus6h_082406_Hybrid_C07', 'CON6h_Aeolus6h_082406_Hybrid_C08']
#labels = ['CON_Aeolus_082406_Hybrid_C05', 'CON_Aeolus_082406_Hybrid_C06', 'CON_Aeolus_082406_Hybrid_C07', 'CON_Aeolus_082406_Hybrid_C08']
#cases  = ['CON6h_Aeolus6h_082412_Hybrid_C05', 'CON6h_Aeolus6h_082412_Hybrid_C06', 'CON6h_Aeolus6h_082412_Hybrid_C07', 'CON6h_Aeolus6h_082412_Hybrid_C08']
#labels = ['CON_Aeolus_082412_Hybrid_C05', 'CON_Aeolus_082412_Hybrid_C06', 'CON_Aeolus_082412_Hybrid_C07', 'CON_Aeolus_082412_Hybrid_C08']
#cases  = ['CON6h_Aeolus6h_082418_Hybrid_C05', 'CON6h_Aeolus6h_082418_Hybrid_C06', 'CON6h_Aeolus6h_082418_Hybrid_C07', 'CON6h_Aeolus6h_082418_Hybrid_C08']
#labels = ['CON_Aeolus_082418_Hybrid_C05', 'CON_Aeolus_082418_Hybrid_C06', 'CON_Aeolus_082418_Hybrid_C07', 'CON_Aeolus_082418_Hybrid_C08']
cases  = ['CON6h_Aeolus6h_082500_Hybrid_C05', 'CON6h_Aeolus6h_082500_Hybrid_C06', 'CON6h_Aeolus6h_082500_Hybrid_C07', 'CON6h_Aeolus6h_082500_Hybrid_C08']
labels = ['CON_Aeolus_082500_Hybrid_C05', 'CON_Aeolus_082500_Hybrid_C06', 'CON_Aeolus_082500_Hybrid_C07', 'CON_Aeolus_082500_Hybrid_C08']

domain = 'd01'

#pdfname = dir_main + '/Figures/Aeolus_082406_intensity.pdf'
#pdfname = dir_main + '/Figures/Aeolus_082412_intensity.pdf'
#pdfname = dir_main + '/Figures/Aeolus_082418_intensity.pdf'
#pdfname = dir_main + '/Figures/Aeolus_082500_intensity.pdf'
#pdfname = dir_main + '/Figures/Aeolus_DA_082406_intensity.pdf'
#pdfname = dir_main + '/Figures/Aeolus_DA_082412_intensity.pdf'
#pdfname = dir_main + '/Figures/Aeolus_DA_082418_intensity.pdf'
pdfname = dir_main + '/Figures/Aeolus_DA_082500_intensity.pdf'

file_best_track = dir_best_track + '/2021_09L_Ida.csv'
#forecast_start_time = datetime.datetime(2021, 8, 24,  6, 0, 0)
#forecast_end_time   = datetime.datetime(2021, 8, 28, 12, 0, 0)
#forecast_start_time = datetime.datetime(2021, 8, 24, 12, 0, 0)
#forecast_end_time   = datetime.datetime(2021, 8, 28, 18, 0, 0)
#forecast_start_time = datetime.datetime(2021, 8, 24, 18, 0, 0)
#forecast_end_time   = datetime.datetime(2021, 8, 29,  0, 0, 0)
forecast_start_time = datetime.datetime(2021, 8, 25,  0, 0, 0)
forecast_end_time   = datetime.datetime(2021, 8, 29,  6, 0, 0)

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
    ax.plot(np.arange(len(MSLP_bt)-1), MSLP_bt[:-1], 'o', color='k', ls='-', ms=2.50, linewidth=1.50, label='NHC', zorder=3)
    ax.plot(np.arange(idx_forecast_start_time, len(MSLP_bt)-1, 4), MSLP_bt[idx_forecast_start_time:-1:4], 'o', color='w', ms=1.00, zorder=3)

    for idc, case in enumerate(cases):

        casename = case + '_' + domain
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
        ax.plot(np.arange(str_index, str_index+len(MSLP)-1), MSLP[:-1], 'o', color=colors[idc], ls='-', ms=2.00, linewidth=1.20, label=mtitle, zorder=3)
        ax.plot(np.arange(str_index+idx_forecast_start_time, str_index+len(MSLP)-1, 4), MSLP[idx_forecast_start_time:-1:4], 'o', color='w', ms=0.80, zorder=3)
        ax.plot(str_index+len(MSLP)-10, MSLP[-10], 'x', color='k', ms=5.00, zorder=3)

        extent = [0, len(MSLP_bt)-2, 965.0, 1015.0]

    ax.set_xticks(np.arange(0, len(MSLP_bt)-1, 1))
    #ax.set_xticklabels(['', '', '', \
                        #'00 UTC\n25 Aug', '', '', '', \
                        #'00 UTC\n26 Aug', '', '', '', \
                        #'00 UTC\n27 Aug', '', '', '', \
                        #'00 UTC\n28 Aug', ''])
    #ax.set_xticklabels(['', '', \
                        #'00 UTC\n25 Aug', '', '', '', \
                        #'00 UTC\n26 Aug', '', '', '', \
                        #'00 UTC\n27 Aug', '', '', '', \
                        #'00 UTC\n28 Aug', '', ''])
    #ax.set_xticklabels(['', \
                        #'00 UTC\n25 Aug', '', '', '', \
                        #'00 UTC\n26 Aug', '', '', '', \
                        #'00 UTC\n27 Aug', '', '', '', \
                        #'00 UTC\n28 Aug', '', '', ''])
    ax.set_xticklabels(['00 UTC\n25 Aug', '', '', '', \
                        '00 UTC\n26 Aug', '', '', '', \
                        '00 UTC\n27 Aug', '', '', '', \
                        '00 UTC\n28 Aug', '', '', '', \
                        '00 UTC\n29 Aug'])
    ax.set_yticks(np.arange(extent[2], extent[3]+1, 5))
    ax.set_ylabel('Time', fontsize=10.0)
    ax.set_ylabel('MSLP (hPa)', fontsize=10.0)
    ax.tick_params('both', direction='in', labelsize=10.0)
    ax.axis(extent)
    ax.grid(True, linewidth=0.5)
    ax.legend(loc='lower left', fontsize=10.0, handlelength=1.0)

    ax = fig.add_subplot(212)
    ax.plot(np.arange(len(MWS_bt)-1), MWS_bt[:-1], 'o', color='k', ls='-', ms=2.50, linewidth=1.50, label='NHC', zorder=3)
    ax.plot(np.arange(idx_forecast_start_time, len(MWS_bt)-1, 4), MWS_bt[idx_forecast_start_time:-1:4], 'o', color='w', ms=1.00, zorder=3)

    for idc, case in enumerate(cases):

        casename = case + '_' + domain
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
        ax.plot(np.arange(str_index, str_index+len(MWS)-1), MWS[:-1], 'o', color=colors[idc], ls='-', ms=2.00, linewidth=1.20, label=mtitle, zorder=3)
        ax.plot(np.arange(str_index+idx_forecast_start_time, str_index+len(MWS)-1, 4), MWS[idx_forecast_start_time:-1:4], 'o', color='w', ms=0.80, zorder=3)
        ax.plot(str_index+len(MWS)-10, MWS[-10], 'x', color='k', ms=5.00, zorder=3)

        extent = [0, len(MWS_bt)-2, 15.0, 95.0]

    ax.set_xticks(np.arange(0, len(MWS_bt)-1, 1))
    #ax.set_xticklabels(['', '', '', \
                        #'00 UTC\n25 Aug', '', '', '', \
                        #'00 UTC\n26 Aug', '', '', '', \
                        #'00 UTC\n27 Aug', '', '', '', \
                        #'00 UTC\n28 Aug', ''])
    #ax.set_xticklabels(['', '', \
                        #'00 UTC\n25 Aug', '', '', '', \
                        #'00 UTC\n26 Aug', '', '', '', \
                        #'00 UTC\n27 Aug', '', '', '', \
                        #'00 UTC\n28 Aug', '', ''])
    #ax.set_xticklabels(['', \
                        #'00 UTC\n25 Aug', '', '', '', \
                        #'00 UTC\n26 Aug', '', '', '', \
                        #'00 UTC\n27 Aug', '', '', '', \
                        #'00 UTC\n28 Aug', '', '', ''])
    ax.set_xticklabels(['00 UTC\n25 Aug', '', '', '', \
                        '00 UTC\n26 Aug', '', '', '', \
                        '00 UTC\n27 Aug', '', '', '', \
                        '00 UTC\n28 Aug', '', '', '', \
                        '00 UTC\n29 Aug'])
    ax.set_yticks(np.arange(extent[2], extent[3]+1, 5))
    ax.set_ylabel('Time', fontsize=10.0)
    ax.set_ylabel('MWS (Knot)', fontsize=10.0)
    ax.tick_params('both', direction='in', labelsize=10.0)
    ax.axis(extent)
    ax.grid(True, linewidth=0.5)
    ax.legend(loc='upper left', fontsize=10.0, handlelength=1.0)

    pdf.savefig(fig)
    plt.cla()
    plt.clf()
    plt.close()
