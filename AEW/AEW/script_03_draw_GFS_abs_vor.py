import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import datetime
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.basemap import Basemap

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021'
dir_main = dir_CPEX + '/AEW'

case = 'GFS'
time = '20210821'

if '20210820' in time:
    start_time = datetime.datetime(2021, 8, 19,  0, 0, 0)
    end_time   = datetime.datetime(2021, 8, 22,  6, 0, 0)
if '20210821' in time:
    start_time = datetime.datetime(2021, 8, 20,  0, 0, 0)
    end_time   = datetime.datetime(2021, 8, 23,  6, 0, 0)

domains = ['d01']
cycling_interval = 6
n_time = int((end_time - start_time).total_seconds()/3600/6+1)

for dom in domains:

    dir_file = dir_main + '/' + time + '/' + case
    filename = dir_file + '/avo_' + dom + '.nc'
    ncfile   = Dataset(filename)
    lat      = ncfile.variables['lat'][:,:]
    lon      = ncfile.variables['lon'][:,:]
    level    = ncfile.variables['level'][:]
    avo      = ncfile.variables['avo'][:,:,:,:]*10000.0
    ncfile.close()

    extent = [lon[0,0], lon[-1,-1], lat[0,0], lat[-1,-1]]

    pdfname = dir_file + '/avo_' + dom + '.pdf'
    with PdfPages(pdfname) as pdf:
        for idt in range(0, n_time):

            time_now     = start_time + datetime.timedelta(hours = idt*cycling_interval)
            time_now_str = time_now.strftime('%Y%m%d%H')
            print(time_now)

            fig, axs   = plt.subplots(1, 3, figsize=(9.00, 2.90))
            fig.subplots_adjust(left=0.050, bottom=0.025, right=0.985, top=0.950, wspace=0.200, hspace=0.250)
            suptitle_str = time_now_str + ', ' + dom + ', absolute vorticity'
            fig.suptitle(suptitle_str, fontsize=7.5)

            for idl, lev in enumerate(level[0:3]):

                ax = axs[idl]
                m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                m.drawcoastlines(linewidth=0.2, color='k')
                m.drawparallels(np.arange(int(extent[2]), int(extent[3])+1, 10), labels=[1,0,0,0], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])
                m.drawmeridians(np.arange(int(extent[0]), int(extent[1])+1, 10), labels=[0,0,0,1], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])

                pcm = ax.contourf(lon, lat, avo[idt,idl,:,:], levels=np.arange(-0.9, 1.0, 0.2), cmap='RdBu_r', extend='both', zorder=0)

                mtitle = '(' + chr(97+idl) + ') ' + str(int(lev)) + ' hPa'
                ax.set_title(mtitle, fontsize=7.5, pad=4.0)

            clb = fig.colorbar(pcm, ax=axs, orientation='horizontal', pad=0.100, aspect=75, shrink=1.00)
            clb.set_label('absolute vorticity $\mathregular{10^{-4} s^{-1}}$', fontsize=7.5, labelpad=4.0)
            clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=7.5)
            clb.set_ticks(np.arange(-0.9, 1.0, 0.2))

            pdf.savefig(fig)
            plt.cla()
            plt.clf()
            plt.close()
