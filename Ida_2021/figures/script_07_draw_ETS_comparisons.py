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
dir_main = dir_CPEX + '/15_ENS/rainfall'
domain = 'd01'

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
thresholds = ['10 mm', '15 mm']
patterns = [None,  '///']

forecast_start_times = [datetime.datetime(2021, 8, 24,  6, 0, 0), datetime.datetime(2021, 8, 24, 12, 0, 0), \
                        datetime.datetime(2021, 8, 24, 18, 0, 0), datetime.datetime(2021, 8, 25,  0, 0, 0)]
forecast_end_times = [datetime.datetime(2021, 8, 28, 12, 0, 0), datetime.datetime(2021, 8, 28, 18, 0, 0), \
                      datetime.datetime(2021, 8, 29,  0, 0, 0), datetime.datetime(2021, 8, 29,  6, 0, 0)]

dir_batlow = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS/figures_V3/ScientificColourMaps7/batlow'
batlow_cm_data = np.loadtxt(dir_batlow + '/batlow.txt')
batlow_map = LinearSegmentedColormap.from_list('batlow', batlow_cm_data[::1])
#colors1 = [batlow_cm_data[0], batlow_cm_data[57], batlow_cm_data[113], batlow_cm_data[170]]
#colors1 = [batlow_cm_data[0], batlow_cm_data[64], batlow_cm_data[128], batlow_cm_data[191]]
colors1 = [batlow_cm_data[0], batlow_cm_data[74], batlow_cm_data[149], batlow_cm_data[223]]
#colors1 = [batlow_cm_data[74], batlow_cm_data[223]]

dir_grayC = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS/figures_V3/ScientificColourMaps7/grayC'
grayC_cm_data = np.loadtxt(dir_grayC + '/grayC.txt')
grayC_map = LinearSegmentedColormap.from_list('grayC', grayC_cm_data[::1])

mtitle = ['(a)', '(b)', '(c)', '(d)']
mtitle_x = [-0.9, -0.9, -0.9, -0.9]
mtitle_y = [0.106, 0.106, 0.106, 0.106]

pdfname = './fig07.pdf'

with PdfPages(pdfname) as pdf:

    fig_width  = 6.50
    fig_height = 6.00
    fig, axs   = plt.subplots(2, 2, figsize=(fig_width, fig_height))
    fig.subplots_adjust(left=0.125, bottom=0.0375, right=0.975, top=0.975, wspace=0.200, hspace=0.100)

    for ide in range(0, 4):

        irow = ide//2
        icol = ide%2

        ax = axs[irow, icol]
        width = 0.15

        n = int(len(cases0[ide]))
        for idc in range(0, n):
            for idth, thres in enumerate(thresholds):

                f0 = dir_main + '/' + cases0[ide][idc] + '/ETS_' + domain + '.csv'
                df0 = pd.read_csv(f0)
                err0 = np.array(df0['ETS'+str(idth+3)][0:8])
                RMSE0 = np.average(err0)
                print(RMSE0)

                f1 = dir_main + '/' + cases1[ide][idc] + '/ETS_' + domain + '.csv'
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
        if icol == 0: ax.set_ylabel('Improvement of ETS', fontsize=10.0)
        ax.tick_params('both', direction='in', labelsize=10.0)
        ax.axis([-1, 4, -0.08, 0.120])
        ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])
        ax.text(mtitle_x[ide], mtitle_y[ide], mtitle[ide], fontsize=10.0)
        ax.text(2.10,  0.106, 'Improvement', fontsize=10.0)
        ax.text(2.10, -0.072, 'Degradation', fontsize=10.0)
        if ide == 3: ax.legend(loc='lower left', fontsize=7.5, handlelength=2.5).set_zorder(102)

    plt.savefig('./fig07.png', dpi=300)
    pdf.savefig(fig)
    plt.cla()
    plt.clf()
    plt.close()
