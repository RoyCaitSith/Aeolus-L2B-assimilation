import os
import datetime
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
import matplotlib.ticker as ticker
from scipy.stats import entropy
from netCDF4 import Dataset
from matplotlib.backends.backend_pdf import PdfPages

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS'
dir_main = '/'.join([dir_CPEX, 'figures'])

status = ['ges']
domains = ['d01']
window_time = 6
cycling_interval = 6.0
sns_cmap = sns.color_palette('bright')

cases = ['CON6h_Aeolus6h_082500_Hybrid_C08']
anl_start_time = datetime.datetime(2021, 8, 25,  6, 0, 0)
anl_end_time   = datetime.datetime(2021, 8, 27,  0, 0, 0)

for dom in domains:
    for stat in status:
        for case in cases:

            dir_out = '/'.join([dir_CPEX, 'display_bufr', case])
            pdfname = './Figure_01_Observation_Error_HLOS_Distribution_' + stat + '_' + dom + '.pdf'

            with PdfPages(pdfname) as pdf:

                fig_width  = 6.00
                fig_height = 6.00
                fig, axs   = plt.subplots(2, 2, figsize=(fig_width, fig_height))
                fig.subplots_adjust(left=0.075, bottom=0.075, right=0.975, top=0.950, wspace=0.250, hspace=0.250)

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

                mtitle = '(a) Mie, Clear Sky, Valid'
                ax = axs[0, 0]
                ax.plot(observation[mie_index_clear_valid], 1.0/inverse_obs_error_input[mie_index_clear_valid], 'o', color='k', ms=0.10)

                ax.set_xlabel('HLOS (m/s)', fontsize=10.0)
                ax.set_ylabel('Observation Error (m/s)', fontsize=10.0)
                ax.set_xticks(np.arange(-60.0, 61.0, 30.0))
                ax.set_yticks(np.arange(0.0, 16.0, 5.0))
                ax.tick_params('both', direction='in', labelsize=10.0)
                ax.set_title(mtitle, fontsize=10.0, pad=4.0)
                ax.grid(True, linewidth=0.5, color=sns_cmap[7])
                ax.axis([-60, 60, 0, 15])

                mtitle = '(b) Mie, Cloudy Sky, Valid'
                ax = axs[0, 1]
                ax.plot(observation[mie_index_cloudy_valid], 1.0/inverse_obs_error_input[mie_index_cloudy_valid], 'o', color='k', ms=0.10)
                ax.plot([-1000, 1000], [2.5, 2.5], '-', color='r')

                ax.set_xlabel('HLOS (m/s)', fontsize=10.0)
                ax.set_ylabel('Observation Error (m/s)', fontsize=10.0)
                ax.set_xticks(np.arange(-60.0, 61.0, 30.0))
                ax.set_yticks(np.arange(0.0, 16.0, 5.0))
                ax.tick_params('both', direction='in', labelsize=10.0)
                ax.set_title(mtitle, fontsize=10.0, pad=4.0)
                ax.grid(True, linewidth=0.5, color=sns_cmap[7])
                ax.axis([-60, 60, 0, 15])

                mtitle = '(c) Rayleigh, Clear Sky, Valid'
                ax = axs[1, 0]
                ax.plot(observation[rayleigh_index_clear_valid], 1.0/inverse_obs_error_input[rayleigh_index_clear_valid], 'o', color='k', ms=0.10)
                ax.plot([-1000, 1000], [4.5, 4.5], '-', color='r')

                ax.set_xlabel('HLOS (m/s)', fontsize=10.0)
                ax.set_ylabel('Observation Error (m/s)', fontsize=10.0)
                ax.set_xticks(np.arange(-60.0, 61.0, 30.0))
                ax.set_yticks(np.arange(0.0, 16.0, 5.0))
                ax.tick_params('both', direction='in', labelsize=10.0)
                ax.set_title(mtitle, fontsize=10.0, pad=4.0)
                ax.grid(True, linewidth=0.5, color=sns_cmap[7])
                ax.axis([-60, 60, 0, 15])

                mtitle = '(d) Rayleigh, Cloudy Sky, Valid'
                ax = axs[1, 1]
                ax.plot(observation[rayleigh_index_cloudy_valid], 1.0/inverse_obs_error_input[rayleigh_index_cloudy_valid], 'o', color='k', ms=0.10)

                ax.set_xlabel('HLOS (m/s)', fontsize=10.0)
                ax.set_ylabel('Observation Error (m/s)', fontsize=10.0)
                ax.set_xticks(np.arange(-60.0, 61.0, 30.0))
                ax.set_yticks(np.arange(0.0, 16.0, 5.0))
                ax.tick_params('both', direction='in', labelsize=10.0)
                ax.set_title(mtitle, fontsize=10.0, pad=4.0)
                ax.grid(True, linewidth=0.5, color=sns_cmap[7])
                ax.axis([-60, 60, 0, 15])

                pdf.savefig(fig)
                plt.cla()
                plt.clf()
                plt.close()
