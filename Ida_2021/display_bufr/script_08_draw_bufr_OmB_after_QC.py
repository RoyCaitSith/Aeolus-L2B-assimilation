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

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS'
dir_main = dir_CPEX + '/display_bufr'
dir_wrfout = '/'.join([dir_CPEX, 'cycling_da', 'Data', case, 'bkg'])

status = ['ges']
domains = ['d01']
window_time = 6
cycling_interval = 6.0
sns_cmap = sns.color_palette('bright')

draw_times = [datetime.datetime(2021, 8, 24, 12, 0, 0), datetime.datetime(2021, 8, 25, 12, 0, 0), datetime.datetime(2021, 8, 26, 12, 0, 0)]
lonmin = -80.0
lonmax = -60.0

TC_lats = [ 12.00,  13.10,  16.50]
TC_lons = [-66.40, -74.90, -78.90]

#file_wrfout_d01 = dir_wrfout + '/wrfout_d01_2021-08-26_06:00:00'
#file_wrfout_d01 = dir_wrfout + '/wrfout_d01_2021-08-26_12:00:00'
#file_wrfout_d01 = dir_wrfout + '/wrfout_d01_2021-08-26_18:00:00'
file_wrfout_d01 = dir_wrfout + '/wrfout_d01_2021-08-27_00:00:00'
wrfout_d01 = Dataset(file_wrfout_d01)
lat_d01 = wrfout_d01.variables['XLAT'][0,:,:]
lon_d01 = wrfout_d01.variables['XLONG'][0,:,:]
wrfout_d01.close()

for dom in domains:

    dir_out = dir_main + '/' + case

    for idt, time_now in enumerate(draw_times):

        time_now_str = time_now.strftime('%Y%m%d%H')

        for stat in status:

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
                receiver_channel = receiver_channel[sort_index]
                analysis_usage_flag = analysis_usage_flag[sort_index]
                classification_type = classification_type[sort_index]
                confidence_flag = confidence_flag[sort_index]
                latitude = latitude[sort_index]
                longitude = longitude[sort_index]
                pressure = pressure[sort_index]
                height = height[sort_index]
                inverse_obs_error_input = inverse_obs_error_input[sort_index]
                inverse_obs_error_adjust = inverse_obs_error_adjust[sort_index]
                inverse_obs_error_final = inverse_obs_error_final[sort_index]
                observation = observation[sort_index]
                obs_minus_ges_analysis = obs_minus_ges_analysis[sort_index]
                elevation_angle = elevation_angle[sort_index]
                azimuth = azimuth[sort_index]
                normalized_OmB = normalized_OmB[sort_index]

                pdfname = dir_out + '/OmB_After_QC_' + time_now_str + '_' + stat + '_' + dom + '.pdf'
                with PdfPages(pdfname) as pdf:

                    extent = [lat_d01[0,0], lat_d01[-1,-1], 0.0, 30]

                    mie_index_analysis = (receiver_channel == 0) & (analysis_usage_flag == 1) & (longitude >= lonmin) & (longitude <= lonmax)
                    mie_index_valid = (receiver_channel == 0) & (confidence_flag == 1) & (longitude >= lonmin) & (longitude <= lonmax)
                    rayleigh_index_analysis = (receiver_channel == 1) & (analysis_usage_flag == 1) & (longitude >= lonmin) & (longitude <= lonmax)
                    rayleigh_index_valid = (receiver_channel == 1) & (confidence_flag == 1) & (longitude >= lonmin) & (longitude <= lonmax)

                    fig, axs = plt.subplots(2, 1, figsize=(6.0, 5.0))
                    fig.subplots_adjust(left=0.075, bottom=-0.025, right=0.975, top=0.950, wspace=0.150, hspace=0.400)

                    mtitle = '(a) Mie Channel, After QC'
                    ax = axs[0]
                    pcm = ax.scatter(latitude[mie_index_analysis], height[mie_index_analysis], c=obs_minus_ges_analysis[mie_index_analysis], \
                                     marker='|', s=25.0, vmin=-10.0, vmax=10.0, cmap='RdBu_r', zorder=0)
                    ax.plot(latitude[mie_index_valid], height[mie_index_valid], 'o', color='k', ms=0.25)
                    ax.plot(TC_lats[idt], 0.0, '^', color='k', ms=10.00)

                    ax.set_xlabel('Latitude', fontsize=10.0)
                    ax.set_ylabel('Height (km)', fontsize=10.0)
                    ax.set_xticks(np.arange(-5.0, 71.0, 5.0))
                    ax.set_yticks(np.arange(0.0, 31.0, 5.0))
                    ax.tick_params('both', direction='in', labelsize=10.0)
                    ax.set_title(mtitle, fontsize=10.0, pad=4.0)
                    ax.grid(True, linewidth=0.5, color=sns_cmap[7])
                    ax.axis(extent)
                    ax.set_xticklabels([ r'$5^{\circ}S$',   r'$0^{\circ}$',  r'$5^{\circ}N$', r'$10^{\circ}N$', \
                                        r'$15^{\circ}N$', r'$20^{\circ}N$', r'$25^{\circ}N$', r'$30^{\circ}N$', \
                                        r'$35^{\circ}N$', r'$40^{\circ}N$', r'$45^{\circ}N$', r'$50^{\circ}N$', \
                                        r'$55^{\circ}N$', r'$60^{\circ}N$', r'$65^{\circ}N$', r'$70^{\circ}N$'])

                    mtitle = '(b) Rayleigh Channel, After QC'
                    ax = axs[1]
                    pcm = ax.scatter(latitude[rayleigh_index_analysis], height[rayleigh_index_analysis], c=obs_minus_ges_analysis[rayleigh_index_analysis], \
                                     marker='|', s=25.0, vmin=-10.0, vmax=10.0, cmap='RdBu_r', zorder=0)
                    ax.plot(latitude[rayleigh_index_valid], height[rayleigh_index_valid], 'o', color='k', ms=0.25)
                    ax.plot(TC_lats[idt], 0.0, '^', color='k', ms=10.00)

                    ax.set_xlabel('Latitude', fontsize=10.0)
                    ax.set_ylabel('Height (km)', fontsize=10.0)
                    ax.set_xticks(np.arange(-5.0, 71.0, 5.0))
                    ax.set_yticks(np.arange(0.0, 31.0, 5.0))
                    ax.tick_params('both', direction='in', labelsize=10.0)
                    ax.set_title(mtitle, fontsize=10.0, pad=4.0)
                    ax.grid(True, linewidth=0.5, color=sns_cmap[7])
                    ax.axis(extent)
                    ax.set_xticklabels([ r'$5^{\circ}S$',   r'$0^{\circ}$',  r'$5^{\circ}N$', r'$10^{\circ}N$', \
                                        r'$15^{\circ}N$', r'$20^{\circ}N$', r'$25^{\circ}N$', r'$30^{\circ}N$', \
                                        r'$35^{\circ}N$', r'$40^{\circ}N$', r'$45^{\circ}N$', r'$50^{\circ}N$', \
                                        r'$55^{\circ}N$', r'$60^{\circ}N$', r'$65^{\circ}N$', r'$70^{\circ}N$'])

                    clb = fig.colorbar(pcm, ax=axs, ticks=np.arange(-10.0, 11.0, 2.0), orientation='horizontal', pad=0.100, aspect=37.5, shrink=1.00)
                    clb.set_label('OmB (m/s)', fontsize=10.0, labelpad=4.0)
                    clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

                    pdf.savefig(fig)
                    plt.cla()
                    plt.clf()
                    plt.close()
