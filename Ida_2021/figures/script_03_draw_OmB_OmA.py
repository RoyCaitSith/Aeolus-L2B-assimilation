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

status = ['ges', 'anl']
domains = ['d01', 'd02']
variables = ['obs_minus_ges_without_BC', 'obs_minus_ges_without_BC']
varlabels = ['OmB', 'OmA']

dir_batlow = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS/figures_V3/ScientificColourMaps7/batlow'
batlow_cm_data = np.loadtxt(dir_batlow + '/batlow.txt')
batlow_map_r = LinearSegmentedColormap.from_list('batlow', batlow_cm_data[::-1])
colors = [batlow_cm_data[74], batlow_cm_data[223]]
linestyles = ['-', '--']

window_time = 6
cycling_interval = 6.0

dir_grayC = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS/figures_V3/ScientificColourMaps7/grayC'
grayC_cm_data = np.loadtxt(dir_grayC + '/grayC.txt')
grayC_map = LinearSegmentedColormap.from_list('grayC', grayC_cm_data[::1])

case = 'CON6h_Aeolus6h_082500_Hybrid_C08'
labels = ['(a) Mie-cloudy wind', '(b) Rayleigh-clear wind']
anl_start_time = datetime.datetime(2021, 8, 25,  6, 0, 0)
anl_end_time   = datetime.datetime(2021, 8, 27,  0, 0, 0)

pdfname = './fig03.pdf'
with PdfPages(pdfname) as pdf:

    fig_width  = 6.00
    fig_height = 3.00
    fig, axs   = plt.subplots(1, 2, figsize=(fig_width, fig_height))
    fig.subplots_adjust(left=0.100, bottom=0.150, right=0.975, top=0.925, wspace=0.150, hspace=0.250)

    ax = axs[0]
    for idd, dom in enumerate(domains):
        for ids, stat in enumerate(status):

            dir_out = '/'.join([dir_CPEX, 'display_bufr', case])
            print(dir_out)

            OmBs = []
            analysis_usage_flag = []
            receiver_channel = []
            classification_type = []
            inverse_obs_error_input = []

            time_now = anl_start_time
            while time_now <= anl_end_time:

                time_now_str = time_now.strftime('%Y%m%d%H')

                filename = dir_out + '/' + time_now_str + '_' + stat + '_' + dom + '.nc'
                print(filename)
                print(os.path.exists(filename))

                if os.path.exists(filename):

                    ncfile = Dataset(filename)
                    OmBs.extend(ncfile.variables[variables[ids]][:].tolist())
                    analysis_usage_flag.extend(ncfile.variables['analysis_usage_flag'][:].tolist())
                    receiver_channel.extend(ncfile.variables['receiver_channel'][:].tolist())
                    classification_type.extend(ncfile.variables['classification_type'][:].tolist())
                    inverse_obs_error_input.extend(ncfile.variables['inverse_obs_error_input'][:].tolist())
                    ncfile.close()

                time_now = time_now + datetime.timedelta(hours=cycling_interval)

            OmBs = np.array(OmBs)
            analysis_usage_flag = np.array(analysis_usage_flag)
            receiver_channel = np.array(receiver_channel)
            classification_type = np.array(classification_type)
            inverse_obs_error_input = np.array(inverse_obs_error_input)

            index = (analysis_usage_flag == 1) & (receiver_channel == 0) & (classification_type == 1)
            OmBs = OmBs[index]
            inverse_obs_error_input = inverse_obs_error_input[index]
            #normalized_OmBs = OmBs*inverse_obs_error_input
            normalized_OmBs = OmBs/2.5
            hist, bin_edges = np.histogram(normalized_OmBs, bins=np.arange(-100.0, 100.1, 0.2), density=True)
            #print(hist)

            label = varlabels[ids] + ', ' + dom
            ax.plot(0.5*(bin_edges[0:-1]+bin_edges[1:]), hist, color=colors[ids], linestyle=linestyles[idd], label=label, linewidth=1.25)
            #ax.plot([0.0, 0.0], [-1000.0, 1000.0], '-', color='k')

    mtitle = labels[0]
    ax.set_xlabel('Normalized OmB or OmA ($\mathrm{m\ s^{-1}}$)', fontsize=10.0)
    ax.set_ylabel('PDF', fontsize=10.0)
    ax.set_xticks(np.arange(-4.0, 4.1, 1.0))
    ax.tick_params('both', which='both', direction='in', labelsize=10.0)
    ax.set_title(mtitle, fontsize=10.0, pad=4.0)
    ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])
    ax.axis([-4.0, 4.0, 0.00, 0.5])
    ax.legend(loc='upper right', fontsize=7.5, handlelength=2.5).set_zorder(102)

    ax = axs[1]
    for idd, dom in enumerate(domains):
        for ids, stat in enumerate(status):

            dir_out = '/'.join([dir_CPEX, 'display_bufr', case])
            print(dir_out)

            OmBs = []
            analysis_usage_flag = []
            receiver_channel = []
            classification_type = []
            inverse_obs_error_input = []

            time_now = anl_start_time
            while time_now <= anl_end_time:

                time_now_str = time_now.strftime('%Y%m%d%H')

                filename = dir_out + '/' + time_now_str + '_' + stat + '_' + dom + '.nc'
                print(filename)
                print(os.path.exists(filename))

                if os.path.exists(filename):

                    ncfile = Dataset(filename)
                    OmBs.extend(ncfile.variables[variables[ids]][:].tolist())
                    analysis_usage_flag.extend(ncfile.variables['analysis_usage_flag'][:].tolist())
                    receiver_channel.extend(ncfile.variables['receiver_channel'][:].tolist())
                    classification_type.extend(ncfile.variables['classification_type'][:].tolist())
                    inverse_obs_error_input.extend(ncfile.variables['inverse_obs_error_input'][:].tolist())
                    ncfile.close()

                time_now = time_now + datetime.timedelta(hours=cycling_interval)

            OmBs = np.array(OmBs)
            analysis_usage_flag = np.array(analysis_usage_flag)
            receiver_channel = np.array(receiver_channel)
            classification_type = np.array(classification_type)
            inverse_obs_error_input = np.array(inverse_obs_error_input)

            index = (analysis_usage_flag == 1) & (receiver_channel == 1) & (classification_type == 0)
            OmBs = OmBs[index]
            inverse_obs_error_input = inverse_obs_error_input[index]
            #normalized_OmBs = OmBs*inverse_obs_error_input
            normalized_OmBs = OmBs/4.5
            hist, bin_edges = np.histogram(normalized_OmBs, bins=np.arange(-100.0, 100.1, 0.2), density=True)
            #print(hist)

            label = varlabels[ids] + ', ' + dom
            ax.plot(0.5*(bin_edges[0:-1]+bin_edges[1:]), hist, color=colors[ids], linestyle=linestyles[idd], label=label, linewidth=1.25)
            #ax.plot([0.0, 0.0], [-1000.0, 1000.0], '-', color='k')

    mtitle = labels[1]
    ax.set_xlabel('Normalized OmB or OmA ($\mathrm{m\ s^{-1}}$)', fontsize=10.0)
    #ax.set_ylabel('PDF', fontsize=10.0)
    ax.set_xticks(np.arange(-4.0, 4.1, 1.0))
    ax.tick_params('both', which='both', direction='in', labelsize=10.0)
    ax.set_title(mtitle, fontsize=10.0, pad=4.0)
    ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])
    ax.axis([-4.0, 4.0, 0.00, 0.5])
    ax.legend(loc='upper right', fontsize=7.5, handlelength=2.5).set_zorder(102)

    plt.savefig('./fig03.png', dpi=300)
    pdf.savefig(fig)
    plt.cla()
    plt.clf()
    plt.close()
