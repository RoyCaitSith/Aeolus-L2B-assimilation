import os
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import LinearSegmentedColormap
from wrf import to_np, getvar, CoordPair, vertcross, latlon_coords, interplevel
from scipy.interpolate import griddata
from metpy.units import units
from metpy.calc import divergence
from geopy.distance import great_circle

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS'
dir_main = dir_CPEX + '/increment'

domains = ['d01']
resolutions = [12000.0, 4000.0]

cases = [['CON6h_082418_Hybrid_C08', 'CON6h_Aeolus6h_082418_Hybrid_C08'], ['CON6h_082500_Hybrid_C08', 'CON6h_Aeolus6h_082500_Hybrid_C08']]
labels = [['2418', '2418_L2B'], ['2500', '2500_L2B']]

dir_batlow = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS/figures_V3/ScientificColourMaps7/batlow'
batlow_cm_data = np.loadtxt(dir_batlow + '/batlow.txt')
batlow_map_r = LinearSegmentedColormap.from_list('batlow', batlow_cm_data[::-1])
colors = [batlow_cm_data[74], batlow_cm_data[223]]

dir_grayC = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS/figures_V3/ScientificColourMaps7/grayC'
grayC_cm_data = np.loadtxt(dir_grayC + '/grayC.txt')
grayC_map = LinearSegmentedColormap.from_list('grayC', grayC_cm_data[::1])

draw_times = [datetime.datetime(2021, 8, 25, 12, 0, 0), datetime.datetime(2021, 8, 26, 12, 0, 0)]
draw_time_strings = ['25 August 2021, 12:00 UTC', '26 August 2021, 12:00 UTC']
linestyles = ['--', '-']
mtitles = [['(a)', '(b)'], ['(c)', '(d)']]

r = 300.0
levels = np.arange(100, 900.1, 100.0)

for idd, dom in enumerate(domains):

    pdfname = './fig12.pdf'

    with PdfPages(pdfname) as pdf:

        fig, axs = plt.subplots(2, 2, figsize=(6.5, 12.0))
        fig.subplots_adjust(left=0.100, bottom=0.050, right=0.975, top=0.980, wspace=0.1625, hspace=0.100)

        for idc, case in enumerate(cases):

            ax = axs[0, idc]

            for idt, time_now in enumerate(draw_times):

                time_now_str = time_now.strftime('%Y%m%d%H')

                for ide, exp in enumerate(case):

                    label = labels[idc][ide]
                    casename = exp + '_d01'
                    filename = dir_CPEX + '/track_intensity/best_track/' + casename + '.csv'
                    df = pd.read_csv(filename)

                    index = []
                    for idx, Date_Time in enumerate(df['Date_Time']):
                        time_temp = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
                        if time_temp == time_now: index = index + [idx]

                    TC_lat = list(df['Latitude'][index])
                    TC_lon = list(df['Longitude'][index])

                    dir_wrfout_bkg = '/'.join([dir_CPEX, 'cycling_da', 'Data', exp, 'bkg'])
                    wrfout_bkg = dir_wrfout_bkg + '/wrfout_' + dom + '_' + time_now.strftime('%Y-%m-%d_%H:00:00')
                    ncfile_bkg = Dataset(wrfout_bkg)
                    p_bkg = getvar(ncfile_bkg, 'pressure')
                    ua_bkg = getvar(ncfile_bkg, 'ua', units='ms-1')
                    va_bkg = getvar(ncfile_bkg, 'va', units='ms-1')
                    lat, lon = latlon_coords(p_bkg)
                    tmp_ua_bkg = interplevel(ua_bkg, p_bkg, levels)
                    tmp_va_bkg = interplevel(va_bkg, p_bkg, levels)
                    ncfile_bkg.close()

                    dir_wrfout_anl = '/'.join([dir_CPEX, 'cycling_da', 'Data', exp, 'da'])
                    wrfout_anl = dir_wrfout_anl + '/wrf_inout.' + time_now.strftime('%Y%m%d%H') + '.' + dom
                    ncfile_anl = Dataset(wrfout_anl)
                    p_anl = getvar(ncfile_bkg, 'pressure')
                    ua_anl = getvar(ncfile_anl, 'ua', units='ms-1')
                    va_anl = getvar(ncfile_anl, 'va', units='ms-1')
                    tmp_ua_anl = interplevel(ua_anl, p_anl, levels)
                    tmp_va_anl = interplevel(va_anl, p_anl, levels)
                    ncfile_anl.close()

                    (n_lat, n_lon) = lat.shape
                    mask_latlon = np.ones((n_lat, n_lon), dtype=bool)
                    for idlat in range(n_lat):
                        for idlon in range(n_lon):
                            distance = great_circle((float(lat[idlat, idlon]), float(lon[idlat, idlon])), (TC_lat[0], TC_lon[0])).kilometers
                            if distance <= 300:
                                mask_latlon[idlat, idlon] = False

                    divs = []
                    for idl, lev in enumerate(levels):
                        tmp_bkg = divergence(np.array(tmp_ua_bkg[idl,:,:])*units('m/s'), np.array(tmp_va_bkg[idl,:,:])*units('m/s'), \
                                             dx=resolutions[idd]*units('m'), dy=resolutions[idd]*units('m'), x_dim=-1, y_dim=-2)
                        tmp_anl = divergence(np.array(tmp_ua_anl[idl,:,:])*units('m/s'), np.array(tmp_va_anl[idl,:,:])*units('m/s'), \
                                             dx=resolutions[idd]*units('m'), dy=resolutions[idd]*units('m'), x_dim=-1, y_dim=-2)
                        tmp_bkg = tmp_bkg*100000.0
                        tmp_anl = tmp_anl*100000.0
                        tmp_inc = tmp_anl-tmp_bkg
                        tmp_inc_masked = np.ma.array(tmp_inc, mask=mask_latlon)
                        np.ma.masked_invalid(tmp_inc_masked)
                        divs.append(np.nanmean(tmp_inc_masked))

                    ax.plot(divs, levels, 'o', color=colors[idt], ls=linestyles[ide], ms=2.00, linewidth=1.25, label=draw_time_strings[idt] + ', ' + label, zorder=3)
                    #ax.plot([0, 0], [0, 2000.0], '-', color='k', linewidth=1.25)

                    ax.set_xlabel('Increment of divergence ($\mathregular{10^{-5}\ s^{-1}}$)', fontsize=10.0)
                    if idc==0: ax.set_ylabel('Pressure (hPa)', fontsize=10.0)
                    ax.set_xticks(np.arange(-1.0, 1.1, 0.5))
                    ax.set_yticks(np.arange(200.0, 901.0, 200.0))
                    ax.tick_params('both', direction='in', labelsize=10.0)
                    ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])
                    ax.axis([-1.0, 1.0, 100, 900])
                    ax.text(-0.90, 125.0, mtitles[0][idc], fontsize=10.0)
                    ax.invert_yaxis()
                    ax.legend(loc='lower left', fontsize=7.5, handlelength=2.5).set_zorder(102)

            ax = axs[1, idc]

            for idt, time_now in enumerate(draw_times):

                time_now_str = time_now.strftime('%Y%m%d%H')

                for ide, exp in enumerate(case):

                    label = labels[idc][ide]
                    casename = exp + '_d01'
                    filename = dir_CPEX + '/track_intensity/best_track/' + casename + '.csv'
                    df = pd.read_csv(filename)

                    index = []
                    for idx, Date_Time in enumerate(df['Date_Time']):
                        time_temp = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
                        if time_temp == time_now: index = index + [idx]

                    TC_lat = list(df['Latitude'][index])
                    TC_lon = list(df['Longitude'][index])

                    dir_wrfout_bkg = '/'.join([dir_CPEX, 'cycling_da', 'Data', exp, 'bkg'])
                    wrfout_bkg = dir_wrfout_bkg + '/wrfout_' + dom + '_' + time_now.strftime('%Y-%m-%d_%H:00:00')
                    ncfile_bkg = Dataset(wrfout_bkg)
                    p_bkg = getvar(ncfile_bkg, 'pressure')
                    var_bkg = getvar(ncfile_bkg, 'rh')
                    lat, lon = latlon_coords(p_bkg)
                    tmp_var_bkg = interplevel(var_bkg, p_bkg, levels)
                    ncfile_bkg.close()

                    dir_wrfout_anl = '/'.join([dir_CPEX, 'cycling_da', 'Data', exp, 'da'])
                    wrfout_anl = dir_wrfout_anl + '/wrf_inout.' + time_now.strftime('%Y%m%d%H') + '.' + dom
                    ncfile_anl = Dataset(wrfout_anl)
                    p_anl = getvar(ncfile_bkg, 'pressure')
                    var_anl = getvar(ncfile_anl, 'rh')
                    tmp_var_anl = interplevel(var_anl, p_anl, levels)
                    ncfile_anl.close()

                    (n_lat, n_lon) = lat.shape
                    mask_latlon = np.ones((n_lat, n_lon), dtype=bool)
                    for idlat in range(n_lat):
                        for idlon in range(n_lon):
                            distance = great_circle((float(lat[idlat, idlon]), float(lon[idlat, idlon])), (TC_lat[0], TC_lon[0])).kilometers
                            if distance <= 300:
                                mask_latlon[idlat, idlon] = False

                    rhs = []
                    for idl, lev in enumerate(levels):
                        tmp_bkg = tmp_var_bkg[idl,:,:]
                        tmp_anl = tmp_var_anl[idl,:,:]
                        tmp_inc = tmp_anl-tmp_bkg
                        tmp_inc_masked = np.ma.array(tmp_inc, mask=mask_latlon)
                        np.ma.masked_invalid(tmp_inc_masked)
                        rhs.append(np.nanmean(tmp_inc_masked))

                    ax.plot(rhs, levels, 'o', color=colors[idt], ls=linestyles[ide], ms=2.00, linewidth=1.25, label=draw_time_strings[idt] + ', ' + label, zorder=3)
                    #ax.plot([0, 0], [0, 2000.0], '-', color='k', linewidth=1.25)

                    ax.set_xlabel('Increment of RH (%)', fontsize=10.0)
                    if idc==0: ax.set_ylabel('Pressure (hPa)', fontsize=10.0)
                    ax.set_xticks(np.arange(-6.0, 6.1, 3.0))
                    ax.set_yticks(np.arange(200.0, 901.0, 200.0))
                    ax.tick_params('both', direction='in', labelsize=10.0)
                    ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])
                    ax.axis([-6.0, 6.0, 100, 900])
                    ax.text(-5.4, 125.0, mtitles[1][idc], fontsize=10.0)
                    ax.invert_yaxis()
                    ax.legend(loc='lower left', fontsize=7.5, handlelength=2.5).set_zorder(102)

        plt.savefig('./fig12.png', dpi=300)
        pdf.savefig(fig)
        plt.cla()
        plt.clf()
        plt.close()
