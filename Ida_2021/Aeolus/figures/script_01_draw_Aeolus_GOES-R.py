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

case = '20210824'

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/14_ENS_20210824'
dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main = dir_CPEX + '/Aeolus'
dir_aeolus = dir_main + '/create_bufr/bufr_temp'
dir_figs = dir_main + '/figures'
dir_abi  = dir_GOES + '/Data/GOES-R/ABI-L2-CMIPF'
dir_best_track = dir_CPEX + '/track_intensity/best_track'
dir_wrfout = dir_main + '/wrfout'
file_wrfout_d01 = dir_wrfout + '/wrfout_d01_2021-08-24_06:00:00'
file_wrfout_d02 = dir_wrfout + '/wrfout_d02_2021-08-24_06:00:00'
time_interval = 6
window_time = 6

if '20210824' in case:
    anl_start_time  = datetime.datetime(2021, 8, 23,  0, 0, 0)
    anl_end_time    = datetime.datetime(2021, 8, 29,  0, 0, 0)

cpt, cpt_r = loadCPT('./GOES-R_BT.rgb')
cpt_convert = LinearSegmentedColormap('cpt', cpt)
cpt_convert_r = LinearSegmentedColormap('cpt', cpt_r)

file_best_track = dir_best_track + '/2021_09L_Ida.csv'
df = pd.read_csv(file_best_track)
TC_lat = list(df['Latitude'][:18])
TC_lon = list(df['Longitude'][:18])
TC_MWS = df['MWS (Knot)'][:18]
TC_dd = df['Date_Time'][:18]
TC_dd = [x[8:10] for x in TC_dd]

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

time_now = anl_start_time
while time_now <= anl_end_time:

    print(time_now)
    time_now_s = time_now - datetime.timedelta(hours = window_time/2.0)
    time_now_e = time_now + datetime.timedelta(hours = window_time/2.0)
    YYMMDD = time_now.strftime('%Y%m%d')
    HH = time_now.strftime('%H')
    time_now_str = YYMMDD + HH

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

    pdfname = dir_figs + '/Aeolus_GOES-R_' + time_now_str + '.pdf'
    print(pdfname)

    with PdfPages(pdfname) as pdf:

        fig, axs = plt.subplots(1, 1, figsize=(6.0, 5.0))
        fig.subplots_adjust(left=0.075, bottom=-0.025, right=0.975, top=0.975, wspace=0.000, hspace=0.000)

        ax = axs
        m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=axs)
        m.drawcoastlines(linewidth=0.2, color='k')
        m.drawparallels(np.arange(int(extent[2]), int(extent[3])+1, 5), labels=[1,0,0,0], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])
        m.drawmeridians(np.arange(int(extent[0]), int(extent[1])+1, 5), labels=[0,0,0,1], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])

        x_abi_lon, y_abi_lat = m(abi_lon, abi_lat, inverse=False)
        pcm = ax.contourf(x_abi_lon, y_abi_lat, CMI, levels=np.arange(190.0, 250.1, 1.0), cmap=cpt_convert, extend='both', zorder=0)

        x_aeolus_lon, y_aeolus_lat = m(aeolus_lon, aeolus_lat, inverse=False)
        ax.plot(x_aeolus_lon, y_aeolus_lat, 'o', color='r', ms=0.25, zorder=2)

        x_TC_lon, x_TC_lat = m(TC_lon, TC_lat, inverse=False)
        sc2 = ax.scatter(x_TC_lon, x_TC_lat, c=TC_MWS, marker='o', edgecolor='none', vmin=20, vmax=125, s=30, cmap='jet', zorder=7)
        ax.plot(x_TC_lon[3::4], x_TC_lat[3::4], 'o', color='w', ms=2.50, zorder=7)
        for (TCdate, TClon, TClat) in zip(TC_dd[3::4], x_TC_lon[3::4], x_TC_lat[3::4]):
            ax.text(TClon, TClat-0.75, TCdate, ha='center', va='center', color='k', fontsize=5.0, zorder=7)

        x_lon_d02, y_lat_d02 = m(lon_d02, lat_d02, inverse=False)
        ax.plot(x_lon_d02, y_lat_d02, '-', color='k', linewidth=0.50, zorder=3)

        clb = fig.colorbar(pcm, ax=axs, ticks=np.arange(190, 250.1, 10.0), orientation='horizontal', pad=0.000, aspect=50, shrink=1.00)
        clb.set_label('GOES-R Channel 8 Brightness Temperatures (K) at ' + time_now_str, fontsize=10.0, labelpad=4.0)
        clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

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
