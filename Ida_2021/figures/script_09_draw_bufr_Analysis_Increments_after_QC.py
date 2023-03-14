import os
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import LinearSegmentedColormap

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS'
dir_main = dir_CPEX + '/display_bufr'

domains = ['d01']
window_time = 6
cycling_interval = 6.0

dir_vik = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS/figures_V3/ScientificColourMaps7/vik'
vik_cm_data = np.loadtxt(dir_vik + '/vik.txt')
vik_map = LinearSegmentedColormap.from_list('vik', vik_cm_data[::1])

dir_grayC = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS/figures_V3/ScientificColourMaps7/grayC'
grayC_cm_data = np.loadtxt(dir_grayC + '/grayC.txt')
grayC_map = LinearSegmentedColormap.from_list('grayC', grayC_cm_data[::1])

cases = ['CON6h_Aeolus6h_082418_Hybrid_C08', 'CON6h_Aeolus6h_082500_Hybrid_C08']
labels = ['2418_L2B', '2500_L2B']
draw_times = [datetime.datetime(2021, 8, 25, 12, 0, 0), datetime.datetime(2021, 8, 26, 12, 0, 0)]
draw_time_strings = ['25 August 2021, 12:00 UTC', '26 August 2021, 12:00 UTC']
file_wrfout_d01s = ['wrfout_d01_2021-08-26_18:00:00', 'wrfout_d01_2021-08-27_00:00:00']

lonmin = -80.0
lonmax = -60.0

for dom in domains:

    pdfname = './fig09.pdf'

    with PdfPages(pdfname) as pdf:

        fig, axs = plt.subplots(4, 2, figsize=(9.0, 10.0))
        fig.subplots_adjust(left=0.050, bottom=-0.075, right=0.975, top=0.975, wspace=0.100, hspace=0.200)

        for idc, case in enumerate(cases):

            dir_out = dir_main + '/' + case
            dir_wrfout = '/'.join([dir_CPEX, 'cycling_da', 'Data', case, 'bkg'])
            file_wrfout_d01 = dir_wrfout + '/' + file_wrfout_d01s[idc]

            wrfout_d01 = Dataset(file_wrfout_d01)
            lat_d01 = wrfout_d01.variables['XLAT'][0,:,:]
            lon_d01 = wrfout_d01.variables['XLONG'][0,:,:]
            wrfout_d01.close()

            casename = case + '_' + dom
            filename = dir_CPEX + '/track_intensity/best_track/' + casename + '.csv'
            df = pd.read_csv(filename)

            for idt, time_now in enumerate(draw_times):

                time_now_str = time_now.strftime('%Y%m%d%H')
                filename1 = dir_out + '/' + time_now_str + '_anl_' + dom + '.nc'
                filename2 = dir_out + '/' + time_now_str + '_ges_' + dom + '.nc'
                print(filename1)
                print(os.path.exists(filename1))

                index = []
                for idx, Date_Time in enumerate(df['Date_Time']):
                    time_temp = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
                    if time_temp == time_now: index = index + [idx]

                TC_lats = list(df['Latitude'][index])
                TC_lons = list(df['Longitude'][index])

                if os.path.exists(filename1):

                    ncfile1 = Dataset(filename1)
                    latitude = ncfile1.variables['latitude'][:]
                    longitude = ncfile1.variables['longitude'][:]-360.0
                    pressure = ncfile1.variables['pressure'][:]
                    height = ncfile1.variables['height'][:]/1000.0
                    observation_time = ncfile1.variables['observation_time'][:]
                    analysis_usage_flag = ncfile1.variables['analysis_usage_flag'][:]
                    inverse_obs_error_input = ncfile1.variables['inverse_obs_error_input'][:]
                    inverse_obs_error_adjust = ncfile1.variables['inverse_obs_error_adjust'][:]
                    inverse_obs_error_final = ncfile1.variables['inverse_obs_error_final'][:]
                    observation = ncfile1.variables['observation'][:]
                    obs_minus_ges_analysis1 = ncfile1.variables['obs_minus_ges_analysis'][:]
                    elevation_angle = ncfile1.variables['elevation_angle'][:]
                    azimuth = ncfile1.variables['azimuth'][:]
                    receiver_channel = ncfile1.variables['receiver_channel'][:]
                    classification_type = ncfile1.variables['classification_type'][:]
                    confidence_flag = ncfile1.variables['confidence_flag'][:]
                    ncfile1.close()

                    ncfile2 = Dataset(filename2)
                    obs_minus_ges_analysis2 = ncfile2.variables['obs_minus_ges_analysis'][:]
                    ncfile2.close()

                    AmB = obs_minus_ges_analysis2-obs_minus_ges_analysis1

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
                    elevation_angle = elevation_angle[sort_index]
                    azimuth = azimuth[sort_index]
                    AmB = AmB[sort_index]
                    print(np.nanmax(np.max(AmB)))

                    extent = [lat_d01[0,0], lat_d01[-1,-1], 0.0, 30]

                    mie_index_analysis = (receiver_channel == 0) & (analysis_usage_flag == 1) & (longitude >= lonmin) & (longitude <= lonmax)
                    mie_index_valid = (receiver_channel == 0) & (confidence_flag == 1) & (longitude >= lonmin) & (longitude <= lonmax)
                    rayleigh_index_analysis = (receiver_channel == 1) & (analysis_usage_flag == 1) & (longitude >= lonmin) & (longitude <= lonmax)
                    rayleigh_index_valid = (receiver_channel == 1) & (confidence_flag == 1) & (longitude >= lonmin) & (longitude <= lonmax)

                    #mtitle = '(' + chr(97+2*idt+idc) + ') Mie-cloudy wind, ' + labels[idc] + ', ' + draw_time_strings[idt]
                    mtitle = '(' + chr(97+2*idt+idc) + ') Mie-cloudy wind, ' + labels[idc]
                    ax = axs[2*idt+idc, 0]
                    pcm = ax.scatter(latitude[mie_index_analysis], height[mie_index_analysis], c=AmB[mie_index_analysis], \
                                     marker='|', s=25.0, vmin=-9.0, vmax=9.0, cmap=vik_map, zorder=0)
                    ax.plot(latitude[mie_index_valid], height[mie_index_valid], '.', color=grayC_cm_data[53], ms=1.25)
                    ax.plot(TC_lats[0], 0.0, '^', color='k', ms=10.00)

                    if idc==1 and idt==1: ax.set_xlabel('Latitude', fontsize=10.0)
                    ax.set_ylabel('Height (km)', fontsize=10.0)
                    ax.set_xticks(np.arange(-5.0, 71.0, 5.0))
                    ax.set_yticks(np.arange(0.0, 31.0, 5.0))
                    ax.tick_params('both', direction='in', labelsize=10.0)
                    ax.set_title(mtitle, fontsize=10.0, pad=4.0)
                    ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])
                    ax.axis(extent)
                    ax.set_xticklabels([ '$\mathrm{5^{\circ}\ S}$',     '$\mathrm{0^{\circ}}$',  '$\mathrm{5^{\circ}\ N}$', '$\mathrm{10^{\circ}\ N}$', \
                                        '$\mathrm{15^{\circ}\ N}$', '$\mathrm{20^{\circ}\ N}$', '$\mathrm{25^{\circ}\ N}$', '$\mathrm{30^{\circ}\ N}$', \
                                        '$\mathrm{35^{\circ}\ N}$', '$\mathrm{40^{\circ}\ N}$', '$\mathrm{45^{\circ}\ N}$', '$\mathrm{50^{\circ}\ N}$', \
                                        '$\mathrm{55^{\circ}\ N}$', '$\mathrm{60^{\circ}\ N}$', '$\mathrm{65^{\circ}\ N}$', '$\mathrm{70^{\circ}\ N}$'])
                    ax.text(lat_d01[-1,-1]-0.5, 27.5, draw_time_strings[idt], ha='right', va='center', color='k', fontsize=7.5, \
                            bbox=dict(boxstyle='round', ec=grayC_cm_data[53], fc=grayC_cm_data[0]), zorder=7)

                    #mtitle = '(' + chr(101+2*idt+idc) + ') Rayleigh-clear wind, ' + labels[idc] + ', ' + draw_time_strings[idt]
                    mtitle = '(' + chr(101+2*idt+idc) + ') Rayleigh-clear wind, ' + labels[idc]
                    ax = axs[2*idt+idc, 1]
                    pcm = ax.scatter(latitude[rayleigh_index_analysis], height[rayleigh_index_analysis], c=AmB[rayleigh_index_analysis], \
                                     marker='|', s=25.0, vmin=-9.0, vmax=9.0, cmap=vik_map, zorder=0)
                    ax.plot(latitude[rayleigh_index_valid], height[rayleigh_index_valid], '.', color=grayC_cm_data[53], ms=1.25)
                    ax.plot(TC_lats[0], 0.0, '^', color='k', ms=10.00)

                    if idc==1 and idt==1: ax.set_xlabel('Latitude', fontsize=10.0)
                    #ax.set_ylabel('Height (km)', fontsize=10.0)
                    ax.set_xticks(np.arange(-5.0, 71.0, 5.0))
                    ax.set_yticks(np.arange(0.0, 31.0, 5.0))
                    ax.tick_params('both', direction='in', labelsize=10.0)
                    ax.set_title(mtitle, fontsize=10.0, pad=4.0)
                    ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])
                    ax.axis(extent)
                    ax.set_xticklabels([ '$\mathrm{5^{\circ}\ S}$',     '$\mathrm{0^{\circ}}$',  '$\mathrm{5^{\circ}\ N}$', '$\mathrm{10^{\circ}\ N}$', \
                                        '$\mathrm{15^{\circ}\ N}$', '$\mathrm{20^{\circ}\ N}$', '$\mathrm{25^{\circ}\ N}$', '$\mathrm{30^{\circ}\ N}$', \
                                        '$\mathrm{35^{\circ}\ N}$', '$\mathrm{40^{\circ}\ N}$', '$\mathrm{45^{\circ}\ N}$', '$\mathrm{50^{\circ}\ N}$', \
                                        '$\mathrm{55^{\circ}\ N}$', '$\mathrm{60^{\circ}\ N}$', '$\mathrm{65^{\circ}\ N}$', '$\mathrm{70^{\circ}\ N}$'])
                    ax.text(lat_d01[-1,-1]-0.5, 27.5, draw_time_strings[idt], ha='right', va='center', color='k', fontsize=7.5, \
                            bbox=dict(boxstyle='round', ec=grayC_cm_data[53], fc=grayC_cm_data[0]), zorder=7)

        clb = fig.colorbar(pcm, ax=axs, ticks=np.arange(-9.0, 9.1, 1.5), orientation='horizontal', pad=0.0400, aspect=37.5, shrink=1.00)
        clb.set_label('Analysis increment of Aeolus HLOS wind ($\mathrm{m\ s^{-1}}$)', fontsize=10.0, labelpad=4.0)
        clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

        plt.savefig('./fig09.png', dpi=300)
        pdf.savefig(fig)
        plt.cla()
        plt.clf()
        plt.close()
