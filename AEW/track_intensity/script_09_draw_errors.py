import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
plt.style.use('ggplot')

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN'
dir_main = dir_CPEX + '/08_CPEX_AW_2021/track_intensity'
dir_best_track = dir_main + '/best_track'

time = '20210824'
cases_082500 = ['CON6h_Hybrid_082500', 'CON6h_Aeolus6h_Hybrid_082500', 'CON6h_DS1h_Hybrid_082500', 'CON6h_DS1h_UV_Hybrid_082500', 'CON6h_DS1h_T_Hybrid_082500', 'CON6h_DS1h_Q_Hybrid_082500']
cases_082512 = ['CON6h_Hybrid_082512', 'CON6h_Aeolus6h_Hybrid_082512', 'CON6h_DS1h_Hybrid_082512', 'CON6h_DS1h_UV_Hybrid_082512', 'CON6h_DS1h_T_Hybrid_082512', 'CON6h_DS1h_Q_Hybrid_082512']
labels = ['CON_Hybrid', 'Aeolus_Hybrid', 'DS_Hybrid', 'DS_UV_Hybrid', 'DS_T_Hybrid', 'DS_Q_Hybrid']

sns_cmap = sns.color_palette('bright')
colors = [sns_cmap[0], sns_cmap[1], sns_cmap[2], sns_cmap[3], sns_cmap[4], sns_cmap[5], sns_cmap[6], sns_cmap[7]]

domain = 'd01'
variables = {}
variables.update({'Track_Error (km)': [-100, 100, 25]})
variables.update({'MSLP_Error (hPa)': [-4,   4,   1]})
variables.update({'MWS_Error (Knot)': [-4,   4,   1]})

pdfname = dir_main + '/' + time + '/figures/Error_Hybrid.pdf'

with PdfPages(pdfname) as pdf:
    for var in variables:

        (ymin, ymax, yint) = variables[var]
        fig, axs = plt.subplots(1, 1, figsize=(9.0, 6.0))
        fig.subplots_adjust(left=0.075, bottom=0.075, right=0.975, top=0.975, wspace=0.250, hspace=0.225)
        ax = axs
        width = 0.10

        for idc in range(1, len(cases_082500)):

            f0 = dir_best_track + '/Error_' + time + '_' + cases_082500[0] + '_' + domain + '.csv'
            df0 = pd.read_csv(f0)
            err0 = np.array(df0[var][:])
            RMSE0 = np.sqrt(np.average(np.square(err0)))

            f1 = dir_best_track + '/Error_' + time + '_' + cases_082500[idc] + '_' + domain + '.csv'
            df1 = pd.read_csv(f1)
            err1 = np.array(df1[var][:])
            RMSE1 = np.sqrt(np.average(np.square(err1)))

            ax.bar(idc*0.10-0.25, RMSE0-RMSE1, width, color=colors[idc], label=labels[idc], zorder=3)

            f0 = dir_best_track + '/Error_' + time + '_' + cases_082512[0] + '_' + domain + '.csv'
            df0 = pd.read_csv(f0)
            err0 = np.array(df0[var][:])
            RMSE0 = np.sqrt(np.average(np.square(err0)))

            f1 = dir_best_track + '/Error_' + time + '_' + cases_082512[idc] + '_' + domain + '.csv'
            df1 = pd.read_csv(f1)
            err1 = np.array(df1[var][:])
            RMSE1 = np.sqrt(np.average(np.square(err1)))

            ax.bar(1.0 + idc*0.10-0.25, RMSE0-RMSE1, width, color=colors[idc], zorder=3)

        ax.set_xticks(np.arange(0, 2, 1))
        ax.set_yticks(np.arange(ymin, ymax+yint, yint))
        ax.set_xticklabels(['00 UTC 25 Aug', '12 UTC 25 Aug'])
        ax.set_xlabel('Forecast Initial Time', fontsize=10.0)
        ax.set_ylabel(var, fontsize=10.0)
        ax.tick_params('both', direction='in', labelsize=10.0)
        ax.legend(loc='upper left', fontsize=10.0, handlelength=1.0)
        ax.axis([-1, 2, ymin, ymax])

        pdf.savefig(fig)
        plt.cla()
        plt.clf()
        plt.close()
