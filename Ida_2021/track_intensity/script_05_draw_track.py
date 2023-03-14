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
#cases  = ['CON6h_Aeolus6h_082500_Hybrid_C05', 'CON6h_Aeolus6h_082500_Hybrid_C06', 'CON6h_Aeolus6h_082500_Hybrid_C07', 'CON6h_Aeolus6h_082500_Hybrid_C08']
#labels = ['CON_Aeolus_082500_Hybrid_C05', 'CON_Aeolus_082500_Hybrid_C06', 'CON_Aeolus_082500_Hybrid_C07', 'CON_Aeolus_082500_Hybrid_C08']
#cases  = ['CON6h_Aeolus6h_082500_H1_Hybrid_C05', 'CON6h_Aeolus6h_082500_H1_Hybrid_C06', 'CON6h_Aeolus6h_082500_H1_Hybrid_C07', 'CON6h_Aeolus6h_082500_H1_Hybrid_C08']
#labels = ['CON_Aeolus_082500_H1_Hybrid_C05', 'CON_Aeolus_082500_H1_Hybrid_C06', 'CON_Aeolus_082500_H1_Hybrid_C07', 'CON_Aeolus_082500_H1_Hybrid_C08']
#cases  = ['CON6h_Aeolus6h_082500_H2_Hybrid_C05', 'CON6h_Aeolus6h_082500_H2_Hybrid_C06', 'CON6h_Aeolus6h_082500_H2_Hybrid_C07', 'CON6h_Aeolus6h_082500_H2_Hybrid_C08']
#labels = ['CON_Aeolus_082500_H2_Hybrid_C05', 'CON_Aeolus_082500_H2_Hybrid_C06', 'CON_Aeolus_082500_H2_Hybrid_C07', 'CON_Aeolus_082500_H2_Hybrid_C08']
#cases  = ['CON6h_Aeolus6h_082500_V1_Hybrid_C05', 'CON6h_Aeolus6h_082500_V1_Hybrid_C06', 'CON6h_Aeolus6h_082500_V1_Hybrid_C07', 'CON6h_Aeolus6h_082500_V1_Hybrid_C08']
#labels = ['CON_Aeolus_082500_V1_Hybrid_C05', 'CON_Aeolus_082500_V1_Hybrid_C06', 'CON_Aeolus_082500_V1_Hybrid_C07', 'CON_Aeolus_082500_V1_Hybrid_C08']
cases  = ['CON6h_Aeolus6h_082500_V2_Hybrid_C05', 'CON6h_Aeolus6h_082500_V2_Hybrid_C06', 'CON6h_Aeolus6h_082500_V2_Hybrid_C07', 'CON6h_Aeolus6h_082500_V2_Hybrid_C08']
labels = ['CON_Aeolus_082500_V2_Hybrid_C05', 'CON_Aeolus_082500_V2_Hybrid_C06', 'CON_Aeolus_082500_V2_Hybrid_C07', 'CON_Aeolus_082500_V2_Hybrid_C08']

domain = 'd01'

#pdfname = dir_main + '/Figures/Aeolus_082406_track.pdf'
#pdfname = dir_main + '/Figures/Aeolus_082412_track.pdf'
#pdfname = dir_main + '/Figures/Aeolus_082418_track.pdf'
#pdfname = dir_main + '/Figures/Aeolus_082500_track.pdf'
#pdfname = dir_main + '/Figures/Aeolus_DA_082406_track.pdf'
#pdfname = dir_main + '/Figures/Aeolus_DA_082412_track.pdf'
#pdfname = dir_main + '/Figures/Aeolus_DA_082418_track.pdf'
#pdfname = dir_main + '/Figures/Aeolus_DA_082500_track.pdf'
#pdfname = dir_main + '/Figures/Aeolus_DA_082500_H1_track.pdf'
#pdfname = dir_main + '/Figures/Aeolus_DA_082500_H2_track.pdf'
#pdfname = dir_main + '/Figures/Aeolus_DA_082500_V1_track.pdf'
pdfname = dir_main + '/Figures/Aeolus_DA_082500_V2_track.pdf'

file_best_track = dir_best_track + '/2021_09L_Ida.csv'
#forecast_start_time = datetime.datetime(2021, 8, 24,  6, 0, 0)
#forecast_end_time   = datetime.datetime(2021, 8, 28, 12, 0, 0)
#forecast_start_time = datetime.datetime(2021, 8, 24, 12, 0, 0)
#forecast_end_time   = datetime.datetime(2021, 8, 28, 18, 0, 0)
#forecast_start_time = datetime.datetime(2021, 8, 24, 18, 0, 0)
#forecast_end_time   = datetime.datetime(2021, 8, 29,  0, 0, 0)
forecast_start_time = datetime.datetime(2021, 8, 25,  0, 0, 0)
forecast_end_time   = datetime.datetime(2021, 8, 29,  6, 0, 0)
extent = [-100.0, -60.0, 10.0, 35.0]

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
    ax.plot(lon[:-1], lat[:-1], 'o', color='k', ls='-', ms=2.50, linewidth=1.50, label='NHC', zorder=3)
    ax.plot(lon[idx_forecast_start_time:-1:4], lat[idx_forecast_start_time:-1:4], 'o', color='w', ms=1.00, zorder=3)

    for idc, case in enumerate(cases):

        casename = case + '_' + domain
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

        ax.plot(lon[:-1:], lat[:-1:], 'o', color=colors[idc], ls='-', ms=1.00, linewidth=0.60, label=labels[idc], zorder=3)
        ax.plot(lon[idx_forecast_start_time:-1:4], lat[idx_forecast_start_time:-1:4], 'o', color='w', ms=0.40, zorder=3)
        ax.plot(lon[-10], lat[-10], 'x', color='k', ms=5.00, zorder=3)

    ax.set_xticks(np.arange(-100, -49, 5))
    ax.set_xticklabels(['100W', '95W', '90W', '85W', '80W', '75W', '70W', '65W', '60W', '55W', '50W'])
    ax.set_yticks(np.arange(10, 36, 5))
    ax.set_yticklabels(['10N', '15N', '20N', '25N', '30N', '35N'])
    ax.tick_params('both', direction='in', labelsize=10.0)
    ax.axis(extent)
    ax.grid(True, linewidth=0.5)
    #ax.text(-72.5, 13.0, '06 UTC 24 Aug', fontsize=10.0)
    #ax.text(-89.0, 25.0, '06 UTC 28 Aug', fontsize=10.0)
    #ax.text(-73.0, 13.0, '12 UTC 24 Aug', fontsize=10.0)
    #ax.text(-89.0, 25.0, '12 UTC 28 Aug', fontsize=10.0)
    #ax.text(-73.0, 13.0, '18 UTC 24 Aug', fontsize=10.0)
    #ax.text(-89.0, 26.5, '18 UTC 28 Aug', fontsize=10.0)
    ax.text(-73.0, 13.0, '00 UTC 25 Aug', fontsize=10.0)
    ax.text(-89.0, 27.5, '00 UTC 29 Aug', fontsize=10.0)
    ax.legend(loc='upper right', fontsize=5.0, handlelength=1.0)

    pdf.savefig(fig)
    plt.cla()
    plt.clf()
    plt.close()
