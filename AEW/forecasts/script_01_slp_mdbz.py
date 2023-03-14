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

cases = ['CON6h_DAWN1hOE1p5', 'CON6h_HALO1hOE0p2']
#cases = ['CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_HALO1h', 'CON6h_DS1h', 'CON6h_Aeolus6h', 'CON6h_DAWN1h_HALO1h_DS1h', 'CON6h_DAWN1h_HALO1h_DS1h_Aeolus6h']

time = '20210904'
domains = ['d01', 'd02']

if '20210820' in time:
    forecast_start_time = datetime.datetime(2021, 8, 20, 18, 0, 0)
    forecast_end_time   = datetime.datetime(2021, 8, 22,  0, 0, 0)
    cycling_interval = 1
if '20210821' in time:
    forecast_start_time = datetime.datetime(2021, 8, 21, 18, 0, 0)
    forecast_end_time   = datetime.datetime(2021, 8, 23,  0, 0, 0)
    cycling_interval = 1
if '20210828' in time:
    forecast_start_time = datetime.datetime(2021, 8, 28, 18, 0, 0)
    forecast_end_time   = datetime.datetime(2021, 8, 31,  0, 0, 0)
    cycling_interval = 6
if '20210904' in time:
    forecast_start_time = datetime.datetime(2021, 9,  4, 18, 0, 0)
    forecast_end_time   = datetime.datetime(2021, 9,  7,  0, 0, 0)
    cycling_interval = 6

cpt = loadCPT('./colormaps/PU_Rain_rate.rgb')
cpt_convert = LinearSegmentedColormap('cpt', cpt)
levs = np.array([-5, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70])

for dom in domains:
    for case in cases:

        dir_wrfout = dir_CPEX + '/bkg/' + time + '/' + case

        time_now = forecast_start_time
        while time_now <= forecast_end_time:

            time_now_str = time_now.strftime('%Y%m%d%H')
            pdfname = dir_main + '/' + time + '/mdbz/mdbz_' + case + '_' + dom + '_' + time_now_str + '.pdf'
            file_wrf = dir_wrfout + '/wrfout_' + dom + '_' + time_now.strftime('%Y-%m-%d_%H:00:00')
            print(pdfname)

            ncfile = Dataset(file_wrf)
            lat = ncfile.variables['XLAT'][0,:,:]
            lon = ncfile.variables['XLONG'][0,:,:]
            mdbz = getvar(ncfile, 'mdbz')
            slp = getvar(ncfile, 'slp', units='hPa')
            (u10, v10) = getvar(ncfile, 'uvmet10', units='kt')
            ncfile.close()

            max_lat = np.max(np.max(lat))
            min_lat = np.min(np.min(lat))
            max_lon = np.max(np.max(lon))
            min_lon = np.min(np.min(lon))
            extent = [min_lon, max_lon, min_lat, max_lat]

            with PdfPages(pdfname) as pdf:

                fig, axs = plt.subplots(1, 1, figsize=(6.0, 4.5))
                fig.subplots_adjust(left=0.075, bottom=0.025, right=1.075, top=0.990, wspace=0.100, hspace=0.100)

                ax = axs
                m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                m.drawcoastlines(linewidth=0.25, color='k')

                space = 20
                pcm1 = ax.contourf(lon, lat, mdbz, levels=levs, cmap=cpt_convert, extend='max', zorder=2)
                #pcm2 = ax.quiver(lon[::space, ::space], lat[::space, ::space], u10[::space, ::space], v10[::space, ::space], \
                                 #width=0.001, headwidth=5.0, headlength=7.5, scale=75.0, scale_units='inches', zorder=1)
                #pcm3 = ax.contour(lon, lat, slp, levels=np.arange(900, 1100.1, 5.0), colors='k', linewidths=1.0, zorder=0)

                #plt.clabel(pcm3, fontsize=7.5, inline=1, fmt='%1.0f')
                ax.set_xticks(np.arange(-90, -29, 5))
                ax.set_yticks(np.arange(-10,  46, 5))
                ax.set_xticklabels(['90W', '85W', '80W', '75W', '70W', '65W', '60W', '55W', '50W', '45W', '40W', '35W', '30W'])
                ax.set_yticklabels(['10S',  '5S',   '0',  '5N', '10N', '15N', '20N', '25N', '30N', '35N', '40N', '45N'])
                ax.tick_params('both', direction='out', labelsize=10.0)
                ax.grid(True, color='k', linestyle='--', linewidth=0.1)
                ax.axis(extent)

                clb = fig.colorbar(pcm1, ax=axs, ticks=levs, orientation='vertical', pad=0.020, aspect=25, shrink=0.90)
                clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=7.5)

                pdf.savefig(fig)
                plt.cla()
                plt.clf()

            time_now = time_now + datetime.timedelta(hours = cycling_interval)
