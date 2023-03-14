import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from cpt_convert import loadCPT
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import LinearSegmentedColormap

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021'
dir_abi = '/'.join([dir_GOES, 'Data', 'GOES-R', 'ABI-L2-CMIPF'])
dir_DC8 = '/'.join([dir_CPEX, 'flight_track', 'DC8'])
dir_wrfout = '/'.join([dir_CPEX, 'flight_track', 'wrfout'])
dir_best_track = '/'.join([dir_CPEX, 'track_intensity', 'best_track'])

#cases = ['20210820']
#cases = ['20210821']
cases = ['20210824']
#cases = ['20210828']
#cases = ['20210904']
time_interval = 6
window_time = 6

cpt, cpt_r = loadCPT('./GOES-R_BT.rgb')
cpt_convert = LinearSegmentedColormap('cpt', cpt)

#pdfname = './figure_01_flight_track_AEW_GOES-R_environment_20210820.pdf'
#pdfname = './figure_01_flight_track_AEW_GOES-R_environment_20210821.pdf'
pdfname = './figure_01_flight_track_AEW_GOES-R_environment_20210824.pdf'
#pdfname = './figure_01_flight_track_AEW_GOES-R_environment_20210828.pdf'
#pdfname = './figure_01_flight_track_AEW_GOES-R_environment_20210904.pdf'
print(pdfname)

with PdfPages(pdfname) as pdf:

    fig, axs = plt.subplots(1, 1, figsize=(6.0, 5.0))
    fig.subplots_adjust(left=0.075, bottom=-0.025, right=0.975, top=0.975, wspace=0.000, hspace=0.000)

    for case in cases:

        file_flight_track = 'flight_track_' + case + '.csv'

        if '20210820' in case:
            file_wrfout_d01 = dir_wrfout + '/wrfout_d01_2021-08-19_18:00:00'
            file_wrfout_d02 = dir_wrfout + '/wrfout_d02_2021-08-19_18:00:00'
            anl_start_time  = datetime.datetime(2021, 8, 21,  0, 0, 0)
            anl_end_time    = datetime.datetime(2021, 8, 21,  0, 0, 0)
            if_AEW          = True
            AEW_dates       = [19, 20, 21, 22]
            GFS_time        = int(8)
        if '20210821' in case:
            file_wrfout_d01 = dir_wrfout + '/wrfout_d01_2021-08-20_18:00:00'
            file_wrfout_d02 = dir_wrfout + '/wrfout_d02_2021-08-20_18:00:00'
            anl_start_time  = datetime.datetime(2021, 8, 22,  0, 0, 0)
            anl_end_time    = datetime.datetime(2021, 8, 22,  0, 0, 0)
            if_AEW          = True
            AEW_dates       = [20, 21, 22, 23]
            GFS_time        = int(8)
        if '20210824' in case:
            file_wrfout_d01 = dir_wrfout + '/wrfout_d01_2021-08-24_06:00:00'
            file_wrfout_d02 = dir_wrfout + '/wrfout_d02_2021-08-24_06:00:00'
            anl_start_time  = datetime.datetime(2021, 8, 25,  0, 0, 0)
            anl_end_time    = datetime.datetime(2021, 8, 25,  0, 0, 0)
            if_AEW          = False
            best_track_name = '2021_09L_Ida.csv'
            (sidx, eidx)    = (0, 14)
            zidx            = 3
            GFS_time        = int(3)
        if '20210828' in case:
            file_wrfout_d01 = dir_wrfout + '/wrfout_d01_2021-08-28_12:00:00'
            file_wrfout_d02 = dir_wrfout + '/wrfout_d02_2021-08-28_12:00:00'
            anl_start_time  = datetime.datetime(2021, 8, 29,  0, 0, 0)
            anl_end_time    = datetime.datetime(2021, 8, 29,  0, 0, 0)
            if_AEW          = False
            best_track_name = '2021_10L_Kate.csv'
            (sidx, eidx)    = (1, 14)
            zidx            = 2
            GFS_time        = int(2)
        if '20210904' in case:
            file_wrfout_d01 = dir_wrfout + '/wrfout_d01_2021-09-03_18:00:00'
            file_wrfout_d02 = dir_wrfout + '/wrfout_d02_2021-09-03_18:00:00'
            anl_start_time  = datetime.datetime(2021, 9,  5,  0, 0, 0)
            anl_end_time    = datetime.datetime(2021, 9,  5,  0, 0, 0)
            if_AEW          = False
            best_track_name = '2021_12L_Larry.csv'
            (sidx, eidx)    = (12, 30)
            zidx            = 1
            GFS_time        = int(5)

        wrfout_d01 = Dataset(file_wrfout_d01)
        lat_d01 = wrfout_d01.variables['XLAT'][0,:,:]
        lon_d01 = wrfout_d01.variables['XLONG'][0,:,:]
        extent = [lon_d01[0,0], lon_d01[-1,-1], lat_d01[0,0], lat_d01[-1,-1]]
        wrfout_d01.close()
        print(extent)

        lat_d02 = []
        lon_d02 = []
        wrfout_d02 = Dataset(file_wrfout_d02)
        lat_temp = wrfout_d02.variables['XLAT'][0,:,:]
        lon_temp = wrfout_d02.variables['XLONG'][0,:,:]
        n_we_d02 = len(lat_temp[0, :])
        n_sn_d02 = len(lat_temp[:, 0])
        lat_d02  = lat_d02 + list(lat_temp[0, 0:n_we_d02-1:1])
        lat_d02  = lat_d02 + list(lat_temp[0:n_sn_d02-1, n_we_d02-1])
        lat_d02  = lat_d02 + list(lat_temp[n_sn_d02-1, n_we_d02-1:0:-1])
        lat_d02  = lat_d02 + list(lat_temp[n_sn_d02-1:0:-1, 0])
        lon_d02  = lon_d02 + list(lon_temp[0, 0:n_we_d02-1:1])
        lon_d02  = lon_d02 + list(lon_temp[0:n_sn_d02-1, n_we_d02-1])
        lon_d02  = lon_d02 + list(lon_temp[n_sn_d02-1, n_we_d02-1:0:-1])
        lon_d02  = lon_d02 + list(lon_temp[n_sn_d02-1:0:-1, 0])
        lat_d02.append(lat_temp[0, 0])
        lon_d02.append(lon_temp[0, 0])
        wrfout_d02.close()

        #Read GFS hgt and rh
        dir_file = '/'.join([dir_CPEX, 'AEW', case, 'GFS'])
        filename = dir_file + '/rh_d01.nc'
        ncfile   = Dataset(filename)
        GFS_lat  = ncfile.variables['lat'][:,:]
        GFS_lon  = ncfile.variables['lon'][:,:]
        GFS_rh   = ncfile.variables['rh'][GFS_time,1,:,:]
        ncfile.close()

        filename = dir_file + '/geopt_d01.nc'
        ncfile   = Dataset(filename)
        GFS_hgt  = ncfile.variables['geopt'][GFS_time,2,:,:]
        ncfile.close()

        #Read flight track
        filename = '/'.join([dir_DC8, file_flight_track])
        df = pd.read_csv(filename)
        flight_time = df['Time']
        flight_lat = df['Latitude']
        flight_lon = df['Longitude']
        index_flight_time = flight_time%10000 == 0
        index_flight_time_00 = flight_time%1000000 == 0
        #print(index_flight_time_00)
        del df

        print('Time')
        print(np.min(flight_time))
        print(np.max(flight_time))
        print('Latitude')
        print(np.min(flight_lat))
        print(np.max(flight_lat))
        print('Longitude')
        print(np.min(flight_lon))
        print(np.max(flight_lon))

        #Read AEW track
        if if_AEW:
            filename = '/'.join([dir_CPEX, 'AEW', case, 'GFS', case+'.csv'])
            df = pd.read_csv(filename)
            AEW_lat = df['Latitude']
            AEW_lon = df['Longitude']
            del df
        else:
            file_best_track = dir_best_track + '/' + best_track_name
            df = pd.read_csv(file_best_track)
            TC_lat = list(df['Latitude'][sidx:eidx])
            TC_lon = list(df['Longitude'][sidx:eidx])
            TC_MWS = df['MWS (Knot)'][sidx:eidx]
            TC_dd = df['Date_Time'][sidx:eidx]
            TC_dd = [x[8:10] for x in TC_dd]
            del df

        time_now = anl_start_time
        while time_now <= anl_end_time:

            print(time_now)
            time_now_s = time_now - datetime.timedelta(hours = window_time/2.0)
            time_now_e = time_now + datetime.timedelta(hours = window_time/2.0)
            YYMMDD = time_now.strftime('%Y%m%d')
            HH = time_now.strftime('%H')
            time_now_str = YYMMDD + HH

            abi = '/'.join([dir_abi, YYMMDD, HH, 'OR_ABI-L2-CMIPF-M6C08_G16_s*' + HH + '00' + '*'])
            fileabi = os.popen('ls ' + abi).read().split()
            print(fileabi)

            ncfile = Dataset(fileabi[0])
            CMI = ncfile.variables['CMI'][:,:]
            x = ncfile.variables['x'][:]
            y = ncfile.variables['y'][:]

            gip      = ncfile.variables['goes_imager_projection']
            r_eq     = gip.semi_major_axis
            r_pol    = gip.semi_minor_axis
            H        = gip.perspective_point_height + gip.semi_major_axis
            phi_0    = gip.latitude_of_projection_origin
            lambda_0 = gip.longitude_of_projection_origin

            x, y    = np.meshgrid(x, y, indexing='xy')
            sin_x   = np.sin(x)
            cos_x   = np.cos(x)
            sin_y   = np.sin(y)
            cos_y   = np.cos(y)
            a       = np.power(sin_x, 2) + np.power(cos_x, 2)*(np.power(cos_y, 2)+np.power(r_eq*sin_y/r_pol, 2))
            b       = -2.0*H*cos_x*cos_y
            c       = np.power(H, 2) - np.power(r_eq, 2)
            r_s     = (-1.0*b - np.sqrt(np.power(b, 2)-4*a*c))/(2*a)
            s_x     = r_s*cos_x*cos_y
            s_y     = -1.0*r_s*sin_x
            s_z     = r_s*cos_x*sin_y
            abi_lat = np.degrees(np.arctan(np.power(r_eq/r_pol, 2)*s_z/np.sqrt(np.power(H-s_x, 2)+np.power(s_y, 2))))
            abi_lon = lambda_0 - np.degrees(np.arctan(s_y/(H-s_x)))

            ax = axs
            m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=axs)
            m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
            m.drawparallels(np.arange(-10,  36, 5), labels=[1,0,0,0], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='w', zorder=8)
            m.drawmeridians(np.arange(-95, -29, 5), labels=[0,0,0,1], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='w', zorder=8)

            x_abi_lon, y_abi_lat = m(abi_lon, abi_lat, inverse=False)
            pcm = ax.contourf(x_abi_lon, y_abi_lat, CMI, levels=np.arange(190.0, 250.1, 0.5), cmap=cpt_convert, extend='both', zorder=1)

            #x_lon_d02, y_lat_d02 = m(lon_d02, lat_d02, inverse=False)
            #ax.plot(x_lon_d02, y_lat_d02, '-', color='k', linewidth=0.75, zorder=3)

            x_GFS_lon, y_GFS_lat = m(GFS_lon, GFS_lat, inverse=False)
            CS1 = ax.contour(x_GFS_lon, y_GFS_lat, GFS_rh, levels=np.arange(5.0, 36.0, 10.0), colors='goldenrod', linewidths=1.00, zorder=4)
            CS2 = ax.contour(x_GFS_lon, y_GFS_lat, GFS_hgt, levels=np.arange(3000.0, 3301.0, 20.0), colors='w', linewidths=1.00, zorder=5)
            ax.clabel(CS1, CS1.levels, inline=True, fmt='%1.0f%%', fontsize=5.0)
            ax.clabel(CS2, CS2.levels, inline=True, fmt='%1.0f', fontsize=5.0)

            x_flight_lon, y_flight_lat = m(flight_lon, flight_lat, inverse=False)
            ax.plot(x_flight_lon, y_flight_lat, '-', color='k', linewidth=2.50, zorder=6)
            ax.plot(x_flight_lon, y_flight_lat, '-', color='magenta', linewidth=1.25, zorder=6)
            ax.plot(x_flight_lon[index_flight_time], y_flight_lat[index_flight_time], 'o', color='w', ms=3.75, zorder=6)
            ax.plot(x_flight_lon[index_flight_time], y_flight_lat[index_flight_time], 'o', color='k', ms=2.50, zorder=6)
            ax.plot(x_flight_lon[index_flight_time_00], y_flight_lat[index_flight_time_00], 'o', color='yellowgreen', ms=2.50, zorder=6)

            if if_AEW:
                x_AEW_lon, y_AEW_lat = m(AEW_lon, AEW_lat, inverse=False)
                ax.plot(x_AEW_lon, y_AEW_lat, '-', color='k', linewidth=2.50, zorder=7)
                ax.plot(x_AEW_lon, y_AEW_lat, '-', color='r', linewidth=1.25, zorder=7)
                ax.plot(x_AEW_lon, y_AEW_lat, 'o', color='w', ms=1.25, zorder=7)
                ax.plot(x_AEW_lon[::4], y_AEW_lat[::4], 'o', color='k', ms=3.75, zorder=7)
                ax.plot(x_AEW_lon[::4], y_AEW_lat[::4], 'o', color='w', ms=2.50, zorder=7)
                for (AEWdate, AEWlon, AEWlat) in zip(AEW_dates, x_AEW_lon[::4], y_AEW_lat[::4]):
                    ax.text(AEWlon, AEWlat-0.75, AEWdate, ha='center', va='center', color='k', fontsize=5.0, zorder=7)
            else:
                x_TC_lon, y_TC_lat = m(TC_lon, TC_lat, inverse=False)
                sc2 = ax.scatter(x_TC_lon, y_TC_lat, c=TC_MWS, marker='o', edgecolor='none', vmin=20, vmax=125, s=30, cmap='jet', zorder=7)
                ax.plot(x_TC_lon[zidx::4], y_TC_lat[zidx::4], 'o', color='w', ms=2.50, zorder=7)
                for (TCdate, TClon, TClat) in zip(TC_dd[zidx::4], x_TC_lon[zidx::4], y_TC_lat[zidx::4]):
                    ax.text(TClon, TClat-0.75, TCdate, ha='center', va='center', color='k', fontsize=5.0, zorder=7)

            if if_AEW:
                clb1 = fig.colorbar(pcm, ax=axs, ticks=np.arange(190, 250.1, 5.0), orientation='horizontal', pad=0.050, aspect=50, shrink=1.00)
                clb1.set_label('GOES-R Channel 8 BTs (K) at ' + time_now.strftime('%H UTC %d Aug %Y'), fontsize=10.0, labelpad=4.0)
                clb1.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
            else:
                clb1 = fig.colorbar(pcm, ax=axs, ticks=np.arange(190, 250.1, 5.0), orientation='horizontal', pad=-0.025, aspect=50, shrink=1.00)
                clb1.set_label('GOES-R Channel 8 BTs (K) at ' + time_now.strftime('%H UTC %d Aug %Y'), fontsize=10.0, labelpad=4.0)
                clb1.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

            if not if_AEW:
                grade = [20, 33, 63, 82, 95, 112, 125]
                cat = ['TD', 'TS', 'Cat1', 'Cat2', 'Cat3', 'Cat4']
                clb2 = plt.colorbar(sc2, ticks=grade, orientation='horizontal', pad=0.050, aspect=50, shrink=1.00)
                clb2.set_ticklabels(grade)
                clb2.set_label('MWS (Knot)', fontsize=10.0)
                clb2.ax.tick_params(axis='both', direction='in', labelsize=10.0)
                for idx, lab in enumerate(cat):
                    clb2.ax.text(0.5*(grade[idx+1]+grade[idx]), -95.0, lab, ha='center', va='center', color='k', fontsize=10.0)

            pdf.savefig(fig)
            plt.cla()
            plt.clf()
            plt.close()

            time_now = time_now + datetime.timedelta(hours = time_interval)
