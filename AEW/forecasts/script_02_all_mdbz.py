import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from wrf import getvar
from netCDF4 import Dataset
from cpt_convert import loadCPT
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_pdf import PdfPages

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021'
dir_main = dir_CPEX + '/forecasts'

#cases = ['CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_DAWN1hOE1p5', 'CON6h_HALO1h', 'CON6h_HALO1hOE0p2', 'CON6h_DS1h', 'CON6h_Aeolus6h', 'CON6h_DAWN1h_HALO1h_DS1h', 'CON6h_DAWN1h_HALO1h_DS1h_Aeolus6h']
#labels = ['CTRL', 'DAWN', 'DAWNOE1', 'DAWNOE1p5', 'HALO', 'HALOOE0p2', 'DS', 'Aeolus', 'HRFD', 'HRFD + Aeolus']

cases = ['CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_DAWN1hOE1p5', 'CON6h_HALO1h', 'CON6h_HALO1h', 'CON6h_DS1h', 'CON6h_Aeolus6h', 'CON6h_DAWN1h_HALO1h_DS1h', 'CON6h_DAWN1h_HALO1h_DS1h_Aeolus6h']
labels = ['CTRL', 'DAWN', 'DAWNOE1', 'DAWNOE1p5', 'HALO', 'HALOOE0p2', 'DS', 'Aeolus', 'HRFD', 'HRFD + Aeolus']

time = '20210821'
domains = ['d01']

if '20210820' in time:
    draw_times = [datetime.datetime(2021, 8, 21,  2, 0, 0), datetime.datetime(2021, 8, 22,  0, 0, 0)]
    AEW_locations = [(-71.81, 14.95), (-80.45, 17.15)]
if '20210821' in time:
    draw_times = [datetime.datetime(2021, 8, 22,  1, 0, 0), datetime.datetime(2021, 8, 22, 15, 0, 0)]
    AEW_locations = [(-50.42, 12.26), (-53.93, 12.34)]

cpt = loadCPT('./colormaps/PU_Rain_rate.rgb')
cpt_convert = LinearSegmentedColormap('cpt', cpt)
levs = np.array([-5, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70])

for dom in domains:

    pdfname = dir_main + '/' + time + '/mdbz/mdbz_' + dom + '.pdf'
    print(pdfname)

    with PdfPages(pdfname) as pdf:

        fig, axs = plt.subplots(5, 4, figsize=(12.0, 14.0))
        fig.subplots_adjust(left=0.025, bottom=-0.125, right=0.975, top=0.990, wspace=0.100, hspace=0.100)

        idx = 0
        for idt, time_now in enumerate(draw_times):
            for idc, case in enumerate(cases):

                dir_wrfout = dir_CPEX + '/bkg/' + time + '/' + case
                time_now_str = time_now.strftime('%Y%m%d%H')
                file_wrf = dir_wrfout + '/wrfout_' + dom + '_' + time_now.strftime('%Y-%m-%d_%H:00:00')
                print(file_wrf)

                ncfile = Dataset(file_wrf)
                lat = ncfile.variables['XLAT'][0,:,:]
                lon = ncfile.variables['XLONG'][0,:,:]
                mdbz = getvar(ncfile, 'mdbz')
                slp = getvar(ncfile, 'slp', units='hPa')
                (u10, v10) = getvar(ncfile, 'uvmet10', units='kt')
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

                pcm = ax.contourf(lon, lat, mdbz, levels=levs, cmap=cpt_convert, extend='max', zorder=1)
                ax.plot(AEW_lon, AEW_lat, 'x', color='k', markersize=7.5, markeredgewidth=1.0)
                ax.text(AEW_lon-6.75, AEW_lat+6.75, '(' + chr(97+idc) + str(idt+1) + ') ' + label, ha='left', va='center', color='k', fontsize=10.0, zorder=7)

                idx += 1

        clb = fig.colorbar(pcm, ax=axs, ticks=levs, orientation='horizontal', pad=0.025, aspect=50, shrink=1.00)
        clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

        pdf.savefig(fig)
        plt.cla()
        plt.clf()
        plt.close()
