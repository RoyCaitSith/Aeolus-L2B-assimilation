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
variables.update({'MSLP_Error (hPa)': [-4, 6, 2]})
variables.update({'MWS_Error (Knot)': [-4, 6, 2]})

cases0  = [['CON6h_Aeolus6h_082500_Hybrid_C05', 'CON6h_Aeolus6h_082500_Hybrid_C06', 'CON6h_Aeolus6h_082500_Hybrid_C07', 'CON6h_Aeolus6h_082500_Hybrid_C08'], \
           ['CON6h_Aeolus6h_082500_Hybrid_C05', 'CON6h_Aeolus6h_082500_Hybrid_C06', 'CON6h_Aeolus6h_082500_Hybrid_C07', 'CON6h_Aeolus6h_082500_Hybrid_C08'], \
           ['CON6h_Aeolus6h_082500_Hybrid_C05', 'CON6h_Aeolus6h_082500_Hybrid_C06', 'CON6h_Aeolus6h_082500_Hybrid_C07', 'CON6h_Aeolus6h_082500_Hybrid_C08']]
cases1  = [['CON6h_Aeolus6h_082500_H2_Hybrid_C05', 'CON6h_Aeolus6h_082500_H2_Hybrid_C06', 'CON6h_Aeolus6h_082500_H2_Hybrid_C07', 'CON6h_Aeolus6h_082500_H2_Hybrid_C08'], \
           ['CON6h_Aeolus6h_082500_V1_Hybrid_C05', 'CON6h_Aeolus6h_082500_V1_Hybrid_C06', 'CON6h_Aeolus6h_082500_V1_Hybrid_C07', 'CON6h_Aeolus6h_082500_V1_Hybrid_C08'], \
           ['CON6h_Aeolus6h_082500_V2_Hybrid_C05', 'CON6h_Aeolus6h_082500_V2_Hybrid_C06', 'CON6h_Aeolus6h_082500_V2_Hybrid_C07', 'CON6h_Aeolus6h_082500_V2_Hybrid_C08']]

thresholds = ['10 mm', '15 mm']
patterns = [None,  '///']

forecast_start_times = [datetime.datetime(2021, 8, 25,  0, 0, 0), datetime.datetime(2021, 8, 25,  0, 0, 0), \
                        datetime.datetime(2021, 8, 25,  0, 0, 0)]
forecast_end_times = [datetime.datetime(2021, 8, 29,  6, 0, 0), datetime.datetime(2021, 8, 29,  6, 0, 0), \
                      datetime.datetime(2021, 8, 29,  6, 0, 0)]

dir_batlow = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS/figures_V3/ScientificColourMaps7/batlow'
batlow_cm_data = np.loadtxt(dir_batlow + '/batlow.txt')
batlow_map = LinearSegmentedColormap.from_list('batlow', batlow_cm_data[::1])
colors0 = [batlow_cm_data[0], batlow_cm_data[74], batlow_cm_data[149], batlow_cm_data[223]]
colors1 = [batlow_cm_data[0], batlow_cm_data[74], batlow_cm_data[149], batlow_cm_data[223]]

dir_grayC = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS/figures_V3/ScientificColourMaps7/grayC'
grayC_cm_data = np.loadtxt(dir_grayC + '/grayC.txt')
grayC_map = LinearSegmentedColormap.from_list('grayC', grayC_cm_data[::1])

mtitle = [['(a) 2500_L2B_H2', '(e) 2500_L2B_V1', '(i) 2500_L2B_V2'], \
          ['(b) 2500_L2B_H2', '(f) 2500_L2B_V1', '(j) 2500_L2B_V2'], \
          ['(c) 2500_L2B_H2', '(g) 2500_L2B_V1', '(k) 2500_L2B_V2'], \
          ['(d) 2500_L2B_H2', '(h) 2500_L2B_V1', '(l) 2500_L2B_V2']]
mtitle_x = [[-0.9, -0.9, -0.9], [-0.9, -0.9, -0.9], [-0.9, -0.9, -0.9], [-0.9, -0.9, -0.9, -0.9]]
mtitle_y = [[67.5, 67.5, 67.5], [5.3, 5.3, 5.3, 5.3], [5.3, 5.3, 5.3, 5.3], [0.106, 0.106, 0.106, 0.106]]

pdfname = './fig08.pdf'

with PdfPages(pdfname) as pdf:

    fig_width  = 12.00
    fig_height = 12.00
    fig, axs   = plt.subplots(4, 3, figsize=(fig_width, fig_height))
    fig.subplots_adjust(left=0.075, bottom=0.025, right=0.975, top=0.975, wspace=0.250, hspace=0.100)

    for ide in range(0, 3):

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

        var = 'Track_Error (km)'
        idv = 0
        (ymin, ymax, yint) = variables[var]
        ax = axs[idv, ide]
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

            ax.bar(idc, RMSE0-RMSE1, width, color=colors1[idc], zorder=3)
            ax.text(idc, 0.0, str(round(RMSE0, 1)), ha='center', va='top', fontsize=10.0)

        ax.set_xticks(np.arange(0, 4, 1))
        ax.set_yticks(np.arange(ymin, ymax+yint, yint))
        ax.set_xticklabels(['C5', 'C6', 'C7', 'C8'])
        ax.set_ylabel('Improvement of track forecast (km)', fontsize=10.0)
        ax.tick_params('both', direction='in', labelsize=10.0)
        ax.axis([-1, 4, ymin, ymax])
        ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])
        ax.text(mtitle_x[idv][ide], mtitle_y[idv][ide], mtitle[idv][ide], fontsize=10.0)
        ax.text(2.15, 66.25, 'Improvement', fontsize=10.0)
        ax.text(2.15,-45.00, 'Degradation', fontsize=10.0)

        var = 'MSLP_Error (hPa)'
        idv = 1
        (ymin, ymax, yint) = variables[var]
        ax = axs[idv, ide]
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

            ax.bar(idc, RMSE0-RMSE1, width, color=colors1[idc], zorder=3)
            ax.text(idc, 0.0, str(round(RMSE0, 1)), ha='center', va='top', fontsize=10.0)

        ax.set_xticks(np.arange(0, 4, 1))
        ax.set_yticks(np.arange(ymin, ymax+yint, yint))
        ax.set_xticklabels(['C5', 'C6', 'C7', 'C8'])
        ax.set_ylabel('Improvement of MSLP forecast (hPa)', fontsize=10.0)
        ax.tick_params('both', direction='in', labelsize=10.0)
        ax.axis([-1, 4, ymin, ymax])
        ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])
        ax.text(mtitle_x[idv][ide], mtitle_y[idv][ide], mtitle[idv][ide], fontsize=10.0)
        ax.text(2.05,  5.3, 'Improvement', fontsize=10.0)
        ax.text(2.05, -3.6, 'Degradation', fontsize=10.0)

        var = 'MWS_Error (Knot)'
        idv = 2
        (ymin, ymax, yint) = variables[var]
        ax = axs[idv, ide]
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

            ax.bar(idc, RMSE0-RMSE1, width, color=colors1[idc], zorder=3)
            ax.text(idc, 0.0, str(round(RMSE0, 1)), ha='center', va='top', fontsize=10.0)

        ax.set_xticks(np.arange(0, 4, 1))
        ax.set_yticks(np.arange(ymin, ymax+yint, yint))
        ax.set_xticklabels(['C5', 'C6', 'C7', 'C8'])
        ax.set_ylabel('Improvement of MWS forecast (Knot)', fontsize=10.0)
        ax.tick_params('both', direction='in', labelsize=10.0)
        ax.axis([-1, 4, ymin, ymax])
        ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])
        ax.text(mtitle_x[idv][ide], mtitle_y[idv][ide], mtitle[idv][ide], fontsize=10.0)
        ax.text(2.15,  5.3, 'Improvement', fontsize=10.0)
        ax.text(2.15, -3.6, 'Degradation', fontsize=10.0)

        idv = 3
        ax = axs[idv, ide]
        width = 0.15

        n = int(len(cases0[ide]))
        for idc in range(0, n):
            for idth, thres in enumerate(thresholds):

                f0 = dir_CPEX + '/15_ENS/rainfall/' + cases0[ide][idc] + '/ETS_' + domain + '.csv'
                df0 = pd.read_csv(f0)
                err0 = np.array(df0['ETS'+str(idth+3)][0:8])
                RMSE0 = np.average(err0)
                print(RMSE0)

                f1 = dir_CPEX + '/15_ENS/rainfall/' + cases1[ide][idc] + '/ETS_' + domain + '.csv'
                df1 = pd.read_csv(f1)
                err1 = np.array(df1['ETS'+str(idth+3)][0:8])
                RMSE1 = np.average(err1)
                print(RMSE1)

                if ide == 3 and idc == 0:
                    ax.bar(idc-0.75*width+(idth+idth*0.5)*width, RMSE1-RMSE0, width, color=colors1[idc], label=str(thres), hatch=patterns[idth], zorder=3)
                    plt.rcParams['hatch.color'] = 'w'
                else:
                    ax.bar(idc-0.75*width+(idth+idth*0.5)*width, RMSE1-RMSE0, width, color=colors1[idc], hatch=patterns[idth], zorder=3)
                    plt.rcParams['hatch.color'] = 'w'

        ax.set_xticks(np.arange(0, 4, 1))
        ax.set_yticks(np.arange(-0.08, 0.121, 0.04))
        ax.set_xticklabels(['C5', 'C6', 'C7', 'C8'])
        ax.set_ylabel('Improvement of ETS', fontsize=10.0)
        ax.tick_params('both', direction='in', labelsize=10.0)
        ax.axis([-1, 4, -0.08, 0.120])
        ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])
        ax.text(mtitle_x[idv][ide], mtitle_y[idv][ide], mtitle[idv][ide], fontsize=10.0)
        ax.text(2.10,  0.106, 'Improvement', fontsize=10.0)
        ax.text(2.10, -0.072, 'Degradation', fontsize=10.0)
        if ide == 3: ax.legend(loc='lower left', fontsize=7.5, handlelength=2.5).set_zorder(102)

    plt.savefig('./fig08.png', dpi=300)
    pdf.savefig(fig)
    plt.cla()
    plt.clf()
    plt.close()
