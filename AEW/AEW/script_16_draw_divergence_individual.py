import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.basemap import Basemap

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021'
dir_main = dir_CPEX + '/AEW'

time = '20210821'

if '20210820' in time:
    start_time = datetime.datetime(2021, 8, 20, 18, 0, 0)
    end_time   = datetime.datetime(2021, 8, 22,  6, 0, 0)
    idt_GFS    = 7
    idx_AEW    = 7
    file_track = dir_CPEX + '/AEW/20210820/GFS/20210820.csv'
    cases = ['CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_DAWN1hOE1p5', 'CON6h_HALO1h', 'CON6h_HALO1hOE0p2', \
             'CON6h_DS1h', 'CON6h_DS1h_UV', 'CON6h_DS1h_T', 'CON6h_DS1h_Q', 'CON6h_Aeolus6h', 'CON6h_DAWN1h_HALO1h_DS1h', 'CON6h_DAWN1h_HALO1h_DS1h_Aeolus6h', \
             'CTRL', 'MP01', 'MP02', 'MP08', 'MP10', 'MP16', 'MP26', 'BL02', 'BL04', 'BL06', 'BL07', \
             'CU02', 'CU11', 'CU14', 'CU16', 'RA03', 'RA04', 'RA05', 'RA14']
    labels = ['CON', 'DAWN', 'DAWNOE1', 'DAWNOE1p5', 'HALO', 'HALOOE0p2', \
              'DS', 'DS_UV', 'DS_T', 'DS_Q', 'Aeolus', 'HRFD', 'HRFD_Aeolus', \
              'CTRL', 'Kessler', 'Purdue Lin', 'Thompson', 'Morrison 2-Moment', 'WDM6', 'WDM7', 'MYJ', 'QNSE', 'MYNN', 'ACM2', \
              'BMJ', 'Multi-Scale KF', 'NewSAS', 'New Tiedtke', 'CAM', 'RRTMG', 'New Goddard', 'RRTMG-K']
if '20210821' in time:
    start_time = datetime.datetime(2021, 8, 21, 18, 0, 0)
    end_time   = datetime.datetime(2021, 8, 23,  6, 0, 0)
    idt_GFS    = 7
    idx_AEW    = 7
    file_track = dir_CPEX + '/AEW/20210821/GFS/20210821.csv'
    cases = ['CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_DAWN1hOE1p5', 'CON6h_HALO1h', \
             'CON6h_DS1h', 'CON6h_DS1h_UV', 'CON6h_DS1h_T', 'CON6h_DS1h_Q', 'CON6h_Aeolus6h', 'CON6h_DAWN1h_HALO1h_DS1h', 'CON6h_DAWN1h_HALO1h_DS1h_Aeolus6h']
    labels = ['CON', 'DAWN', 'DAWNOE1', 'DAWNOE1p5', 'HALO', \
              'DS', 'DS_UV', 'DS_T', 'DS_Q', 'Aeolus', 'HRFD', 'HRFD_Aeolus']

cycling_interval = 6
domains = ['d01']
levels = [925, 850, 700, 600, 500, 300, 200]
n_time = int((end_time - start_time).total_seconds()/3600/6+1)

df = pd.read_csv(file_track)
AEW_Date_Times = df['Date_Time']
AEW_lats = df['Latitude']
AEW_lons = df['Longitude']
print(AEW_Date_Times[idx_AEW])
del df

for dom in domains:
    for idt in range(n_time):

        time_now = start_time + datetime.timedelta(hours = idt*cycling_interval)
        print(time_now)
        if time_now < datetime.datetime(2021, 8, 22,  0, 0, 0):
            continue
        time_now_str = time_now.strftime('%Y%m%d%H')
        dir_file = dir_main + '/' + time

        (AEW_lon, AEW_lat) = (AEW_lons[idt+idx_AEW], AEW_lats[idt+idx_AEW])
        extent = [AEW_lon-5.0, AEW_lon+5.0, AEW_lat-5.0, AEW_lat+5.0]

        for idc, case in enumerate(cases):

            time_idx = idt
            label = labels[idc]
            if 'GFS' in case: time_idx = time_idx + idt_GFS

            filename = dir_file + '/' + case + '/div_' + dom + '.nc'
            ncfile   = Dataset(filename)
            lat      = ncfile.variables['lat'][:,:]
            lon      = ncfile.variables['lon'][:,:]
            level    = ncfile.variables['level'][:]
            div      = ncfile.variables['div'][time_idx,:,:,:]*100000.0
            ncfile.close()

            pdfname = '_'.join([time_now_str, 'div', case, dom+'.pdf'])
            pdfname = dir_file + '/figures/' + pdfname
            print(pdfname)

            with PdfPages(pdfname) as pdf:
                for idl, lev in enumerate(levels):

                    fig, axs   = plt.subplots(1, 1, figsize=(6.00, 6.25))
                    fig.subplots_adjust(left=0.075, bottom=-0.040, right=0.975, top=0.980, wspace=0.100, hspace=0.100)

                    ax = axs

                    m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                    m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                    m.drawparallels(np.arange(-10,  36, 5), labels=[1,0,0,0], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)
                    m.drawmeridians(np.arange(-95, -29, 5), labels=[0,0,0,1], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)

                    pcm = ax.contourf(lon, lat, div[idl,:,:], levels=np.arange(-9.0, 10.0, 2.0), cmap='RdBu_r', extend='both', zorder=1)
                    ax.plot(AEW_lon, AEW_lat, 'x', color='k', markersize=7.5, markeredgewidth=1.0)

                    clb = fig.colorbar(pcm, ax=axs, orientation='horizontal', pad=0.035, aspect=50, shrink=1.00)
                    clb.set_label('Relative Vorticity ($\mathregular{10^{-5} s^{-1}}$) of ' + label + ' at ' + str(lev) + ' hPa', fontsize=10.0, labelpad=4.0)
                    clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
                    clb.set_ticks(np.arange(-9.0, 10.0, 2.0))

                    pdf.savefig(fig)
                    plt.cla()
                    plt.clf()
                    plt.close()
