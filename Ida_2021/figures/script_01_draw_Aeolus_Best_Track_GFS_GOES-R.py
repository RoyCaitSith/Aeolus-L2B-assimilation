import os
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from cpt_convert import loadCPT
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.gridspec import GridSpec

dir_CPEXs = []
dir_GOESs = []
dir_CPEXs.append('/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS')
dir_CPEXs.append('/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021')
dir_GOESs.append('/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction')
dir_GOESs.append('/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction')

cases= ['CON6h_082500_Hybrid_C08', '20210820']
mtitles = ['(a)', '(b)']

anl_start_times = [datetime.datetime(2021, 8, 24, 12, 0, 0), datetime.datetime(2021, 8, 20,  0, 0, 0)]
anl_end_times = [datetime.datetime(2021, 8, 27,  0, 0, 0), datetime.datetime(2021, 8, 21,  0, 0, 0)]

file_wrfout_d01s = ['wrfout_d01_2021-08-25_00:00:00', 'wrfout_d01_2021-08-19_18:00:00']
file_wrfout_d02s = ['wrfout_d02_2021-08-25_00:00:00', 'wrfout_d02_2021-08-19_18:00:00']
time_GOES_nows = [datetime.datetime(2021, 8, 25, 12, 0, 0), datetime.datetime(2021, 8, 21,  0, 0, 0)]
AEW_dates = [[], [19, 20, 21, 22]]

#Here
GFS_times = [2, 8]
sidxs = [0, -1]
eidxs = [21, -1]
zidxs = [3, -1]
file_best_tracks = ['2021_09L_Ida.csv', '']
file_dropsondes = ['', '20210820.csv']

time_interval = 6
window_time = 6

cpt, cpt_r = loadCPT('./GOES-R_BT.rgb')
cpt_convert = LinearSegmentedColormap('cpt', cpt)

dir_fes = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS/figures_V3/ScientificColourMaps7/fes'
fes_cm_data = np.loadtxt(dir_fes + '/fes.txt')
fes_map_r = LinearSegmentedColormap.from_list('fes', fes_cm_data[::-1])

dir_lajolla = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS/figures_V3/ScientificColourMaps7/lajolla'
lajolla_cm_data = np.loadtxt(dir_lajolla + '/lajolla.txt')
lajolla_map = LinearSegmentedColormap.from_list('lajolla', lajolla_cm_data[::1])

dir_buda = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS/figures_V3/ScientificColourMaps7/buda'
buda_cm_data = np.loadtxt(dir_buda + '/buda.txt')
buda_map = LinearSegmentedColormap.from_list('buda', buda_cm_data[::1])

dir_hawaii = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS/figures_V3/ScientificColourMaps7/hawaii'
hawaii_cm_data = np.loadtxt(dir_hawaii + '/hawaii.txt')
hawaii_map = LinearSegmentedColormap.from_list('hawaii', hawaii_cm_data[::1])

dir_grayC = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS/figures_V3/ScientificColourMaps7/grayC'
grayC_cm_data = np.loadtxt(dir_grayC + '/grayC.txt')
grayC_map = LinearSegmentedColormap.from_list('grayC', grayC_cm_data[::1])

colors = [hawaii_cm_data[255], hawaii_cm_data[204], hawaii_cm_data[153], hawaii_cm_data[102], hawaii_cm_data[51], hawaii_cm_data[0]]
idcolor = [0, 0]

pdfname = './fig01.pdf'
print(pdfname)

with PdfPages(pdfname) as pdf:

    fig_width  = 6.00
    fig_height = 9.00
    fig, axs   = plt.subplots(2, 1, figsize=(fig_width, fig_height))
    fig.subplots_adjust(left=0.050, bottom=-0.090, right=1.000, top=0.975, wspace=0.075, hspace=0.100)

    for idc, case in enumerate(cases):

        dir_CPEX = dir_CPEXs[idc]
        dir_GOES = dir_GOESs[idc]
        dir_main = '/'.join([dir_CPEX, 'figures'])
        dir_aeolus = '/'.join([dir_CPEX, 'Aeolus', 'create_bufr', 'bufr_temp'])
        dir_abi = '/'.join([dir_GOES, 'Data', 'GOES-R', 'ABI-L2-CMIPF'])
        dir_best_track = '/'.join([dir_CPEX, 'track_intensity', 'best_track'])
        dir_DC8 = '/'.join([dir_CPEX, 'flight_track', 'DC8'])
        dir_soundings = '/'.join([dir_CPEX, 'Soundings'])
        dir_dropsondes = '/'.join([dir_CPEX, 'Dropsondes', 'data'])

        if '20210820' in case or '20210821' in case:
            dir_wrfout = '/'.join([dir_CPEX, 'bkg', case, 'CON6h'])
        else:
            dir_wrfout = '/'.join([dir_CPEX, 'cycling_da', 'Data', case, 'bkg'])
        file_wrfout_d01 = dir_wrfout + '/' + file_wrfout_d01s[idc]
        file_wrfout_d02 = dir_wrfout + '/' + file_wrfout_d02s[idc]
        anl_start_time = anl_start_times[idc]
        anl_end_time = anl_end_times[idc]

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

        GFS_time = GFS_times[idc]
        if '20210820' in case or '20210821' in case:
            dir_file = '/'.join([dir_CPEX, 'AEW', case, 'GFS'])
        else:
            dir_file = '/'.join([dir_CPEX, 'forecasts', 'gfs', case])
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

        if '20210820' in case or '20210821' in case:
            file_flight_track = 'flight_track_' + case + '.csv'
            filename = '/'.join([dir_DC8, file_flight_track])
            df = pd.read_csv(filename)
            flight_time = df['Time']
            flight_lat = df['Latitude']
            flight_lon = df['Longitude']
            index_flight_time = flight_time%10000 == 0
            index_flight_time_00 = flight_time%1000000 == 0
            del df

            filename = '/'.join([dir_CPEX, 'AEW', case, 'GFS', case+'.csv'])
            df = pd.read_csv(filename)
            AEW_lat = df['Latitude']
            AEW_lon = df['Longitude']
            del df
        else:
            (sidx, eidx, zidx) = (sidxs[idc], eidxs[idc], zidxs[idc])
            file_best_track = dir_best_track + '/' + file_best_tracks[idc]
            df = pd.read_csv(file_best_track)
            TC_lat = list(df['Latitude'][sidx:eidx])
            TC_lon = list(df['Longitude'][sidx:eidx])
            TC_MWS = df['MWS (Knot)'][sidx:eidx]
            TC_dd = df['Date_Time'][sidx:eidx]
            TC_dd = [x[8:10] for x in TC_dd]
            del df

        time_GOES_now = time_GOES_nows[idc]
        YYMMDD = time_GOES_now.strftime('%Y%m%d')
        HH = time_GOES_now.strftime('%H')
        time_GOES_now_str = YYMMDD + HH

        abi = dir_abi + '/' + YYMMDD + '/' + HH + '/OR_ABI-L2-CMIPF-M6C08_G16_s*' + HH + '00' + '*'
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
        ncfile.close()

        ax = axs[idc]
        m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
        m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
        m.drawparallels(np.arange(-10,   51, 10), labels=[1,0,0,0], fontsize=10.0, linewidth=0.25, dashes=[1,1], color='w', zorder=8)
        m.drawmeridians(np.arange(-120, -19, 10), labels=[0,0,0,1], fontsize=10.0, linewidth=0.25, dashes=[1,1], color='w', zorder=8)

        x_abi_lon, y_abi_lat = m(abi_lon, abi_lat, inverse=False)
        pcm = ax.contourf(x_abi_lon, y_abi_lat, CMI, levels=np.arange(190.0, 250.1, 0.5), cmap=fes_map_r, extend='both', zorder=1)
        #pcm = ax.contourf(x_abi_lon, y_abi_lat, CMI, levels=np.arange(190.0, 250.1, 10.0), cmap=fes_map_r, extend='both', zorder=1)

        x_GFS_lon, y_GFS_lat = m(GFS_lon, GFS_lat, inverse=False)
        CS1 = ax.contour(x_GFS_lon, y_GFS_lat, GFS_rh, levels=np.arange(5.0, 36.0, 10.0), colors=buda_cm_data[255], linewidths=1.00, zorder=4)
        CS2 = ax.contour(x_GFS_lon, y_GFS_lat, GFS_hgt, levels=np.arange(3000.0, 3301.0, 20.0), colors='w', linewidths=1.00, zorder=5)
        ax.clabel(CS1, CS1.levels, inline=True, fmt='%1.0f%%', fontsize=10.0)
        ax.clabel(CS2, CS2.levels, inline=True, fmt='%1.0f', fontsize=10.0)

        if '20210820' in case or '20210821' in case:
            x_flight_lon, y_flight_lat = m(flight_lon, flight_lat, inverse=False)
            #ax.plot(x_flight_lon, y_flight_lat, '-', color='k', linewidth=2.50, zorder=6)
            #ax.plot(x_flight_lon, y_flight_lat, '-', color=buda_cm_data[142], linewidth=1.25, zorder=6)
            #ax.plot(x_flight_lon[index_flight_time], y_flight_lat[index_flight_time], 'o', color='w', ms=3.75, zorder=6)
            #ax.plot(x_flight_lon[index_flight_time], y_flight_lat[index_flight_time], 'o', color='k', ms=2.50, zorder=6)
            #ax.plot(x_flight_lon[index_flight_time_00], y_flight_lat[index_flight_time_00], 'o', color=sns_set2[2], ms=2.50, zorder=6)

            file_dropsonde = '/'.join([dir_dropsondes, case, file_dropsondes[idc]])
            df = pd.read_csv(file_dropsonde)
            name_set = set(list(df['NAME']))
            for name_dropsonde in name_set:
                dropsonde = df[df['NAME'] == name_dropsonde]
                #ax.plot(dropsonde['CLON'].tolist()[0], dropsonde['CLAT'].tolist()[0], 'x', color='k', markersize=5.0, zorder=6)
                del dropsonde

            if '20210820' in case:
                sounding_dropsonde = 202108210006
                dropsonde = df[df['NAME'] == sounding_dropsonde]
                #ax.plot(dropsonde['CLON'].tolist()[0], dropsonde['CLAT'].tolist()[0], 'x', color=sns_set2[0], markersize=5.0, zorder=6)
                #ax.plot(dropsonde['CLON'].tolist()[0], dropsonde['CLAT'].tolist()[0], 'x', color='k', markersize=5.0, zorder=6)
                del dropsonde
                del df

                file_sounding = '/'.join([dir_soundings, 'St_Croix', 'St_Croix_20210820200600_20210820211945_V1.csv'])
                df = pd.read_csv(file_sounding)
                #ax.plot(df['Longitude'].tolist()[0], df['Latitude'].tolist()[0], 'v', color=sns_set2[0], markersize=5.0, zorder=6)
                #ax.plot(df['Longitude'].tolist()[0], df['Latitude'].tolist()[0], 'v', color='k', markersize=5.0, zorder=6)
                del df

            x_AEW_lon, y_AEW_lat = m(AEW_lon, AEW_lat, inverse=False)
            ax.plot(x_AEW_lon, y_AEW_lat, '-', color='k', linewidth=2.50, zorder=7)
            ax.plot(x_AEW_lon, y_AEW_lat, '-', color=buda_cm_data[0], linewidth=1.25, label='Track of AEW', zorder=7)
            ax.plot(x_AEW_lon, y_AEW_lat, 'o', color='w', ms=1.25, zorder=7)
            ax.plot(x_AEW_lon[::4], y_AEW_lat[::4], 'o', color='k', ms=3.75, zorder=7)
            ax.plot(x_AEW_lon[::4], y_AEW_lat[::4], 'o', color='w', ms=2.50, zorder=7)
            for (AEWdate, AEWlon, AEWlat) in zip(AEW_dates[idc], x_AEW_lon[::4], y_AEW_lat[::4]):
                ax.text(AEWlon, AEWlat-1.50, AEWdate, ha='center', va='center', color='k', fontsize=10.0, zorder=7)
        else:
            x_TC_lon, y_TC_lat = m(TC_lon, TC_lat, inverse=False)
            sc2 = ax.scatter(x_TC_lon, y_TC_lat, c=TC_MWS, marker='o', edgecolor='none', vmin=20, vmax=125, s=30, cmap=lajolla_map, zorder=7)
            ax.plot(x_TC_lon[zidx::4], y_TC_lat[zidx::4], 'o', color='w', ms=2.50, zorder=7)
            for (TCdate, TClon, TClat) in zip(TC_dd[zidx::4], x_TC_lon[zidx::4], y_TC_lat[zidx::4]):
                ax.text(TClon, TClat-1.50, TCdate, ha='center', va='center', color='k', fontsize=10.0, zorder=7)

        i_time = 0
        time_now = anl_start_time
        while time_now <= anl_end_time:

            print(time_now)
            time_now_s = time_now - datetime.timedelta(hours = window_time/2.0)
            time_now_e = time_now + datetime.timedelta(hours = window_time/2.0)
            YYMMDD = time_now.strftime('%Y%m%d')
            HH = time_now.strftime('%H')
            #time_now_str = YYMMDD + HH
            time_now_str = time_now.strftime('%d August 2021, %H:00 UTC')

            dir_aeolus_bufr_temp = dir_aeolus + '/' + YYMMDD + HH
            print(dir_aeolus_bufr_temp)

            filename = dir_aeolus_bufr_temp + '/5.txt'
            YEAR = np.loadtxt(filename)
            filename = dir_aeolus_bufr_temp + '/6.txt'
            MNTH = np.loadtxt(filename)
            filename = dir_aeolus_bufr_temp + '/7.txt'
            DAYS = np.loadtxt(filename)
            filename = dir_aeolus_bufr_temp + '/8.txt'
            HOUR = np.loadtxt(filename)
            filename = dir_aeolus_bufr_temp + '/9.txt'
            MINU = np.loadtxt(filename)
            filename = dir_aeolus_bufr_temp + '/10.txt'
            SECW = np.loadtxt(filename)
            filename = dir_aeolus_bufr_temp + '/20.txt'
            CLATH_4 = np.loadtxt(filename)
            filename = dir_aeolus_bufr_temp + '/21.txt'
            CLONH_4 = np.loadtxt(filename)
            CLONH_4[CLONH_4>180.0] = CLONH_4[CLONH_4>180.0]-360.0

            time_temp = np.zeros((len(YEAR)))
            for idt, (yy, mm, dd, hh, minute, second) in enumerate(zip(YEAR, MNTH, DAYS, HOUR, MINU, SECW)):
                time_temp[idt] = (datetime.datetime(int(yy), int(mm), int(dd), int(hh), int(minute), int(second)) - time_now_s).total_seconds()/3600.0

            time_index = (time_temp >= 0) & (time_temp <= window_time)
            aeolus_lat = CLATH_4[time_index]
            aeolus_lon = CLONH_4[time_index]
            aeolus_time = time_temp[time_index]
            print(aeolus_lat)
            print(aeolus_lon)
            print(aeolus_time)

            print(len(aeolus_lat))

            x_aeolus_lon, y_aeolus_lat = m(aeolus_lon, aeolus_lat, inverse=False)
            ax.plot(x_aeolus_lon, y_aeolus_lat, 'o', color=colors[idcolor[idc]+i_time], ms=0.25, zorder=2)
            ax.plot(x_aeolus_lon[0:2], y_aeolus_lat[0:2], '-', color=colors[idcolor[idc]+i_time], linewidth=1.25, label=time_now_str, zorder=0)

            i_time += 1
            time_now += datetime.timedelta(hours = time_interval*2)

        ax.text(np.max(lon_d01)-2.00, np.min(lat_d01)+1.50, 'D01', ha='center', va='center', color='w', fontsize=10.0, zorder=7)
        ax.text(np.max(lon_d02)-2.00, np.min(lat_d02)+1.50, 'D02', ha='center', va='center', color='w', fontsize=10.0, zorder=7)
        ax.text(np.max(lon_d01)-2.00, np.max(lat_d01)-1.50, mtitles[idc], ha='center', va='center', color='k', fontsize=10.0, \
                bbox=dict(boxstyle='round', ec=grayC_cm_data[53], fc=grayC_cm_data[0]), zorder=7)

        x_lon_d02, y_lat_d02 = m(lon_d02, lat_d02, inverse=False)
        ax.plot(x_lon_d02, y_lat_d02, '-', color='k', linewidth=0.50, zorder=1)
        ax.legend(loc='lower left', fontsize=7.5, markerscale=7.5, handlelength=1.0).set_zorder(102)

    clb = fig.colorbar(pcm, ax=axs, ticks=np.arange(190, 250.1, 5.0), orientation='horizontal', pad=-0.075, aspect=50, shrink=0.900)
    clb.set_label('GOES-16 channel eight BT (K)', fontsize=10.0, labelpad=4.0)
    clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

    grade = [20, 33, 63, 82, 95, 112, 125]
    cat = ['TD', 'TS', 'Cat1', 'Cat2', 'Cat3', 'Cat4']
    clb2 = plt.colorbar(sc2, ax=axs, ticks=grade, orientation='horizontal', pad=0.030, aspect=50, shrink=0.900)
    clb2.set_ticklabels(grade)
    clb2.set_label('MWS (Knot)', fontsize=10.0)
    clb2.ax.tick_params(axis='both', direction='in', labelsize=10.0)
    for idx, lab in enumerate(cat):
        clb2.ax.text(0.5*(grade[idx+1]+grade[idx]), -0.875, lab, ha='center', va='center', color='k', fontsize=10.0)

    plt.savefig('./fig01.png', dpi=300)
    pdf.savefig(fig)
    plt.cla()
    plt.clf()
    plt.close()
