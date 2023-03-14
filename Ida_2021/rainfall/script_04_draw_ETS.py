import os
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from wrf import getvar
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_pdf import PdfPages

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS'
dir_best_track = '/'.join([dir_CPEX, 'track_intensity', 'best_track'])
dir_main = dir_CPEX + '/rainfall'

domains = ['d01']
cycling_interval = 6
n_time = 9
box = 500.0
thresholds = [1.0, 5.0, 10.0, 15.0]

#cases = ['CON6h_082406_Hybrid_C05', 'CON6h_082406_Hybrid_C06', 'CON6h_082406_Hybrid_C07', 'CON6h_082406_Hybrid_C08']
#cases = ['CON6h_Aeolus6h_082406_Hybrid_C05', 'CON6h_Aeolus6h_082406_Hybrid_C06', 'CON6h_Aeolus6h_082406_Hybrid_C07', 'CON6h_Aeolus6h_082406_Hybrid_C08']
#cases = ['CON6h_082412_Hybrid_C05', 'CON6h_082412_Hybrid_C06', 'CON6h_082412_Hybrid_C07', 'CON6h_082412_Hybrid_C08']
#cases = ['CON6h_Aeolus6h_082412_Hybrid_C05', 'CON6h_Aeolus6h_082412_Hybrid_C06', 'CON6h_Aeolus6h_082412_Hybrid_C07', 'CON6h_Aeolus6h_082412_Hybrid_C08']
#cases = ['CON6h_082418_Hybrid_C05', 'CON6h_082418_Hybrid_C06', 'CON6h_082418_Hybrid_C07', 'CON6h_082418_Hybrid_C08']
#cases = ['CON6h_Aeolus6h_082418_Hybrid_C05', 'CON6h_Aeolus6h_082418_Hybrid_C06', 'CON6h_Aeolus6h_082418_Hybrid_C07', 'CON6h_Aeolus6h_082418_Hybrid_C08']
#cases = ['CON6h_082500_Hybrid_C05', 'CON6h_082500_Hybrid_C06', 'CON6h_082500_Hybrid_C07', 'CON6h_082500_Hybrid_C08']
cases = ['CON6h_Aeolus6h_082500_Hybrid_C05', 'CON6h_Aeolus6h_082500_Hybrid_C06', 'CON6h_Aeolus6h_082500_Hybrid_C07', 'CON6h_Aeolus6h_082500_Hybrid_C08']

#forecast_start_time = datetime.datetime(2021, 8, 25, 15, 0, 0)
#forecast_start_time = datetime.datetime(2021, 8, 25, 21, 0, 0)
#forecast_start_time = datetime.datetime(2021, 8, 26,  3, 0, 0)
#forecast_start_time = datetime.datetime(2021, 8, 26,  9, 0, 0)
file_best_track = dir_best_track + '/2021_09L_Ida.csv'

for dom in domains:
    for idc, case in enumerate(cases):

        filename = dir_main + '/' + case + '/ETS_' + dom + '.csv'
        pdfname = dir_main + '/' + case + '/ETS_' + dom + '.pdf'
        ETS_df = pd.read_csv(filename)

        with PdfPages(pdfname) as pdf:

            fig, axs = plt.subplots(1, 1, figsize=(6.0, 6.0))
            fig.subplots_adjust(left=0.075, bottom=0.075, right=0.975, top=0.975, wspace=0.250, hspace=0.225)

            ax = axs

            for idth, thres in enumerate(thresholds):

                ETS = np.array(ETS_df['ETS'+str(idth+1)][:])
                ax.plot(np.arange(n_time), ETS, label=str(thres))

            ax.axis([0, 8, 0.0, 0.60])
            ax.legend(loc='upper right')

            plt.savefig(dir_main + '/' + case + '/ETS_' + dom + '.png', dpi=600)
            pdf.savefig(fig)
            plt.cla()
            plt.clf()
            plt.close()
