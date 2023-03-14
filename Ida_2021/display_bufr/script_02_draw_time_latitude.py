import os
import datetime
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from matplotlib.backends.backend_pdf import PdfPages

#case = 'CON6h_Aeolus6h_082406_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082412_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082418_Hybrid_C08'
case = 'CON6h_Aeolus6h_082500_Hybrid_C08'

#anl_start_time = datetime.datetime(2021, 8, 24, 12, 0, 0)
#anl_end_time   = datetime.datetime(2021, 8, 26,  6, 0, 0)
#anl_start_time = datetime.datetime(2021, 8, 24, 18, 0, 0)
#anl_end_time   = datetime.datetime(2021, 8, 26, 12, 0, 0)
#anl_start_time = datetime.datetime(2021, 8, 25,  0, 0, 0)
#anl_end_time   = datetime.datetime(2021, 8, 26, 18, 0, 0)
anl_start_time = datetime.datetime(2021, 8, 25,  6, 0, 0)
anl_end_time   = datetime.datetime(2021, 8, 27,  0, 0, 0)

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS'
dir_main = dir_CPEX + '/display_bufr'
dir_wrfout = '/'.join([dir_CPEX, 'cycling_da', 'Data', case, 'bkg'])

status = ['ges']
domains = ['d01']
window_time = 6
cycling_interval = 6.0
sns_cmap = sns.color_palette('bright')

#file_wrfout_d01 = dir_wrfout + '/wrfout_d01_2021-08-26_06:00:00'
#file_wrfout_d01 = dir_wrfout + '/wrfout_d01_2021-08-26_12:00:00'
#file_wrfout_d01 = dir_wrfout + '/wrfout_d01_2021-08-26_18:00:00'
file_wrfout_d01 = dir_wrfout + '/wrfout_d01_2021-08-27_00:00:00'
wrfout_d01 = Dataset(file_wrfout_d01)
lat_d01 = wrfout_d01.variables['XLAT'][0,:,:]
lon_d01 = wrfout_d01.variables['XLONG'][0,:,:]
wrfout_d01.close()

extent = [-1.0*window_time/2.0, window_time/2.0, lat_d01[0,0], lat_d01[-1,-1]]
print(extent)

for dom in domains:
    for stat in status:

        dir_out = dir_main + '/' + case
        pdfname = dir_out + '/Time_Latitude_' + stat + '_' + dom + '.pdf'

        with PdfPages(pdfname) as pdf:

            fig, axs = plt.subplots(1, 1, figsize=(6.0, 6.0))
            fig.subplots_adjust(left=0.125, bottom=0.100, right=0.950, top=0.950, wspace=0.150, hspace=0.400)

            ax = axs

            time_now = anl_start_time
            icycle = 0
            while time_now <= anl_end_time:

                time_now_str = time_now.strftime('%Y%m%d%H')

                filename = dir_out + '/' + time_now_str + '_' + stat + '_' + dom + '.nc'
                print(filename)
                print(os.path.exists(filename))

                if os.path.exists(filename):

                    ncfile = Dataset(filename)
                    latitude = ncfile.variables['latitude'][:]
                    longitude = ncfile.variables['longitude'][:]-360.0
                    pressure = ncfile.variables['pressure'][:]
                    height = ncfile.variables['height'][:]/1000.0
                    observation_time = ncfile.variables['observation_time'][:]
                    analysis_usage_flag = ncfile.variables['analysis_usage_flag'][:]
                    inverse_obs_error_input = ncfile.variables['inverse_obs_error_input'][:]
                    inverse_obs_error_adjust = ncfile.variables['inverse_obs_error_adjust'][:]
                    inverse_obs_error_final = ncfile.variables['inverse_obs_error_final'][:]
                    observation = ncfile.variables['observation'][:]
                    obs_minus_ges_analysis = ncfile.variables['obs_minus_ges_analysis'][:]
                    elevation_angle = ncfile.variables['elevation_angle'][:]
                    azimuth = ncfile.variables['azimuth'][:]
                    receiver_channel = ncfile.variables['receiver_channel'][:]
                    classification_type = ncfile.variables['classification_type'][:]
                    confidence_flag = ncfile.variables['confidence_flag'][:]
                    ncfile.close()

                    normalized_OmB = obs_minus_ges_analysis*inverse_obs_error_final

                    sort_index = np.argsort(observation_time)
                    observation_time = observation_time[sort_index]
                    latitude = latitude[sort_index]
                    longitude = longitude[sort_index]

                    delta_obs_time = np.zeros((len(observation_time)))
                    delta_obs_time[1::] = observation_time[1::] - observation_time[0:-1]
                    delta_obs_index = np.where(np.abs(delta_obs_time) > 0.5)
                    delta_obs_index = np.append(delta_obs_index, -1)
                    delta_obs_index = np.append(0, delta_obs_index)

                    for idx in range(0, len(delta_obs_index)-1):
                        if idx == 0:
                            ax.plot(observation_time[delta_obs_index[idx]:delta_obs_index[idx+1]], \
                                    latitude[delta_obs_index[idx]:delta_obs_index[idx+1]], 'o', \
                                    color=sns_cmap[icycle+1], ms=2.50, label=time_now_str, zorder=2)
                        else:
                            ax.plot(observation_time[delta_obs_index[idx]:delta_obs_index[idx+1]], \
                                    latitude[delta_obs_index[idx]:delta_obs_index[idx+1]], 'o', \
                                    color=sns_cmap[icycle+1], ms=2.50, zorder=2)
                        print(observation_time[delta_obs_index[idx+1]-1]-observation_time[delta_obs_index[idx]])
                        print(latitude[delta_obs_index[idx]])
                        print(latitude[delta_obs_index[idx+1]-1])
                        print(longitude[delta_obs_index[idx]])
                        print(longitude[delta_obs_index[idx+1]-1])

                    icycle += 1

                time_now = time_now + datetime.timedelta(hours=cycling_interval)

            ax.set_xlabel('Observation Time (hr)', fontsize=10.0)
            ax.set_ylabel('Latitude', fontsize=10.0)
            ax.set_xticks(np.arange(-3.0, 3.1, 0.5))
            ax.set_yticks(np.arange(-5.0, 46.0, 5.0))
            ax.set_yticklabels([ r'$5^{\circ}S$',   r'$0^{\circ}$',  r'$5^{\circ}N$', r'$10^{\circ}N$', r'$15^{\circ}N$', r'$20^{\circ}N$', \
                                r'$25^{\circ}N$', r'$30^{\circ}N$', r'$35^{\circ}N$', r'$40^{\circ}N$', r'$45^{\circ}N$'])
            ax.tick_params('both', direction='in', labelsize=10.0)
            ax.grid(True, linewidth=0.5, color=sns_cmap[7], zorder=1)
            ax.legend(loc='upper right', fontsize=10.0, scatterpoints=1, handlelength=0.25)
            ax.axis(extent)

            pdf.savefig(fig)
            plt.cla()
            plt.clf()
            plt.close()
