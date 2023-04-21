import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from wrf import getvar
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import LinearSegmentedColormap
from subroutine import cal_polar_to_latlon as clatlon

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021'
dir_main = dir_CPEX + '/rainfall'
dir_wind = dir_CPEX + '/AEW'

cases = ['IMERG', 'CON6h', 'CON6h_Aeolus6h']
wind_cases = ['GFS', 'CON6h', 'CON6h_Aeolus6h']
mtitles = ['(a)', '(b)', '(c)']

time = '20210820'
domains = ['d01']

dir_batlowW = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS/figures_V3/ScientificColourMaps7/batlowW'
batlowW_cm_data = np.loadtxt(dir_batlowW + '/batlowW.txt')
batlowW_map_r = LinearSegmentedColormap.from_list('batlowW', batlowW_cm_data[::-1])

dir_grayC = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS/figures_V3/ScientificColourMaps7/grayC'
grayC_cm_data = np.loadtxt(dir_grayC + '/grayC.txt')
grayC_map = LinearSegmentedColormap.from_list('grayC', grayC_cm_data[::1])

if '20210820' in time:
    draw_times = [3]
    AEW_locations = [(-79.095, 17.095)]

rain_levels = [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.6, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, \
               6.0, 8.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0]
rain_labels = ['0.1', '0.15', '0.2', '0.25', '0.3', '0.4', '0.6', '1.0', '1.5', \
               '2', '3', '4', '5', '6', '8', '10', '15', '20', '25', '30', '35', '40']

radii = [150.0, 300.0, 450.0]
angles = np.arange(0.0, 360.0, 2.0)

for dom in domains:

    pdfname = './fig13.pdf'
    print(pdfname)

    with PdfPages(pdfname) as pdf:

        fig, axs = plt.subplots(1, 3, figsize=(9.0, 3.25))
        fig.subplots_adjust(left=0.050, bottom=0.025, right=0.975, top=0.990, wspace=0.200, hspace=0.100)

        for idt, time_now in enumerate(draw_times):
            for idc, (case, wind_case) in enumerate(zip(cases, wind_cases)):

                var = 'rainfall'
                filename = dir_main + '/' + time + '/' + case + '/rainfall_6h_' + dom + '.nc'
                ncfile   = Dataset(filename)
                rain     = ncfile.variables[var][time_now,:,:]*6.0
                rain_lat = ncfile.variables['lat'][:,:]
                rain_lon = ncfile.variables['lon'][:,:]
                ncfile.close()

                var = 'div'
                filename = dir_wind + '/' + time + '/' + wind_case + '/div_' + dom + '.nc'
                ncfile   = Dataset(filename)
                div      = ncfile.variables[var][-2,1,:,:]*100000.0
                div_lat  = ncfile.variables['lat'][:,:]
                div_lon  = ncfile.variables['lon'][:,:]
                ncfile.close()

                (AEW_lon, AEW_lat) = AEW_locations[idt]
                extent = [AEW_lon-5.0, AEW_lon+5.0, AEW_lat-5.0, AEW_lat+5.0]

                ax = axs[idc]

                m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                m.drawparallels(np.arange(-10,  36, 5), labels=[1,0,0,0], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)
                m.drawmeridians(np.arange(-95, -29, 5), labels=[0,0,0,1], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)

                rain[rain<=0] = 0
                rain_lon, rain_lat = m(rain_lon, rain_lat, inverse=False)
                pcm = ax.contourf(rain_lon, rain_lat, rain, locator=ticker.LogLocator(), levels=rain_levels, cmap=batlowW_map_r, extend='max', zorder=1)
                #ax.plot(AEW_lon, AEW_lat, 'x', color='k', markersize=10.0, markeredgewidth=1.25)
                #div_contour1 = ax.contour(div_lon, div_lat, div, levels=np.arange(-35.0, -0.5, 10.0), linestyles='dashed', colors='k', linewidths=1.0, zorder=2)
                div_contour2 = ax.contour(div_lon, div_lat, div, levels=np.arange(  5.0, 5.5, 10.0), linestyles='solid',  colors='k', linewidths=1.0, zorder=2)
                #plt.clabel(div_contour1, div_contour1.levels[1::2], fontsize=5.0, inline=1, fmt='%1.0f')
                #plt.clabel(div_contour2, div_contour2.levels[1::2], fontsize=5.0, inline=1, fmt='%1.0f')
                ax.plot([-180.0, 180.0], [AEW_lat, AEW_lat], '--', color=grayC_cm_data[53], linewidth=0.5, zorder=3)
                ax.plot([AEW_lon, AEW_lon], [-90.0, 90.0],   '--', color=grayC_cm_data[53], linewidth=0.5, zorder=3)
                ax.text(AEW_lon-4.3, AEW_lat+4.4, mtitles[idc], ha='center', va='center', color='k', fontsize=10.0, \
                        bbox=dict(boxstyle='round', ec=grayC_cm_data[53], fc=grayC_cm_data[0]), zorder=7)

                lat_polar = np.zeros((len(radii), len(angles)))
                lon_polar = np.zeros((len(radii), len(angles)))
                for idr in range(0, len(radii)):
                    for ida in range(0, len(angles)):
                        lat_polar[idr,ida], lon_polar[idr,ida] = clatlon.Cal_LatLon(AEW_lat, AEW_lon, radii[idr], angles[ida])
                    ax.plot(lon_polar[idr,:], lat_polar[idr,:], '--', color=grayC_cm_data[53], linewidth=0.5, zorder=3)

        clb = fig.colorbar(pcm, ax=axs, orientation='horizontal', pad=0.060, aspect=50, shrink=1.00)
        clb.set_label('Six hour accumulated precipitation (mm)', fontsize=10.0, labelpad=4.0)
        clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
        clb.ax.minorticks_off()
        clb.set_ticks(rain_levels)
        clb.set_ticklabels(rain_labels)

        plt.savefig('./fig13.png', dpi=300)
        pdf.savefig(fig)
        plt.cla()
        plt.clf()
        plt.close()
