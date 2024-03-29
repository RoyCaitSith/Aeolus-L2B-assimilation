import os
import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from cpt_convert import loadCPT
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import LinearSegmentedColormap

case = 'CON6h_082412_Hybrid_C08'

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS'
dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main = '/'.join([dir_CPEX, 'figures'])
dir_aeolus = '/'.join([dir_CPEX, 'Aeolus', 'create_bufr', 'bufr_temp'])
dir_abi = '/'.join([dir_GOES, 'Data', 'GOES-R', 'ABI-L2-CMIPF'])
dir_wrfout = '/'.join([dir_CPEX, 'cycling_da', 'Data', case, 'bkg'])
dir_best_track = '/'.join([dir_CPEX, 'track_intensity', 'best_track'])

time_interval = 6
window_time = 6

file_wrfout_d01 = dir_wrfout + '/wrfout_d01_2021-08-24_12:00:00'
file_wrfout_d02 = dir_wrfout + '/wrfout_d02_2021-08-24_12:00:00'
anl_start_time = datetime.datetime(2021, 8, 25,  0, 0, 0)
anl_end_time = datetime.datetime(2021, 8, 26, 12, 0, 0)

cpt, cpt_r = loadCPT('./GOES-R_BT.rgb')
cpt_convert = LinearSegmentedColormap('cpt', cpt)

sns_cmap = sns.color_palette('Paired')
sns_set2 = sns.color_palette('Set2')
#colors = [sns_cmap[1], sns_cmap[3], sns_cmap[5], sns_cmap[7], sns_cmap[9], sns_cmap[11]]
colors = [sns_cmap[3], sns_cmap[5], sns_cmap[7], sns_cmap[9]]

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

#Read GFS hgt and rh at 2021082512
GFS_time = 4
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

#Best track data from 2021082412 to 2021082818
(sidx, eidx, zidx) = (1, 19, 0)
file_best_track = dir_best_track + '/2021_09L_Ida.csv'
df = pd.read_csv(file_best_track)
TC_lat = list(df['Latitude'][sidx:eidx])
TC_lon = list(df['Longitude'][sidx:eidx])
TC_MWS = df['MWS (Knot)'][sidx:eidx]
TC_dd = df['Date_Time'][sidx:eidx]
TC_dd = [x[8:10] for x in TC_dd]
del df

pdfname = '_'.join(['Figure_02b_2021082412_2021082818_GFS_GOES-R_2021082512.pdf'])
pdfname = '/'.join([dir_main, pdfname])
print(pdfname)

with PdfPages(pdfname) as pdf:

    fig, axs = plt.subplots(1, 1, figsize=(6.0, 5.0))
    fig.subplots_adjust(left=0.075, bottom=-0.025, right=0.975, top=0.975, wspace=0.000, hspace=0.000)

    time_GOES_now = datetime.datetime(2021, 8, 25, 12, 0, 0)
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

    ax = axs
    m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=axs)
    m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
    m.drawparallels(np.arange(-10,   46, 5), labels=[1,0,0,0], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)
    m.drawmeridians(np.arange(-120, -29, 5), labels=[0,0,0,1], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)

    x_abi_lon, y_abi_lat = m(abi_lon, abi_lat, inverse=False)
    pcm = ax.contourf(x_abi_lon, y_abi_lat, CMI, levels=np.arange(190.0, 250.1, 0.5), cmap=cpt_convert, extend='both', zorder=1)

    x_GFS_lon, y_GFS_lat = m(GFS_lon, GFS_lat, inverse=False)
    CS1 = ax.contour(x_GFS_lon, y_GFS_lat, GFS_rh, levels=np.arange(5.0, 36.0, 10.0), colors=sns_set2[5], linewidths=1.00, zorder=4)
    CS2 = ax.contour(x_GFS_lon, y_GFS_lat, GFS_hgt, levels=np.arange(3000.0, 3301.0, 20.0), colors='w', linewidths=1.00, zorder=5)
    ax.clabel(CS1, CS1.levels, inline=True, fmt='%1.0f%%', fontsize=5.0)
    ax.clabel(CS2, CS2.levels, inline=True, fmt='%1.0f', fontsize=5.0)

    x_TC_lon, y_TC_lat = m(TC_lon, TC_lat, inverse=False)
    sc2 = ax.scatter(x_TC_lon, y_TC_lat, c=TC_MWS, marker='o', edgecolor='none', vmin=20, vmax=125, s=30, cmap='jet', zorder=7)
    ax.plot(x_TC_lon[zidx::4], y_TC_lat[zidx::4], 'o', color='w', ms=2.50, zorder=7)
    for (TCdate, TClon, TClat) in zip(TC_dd[zidx::4], x_TC_lon[zidx::4], y_TC_lat[zidx::4]):
        ax.text(TClon, TClat-0.75, TCdate, ha='center', va='center', color='k', fontsize=5.0, zorder=7)

    i_time = 0
    time_now = anl_start_time
    while time_now <= anl_end_time:

        print(time_now)
        time_now_s = time_now - datetime.timedelta(hours = window_time/2.0)
        time_now_e = time_now + datetime.timedelta(hours = window_time/2.0)
        YYMMDD = time_now.strftime('%Y%m%d')
        HH = time_now.strftime('%H')
        time_now_str = YYMMDD + HH

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
        ax.plot(x_aeolus_lon, y_aeolus_lat, 'o', color=colors[i_time], ms=0.25, label=time_now_str, zorder=2)

        i_time += 1
        time_now += datetime.timedelta(hours = time_interval*2)

    ax.text(np.min(lon_d01)+1.5, np.max(lat_d01)-0.75, 'D01', ha='center', va='center', color='k', fontsize=7.5, zorder=7)
    ax.text(np.min(lon_d02)+1.5, np.max(lat_d02)-0.75, 'D02', ha='center', va='center', color='k', fontsize=7.5, zorder=7)

    x_lon_d02, y_lat_d02 = m(lon_d02, lat_d02, inverse=False)
    ax.plot(x_lon_d02, y_lat_d02, '-', color='k', linewidth=0.50, zorder=1)
    ax.legend(loc='lower right', fontsize=7.5, markerscale=5.0, handlelength=1.0)

    clb = fig.colorbar(pcm, ax=axs, ticks=np.arange(190, 250.1, 5.0), orientation='horizontal', pad=-0.025, aspect=50, shrink=1.00)
    clb.set_label('GOES-R Channel 8 BTs (K) at ' + time_GOES_now.strftime('%H UTC %d Aug %Y'), fontsize=10.0, labelpad=4.0)
    clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

    grade = [20, 33, 63, 82, 95, 112, 125]
    cat = ['TD', 'TS', 'Cat1', 'Cat2', 'Cat3', 'Cat4']
    clb2 = plt.colorbar(sc2, ticks=grade, orientation='horizontal', pad=0.050, aspect=50, shrink=1.00)
    clb2.set_ticklabels(grade)
    clb2.set_label('MWS (Knot)', fontsize=10.0)
    clb2.ax.tick_params(axis='both', direction='in', labelsize=10.0)
    for idx, lab in enumerate(cat):
        clb2.ax.text(0.5*(grade[idx+1]+grade[idx]), -1.0, lab, ha='center', va='center', color='k', fontsize=10.0)

    pdf.savefig(fig)
    plt.cla()
    plt.clf()
    plt.close()
