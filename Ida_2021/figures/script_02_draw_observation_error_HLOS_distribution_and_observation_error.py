import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import matplotlib.ticker as ticker
from matplotlib.gridspec import GridSpec
from scipy.stats import entropy
from netCDF4 import Dataset
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import LinearSegmentedColormap

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS'
dir_main = '/'.join([dir_CPEX, 'figures'])
dir_bufr = '/'.join([dir_CPEX, 'display_bufr'])

status = ['ges']
domains = ['d01']
window_time = 6
cycling_interval = 6.0

dir_grayC = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS/figures_V3/ScientificColourMaps7/grayC'
grayC_cm_data = np.loadtxt(dir_grayC + '/grayC.txt')
grayC_map = LinearSegmentedColormap.from_list('grayC', grayC_cm_data[::1])

cases = ['CON6h_Aeolus6h_082500_Hybrid_C08']
anl_start_time = datetime.datetime(2021, 8, 25,  0, 0, 0)
anl_end_time = datetime.datetime(2021, 8, 26, 18, 0, 0)

for dom in domains:
    for stat in status:
        for case in cases:

            dir_out = '/'.join([dir_CPEX, 'display_bufr', case])
            pdfname = './fig02.pdf'

            with PdfPages(pdfname) as pdf:

                fig_width  = 6.00
                fig_height = 3.00
                fig, axs   = plt.subplots(1, 2, figsize=(fig_width, fig_height))
                fig.subplots_adjust(left=0.100, bottom=0.150, right=0.975, top=0.925, wspace=0.150, hspace=0.250)

                receiver_channel = []
                classification_type = []
                inverse_obs_error_input = []
                observation = []
                confidence_flag = []

                time_now = anl_start_time
                while time_now <= anl_end_time:

                    time_now_str = time_now.strftime('%Y%m%d%H')

                    filename = dir_out + '/' + time_now_str + '_' + stat + '_' + dom + '.nc'
                    print(filename)
                    print(os.path.exists(filename))

                    if os.path.exists(filename):

                        ncfile = Dataset(filename)
                        receiver_channel.extend(ncfile.variables['receiver_channel'][:].tolist())
                        classification_type.extend(ncfile.variables['classification_type'][:].tolist())
                        inverse_obs_error_input.extend(ncfile.variables['inverse_obs_error_input'][:].tolist())
                        observation.extend(ncfile.variables['observation'][:].tolist())
                        confidence_flag.extend(ncfile.variables['confidence_flag'][:].tolist())
                        ncfile.close()

                    time_now = time_now + datetime.timedelta(hours=cycling_interval)

                receiver_channel = np.array(receiver_channel)
                classification_type = np.array(classification_type)
                inverse_obs_error_input = np.array(inverse_obs_error_input)
                observation = np.array(observation)
                confidence_flag = np.array(confidence_flag)

                mie_index_clear_valid = (receiver_channel == 0) & (classification_type == 0) & (confidence_flag == 0)
                rayleigh_index_clear_valid = (receiver_channel == 1) & (classification_type == 0) & (confidence_flag == 0)
                mie_index_cloudy_valid = (receiver_channel == 0) & (classification_type == 1) & (confidence_flag == 0)
                rayleigh_index_cloudy_valid = (receiver_channel == 1) & (classification_type == 1) & (confidence_flag == 0)

                ax = axs[0]
                mtitle = '(a) Mie-cloudy wind'
                ax.plot(observation[mie_index_cloudy_valid], 1.0/inverse_obs_error_input[mie_index_cloudy_valid], '.', color='k', ms=0.25)
                ax.plot([-1000, 1000], [2.5, 2.5], '-', color='k', label='2.5 $\mathrm{m\ s^{-1}}$')

                ax.set_xlabel('Observed Aeolus HLOS wind ($\mathrm{m\ s^{-1}}$)', fontsize=10.0)
                ax.set_ylabel('Estimated instrumental error ($\mathrm{m\ s^{-1}}$)', fontsize=10.0)
                ax.set_xticks(np.arange(-60.0, 61.0, 30.0))
                ax.set_yticks(np.arange(0.0, 16.0, 5.0))
                ax.tick_params('both', direction='in', labelsize=10.0)
                ax.set_title(mtitle, fontsize=10.0, pad=4.0)
                ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])
                ax.axis([-60, 60, 0, 15])
                ax.legend(loc='upper right', fontsize=7.5, markerscale=7.5, handlelength=1.0).set_zorder(102)

                ax = axs[1]
                mtitle = '(b) Rayleigh-clear wind'
                ax.plot(observation[rayleigh_index_clear_valid], 1.0/inverse_obs_error_input[rayleigh_index_clear_valid], '.', color='k', ms=0.25)
                ax.plot([-1000, 1000], [4.5, 4.5], '-', color='k', label='4.5 $\mathrm{m\ s^{-1}}$')

                ax.set_xlabel('Observed Aeolus HLOS wind ($\mathrm{m\ s^{-1}}$)', fontsize=10.0)
                #ax.set_ylabel('Estimated instrumental error ($\mathrm{m\ s^{-1}}$)', fontsize=10.0)
                ax.set_xticks(np.arange(-60.0, 61.0, 30.0))
                ax.set_yticks(np.arange(0.0, 16.0, 5.0))
                ax.tick_params('both', direction='in', labelsize=10.0)
                ax.set_title(mtitle, fontsize=10.0, pad=4.0)
                ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])
                ax.axis([-60, 60, 0, 15])
                ax.legend(loc='upper right', fontsize=7.5, markerscale=7.5, handlelength=1.0).set_zorder(102)

                plt.savefig('./fig02.png', dpi=300)
                pdf.savefig(fig)
                plt.cla()
                plt.clf()
                plt.close()
