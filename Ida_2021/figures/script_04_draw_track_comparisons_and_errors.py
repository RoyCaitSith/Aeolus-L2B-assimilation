import os
import re
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.basemap import Basemap
#plt.style.use('ggplot')

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN'
dir_main = dir_CPEX + '/15_ENS/track_intensity'
dir_best_track = dir_main + '/best_track'
file_best_track = dir_best_track + '/2021_09L_Ida.csv'
domain = 'd01'

variables = {}
variables.update({'Track_Error (km)': [-50, 75, 25]})

cases0  = [['CON6h_082406_Hybrid_C05', 'CON6h_082406_Hybrid_C06', 'CON6h_082406_Hybrid_C07', 'CON6h_082406_Hybrid_C08'], \
           ['CON6h_082412_Hybrid_C05', 'CON6h_082412_Hybrid_C06', 'CON6h_082412_Hybrid_C07', 'CON6h_082412_Hybrid_C08'], \
           ['CON6h_082418_Hybrid_C05', 'CON6h_082418_Hybrid_C06', 'CON6h_082418_Hybrid_C07', 'CON6h_082418_Hybrid_C08'], \
           ['CON6h_082500_Hybrid_C05', 'CON6h_082500_Hybrid_C06', 'CON6h_082500_Hybrid_C07', 'CON6h_082500_Hybrid_C08']]
cases1  = [['CON6h_Aeolus6h_082406_Hybrid_C05', 'CON6h_Aeolus6h_082406_Hybrid_C06', 'CON6h_Aeolus6h_082406_Hybrid_C07', 'CON6h_Aeolus6h_082406_Hybrid_C08'], \
           ['CON6h_Aeolus6h_082412_Hybrid_C05', 'CON6h_Aeolus6h_082412_Hybrid_C06', 'CON6h_Aeolus6h_082412_Hybrid_C07', 'CON6h_Aeolus6h_082412_Hybrid_C08'], \
           ['CON6h_Aeolus6h_082418_Hybrid_C05', 'CON6h_Aeolus6h_082418_Hybrid_C06', 'CON6h_Aeolus6h_082418_Hybrid_C07', 'CON6h_Aeolus6h_082418_Hybrid_C08'], \
           ['CON6h_Aeolus6h_082500_Hybrid_C05', 'CON6h_Aeolus6h_082500_Hybrid_C06', 'CON6h_Aeolus6h_082500_Hybrid_C07', 'CON6h_Aeolus6h_082500_Hybrid_C08']]

labels0 = ['2406', '2412', '2418', '2500']
labels1 = ['2406_L2B', '2412_L2B', '2418_L2B', '2500_L2B']

forecast_start_times = [datetime.datetime(2021, 8, 24,  6, 0, 0), datetime.datetime(2021, 8, 24, 12, 0, 0), \
                        datetime.datetime(2021, 8, 24, 18, 0, 0), datetime.datetime(2021, 8, 25,  0, 0, 0)]
forecast_end_times = [datetime.datetime(2021, 8, 28, 12, 0, 0), datetime.datetime(2021, 8, 28, 18, 0, 0), \
                      datetime.datetime(2021, 8, 29,  0, 0, 0), datetime.datetime(2021, 8, 29,  6, 0, 0)]

extents = [[-87.5, -72.5, 10.0, 25.0], [-90.0, -75.0, 10.0, 25.0], [-90.0, -75.0, 12.0, 27.0], [-91.5, -76.5, 13.0, 28.0]]

dir_batlow = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS/figures_V3/ScientificColourMaps7/batlow'
batlow_cm_data = np.loadtxt(dir_batlow + '/batlow.txt')
batlow_map = LinearSegmentedColormap.from_list('batlow', batlow_cm_data[::1])
colors0 = [batlow_cm_data[0], batlow_cm_data[74], batlow_cm_data[149], batlow_cm_data[223]]
colors1 = [batlow_cm_data[0], batlow_cm_data[74], batlow_cm_data[149], batlow_cm_data[223]]

dir_grayC = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS/figures_V3/ScientificColourMaps7/grayC'
grayC_cm_data = np.loadtxt(dir_grayC + '/grayC.txt')
grayC_map = LinearSegmentedColormap.from_list('grayC', grayC_cm_data[::1])

start_times = ['12 UTC 25 Aug', '18 UTC 25 Aug', '00 UTC 26 Aug', '06 UTC 26 Aug']
end_times = ['06 UTC 28 Aug', '12 UTC 28 Aug', '18 UTC 28 Aug', '00 UTC 29 Aug']

mtitle1 = ['(a)', '(b)', '(c)', '(d)']
mtitle1_lons = [-87.25, -89.75, -89.75, -91.25]
mtitle1_lats = [24.0, 24.0, 26.0, 27.0]
mtitle2 = ['(e)', '(f)', '(g)', '(h)']
mtitle2_x = [-0.9, -0.9, -0.9, -0.9]
mtitle2_y = [67.5, 67.5, 67.5, 67.5]

pdfname = './fig04.pdf'

with PdfPages(pdfname) as pdf:

    fig_width  = 6.50
    fig_height = 12.00
    fig, axs   = plt.subplots(4, 2, figsize=(fig_width, fig_height))
    fig.subplots_adjust(left=0.075, bottom=0.025, right=0.975, top=0.975, wspace=0.250, hspace=0.100)

    for ide in range(0, 4):

        df = pd.read_csv(file_best_track)
        forecast_start_time_min = forecast_start_times[ide] + datetime.timedelta(hours=6.0*int(cases0[ide][0][-2:]))

        index = []
        for idx, Date_Time in enumerate(df['Date_Time']):
            time_now = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
            if time_now >= forecast_start_time_min and time_now <= forecast_end_times[ide]: index = index + [idx]

        lat = list(df['Latitude'][index])
        lon = list(df['Longitude'][index])
        TC_dd = list(df['Date_Time'][index])
        TC_dd = [x[8:10] for x in TC_dd]
        idx_forecast_start_time_min = int((24-float(forecast_start_time_min.strftime('%H')))%24/6)

        ax = axs[ide, 0]
        m = Basemap(projection='cyl', llcrnrlat=extents[ide][2], llcrnrlon=extents[ide][0], urcrnrlat=extents[ide][3], urcrnrlon=extents[ide][1], resolution='h', ax=ax)
        m.drawcoastlines(linewidth=0.2, color='k')
        ax.plot(lon[:-1], lat[:-1], 'o', color='k', ls='-', ms=4.00, linewidth=2.50, label='NHC', zorder=3)
        ax.plot(lon[idx_forecast_start_time_min:-1:4], lat[idx_forecast_start_time_min:-1:4], 'o', color='w', ms=1.50, zorder=3)
        for (TCdate, TClon, TClat) in zip(TC_dd[idx_forecast_start_time_min:-1:4], lon[idx_forecast_start_time_min:-1:4], lat[idx_forecast_start_time_min:-1:4]):
            ax.text(TClon+0.50, TClat+0.50, TCdate, ha='center', va='center', color='k', fontsize=10.0, zorder=4)

        for idc, case0 in enumerate(cases0[ide]):

            casename = case0 + '_' + domain
            filename = dir_main + '/best_track/' + casename + '.csv'

            df = pd.read_csv(filename)
            print(df)

            forecast_start_time_cycle = forecast_start_times[ide] + datetime.timedelta(hours=6.0*int(case0[-2:]))

            index = []
            for idx, Date_Time in enumerate(df['Date_Time']):
                time_now = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
                if time_now >= forecast_start_time_cycle and time_now <= forecast_end_times[ide]: index = index + [idx]

            lat = list(df['Latitude'][index])
            lon = list(df['Longitude'][index])
            idx_forecast_start_time_cycle = int((24-float(forecast_start_time_cycle.strftime('%H')))%24/6)

            if idc == 3:
                ax.plot(lon[:-1:], lat[:-1:], 'o', color='k', ls='--', ms=2.00, linewidth=1.25, label=labels0[ide], zorder=3)
            #else:
                #ax.plot(lon[:-1:], lat[:-1:], 'o', color=colors0[idc], ls='--', ms=2.00, linewidth=1.25, zorder=3)
            ax.plot(lon[:-1:], lat[:-1:], 'o', color=colors0[idc], ls='--', ms=2.00, linewidth=1.25, zorder=3)
            ax.plot(lon[idx_forecast_start_time_cycle:-1:4], lat[idx_forecast_start_time_cycle:-1:4], 'o', color='w', ms=0.75, zorder=3)

        for idc, case1 in enumerate(cases1[ide]):

            casename = case1 + '_' + domain
            filename = dir_main + '/best_track/' + casename + '.csv'

            df = pd.read_csv(filename)
            print(df)

            forecast_start_time_cycle = forecast_start_times[ide] + datetime.timedelta(hours=6.0*int(case1[-2:]))

            index = []
            for idx, Date_Time in enumerate(df['Date_Time']):
                time_now = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
                if time_now >= forecast_start_time_cycle and time_now <= forecast_end_times[ide]: index = index + [idx]

            lat = list(df['Latitude'][index])
            lon = list(df['Longitude'][index])
            idx_forecast_start_time_cycle = int((24-float(forecast_start_time_cycle.strftime('%H')))%24/6)

            if idc == 3:
                ax.plot(lon[:-1:], lat[:-1:], 'o', color='k', ls='-', ms=2.00, linewidth=1.25, label=labels1[ide], zorder=3)
            #else:
                #ax.plot(lon[:-1:], lat[:-1:], 'o', color=colors1[idc], ls='-', ms=2.00, linewidth=1.25, zorder=3)
            ax.plot(lon[:-1:], lat[:-1:], 'o', color=colors1[idc], ls='-', ms=2.00, linewidth=1.25, zorder=3)
            ax.plot(lon[idx_forecast_start_time_cycle:-1:4], lat[idx_forecast_start_time_cycle:-1:4], 'o', color='w', ms=0.75, zorder=3)

        ax.set_xticks(np.arange(-90, -49, 5))
        ax.set_xticklabels(['$\mathrm{90^{\circ}\ W}$', '$\mathrm{85^{\circ}\ W}$', '$\mathrm{80^{\circ}\ W}$', \
                            '$\mathrm{75^{\circ}\ W}$', '$\mathrm{70^{\circ}\ W}$', '$\mathrm{65^{\circ}\ W}$', \
                            '$\mathrm{60^{\circ}\ W}$', '$\mathrm{55^{\circ}\ W}$', '$\mathrm{50^{\circ}\ W}$'])
        ax.set_yticks(np.arange(10, 36, 5))
        ax.set_yticklabels(['$\mathrm{10^{\circ}\ W}$', '$\mathrm{15^{\circ}\ W}$', '$\mathrm{20^{\circ}\ W}$', \
                            '$\mathrm{25^{\circ}\ W}$', '$\mathrm{30^{\circ}\ W}$', '$\mathrm{35^{\circ}\ W}$'])
        ax.tick_params('both', direction='in', labelsize=10.0)
        ax.axis(extents[ide])
        ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])
        ax.text(mtitle1_lons[ide], mtitle1_lats[ide], mtitle1[ide], fontsize=10.0)
        ax.legend(loc='lower left', fontsize=7.5, handlelength=2.5).set_zorder(102)

        for var in variables:

            (ymin, ymax, yint) = variables[var]
            ax = axs[ide, 1]
            width = 0.15

            n = int(len(cases0[ide]))
            for idc in range(0, n):

                f0 = dir_best_track + '/Error_' + cases0[ide][idc] + '_' + domain + '.csv'
                df0 = pd.read_csv(f0)
                err0 = np.array(df0[var][-10:-1])
                RMSE0 = np.sqrt(np.average(np.square(err0)))
                print(RMSE0)

                f1 = dir_best_track + '/Error_' + cases1[ide][idc] + '_' + domain + '.csv'
                df1 = pd.read_csv(f1)
                err1 = np.array(df1[var][-10:-1])
                RMSE1 = np.sqrt(np.average(np.square(err1)))
                print(RMSE1)

                #if idc == 3:
                    #ax.bar(idc, RMSE0-RMSE1, width, color=colors1[idc], label=labels1[ide], zorder=3)
                #else:
                    #ax.bar(idc, RMSE0-RMSE1, width, color=colors1[idc], zorder=3)
                ax.bar(idc, RMSE0-RMSE1, width, color=colors1[idc], zorder=3)
                ax.text(idc, 0.0, str(round(RMSE0, 1)), ha='center', va='top', fontsize=10.0)

        ax.set_xticks(np.arange(0, 4, 1))
        ax.set_yticks(np.arange(ymin, ymax+yint, yint))
        ax.set_xticklabels(['C5', 'C6', 'C7', 'C8'])
        ax.set_ylabel('Improvement of track forecast (km)', fontsize=10.0)
        ax.tick_params('both', direction='in', labelsize=10.0)
        ax.axis([-1, 4, ymin, ymax])
        ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])
        ax.text(mtitle2_x[ide], mtitle2_y[ide], mtitle2[ide], fontsize=10.0)
        ax.text(2.15, 66.25, 'Improvement', fontsize=10.0)
        ax.text(2.15,-45.00, 'Degradation', fontsize=10.0)
        #ax.legend(loc='lower left', fontsize=7.5, handlelength=2.5).set_zorder(102)

    plt.savefig('./fig04.png', dpi=300)
    pdf.savefig(fig)
    plt.cla()
    plt.clf()
    plt.close()
