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
    filename = dir_file + '/va_' + dom + '.nc'
    ncfile   = Dataset(filename)
    lat      = ncfile.variables['lat'][:,:]
    lon      = ncfile.variables['lon'][:,:]
    level    = ncfile.variables['level'][:]
    #va       = np.mean(ncfile.variables['va'][:,:, 95:187,:], axis=2)
    va       = np.mean(ncfile.variables['va'][:,:,131:225,:], axis=2)
    ncfile.close()

    xi = lon[0, :]
    yi = np.arange(0, n_time)
    Xi, Yi = np.meshgrid(xi, yi)
    extent = [lon[0,0], lon[-1,-1], 0, n_time-1]

    pdfname = dir_file + '/Hovmoller_v_' + dom + '.pdf'
    with PdfPages(pdfname) as pdf:

        start_time_str = start_time.strftime('%Y%m%d%H')
        end_time_str   = end_time.strftime('%Y%m%d%H')

        fig, axs   = plt.subplots(1, 3, figsize=(9.00, 4.00))
        fig.subplots_adjust(left=0.050, bottom=-0.025, right=0.985, top=0.900, wspace=0.200, hspace=0.250)
        suptitle_str = start_time_str + ', ' + end_time_str + ', ' + dom + ', v'
        fig.suptitle(suptitle_str, fontsize=7.5)

        for idl, lev in enumerate(level[0:3]):

            ax = axs[idl]
            pcm = ax.contourf(Xi, Yi, va[::-1,idl,:], levels=np.arange(-4.5, 5.0, 1.0), cmap='RdBu_r', extend='both', zorder=0)

            ax.set_yticks([1, 5, 9, 13])
            #ax.set_yticklabels(['08/22', '08/21', '08/20', '08/19'], rotation=90, va='center')
            ax.set_yticklabels(['08/23', '08/22', '08/21', '08/20'], rotation=90, va='center')
            mtitle = '(' + chr(97+idl) + ') ' + str(int(lev)) + ' hPa'
            ax.set_title(mtitle, fontsize=7.5, pad=4.0)

        clb = fig.colorbar(pcm, ax=axs, orientation='horizontal', pad=0.100, aspect=75, shrink=1.00)
        clb.set_label('v (m/s)', fontsize=7.5, labelpad=4.0)
        clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=7.5)
        clb.set_ticks(np.arange(-4.5, 5.0, 1.0))

        pdf.savefig(fig)
        plt.cla()
        plt.clf()
        plt.close()
