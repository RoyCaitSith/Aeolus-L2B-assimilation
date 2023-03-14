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
variables.update({'MWS_Error (Knot)': [-4, 6, 2]})

cases0  = [['CON6h_Aeolus6h_082500_Hybrid_C05', 'CON6h_Aeolus6h_082500_Hybrid_C06', 'CON6h_Aeolus6h_082500_Hybrid_C07', 'CON6h_Aeolus6h_082500_Hybrid_C08'], \
           ['CON6h_Aeolus6h_082500_Hybrid_C05', 'CON6h_Aeolus6h_082500_Hybrid_C06', 'CON6h_Aeolus6h_082500_Hybrid_C07', 'CON6h_Aeolus6h_082500_Hybrid_C08'], \
           ['CON6h_Aeolus6h_082500_Hybrid_C05', 'CON6h_Aeolus6h_082500_Hybrid_C06', 'CON6h_Aeolus6h_082500_Hybrid_C07', 'CON6h_Aeolus6h_082500_Hybrid_C08'], \
           ['CON6h_Aeolus6h_082500_Hybrid_C05', 'CON6h_Aeolus6h_082500_Hybrid_C06', 'CON6h_Aeolus6h_082500_Hybrid_C07', 'CON6h_Aeolus6h_082500_Hybrid_C08']]
cases1  = [['CON6h_Aeolus6h_082500_H2_Hybrid_C05', 'CON6h_Aeolus6h_082500_H2_Hybrid_C06', 'CON6h_Aeolus6h_082500_H2_Hybrid_C07', 'CON6h_Aeolus6h_082500_H2_Hybrid_C08'], \
           ['CON6h_Aeolus6h_082500_H2_Hybrid_C05', 'CON6h_Aeolus6h_082500_H2_Hybrid_C06', 'CON6h_Aeolus6h_082500_H2_Hybrid_C07', 'CON6h_Aeolus6h_082500_H2_Hybrid_C08'], \
           ['CON6h_Aeolus6h_082500_V1_Hybrid_C05', 'CON6h_Aeolus6h_082500_V1_Hybrid_C06', 'CON6h_Aeolus6h_082500_V1_Hybrid_C07', 'CON6h_Aeolus6h_082500_V1_Hybrid_C08'], \
           ['CON6h_Aeolus6h_082500_V2_Hybrid_C05', 'CON6h_Aeolus6h_082500_V2_Hybrid_C06', 'CON6h_Aeolus6h_082500_V2_Hybrid_C07', 'CON6h_Aeolus6h_082500_V2_Hybrid_C08']]

labels0 = ['2500_L2B', '2500_L2B', '2500_L2B', '2500_L2B']
labels1 = ['2500_L2B_H2', '2500_L2B_H2', '2500_L2B_V1', '2500_L2B_V2']

forecast_start_times = [datetime.datetime(2021, 8, 25,  0, 0, 0), datetime.datetime(2021, 8, 25,  0, 0, 0), \
                        datetime.datetime(2021, 8, 25,  0, 0, 0), datetime.datetime(2021, 8, 25,  0, 0, 0)]
forecast_end_times = [datetime.datetime(2021, 8, 29,  6, 0, 0), datetime.datetime(2021, 8, 29,  6, 0, 0), \
                      datetime.datetime(2021, 8, 29,  6, 0, 0), datetime.datetime(2021, 8, 29,  6, 0, 0)]

dir_batlow = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS/figures_V3/ScientificColourMaps7/batlow'
batlow_cm_data = np.loadtxt(dir_batlow + '/batlow.txt')
batlow_map = LinearSegmentedColormap.from_list('batlow', batlow_cm_data[::1])
colors0 = [batlow_cm_data[0], batlow_cm_data[74], batlow_cm_data[149], batlow_cm_data[223]]
colors1 = [batlow_cm_data[0], batlow_cm_data[74], batlow_cm_data[149], batlow_cm_data[223]]

dir_grayC = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS/figures_V3/ScientificColourMaps7/grayC'
grayC_cm_data = np.loadtxt(dir_grayC + '/grayC.txt')
grayC_map = LinearSegmentedColormap.from_list('grayC', grayC_cm_data[::1])

xticklables = [['', '', '', '27', '', '', '', '28', '', '', '', '29'], \
               ['', '', '', '27', '', '', '', '28', '', '', '', '29'], \
               ['', '', '', '27', '', '', '', '28', '', '', '', '29'], \
               ['', '', '', '27', '', '', '', '28', '', '', '', '29']]

mtitle1 = ['(a)', '(b)', '(c)', '(d)']
mtitle1_x = [10.10, 10.10, 10.10, 10.10]
mtitle1_y = [24.75, 24.75, 24.75, 24.75]
mtitle2 = ['(e)', '(f)', '(g)', '(h)']
mtitle2_x = [-0.9, -0.9, -0.9, -0.9]
mtitle2_y = [5.3, 5.3, 5.3, 5.3]

pdfname = './fig99.pdf'

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

        MWS_bt = list(df['MWS (Knot)'][index])
        idx_forecast_start_time_min = int((24-float(forecast_start_time_min.strftime('%H')))%24/6)

        ax = axs[ide, 0]
        ax.plot(np.arange(len(MWS_bt)-1), MWS_bt[:-1], 'o', color='k', ls='-', ms=4.00, linewidth=2.50, label='NHC', zorder=3)
        ax.plot(np.arange(idx_forecast_start_time_min, len(MWS_bt)-1, 4), MWS_bt[idx_forecast_start_time_min:-1:4], 'o', color='w', ms=1.50, zorder=3)

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
                if time_now == forecast_start_time_cycle: str_index = idx
            str_index = index[0] - str_index + idc

            MWS = list(df['MWS (Knot)'][index])
            idx_forecast_start_time_cycle = int((24-float(forecast_start_time_cycle.strftime('%H')))%24/6)

            if idc == 3:
                ax.plot(np.arange(str_index, str_index+len(MWS)-1), MWS[:-1], 'o', color='k', ls='--', ms=2.00, linewidth=1.25, label=labels0[ide], zorder=3)
            #else:
                #ax.plot(np.arange(str_index, str_index+len(MWS)-1), MWS[:-1], 'o', color=colors0[idc], ls='--', ms=2.00, linewidth=1.25, zorder=3)
            ax.plot(np.arange(str_index, str_index+len(MWS)-1), MWS[:-1], 'o', color=colors0[idc], ls='--', ms=2.00, linewidth=1.25, zorder=3)
            ax.plot(np.arange(str_index+idx_forecast_start_time_cycle, str_index+len(MWS)-1, 4), MWS[idx_forecast_start_time_cycle:-1:4], 'o', color='w', ms=0.75, zorder=3)

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
                if time_now == forecast_start_time_cycle: str_index = idx
            str_index = index[0] - str_index + idc

            MWS = list(df['MWS (Knot)'][index])
            idx_forecast_start_time_cycle = int((24-float(forecast_start_time_cycle.strftime('%H')))%24/6)

            if idc == 3:
                ax.plot(np.arange(str_index, str_index+len(MWS)-1), MWS[:-1], 'o', color='k', ls='-', ms=2.00, linewidth=1.25, label=labels1[ide], zorder=3)
            #else:
                #ax.plot(np.arange(str_index, str_index+len(MWS)-1), MWS[:-1], 'o', color=colors1[idc], ls='-', ms=2.00, linewidth=1.25, zorder=3)
            ax.plot(np.arange(str_index, str_index+len(MWS)-1), MWS[:-1], 'o', color=colors1[idc], ls='-', ms=2.00, linewidth=1.25, zorder=3)
            ax.plot(np.arange(str_index+idx_forecast_start_time_cycle, str_index+len(MWS)-1, 4), MWS[idx_forecast_start_time_cycle:-1:4], 'o', color='w', ms=0.75, zorder=3)

        extent = [0, len(MWS_bt)-2, 22.5, 97.5]

        ax.set_xticks(np.arange(0, len(MWS_bt)-1, 1))
        ax.set_xticklabels(xticklables[ide])
        ax.set_yticks(np.arange(extent[2]+7.5, extent[3]+1, 15.0))
        ax.set_ylabel('Time', fontsize=10.0)
        ax.set_ylabel('MWS (Knot)', fontsize=10.0)
        ax.tick_params('both', direction='in', labelsize=10.0)
        ax.axis(extent)
        ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])
        ax.text(mtitle1_x[ide], mtitle1_y[ide], mtitle1[ide], fontsize=10.0)
        ax.legend(loc='upper left', fontsize=7.5, handlelength=2.5).set_zorder(102)

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
        ax.set_ylabel('Improvement of MWS forecast (Knot)', fontsize=10.0)
        ax.tick_params('both', direction='in', labelsize=10.0)
        ax.axis([-1, 4, ymin, ymax])
        ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])
        ax.text(mtitle2_x[ide], mtitle2_y[ide], mtitle2[ide], fontsize=10.0)
        ax.text(2.15,  5.3, 'Improvement', fontsize=10.0)
        ax.text(2.15, -3.6, 'Degradation', fontsize=10.0)
        #ax.legend(loc='lower left', fontsize=7.5, handlelength=2.5).set_zorder(102)

    plt.savefig('./fig99.png', dpi=300)
    pdf.savefig(fig)
    plt.cla()
    plt.clf()
    plt.close()
