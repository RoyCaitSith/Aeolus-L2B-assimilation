import os
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from netCDF4 import Dataset
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import LinearSegmentedColormap
from wrf import to_np, getvar, CoordPair, vertcross
from scipy.interpolate import griddata

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS'
dir_main = dir_CPEX + '/cross_section'

domains = ['d01']

cases0 = ['CON6h_082418_Hybrid_C08', 'CON6h_082500_Hybrid_C08']
cases1 = ['CON6h_Aeolus6h_082418_Hybrid_C08', 'CON6h_Aeolus6h_082500_Hybrid_C08']
mtitles = [['(a) 2418', '(b) 2418_L2B', '(c) 2418_L2B - 2418'], ['(d) 2500', '(e) 2500_L2B', '(f) 2500_L2B - 2500']]

draw_time = datetime.datetime(2021, 8, 25, 12, 0, 0)
draw_time_string = '25 August 2021, 12:00 UTC'
draw_time_str = draw_time.strftime('%Y%m%d%H')
lonmin = -80.0
lonmax = -60.0

dir_cork = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS/figures_V3/ScientificColourMaps7/cork'
cork_cm_data = np.loadtxt(dir_cork + '/cork.txt')
cork_map = LinearSegmentedColormap.from_list('cork', cork_cm_data[::1])

for dom in domains:

    pdfname = './fig11.pdf'
    print(pdfname)

    with PdfPages(pdfname) as pdf:

        fig, axs = plt.subplots(2, 3, figsize=(9.0, 6.0))
        fig.subplots_adjust(left=0.075, bottom=-0.050, right=0.975, top=0.950, wspace=0.1625, hspace=0.250)

        for idc, (case0, case1) in enumerate(zip(cases0, cases1)):

            dir_bufr = '/'.join([dir_CPEX, 'display_bufr', case1])
            bufrname = dir_bufr + '/' + draw_time_str + '_ges_' + dom + '.nc'
            print(bufrname)
            print(os.path.exists(bufrname))

            if os.path.exists(bufrname):

                ncfile = Dataset(bufrname)
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

                mie_index_all = (receiver_channel == 0) & (longitude >= lonmin) & (longitude <= lonmax)
                mie_index_valid = (receiver_channel == 0) & (confidence_flag == 1) & (longitude >= lonmin) & (longitude <= lonmax)
                rayleigh_index_all = (receiver_channel == 1) & (longitude >= lonmin) & (longitude <= lonmax)
                rayleigh_index_valid = (receiver_channel == 1) & (confidence_flag == 1) & (longitude >= lonmin) & (longitude <= lonmax)

                slat = np.max([np.max( latitude[mie_index_all]), np.max( latitude[rayleigh_index_all])])
                elat = np.min([np.min( latitude[mie_index_all]), np.min( latitude[rayleigh_index_all])])
                slon = np.max([np.max(longitude[mie_index_all]), np.max(longitude[rayleigh_index_all])])
                elon = np.min([np.min(longitude[mie_index_all]), np.min(longitude[rayleigh_index_all])])
                #slon = TC_lon[0]
                #elon = TC_lon[0]
                print([slat, elat, slon, elon])

                start_point = CoordPair(lat=slat, lon=slon)
                end_point = CoordPair(lat=elat, lon=elon)
                lat = np.linspace(slat, elat, 2201)
                lon = np.linspace(slon, elon, 2201)
                level = np.arange(0, 31, 0.02)

                casename = case0 + '_d01'
                filename = dir_CPEX + '/track_intensity/best_track/' + casename + '.csv'
                df = pd.read_csv(filename)

                index = []
                for idx, Date_Time in enumerate(df['Date_Time']):
                    time_temp = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
                    if time_temp == draw_time: index = index + [idx]

                TC_lat = list(df['Latitude'][index])
                TC_lon = list(df['Longitude'][index])
                print([TC_lat, TC_lon])

                dir_wrfout_bkg_0 = '/'.join([dir_CPEX, 'cycling_da', 'Data', case0, 'bkg'])
                wrfout_bkg_0 = dir_wrfout_bkg_0 + '/wrfout_' + dom + '_' + draw_time.strftime('%Y-%m-%d_%H:00:00')
                ncfile_bkg_0 = Dataset(wrfout_bkg_0)
                ht_bkg_0 = getvar(ncfile_bkg_0, 'z')
                rh_bkg_0 = getvar(ncfile_bkg_0, 'rh')
                temp_bkg_0 = vertcross(rh_bkg_0, ht_bkg_0, wrfin=ncfile_bkg_0, levels=level*1000.0, start_point=start_point, end_point=end_point, latlon=True, meta=True)
                ncfile_bkg_0.close()

                dir_wrfout_anl_0 = '/'.join([dir_CPEX, 'cycling_da', 'Data', case0, 'da'])
                wrfout_anl_0 = dir_wrfout_anl_0 + '/wrf_inout.' + draw_time.strftime('%Y%m%d%H') + '.' + dom
                ncfile_anl_0 = Dataset(wrfout_anl_0)
                ht_anl_0 = getvar(ncfile_anl_0, 'z')
                rh_anl_0 = getvar(ncfile_anl_0, 'rh')
                temp_anl_0 = vertcross(rh_anl_0, ht_anl_0, wrfin=ncfile_anl_0, levels=level*1000.0, start_point=start_point, end_point=end_point, latlon=True, meta=True)
                ncfile_anl_0.close()

                lats = []
                lons = []
                coord_pairs = to_np(temp_bkg_0.coords['xy_loc'])
                for pair in coord_pairs:
                    latlon_str = pair.latlon_str()
                    lats.append(float(latlon_str.split(',')[0]))
                    lons.append(float(latlon_str.split(',')[1]))

                lat_2d, level_2d = np.meshgrid(lats, level, sparse=False, indexing='xy')
                lat_1d = np.reshape(lat_2d, -1)
                level_1d = np.reshape(level_2d, -1)
                bkg_0_1d = np.reshape(temp_bkg_0.data, -1)
                inc_0_1d = np.reshape(temp_anl_0.data-temp_bkg_0.data, -1)
                bkg_0_2d = griddata((lat_1d, level_1d), bkg_0_1d, (lat_2d, level_2d), method='linear')
                inc_0_2d = griddata((lat_1d, level_1d), inc_0_1d, (lat_2d, level_2d), method='linear')

                ax = axs[idc, 0]
                inc_0_contourf = ax.contourf(lat_2d, level_2d, inc_0_2d, levels=np.arange(-10.0,  10.1,  2.0), cmap=cork_map, extend='both', zorder=1)
                bkg_0_contour1 = ax.contour (lat_2d, level_2d, bkg_0_2d, levels=np.arange(  0.0, 200.5, 20.0), linestyles='solid',  colors='k', linewidths=1.0, zorder=2)
                plt.clabel(bkg_0_contour1, bkg_0_contour1.levels[0::1], fontsize=7.5, inline=1, fmt='%1.0f')
                ax.plot(TC_lat[0], 0.0, '^', color='k', ms=10.0)

                ax.set_xticks(np.arange(-5.0, 71.0, 5.0))
                ax.set_xticklabels([ '$\mathrm{5^{\circ}\ S}$', '',  '$\mathrm{5^{\circ}\ N}$', '', \
                                    '$\mathrm{15^{\circ}\ N}$', '', '$\mathrm{25^{\circ}\ N}$', '', \
                                    '$\mathrm{35^{\circ}\ N}$', '', '$\mathrm{45^{\circ}\ N}$', '', \
                                    '$\mathrm{55^{\circ}\ N}$', '', '$\mathrm{65^{\circ}\ N}$', ''])
                ax.set_yticks(np.arange(0, 31, 2.5))
                ax.set_yticklabels(['0', '2.5', '5.0', '7.5', '10.0', '12.5', '15.0', '17.5', '20.0', '22.5', '25.0', '27.5', '30.0'])
                if idc == 1: ax.set_xlabel('Latitude', fontsize=10.0)
                ax.set_ylabel('Height (km)', fontsize=10.0)
                ax.set_title(mtitles[idc][0], fontsize=10.0, pad=4.0)
                ax.tick_params('both', direction='in', labelsize=10.0)
                ax.axis([lat.min(), lat.max(), 0, 17.5])

                casename = case1 + '_d01'
                filename = dir_CPEX + '/track_intensity/best_track/' + casename + '.csv'
                df = pd.read_csv(filename)

                index = []
                for idx, Date_Time in enumerate(df['Date_Time']):
                    time_temp = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
                    if time_temp == draw_time: index = index + [idx]

                TC_lat = list(df['Latitude'][index])
                TC_lon = list(df['Longitude'][index])
                print([TC_lat, TC_lon])

                dir_wrfout_bkg_1 = '/'.join([dir_CPEX, 'cycling_da', 'Data', case1, 'bkg'])
                wrfout_bkg_1 = dir_wrfout_bkg_1 + '/wrfout_' + dom + '_' + draw_time.strftime('%Y-%m-%d_%H:00:00')
                ncfile_bkg_1 = Dataset(wrfout_bkg_1)
                ht_bkg_1 = getvar(ncfile_bkg_1, 'z')
                rh_bkg_1 = getvar(ncfile_bkg_1, 'rh')
                temp_bkg_1 = vertcross(rh_bkg_1, ht_bkg_1, wrfin=ncfile_bkg_1, levels=level*1000.0, start_point=start_point, end_point=end_point, latlon=True, meta=True)
                ncfile_bkg_1.close()

                dir_wrfout_anl_1 = '/'.join([dir_CPEX, 'cycling_da', 'Data', case1, 'da'])
                wrfout_anl_1 = dir_wrfout_anl_1 + '/wrf_inout.' + draw_time.strftime('%Y%m%d%H') + '.' + dom
                ncfile_anl_1 = Dataset(wrfout_anl_1)
                ht_anl_1 = getvar(ncfile_anl_1, 'z')
                rh_anl_1 = getvar(ncfile_anl_1, 'rh')
                temp_anl_1 = vertcross(rh_anl_1, ht_anl_1, wrfin=ncfile_anl_1, levels=level*1000.0, start_point=start_point, end_point=end_point, latlon=True, meta=True)
                ncfile_anl_1.close()

                lats = []
                lons = []
                coord_pairs = to_np(temp_bkg_1.coords['xy_loc'])
                for pair in coord_pairs:
                    latlon_str = pair.latlon_str()
                    lats.append(float(latlon_str.split(',')[0]))
                    lons.append(float(latlon_str.split(',')[1]))

                lat_2d, level_2d = np.meshgrid(lats, level, sparse=False, indexing='xy')
                lat_1d = np.reshape(lat_2d, -1)
                level_1d = np.reshape(level_2d, -1)
                bkg_1_1d = np.reshape(temp_bkg_1.data, -1)
                inc_1_1d = np.reshape(temp_anl_1.data-temp_bkg_1.data, -1)
                bkg_1_2d = griddata((lat_1d, level_1d), bkg_1_1d, (lat_2d, level_2d), method='linear')
                inc_1_2d = griddata((lat_1d, level_1d), inc_1_1d, (lat_2d, level_2d), method='linear')

                ax = axs[idc, 1]
                inc_1_contourf = ax.contourf(lat_2d, level_2d, inc_1_2d, levels=np.arange(-10.0,  10.1,  2.0), cmap=cork_map, extend='both', zorder=1)
                bkg_1_contour1 = ax.contour (lat_2d, level_2d, bkg_1_2d, levels=np.arange(  0.0, 200.5, 20.0), linestyles='solid',  colors='k', linewidths=1.0, zorder=2)
                plt.clabel(bkg_1_contour1, bkg_1_contour1.levels[0::1], fontsize=7.5, inline=1, fmt='%1.0f')
                ax.plot(TC_lat[0], 0.0, '^', color='k', ms=10.0)

                ax.set_xticks(np.arange(-5.0, 71.0, 5.0))
                ax.set_xticklabels([ '$\mathrm{5^{\circ}\ S}$', '',  '$\mathrm{5^{\circ}\ N}$', '', \
                                    '$\mathrm{15^{\circ}\ N}$', '', '$\mathrm{25^{\circ}\ N}$', '', \
                                    '$\mathrm{35^{\circ}\ N}$', '', '$\mathrm{45^{\circ}\ N}$', '', \
                                    '$\mathrm{55^{\circ}\ N}$', '', '$\mathrm{65^{\circ}\ N}$', ''])
                ax.set_yticks(np.arange(0, 31, 2.5))
                ax.set_yticklabels(['0', '2.5', '5.0', '7.5', '10.0', '12.5', '15.0', '17.5', '20.0', '22.5', '25.0', '27.5', '30.0'])
                if idc == 1: ax.set_xlabel('Latitude', fontsize=10.0)
                ax.set_title(mtitles[idc][1], fontsize=10.0, pad=4.0)
                ax.tick_params('both', direction='in', labelsize=10.0)
                ax.axis([lat.min(), lat.max(), 0, 17.5])

                ax = axs[idc, 2]
                inc_diff_contourf = ax.contourf(lat_2d, level_2d, inc_1_2d-inc_0_2d, levels=np.arange(-10.0, 10.1, 2.0), cmap=cork_map, extend='both', zorder=1)
                #bkg_diff_contour1 = ax.contour (lat_2d, level_2d, bkg_1_2d-bkg_0_2d, levels=np.arange(  0.0, 200.5, 20.0), linestyles='solid',  colors='k', linewidths=1.0, zorder=2)
                #plt.clabel(bkg_diff_contour1, bkg_diff_contour1.levels[0::1], fontsize=7.5, inline=1, fmt='%1.0f')
                ax.plot(TC_lat[0], 0.0, '^', color='k', ms=10.0)

                ax.set_xticks(np.arange(-5.0, 71.0, 5.0))
                ax.set_xticklabels([ '$\mathrm{5^{\circ}\ S}$', '',  '$\mathrm{5^{\circ}\ N}$', '', \
                                    '$\mathrm{15^{\circ}\ N}$', '', '$\mathrm{25^{\circ}\ N}$', '', \
                                    '$\mathrm{35^{\circ}\ N}$', '', '$\mathrm{45^{\circ}\ N}$', '', \
                                    '$\mathrm{55^{\circ}\ N}$', '', '$\mathrm{65^{\circ}\ N}$', ''])
                ax.set_yticks(np.arange(0, 31, 2.5))
                ax.set_yticklabels(['0', '2.5', '5.0', '7.5', '10.0', '12.5', '15.0', '17.5', '20.0', '22.5', '25.0', '27.5', '30.0'])
                if idc == 1: ax.set_xlabel('Latitude', fontsize=10.0)
                ax.set_title(mtitles[idc][2], fontsize=10.0, pad=4.0)
                ax.tick_params('both', direction='in', labelsize=10.0)
                ax.axis([lat.min(), lat.max(), 0, 17.5])

        clb1 = fig.colorbar(inc_0_contourf, ax=axs[:, 0:2], ticks=np.arange(-10.0, 10.1, 2.0), orientation='horizontal', pad=0.075, aspect=50, shrink=1.00)
        clb1.set_label('RH increment (%) on ' + draw_time_string, fontsize=10.0, labelpad=4.0)
        clb1.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

        clb2 = fig.colorbar(inc_diff_contourf, ax=axs[:, 2], ticks=np.arange(-10.0, 10.1, 2.0), orientation='horizontal', pad=0.075, aspect=25, shrink=1.10)
        clb2.set_label('Difference of increment (%)', fontsize=10.0, labelpad=4.0)
        clb2.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

        plt.savefig('./fig11.png', dpi=300)
        pdf.savefig(fig)
        plt.cla()
        plt.clf()
        plt.close()
