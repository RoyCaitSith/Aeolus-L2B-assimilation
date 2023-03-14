import os
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from wrf import getvar
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_pdf import PdfPages

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS'
dir_best_track = '/'.join([dir_CPEX, 'track_intensity', 'best_track'])
dir_main = dir_CPEX + '/rainfall'

domains = ['d01']
cycling_interval = 6

#cases = ['IMERG', 'CON6h_082406_Hybrid_C08']
#labels = ['IMERG', 'CON_082406_Hybrid_C08']
#cases = ['IMERG', 'CON6h_082412_Hybrid_C08']
#labels = ['IMERG', 'CON_082412_Hybrid_C08']
#cases = ['IMERG', 'CON6h_082418_Hybrid_C08']
#labels = ['IMERG', 'CON_082418_Hybrid_C08']
#cases = ['IMERG', 'CON6h_082500_Hybrid_C08']
#labels = ['IMERG', 'CON_082500_Hybrid_C08']
#cases = ['IMERG', 'CON6h_Aeolus6h_082406_Hybrid_C08']
#labels = ['IMERG', 'CON_Aeolus_082406_Hybrid_C08']
#cases = ['IMERG', 'CON6h_Aeolus6h_082412_Hybrid_C08']
#labels = ['IMERG', 'CON_Aeolus_082412_Hybrid_C08']
#cases = ['IMERG', 'CON6h_Aeolus6h_082418_Hybrid_C08']
#labels = ['IMERG', 'CON_Aeolus_082418_Hybrid_C08']
#cases = ['IMERG', 'CON6h_Aeolus6h_082500_Hybrid_C08']
#labels = ['IMERG', 'CON_Aeolus_082500_Hybrid_C08']
#cases = ['IMERG', 'CON6h_Aeolus6h_082500_H1_Hybrid_C07']
#labels = ['IMERG', 'CON_Aeolus_082500_H1_Hybrid_C07']
cases = ['IMERG', 'CON6h_Aeolus6h_082500_H2_Hybrid_C07']
labels = ['IMERG', 'CON_Aeolus_082500_H2_Hybrid_C07']
#cases = ['IMERG', 'CON6h_Aeolus6h_082500_V1_Hybrid_C07']
#labels = ['IMERG', 'CON_Aeolus_082500_V1_Hybrid_C07']
#cases = ['IMERG', 'CON6h_Aeolus6h_082500_V2_Hybrid_C07']
#labels = ['IMERG', 'CON_Aeolus_082500_V2_Hybrid_C07']

forecast_start_time = datetime.datetime(2021, 8, 26, 18, 0, 0)
forecast_end_time   = datetime.datetime(2021, 8, 28, 18, 0, 0)
file_best_track = dir_best_track + '/2021_09L_Ida.csv'

rain_levels = [0.6, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0]
rain_labels = ['0.6', '1', '1.5', '2', '3', '4', '5', '6', '8', '10', '15', '20', '25', '30', '35', '40']
n_time = int((forecast_end_time - forecast_start_time).total_seconds()/3600/6+1)
print(len(cases))
print(len(labels))

for dom in domains:
    for idc, case in enumerate(cases):

        var = 'rainfall'
        filename = dir_main + '/' + case + '/rainfall_6h_' + dom + '.nc'
        if 'IMERG' in case:
            filename = dir_main + '/' + cases[-1] + '/IMERG_6h_' + dom + '.nc'
        ncfile   = Dataset(filename)
        rain     = ncfile.variables[var][:,:,:]*6.0
        rain_lat = ncfile.variables['lat'][:,:]
        rain_lon = ncfile.variables['lon'][:,:]
        ncfile.close()

        if 'IMERG' in case:
            file_track = file_best_track
        else:
            best_track_name = '_'.join([case, 'd01.csv'])
            file_track = dir_best_track + '/' + best_track_name
        df = pd.read_csv(file_track)
        TC_lats = list(df['Latitude'][:])
        TC_lons = list(df['Longitude'][:])
        TC_dates = list(df['Date_Time'][:])
        del df

        for idt in range(n_time):

            label = labels[idc]
            time_now = forecast_start_time + datetime.timedelta(hours = idt*cycling_interval)
            time_now_str = time_now.strftime('%Y%m%d%H')
            pdfname = '_'.join([time_now_str, 'rainfall', case, dom+'.pdf'])
            pdfname = dir_main + '/' + cases[-1] + '/' + pdfname
            print(pdfname)

            with PdfPages(pdfname) as pdf:

                fig, axs = plt.subplots(1, 1, figsize=(6.0, 6.25))
                fig.subplots_adjust(left=0.075, bottom=-0.040, right=0.975, top=0.980, wspace=0.100, hspace=0.100)

                time_now_end = time_now + datetime.timedelta(hours = 3.0)
                for id_TC, TC_date in enumerate(TC_dates):
                    TC_datetime = datetime.datetime.strptime(TC_date, '%Y-%m-%d %H:%M:%S')
                    if TC_datetime == time_now_end:
                        TC_lat = 0.5*(TC_lats[id_TC] + TC_lats[id_TC-1])
                        TC_lon = 0.5*(TC_lons[id_TC] + TC_lons[id_TC-1])
                        extent = [TC_lon-5.0, TC_lon+5.0, TC_lat-5.0, TC_lat+5.0]

                ax = axs
                m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                m.drawparallels(np.arange(-10,  36, 5), labels=[1,0,0,0], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)
                m.drawmeridians(np.arange(-95, -29, 5), labels=[0,0,0,1], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)

                rain[rain<=0] = 0
                #rain_lon, rain_lat = m(rain_lon, rain_lat, inverse=False)
                pcm = ax.contourf(rain_lon, rain_lat, rain[idt,:,:], locator=ticker.LogLocator(), levels=rain_levels, cmap='jet', extend='max', zorder=1)
                ax.plot(TC_lon, TC_lat, 'x', color='k', markersize=10.0, markeredgewidth=1.0)

                clb = fig.colorbar(pcm, ax=axs, orientation='horizontal', pad=0.035, aspect=50, shrink=1.00)
                clb.set_label('6-hr Accumulated Precipitation (mm) of ' + label, fontsize=10.0, labelpad=4.0)
                clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
                clb.ax.minorticks_off()
                clb.set_ticks(rain_levels)
                clb.set_ticklabels(rain_labels)

                pdf.savefig(fig)
                plt.cla()
                plt.clf()
                plt.close()
