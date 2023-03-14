import os
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from netCDF4 import Dataset
from matplotlib.backends.backend_pdf import PdfPages
from wrf import to_np, getvar, CoordPair, vertcross
from scipy.interpolate import griddata

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS'
dir_main = dir_CPEX + '/cross_section'

domains = ['d01', 'd02']

#cases = ['CON6h_082406_Hybrid_C08', 'CON6h_Aeolus6h_082406_Hybrid_C08']
#labels = ['082406_C08', 'Aeolus_082406_C08']
#cases = ['CON6h_082412_Hybrid_C08', 'CON6h_Aeolus6h_082412_Hybrid_C08']
#labels = ['082412_C08', 'Aeolus_082412_C08']
#cases = ['CON6h_082418_Hybrid_C08', 'CON6h_Aeolus6h_082418_Hybrid_C08']
#labels = ['082418_C08', 'Aeolus_082418_C08']
cases = ['CON6h_082500_Hybrid_C08', 'CON6h_Aeolus6h_082500_Hybrid_C08']
labels = ['082500_C08', 'Aeolus_082500_C08']

draw_times = [datetime.datetime(2021, 8, 24, 12, 0, 0), datetime.datetime(2021, 8, 25, 12, 0, 0), datetime.datetime(2021, 8, 26, 12, 0, 0)]
lonmin = -80.0
lonmax = -60.0

for dom in domains:
    for idc, case in enumerate(cases):

        label = labels[idc]

        dir_bufr = '/'.join([dir_CPEX, 'display_bufr', cases[1]])
        dir_pdf = dir_main + '/rh/' + case
        os.system('mkdir ' + dir_pdf)

        casename = case + '_d01'
        filename = dir_CPEX + '/track_intensity/best_track/' + casename + '.csv'

        df = pd.read_csv(filename)

        for idc, time_now in enumerate(draw_times):

            time_now_str = time_now.strftime('%Y%m%d%H')
            bufrname = dir_bufr + '/' + time_now_str + '_ges_' + dom + '.nc'
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

                index = []
                for idx, Date_Time in enumerate(df['Date_Time']):
                    time_temp = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
                    if time_temp == time_now: index = index + [idx]

                TC_lat = list(df['Latitude'][index])
                TC_lon = list(df['Longitude'][index])
                print([TC_lat, TC_lon])

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

                pdfname = '_'.join([time_now_str, 'rh', case, dom+'.pdf'])
                pdfname = dir_pdf + '/' + pdfname
                print(pdfname)

                with PdfPages(pdfname) as pdf:

                    fig, axs = plt.subplots(1, 1, figsize=(6.0, 6.0))
                    fig.subplots_adjust(left=0.075, bottom=-0.050, right=0.975, top=0.980, wspace=0.100, hspace=0.100)

                    dir_wrfout_bkg = '/'.join([dir_CPEX, 'cycling_da', 'Data', case, 'bkg'])
                    wrfout_bkg = dir_wrfout_bkg + '/wrfout_' + dom + '_' + time_now.strftime('%Y-%m-%d_%H:00:00')
                    ncfile_bkg = Dataset(wrfout_bkg)
                    ht_bkg = getvar(ncfile_bkg, 'z')
                    rh_bkg = getvar(ncfile_bkg, 'rh')
                    temp_bkg = vertcross(rh_bkg, ht_bkg, wrfin=ncfile_bkg, levels=level*1000.0, start_point=start_point, end_point=end_point, latlon=True, meta=True)
                    ncfile_bkg.close()

                    dir_wrfout_anl = '/'.join([dir_CPEX, 'cycling_da', 'Data', case, 'da'])
                    wrfout_anl = dir_wrfout_anl + '/wrf_inout.' + time_now.strftime('%Y%m%d%H') + '.' + dom
                    ncfile_anl = Dataset(wrfout_anl)
                    ht_anl = getvar(ncfile_anl, 'z')
                    rh_anl = getvar(ncfile_anl, 'rh')
                    temp_anl = vertcross(rh_anl, ht_anl, wrfin=ncfile_anl, levels=level*1000.0, start_point=start_point, end_point=end_point, latlon=True, meta=True)
                    ncfile_anl.close()

                    lats = []
                    lons = []
                    coord_pairs = to_np(temp_bkg.coords['xy_loc'])
                    for pair in coord_pairs:
                        latlon_str = pair.latlon_str()
                        lats.append(float(latlon_str.split(',')[0]))
                        lons.append(float(latlon_str.split(',')[1]))

                    lat_2d, level_2d = np.meshgrid(lats, level, sparse=False, indexing='xy')
                    lat_1d = np.reshape(lat_2d, -1)
                    level_1d = np.reshape(level_2d, -1)
                    bkg_1d = np.reshape(temp_bkg.data, -1)
                    inc_1d = np.reshape(temp_anl.data-temp_bkg.data, -1)
                    bkg_2d = griddata((lat_1d, level_1d), bkg_1d, (lat_2d, level_2d), method='linear')
                    inc_2d = griddata((lat_1d, level_1d), inc_1d, (lat_2d, level_2d), method='linear')

                    ax = axs
                    inc_contourf = ax.contourf(lat_2d, level_2d, inc_2d, levels=np.arange(-5.0, 5.1, 1.0), cmap='BrBG', extend='both', zorder=1)
                    bkg_contour1 = ax.contour(lat_2d, level_2d, bkg_2d, levels=np.arange(0.0, 200.0, 20.0), linestyles='solid',  colors='k', linewidths=1.0, zorder=2)
                    ax.plot(TC_lat[0], 0.0, '^', color='k', ms=10.0)

                    ax.set_xticks(np.arange(-10.0, 71.0, 5.0))
                    ax.set_xticklabels(['10S', '5S', '0', '5N', '10N', '15N', '20N', '25N', '30N', '35N', '40N', '45N', '50N', '55N', '60N', '65N', '70N'])
                    ax.set_yticks(np.arange(0, 31, 5.0))
                    ax.set_yticklabels(['0', '5', '10', '15', '20', '25', '30'])
                    ax.set_xlabel('Latitude', fontsize=10.0)
                    ax.set_ylabel('Height (km)', fontsize=10.0)
                    ax.tick_params('both', direction='in', labelsize=10.0)
                    ax.axis([lat.min(), lat.max(), 0, 30])

                    clb = fig.colorbar(inc_contourf, ax=axs, ticks=np.arange(-5.0, 5.1, 1.0), orientation='horizontal', pad=0.075, aspect=50, shrink=1.00)
                    clb.set_label('RH Increment (%) of Exp. ' + label + \
                                  ' at ' + time_now_str, fontsize=7.5, labelpad=4.0)
                    clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
                    plt.clabel(bkg_contour1, bkg_contour1.levels[0::1], fontsize=10.0, inline=1, fmt='%1.0f')

                    pdf.savefig(fig)
                    plt.cla()
                    plt.clf()
                    plt.close()
