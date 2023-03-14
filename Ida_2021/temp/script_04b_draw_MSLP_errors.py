import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
plt.style.use('ggplot')

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN'
dir_main = dir_CPEX + '/15_ENS/track_intensity'
dir_best_track = dir_main + '/best_track'

#cases  = ['CON6h_082406_Hybrid_C05', 'CON6h_082406_Hybrid_C06', 'CON6h_082406_Hybrid_C07', 'CON6h_082406_Hybrid_C08']
#labels = ['082406_C05', '082406_C06', '082406_C07', '082406_C08']
#cases  = ['CON6h_082412_Hybrid_C05', 'CON6h_082412_Hybrid_C06', 'CON6h_082412_Hybrid_C07', 'CON6h_082412_Hybrid_C08']
#labels = ['082412_C05', '082412_C06', '082412_C07', '082412_C08']
#cases  = ['CON6h_082418_Hybrid_C05', 'CON6h_082418_Hybrid_C06', 'CON6h_082418_Hybrid_C07', 'CON6h_082418_Hybrid_C08']
#labels = ['082418_C05', '082418_C06', '082418_C07', '082418_C08']
cases  = ['CON6h_082500_Hybrid_C05', 'CON6h_082500_Hybrid_C06', 'CON6h_082500_Hybrid_C07', 'CON6h_082500_Hybrid_C08']
labels = ['082500_C05', '082500_C06', '082500_C07', '082500_C08']
#cases_Aeolus  = ['CON6h_Aeolus6h_082406_Hybrid_C05', 'CON6h_Aeolus6h_082406_Hybrid_C06', 'CON6h_Aeolus6h_082406_Hybrid_C07', 'CON6h_Aeolus6h_082406_Hybrid_C08']
#labels_Aeolus = ['Aeolus_082406_C05', 'Aeolus_082406_C06', 'Aeolus_082406_C07', 'Aeolus_082406_C08']
#cases_Aeolus  = ['CON6h_Aeolus6h_082412_Hybrid_C05', 'CON6h_Aeolus6h_082412_Hybrid_C06', 'CON6h_Aeolus6h_082412_Hybrid_C07', 'CON6h_Aeolus6h_082412_Hybrid_C08']
#labels_Aeolus = ['Aeolus_082412_C05', 'Aeolus_082412_C06', 'Aeolus_082412_C07', 'Aeolus_082412_C08']
#cases_Aeolus  = ['CON6h_Aeolus6h_082418_Hybrid_C05', 'CON6h_Aeolus6h_082418_Hybrid_C06', 'CON6h_Aeolus6h_082418_Hybrid_C07', 'CON6h_Aeolus6h_082418_Hybrid_C08']
#labels_Aeolus = ['Aeolus_082418_C05', 'Aeolus_082418_C06', 'Aeolus_082418_C07', 'Aeolus_082418_C08']
cases_Aeolus  = ['CON6h_Aeolus6h_082500_Hybrid_C05', 'CON6h_Aeolus6h_082500_Hybrid_C06', 'CON6h_Aeolus6h_082500_Hybrid_C07', 'CON6h_Aeolus6h_082500_Hybrid_C08']
labels_Aeolus = ['Aeolus_082500_C05', 'Aeolus_082500_C06', 'Aeolus_082500_C07', 'Aeolus_082500_C08']

sns_cmap = sns.color_palette('Paired')
colors = [sns_cmap[1], sns_cmap[3], sns_cmap[5], sns_cmap[7]]

domain = 'd01'
variables = {}
variables.update({'MSLP_Error (hPa)': [-6, 6, 2]})

#pdfname = './Figure_04b_Comparison_MSLP_082406.pdf'
#pdfname = './Figure_04d_Comparison_MSLP_082412.pdf'
#pdfname = './Figure_04f_Comparison_MSLP_082418.pdf'
pdfname = './Figure_04h_Comparison_MSLP_082500.pdf'

with PdfPages(pdfname) as pdf:
    for var in variables:

        (ymin, ymax, yint) = variables[var]
        fig, axs = plt.subplots(1, 1, figsize=(6.0, 6.0))
        fig.subplots_adjust(left=0.125, bottom=0.075, right=0.975, top=0.975, wspace=0.250, hspace=0.225)
        ax = axs
        width = 0.15

        n = int(len(cases))
        for idc in range(0, n):

            f0 = dir_best_track + '/Error_' + cases[idc] + '_' + domain + '.csv'
            df0 = pd.read_csv(f0)
            err0 = np.array(df0[var][-10:-1])
            RMSE0 = np.sqrt(np.average(np.square(err0)))
            print(RMSE0)

            f1 = dir_best_track + '/Error_' + cases_Aeolus[idc] + '_' + domain + '.csv'
            df1 = pd.read_csv(f1)
            err1 = np.array(df1[var][-10:-1])
            RMSE1 = np.sqrt(np.average(np.square(err1)))
            print(RMSE1)

            ax.bar(idc, RMSE0-RMSE1, width, color=colors[idc], label=labels_Aeolus[idc], zorder=3)

        ax.set_xticks(np.arange(0, 4, 1))
        ax.set_yticks(np.arange(ymin, ymax+yint, yint))
        #ax.set_xticklabels(['C05: 12 UTC 25 Aug', 'C06: 18 UTC 25 Aug', 'C07: 00 UTC 26 Aug', 'C08: 06 UTC 26 Aug'])
        #ax.set_xticklabels(['C05: 18 UTC 25 Aug', 'C06: 00 UTC 26 Aug', 'C07: 06 UTC 26 Aug', 'C08: 12 UTC 26 Aug'])
        #ax.set_xticklabels(['C05: 00 UTC 26 Aug', 'C06: 06 UTC 26 Aug', 'C07: 12 UTC 26 Aug', 'C08: 18 UTC 26 Aug'])
        #ax.set_xticklabels(['C05: 06 UTC 26 Aug', 'C06: 12 UTC 26 Aug', 'C07: 18 UTC 26 Aug', 'C08: 00 UTC 27 Aug'])
        #ax.set_xlabel('Forecast Initial Time', fontsize=10.0)
        ax.set_xticklabels(['C05', 'C06', 'C07', 'C08'])
        ax.set_ylabel('Improvement of 48-h MSLP Forecast (hPa)', fontsize=10.0)
        ax.tick_params('both', direction='in', labelsize=10.0)
        ax.legend(loc='lower right', fontsize=10.0, handlelength=1.0)
        ax.axis([-1, 4, ymin, ymax])

        pdf.savefig(fig)
        plt.cla()
        plt.clf()
        plt.close()
