import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from wrf import getvar
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_pdf import PdfPages

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021'
dir_main = dir_CPEX + '/rainfall'

#cases = ['IMERG', 'CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_DAWN1hOE1p5', 'CON6h_HALO1h', 'CON6h_HALO1hOE0p2', 'CON6h_DS1h', 'CON6h_Aeolus6h', 'CON6h_DAWN1h_HALO1h_DS1h']
#labels = ['IMERG', 'CTRL', 'DAWN', 'DAWNOE1', 'DAWNOE1p5', 'HALO', 'HALOOE0p2', 'DS', 'Aeolus', 'HRFD']

cases = ['IMERG', 'CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_DAWN1hOE1p5', 'CON6h_HALO1h', 'CON6h_DS1h', 'CON6h_Aeolus6h', 'CON6h_DAWN1h_HALO1h_DS1h', 'CON6h_DAWN1h_HALO1h_DS1h_Aeolus6h']
labels = ['IMERG', 'CTRL', 'DAWN', 'DAWNOE1', 'DAWNOE1p5', 'HALO', 'DS', 'Aeolus', 'HRFD', 'HRFD + Aeolus']

time = '20210820'
domains = ['d01']

if '20210820' in time:
    draw_times = [1, 4]
    AEW_locations = [(-72.115, 15.04), (-79.095, 17.095)]
if '20210821' in time:
    draw_times = [1, 4]
    AEW_locations = [(-50.83, 12.23), (-53.93, 12.34)]

rain_levels = [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.6, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, \
               6.0, 8.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0]
rain_labels = ['0.1', '0.15', '0.2', '0.25', '0.3', '0.4', '0.6', '1.0', '1.5', \
               '2', '3', '4', '5', '6', '8', '10', '15', '20', '25', '30', '35', '40']

for dom in domains:

    pdfname = dir_main + '/' + time + '/figures/rainfall_' + dom + '.pdf'
    print(pdfname)

    with PdfPages(pdfname) as pdf:

        fig, axs = plt.subplots(5, 4, figsize=(12.0, 14.0))
        fig.subplots_adjust(left=0.025, bottom=-0.100, right=0.975, top=0.990, wspace=0.100, hspace=0.100)

        idx = 0
        for idt, time_now in enumerate(draw_times):
            for idc, case in enumerate(cases):

                var = 'rainfall'
                filename = dir_main + '/' + time + '/' + case + '/rainfall_6h_' + dom + '.nc'
                ncfile   = Dataset(filename)
                rain     = ncfile.variables[var][time_now,:,:]
                rain_lat = ncfile.variables['lat'][:,:]
                rain_lon = ncfile.variables['lon'][:,:]
                ncfile.close()

                (AEW_lon, AEW_lat) = AEW_locations[idt]
                label = labels[idc]
                extent = [AEW_lon-7.5, AEW_lon+7.5, AEW_lat-7.5, AEW_lat+7.5]

                irow = idx//5
                icol = idx%5
                print(irow, icol)
                ax = axs[icol, irow]

                m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                m.drawparallels(np.arange(-10,  36, 5), labels=[1,0,0,0], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)
                m.drawmeridians(np.arange(-95, -29, 5), labels=[0,0,0,1], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)

                rain[rain<=0] = 0
                rain_lon, rain_lat = m(rain_lon, rain_lat, inverse=False)
                pcm = ax.contourf(rain_lon, rain_lat, rain, locator=ticker.LogLocator(), levels=rain_levels, cmap='jet', extend='max', zorder=1)
                ax.plot(AEW_lon, AEW_lat, 'x', color='k', markersize=7.5, markeredgewidth=1.0)
                ax.text(AEW_lon-6.75, AEW_lat+6.75, '(' + chr(97+idc) + str(idt+1) + ') ' + label, ha='left', va='center', color='k', fontsize=10.0, zorder=7)
                idx += 1

        clb = fig.colorbar(pcm, ax=axs, orientation='horizontal', pad=0.025, aspect=50, shrink=1.00)
        clb.set_label('6-hr Accumulated Precipitation (mm/hr)', fontsize=10.0, labelpad=4.0)
        clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
        clb.ax.minorticks_off()
        clb.set_ticks(rain_levels)
        clb.set_ticklabels(rain_labels)

        pdf.savefig(fig)
        plt.cla()
        plt.clf()
        plt.close()
