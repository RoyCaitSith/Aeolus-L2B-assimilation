import os
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from wrf import getvar
from netCDF4 import Dataset
from cpt_convert import loadCPT
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_pdf import PdfPages

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS'
dir_best_track = '/'.join([dir_CPEX, 'track_intensity', 'best_track'])
dir_main = dir_CPEX + '/forecasts'

domains = ['d01']

#cases = ['CON6h_082406_Hybrid_C08']
#labels = ['CON6h_082406_Hybrid_C08']
#cases = ['CON6h_082412_Hybrid_C08']
#labels = ['CON6h_082412_Hybrid_C08']
#cases = ['CON6h_082418_Hybrid_C08']
#labels = ['CON6h_082418_Hybrid_C08']
#cases = ['CON6h_082500_Hybrid_C08']
#labels = ['CON6h_082500_Hybrid_C08']
#cases = ['CON6h_Aeolus6h_082406_Hybrid_C08']
#labels = ['CON6h_Aeolus6h_082406_Hybrid_C08']
#cases = ['CON6h_Aeolus6h_082412_Hybrid_C08']
#labels = ['CON6h_Aeolus6h_082412_Hybrid_C08']
#cases = ['CON6h_Aeolus6h_082418_Hybrid_C08']
#labels = ['CON6h_Aeolus6h_082418_Hybrid_C08']
cases = ['CON6h_Aeolus6h_082500_Hybrid_C08']
labels = ['CON6h_Aeolus6h_082500_Hybrid_C08']

forecast_start_time = datetime.datetime(2021, 8, 27,  0, 0, 0)
forecast_end_time   = datetime.datetime(2021, 8, 29,  6, 0, 0)

cpt = loadCPT('./colormaps/PU_Wind_speed.rgb')
cpt_convert = LinearSegmentedColormap('cpt', cpt)
levs = np.arange(0, 30.1, 1.0)

for dom in domains:
    for idc, case in enumerate(cases):

        label = labels[idc]
        best_track_name = '_'.join([case, 'd01.csv'])
        file_best_track = dir_best_track + '/' + best_track_name
        df = pd.read_csv(file_best_track)
        TC_lats = list(df['Latitude'][:])
        TC_lons = list(df['Longitude'][:])
        TC_dates = list(df['Date_Time'][:])
        del df

        dir_pdf = dir_main + '/slp_10mwind/' + case
        os.system('mkdir ' + dir_pdf)

        time_now = forecast_start_time
        while time_now <= forecast_end_time:

            time_now_str = time_now.strftime('%Y%m%d%H')
            pdfname = '_'.join([time_now_str, 'slp_10mwind', case, dom+'.pdf'])
            pdfname = dir_pdf + '/' + pdfname
            print(pdfname)

            with PdfPages(pdfname) as pdf:

                fig, axs = plt.subplots(1, 1, figsize=(6.0, 6.25))
                fig.subplots_adjust(left=0.075, bottom=-0.040, right=0.975, top=0.980, wspace=0.100, hspace=0.100)

                dir_wrfout = '/'.join([dir_CPEX, 'cycling_da', 'Data', case, 'bkg'])
                file_wrf = dir_wrfout + '/wrfout_' + dom + '_' + time_now.strftime('%Y-%m-%d_%H:00:00')
                print(file_wrf)

                ncfile = Dataset(file_wrf)
                lat = ncfile.variables['XLAT'][0,:,:]
                lon = ncfile.variables['XLONG'][0,:,:]
                slp = getvar(ncfile, 'slp', units='hPa')
                (u10, v10) = getvar(ncfile, 'uvmet10', units='kt')
                (spd, dirc) = getvar(ncfile, 'uvmet10_wspd_wdir', units='kt')
                ncfile.close()

                for id_TC, TC_date in enumerate(TC_dates):
                    TC_datetime = datetime.datetime.strptime(TC_date, '%Y-%m-%d %H:%M:%S')
                    if TC_datetime == time_now:
                        TC_lat = TC_lats[id_TC]
                        TC_lon = TC_lons[id_TC]
                        extent = [TC_lon-5.0, TC_lon+5.0, TC_lat-5.0, TC_lat+5.0]

                ax = axs
                m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                m.drawparallels(np.arange(-10,  36, 5), labels=[1,0,0,0], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)
                m.drawmeridians(np.arange(-95, -29, 5), labels=[0,0,0,1], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)

                space = 2
                pcm1 = ax.contourf(lon, lat, spd, levels=levs, cmap=cpt_convert, extend='max', zorder=1)
                pcm2 = ax.contour(lon, lat, slp, levels=np.arange(900, 1100.1, 1.0), colors='w', linewidths=1.0, zorder=2)
                pcm3 = ax.quiver(lon[::space, ::space], lat[::space, ::space], u10[::space, ::space], v10[::space, ::space], \
                                 width=0.001, headwidth=5.0, headlength=7.5, scale=75.0, scale_units='inches', zorder=3)
                ax.plot(TC_lon, TC_lat, 'x', color='k', markersize=10.0, markeredgewidth=1.0, zorder=4)

                clb = fig.colorbar(pcm1, ax=axs, ticks=range(0, 31, 5), orientation='horizontal', pad=0.035, aspect=50, shrink=1.00)
                clb.set_label('10m Wind Speed of ' + label, fontsize=10.0, labelpad=4.0)
                clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
                plt.clabel(pcm2, fontsize=7.5, inline=1, fmt='%1.0f')

                pdf.savefig(fig)
                plt.cla()
                plt.clf()
                plt.close()

                time_now = time_now + datetime.timedelta(hours = 6.0)
