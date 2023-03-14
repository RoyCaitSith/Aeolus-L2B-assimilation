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

#cases0  = ['CON6h_082406_Hybrid_C05', 'CON6h_082406_Hybrid_C06', 'CON6h_082406_Hybrid_C07', 'CON6h_082406_Hybrid_C08']
#labels0 = ['082406_C05', '082406_C06', '082406_C07', '082406_C08']
#cases1  = ['CON6h_Aeolus6h_082406_Hybrid_C05', 'CON6h_Aeolus6h_082406_Hybrid_C06', 'CON6h_Aeolus6h_082406_Hybrid_C07', 'CON6h_Aeolus6h_082406_Hybrid_C08']
#labels1 = ['Aeolus_082406_C05', 'Aeolus_082406_C06', 'Aeolus_082406_C07', 'Aeolus_082406_C08']

#cases0  = ['CON6h_082412_Hybrid_C05', 'CON6h_082412_Hybrid_C06', 'CON6h_082412_Hybrid_C07', 'CON6h_082412_Hybrid_C08']
#labels0 = ['082412_C05', '082412_C06', '082412_C07', '082412_C08']
#cases1  = ['CON6h_Aeolus6h_082412_Hybrid_C05', 'CON6h_Aeolus6h_082412_Hybrid_C06', 'CON6h_Aeolus6h_082412_Hybrid_C07', 'CON6h_Aeolus6h_082412_Hybrid_C08']
#labels1 = ['Aeolus_082412_C05', 'Aeolus_082412_C06', 'Aeolus_082412_C07', 'Aeolus_082412_C08']

#cases0  = ['CON6h_082418_Hybrid_C05', 'CON6h_082418_Hybrid_C06', 'CON6h_082418_Hybrid_C07', 'CON6h_082418_Hybrid_C08']
#labels0 = ['082418_C05', '082418_C06', '082418_C07', '082418_C08']
#cases1  = ['CON6h_Aeolus6h_082418_Hybrid_C05', 'CON6h_Aeolus6h_082418_Hybrid_C06', 'CON6h_Aeolus6h_082418_Hybrid_C07', 'CON6h_Aeolus6h_082418_Hybrid_C08']
#labels1 = ['Aeolus_082418_C05', 'Aeolus_082418_C06', 'Aeolus_082418_C07', 'Aeolus_082418_C08']

cases0  = ['CON6h_082500_Hybrid_C05', 'CON6h_082500_Hybrid_C06', 'CON6h_082500_Hybrid_C07', 'CON6h_082500_Hybrid_C08']
labels0 = ['082500_C05', '082500_C06', '082500_C07', '082500_C08']
cases1  = ['CON6h_Aeolus6h_082500_Hybrid_C05', 'CON6h_Aeolus6h_082500_Hybrid_C06', 'CON6h_Aeolus6h_082500_Hybrid_C07', 'CON6h_Aeolus6h_082500_Hybrid_C08']
labels1 = ['Aeolus_082500_C05', 'Aeolus_082500_C06', 'Aeolus_082500_C07', 'Aeolus_082500_C08']

domain = 'd01'

#pdfname = './Figure_03a_Comparison_track_082406.pdf'
#pdfname = './Figure_03c_Comparison_track_082412.pdf'
#pdfname = './Figure_03e_Comparison_track_082418.pdf'
pdfname = './Figure_03g_Comparison_track_082500.pdf'

file_best_track = dir_best_track + '/2021_09L_Ida.csv'
#forecast_start_time = datetime.datetime(2021, 8, 24,  6, 0, 0)
#forecast_end_time   = datetime.datetime(2021, 8, 28, 12, 0, 0)
#forecast_start_time = datetime.datetime(2021, 8, 24, 12, 0, 0)
#forecast_end_time   = datetime.datetime(2021, 8, 28, 18, 0, 0)
#forecast_start_time = datetime.datetime(2021, 8, 24, 18, 0, 0)
#forecast_end_time   = datetime.datetime(2021, 8, 29,  0, 0, 0)
forecast_start_time = datetime.datetime(2021, 8, 25,  0, 0, 0)
forecast_end_time   = datetime.datetime(2021, 8, 29,  6, 0, 0)

#extent = [-87.5, -72.5, 10.0, 25.0]
#extent = [-90.0, -75.0, 11.5, 26.5]
#extent = [-90.0, -75.0, 12.5, 27.5]
extent = [-90.0, -75.0, 13.5, 28.5]

sns_cmap = sns.color_palette('Paired')
colors0 = [sns_cmap[0], sns_cmap[2], sns_cmap[4], sns_cmap[6]]
colors1 = [sns_cmap[1], sns_cmap[3], sns_cmap[5], sns_cmap[7]]

with PdfPages(pdfname) as pdf:

    fig = plt.figure(1, [6.0, 6.0])
    fig.subplots_adjust(left=0.100, bottom=0.050, right=0.950, top=0.975, wspace=0.000, hspace=0.000)

    #Read Best Track
    df = pd.read_csv(file_best_track)
    #print(df)

    forecast_start_time_min = forecast_start_time + datetime.timedelta(hours=6.0*int(cases0[0][-2:]))

    index = []
    for idx, Date_Time in enumerate(df['Date_Time']):
        time_now = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
        if time_now >= forecast_start_time_min and time_now <= forecast_end_time: index = index + [idx]

    lat = list(df['Latitude'][index])
    lon = list(df['Longitude'][index])
    idx_forecast_start_time_min = int((24-float(forecast_start_time_min.strftime('%H')))%24/6)

    # Draw best track
    ax = fig.add_subplot(111)
    m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='h', ax=ax)
    m.drawcoastlines(linewidth=0.2, color='k')
    ax.plot(lon[:-1], lat[:-1], 'o', color='k', ls='-', ms=4.00, linewidth=2.50, label='NHC', zorder=3)
    ax.plot(lon[idx_forecast_start_time_min:-1:4], lat[idx_forecast_start_time_min:-1:4], 'o', color='w', ms=1.50, zorder=3)

    for idc, case0 in enumerate(cases0):

        casename = case0 + '_' + domain
        filename = dir_main + '/best_track/' + casename + '.csv'

        df = pd.read_csv(filename)
        print(df)

        forecast_start_time_cycle = forecast_start_time + datetime.timedelta(hours=6.0*int(case0[-2:]))

        index = []
        for idx, Date_Time in enumerate(df['Date_Time']):
            time_now = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
            if time_now >= forecast_start_time_cycle and time_now <= forecast_end_time: index = index + [idx]

        lat = list(df['Latitude'][index])
        lon = list(df['Longitude'][index])
        idx_forecast_start_time_cycle = int((24-float(forecast_start_time_cycle.strftime('%H')))%24/6)

        ax.plot(lon[:-1:], lat[:-1:], 'o', color=colors0[idc], ls='--', ms=2.00, linewidth=1.25, label=labels0[idc], zorder=3)
        ax.plot(lon[idx_forecast_start_time_cycle:-1:4], lat[idx_forecast_start_time_cycle:-1:4], 'o', color='w', ms=0.75, zorder=3)

    for idc, case1 in enumerate(cases1):

        casename = case1 + '_' + domain
        filename = dir_main + '/best_track/' + casename + '.csv'

        df = pd.read_csv(filename)
        print(df)

        forecast_start_time_cycle = forecast_start_time + datetime.timedelta(hours=6.0*int(case1[-2:]))

        index = []
        for idx, Date_Time in enumerate(df['Date_Time']):
            time_now = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
            if time_now >= forecast_start_time_cycle and time_now <= forecast_end_time: index = index + [idx]

        lat = list(df['Latitude'][index])
        lon = list(df['Longitude'][index])
        idx_forecast_start_time_cycle = int((24-float(forecast_start_time_cycle.strftime('%H')))%24/6)

        ax.plot(lon[:-1:], lat[:-1:], 'o', color=colors1[idc], ls='-', ms=2.00, linewidth=1.25, label=labels1[idc], zorder=3)
        ax.plot(lon[idx_forecast_start_time_cycle:-1:4], lat[idx_forecast_start_time_cycle:-1:4], 'o', color='w', ms=0.75, zorder=3)

    ax.set_xticks(np.arange(-100, -49, 5))
    ax.set_xticklabels(['100W', '95W', '90W', '85W', '80W', '75W', '70W', '65W', '60W', '55W', '50W'])
    ax.set_yticks(np.arange(10, 36, 5))
    ax.set_yticklabels(['10N', '15N', '20N', '25N', '30N', '35N'])
    ax.tick_params('both', direction='in', labelsize=10.0)
    ax.axis(extent)
    ax.grid(True, linewidth=0.5)
    #ax.text(-76.0, 14.0, '12 UTC 25 Aug', fontsize=10.0)
    #ax.text(-86.0, 24.0, '06 UTC 28 Aug', fontsize=10.0)
    #ax.text(-78.5, 12.0, '18 UTC 25 Aug', fontsize=10.0)
    #ax.text(-86.5, 25.0, '12 UTC 28 Aug', fontsize=10.0)
    #ax.text(-78.5, 13.0, '00 UTC 26 Aug', fontsize=10.0)
    #ax.text(-87.0, 26.0, '18 UTC 28 Aug', fontsize=10.0)
    ax.text(-78.5, 14.0, '06 UTC 26 Aug', fontsize=10.0)
    ax.text(-87.0, 27.0, '00 UTC 29 Aug', fontsize=10.0)
    ax.legend(loc='upper right', fontsize=10.0, handlelength=2.5)

    pdf.savefig(fig)
    plt.cla()
    plt.clf()
    plt.close()
