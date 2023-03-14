import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import h5py
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
dir_GMI = '/'.join([dir_GOES, 'Data', 'GPM'])
dir_abi = '/'.join([dir_GOES, 'Data', 'GOES-R', 'ABI-L2-CMIPF'])
dir_best_track = '/'.join([dir_CPEX, 'track_intensity', 'best_track'])

cases = ['20210904']

cpt, cpt_r = loadCPT('./GOES-R_BT.rgb')
cpt_convert = LinearSegmentedColormap('cpt', cpt)
cpt_convert_r = LinearSegmentedColormap('cpt', cpt_r)

for case in cases:

    if '20210820' in case:
        draw_times = [datetime.datetime(2021, 8, 21,  2, 0, 0), datetime.datetime(2021, 8, 21, 16, 0, 0), datetime.datetime(2021, 8, 22,  3, 0, 0)]
        GMI_files  = ['/'.join(['20210821', '1A.GPM.GMI.COUNT2016.20210821-S013011-E030245.042491.V05B.HDF5']), \
                      '/'.join(['20210821', '1A.GPM.GMI.COUNT2016.20210821-S152320-E165553.042500.V05B.HDF5']), \
                      '/'.join(['20210822', '1A.GPM.GMI.COUNT2016.20210822-S021120-E034352.042507.V05B.HDF5'])]
        if_AEW = True
        AEW_locations = [(-71.81, 14.95), (-77.03, 16.72), (-81.235, 17.74)]
    if '20210821' in case:
        draw_times = [datetime.datetime(2021, 8, 22,  1, 0, 0), datetime.datetime(2021, 8, 22, 15, 0, 0), \
                      datetime.datetime(2021, 8, 23,  0, 0, 0), datetime.datetime(2021, 8, 23,  2, 0, 0)]
        GMI_files  = ['/'.join(['20210822', '1A.GPM.GMI.COUNT2016.20210822-S003845-E021119.042506.V05B.HDF5']), \
                      '/'.join(['20210822', '1A.GPM.GMI.COUNT2016.20210822-S143153-E160427.042515.V05B.HDF5']), \
                      '/'.join(['20210822', '1A.GPM.GMI.COUNT2016.20210822-S234718-E011952.042521.V05B.HDF5']), \
                      '/'.join(['20210823', '1A.GPM.GMI.COUNT2016.20210823-S011953-E025226.042522.V05B.HDF5'])]
        if_AEW = True
        AEW_locations = [(-50.42, 12.26), (-53.93, 12.34), (-56.97, 12.39), (-57.85, 12.35)]
    if '20210824' in case:
        draw_times = [datetime.datetime(2021, 8, 25,  0, 0, 0), datetime.datetime(2021, 8, 25, 12, 0, 0), datetime.datetime(2021, 8, 25, 18, 0, 0), \
                      datetime.datetime(2021, 8, 26,  0, 0, 0), datetime.datetime(2021, 8, 26, 12, 0, 0), datetime.datetime(2021, 8, 27,  0, 0, 0), \
                      datetime.datetime(2021, 8, 27, 18, 0, 0), datetime.datetime(2021, 8, 28,  0, 0, 0), datetime.datetime(2021, 8, 28, 12, 0, 0)]
        GMI_files  = ['/'.join(['20210825', '1A.GPM.GMI.COUNT2016.20210825-S010933-E024206.042553.V05B.HDF5']), \
                      '/'.join(['20210825', '1A.GPM.GMI.COUNT2016.20210825-S133005-E150239.042561.V05B.HDF5']), \
                      '/'.join(['20210825', '1A.GPM.GMI.COUNT2016.20210825-S150240-E163513.042562.V05B.HDF5']), \
                      '/'.join(['20210826', '1A.GPM.GMI.COUNT2016.20210826-S001805-E015038.042568.V05B.HDF5']), \
                      '/'.join(['20210826', '1A.GPM.GMI.COUNT2016.20210826-S141111-E154345.042577.V05B.HDF5']), \
                      '/'.join(['20210827', '1A.GPM.GMI.COUNT2016.20210827-S005910-E023143.042584.V05B.HDF5']), \
                      '/'.join(['20210827', '1A.GPM.GMI.COUNT2016.20210827-S145217-E162450.042593.V05B.HDF5']), \
                      '/'.join(['20210828', '1A.GPM.GMI.COUNT2016.20210828-S000741-E014014.042599.V05B.HDF5']), \
                      '/'.join(['20210828', '1A.GPM.GMI.COUNT2016.20210828-S140047-E153320.042608.V05B.HDF5'])]
        if_AEW = False
        best_track_name = '2021_09L_Ida.csv'
    if '20210828' in case:
        draw_times = [datetime.datetime(2021, 8, 29,  0, 0, 0), datetime.datetime(2021, 8, 29, 12, 0, 0), datetime.datetime(2021, 8, 30,  0, 0, 0), \
                      datetime.datetime(2021, 8, 30, 12, 0, 0), datetime.datetime(2021, 8, 31,  0, 0, 0)]
        GMI_files  = ['/'.join(['20210828', '1A.GPM.GMI.COUNT2016.20210828-S214337-E231610.042613.V05B.HDF5']), \
                      '/'.join(['20210829', '1A.GPM.GMI.COUNT2016.20210829-S113643-E130915.042622.V05B.HDF5']), \
                      '/'.join(['20210829', '1A.GPM.GMI.COUNT2016.20210829-S222440-E235713.042629.V05B.HDF5']), \
                      '/'.join(['20210830', '1A.GPM.GMI.COUNT2016.20210830-S121745-E135018.042638.V05B.HDF5']), \
                      '/'.join(['20210830', '1A.GPM.GMI.COUNT2016.20210830-S213309-E230541.042644.V05B.HDF5'])]
        if_AEW = False
        best_track_name = '2021_10L_Kate.csv'
    if '20210904' in case:
        draw_times = [datetime.datetime(2021, 9,  5,  0, 0, 0), datetime.datetime(2021, 9,  5, 12, 0, 0), datetime.datetime(2021, 9,  5, 18, 0, 0), \
                      datetime.datetime(2021, 9,  6, 12, 0, 0), datetime.datetime(2021, 9,  7,  0, 0, 0)]
        GMI_files  = ['/'.join(['20210904', '1A.GPM.GMI.COUNT2016.20210904-S202151-E215425.042721.V05B.HDF5']), \
                      '/'.join(['20210905', '1A.GPM.GMI.COUNT2016.20210905-S101509-E114743.042730.V05B.HDF5']), \
                      '/'.join(['20210905', '1A.GPM.GMI.COUNT2016.20210905-S193041-E210315.042736.V05B.HDF5']), \
                      '/'.join(['20210906', '1A.GPM.GMI.COUNT2016.20210906-S092358-E105632.042745.V05B.HDF5']), \
                      '/'.join(['20210906', '1A.GPM.GMI.COUNT2016.20210906-S201205-E214439.042752.V05B.HDF5'])]
        if_AEW = False
        best_track_name = '2021_12L_Larry.csv'

    if not if_AEW:
        file_best_track = dir_best_track + '/' + best_track_name
        df = pd.read_csv(file_best_track)
        TC_lats = list(df['Latitude'][:])
        TC_lons = list(df['Longitude'][:])
        TC_dates = list(df['Date_Time'][:])
        del df

    for (idt, time_now) in enumerate(draw_times):

        YYMMDD = time_now.strftime('%Y%m%d')
        HH = time_now.strftime('%H')
        time_now_str = YYMMDD + HH
        pdfname = '_'.join(['./figure_02_GMI_GOES_MdBZ', case, time_now_str+'.pdf'])
        print(pdfname)

        if if_AEW:
            (AEW_lon, AEW_lat) = AEW_locations[idt]
            extent = [AEW_lon-5.0, AEW_lon+5.0, AEW_lat-5.0, AEW_lat+5.0]
        else:
            for id_TC, TC_date in enumerate(TC_dates):
                TC_datetime = datetime.datetime.strptime(TC_date, '%Y-%m-%d %H:%M:%S')
                if TC_datetime == time_now:
                    TC_lat = TC_lats[id_TC]
                    TC_lon = TC_lons[id_TC]
                    extent = [TC_lon-5.0, TC_lon+5.0, TC_lat-5.0, TC_lat+5.0]

        with PdfPages(pdfname) as pdf:

            fig, axs = plt.subplots(2, 2, figsize=(6.0, 6.5))
            fig.subplots_adjust(left=0.050, bottom=0.025, right=0.975, top=0.975, wspace=0.050, hspace=0.050)

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

            ax = axs[0, 0]
            m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
            m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
            m.drawparallels(np.arange(-10,  36, 5), labels=[1,0,0,0], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='w', zorder=8)
            m.drawmeridians(np.arange(-95, -29, 5), labels=[0,0,0,1], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='w', zorder=8)

            x_abi_lon, y_abi_lat = m(abi_lon, abi_lat, inverse=False)
            pcm = ax.contourf(x_abi_lon, y_abi_lat, CMI, levels=np.arange(190.0, 250.1, 1.0), cmap=cpt_convert, extend='both', zorder=1)
            if if_AEW:
                ax.plot(AEW_lon, AEW_lat, 'x', color='k', markersize=7.5, markeredgewidth=1.0)
                ax.text(AEW_lon-4.5, AEW_lat+4.5, '(a)', ha='center', va='center', color='k', fontsize=10.0, zorder=7)
            else:
                ax.plot(TC_lon, TC_lat, 'x', color='k', markersize=7.5, markeredgewidth=1.0)
                ax.text(TC_lon-4.5, TC_lat+4.5, '(a)', ha='center', va='center', color='k', fontsize=10.0, zorder=7)

            clb_label = 'GOES-R Channel 8 BTs (K)'
            clb = fig.colorbar(pcm, ax=ax, ticks=np.arange(190, 250.1, 10.0), orientation='horizontal', pad=0.060, aspect=25, shrink=0.90)
            clb.set_label(clb_label, fontsize=10.0, labelpad=4.0)
            clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

            filename = dir_GMI + '/' + GMI_files[idt]
            GMI = h5py.File(filename, 'r')
            S1_Latitude = np.array(GMI['S1']['Latitude'])
            S1_Longitude = np.array(GMI['S1']['Longitude'])
            S1_earthView = np.array(GMI['S1']['earthView'])
            S2_Latitude = np.array(GMI['S2']['Latitude'])
            S2_Longitude = np.array(GMI['S2']['Longitude'])
            S2_earthView = np.array(GMI['S2']['earthView'])
            GMI.close()

            ax = axs[0, 1]

            m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
            m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
            m.drawparallels(np.arange(-10,  36, 5), labels=[1,0,0,0], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)
            m.drawmeridians(np.arange(-95, -29, 5), labels=[0,0,0,1], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)

            x_s1_lon, y_s1_lat = m(S1_Longitude, S1_Latitude, inverse=False)
            pcm = ax.contourf(x_s1_lon, y_s1_lat, S1_earthView[:,:,0]/100.0, levels=np.arange(190, 205.1, 0.25), cmap=cpt_convert_r, extend='both', zorder=1)
            if if_AEW:
                ax.plot(AEW_lon, AEW_lat, 'x', color='k', markersize=7.5, markeredgewidth=1.0)
                ax.text(AEW_lon-4.5, AEW_lat+4.5, '(b)', ha='center', va='center', color='k', fontsize=10.0, zorder=7)
            else:
                ax.plot(TC_lon, TC_lat, 'x', color='k', markersize=7.5, markeredgewidth=1.0)
                ax.text(TC_lon-4.5, TC_lat+4.5, '(b)', ha='center', va='center', color='k', fontsize=10.0, zorder=7)

            clb_label = '10.65 GHz V BTs (K)'
            clb = fig.colorbar(pcm, ax=ax, ticks=np.arange(190, 205.1, 5), orientation='horizontal', pad=0.060, aspect=25, shrink=0.90)
            clb.set_label(clb_label, fontsize=10.0, labelpad=4.0)
            clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

            ax = axs[1, 0]

            m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
            m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
            m.drawparallels(np.arange(-10,  36, 5), labels=[1,0,0,0], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)
            m.drawmeridians(np.arange(-95, -29, 5), labels=[0,0,0,1], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)

            x_s1_lon, y_s1_lat = m(S1_Longitude, S1_Latitude, inverse=False)
            pcm = ax.contourf(x_s1_lon, y_s1_lat, S1_earthView[:,:,5]/100.0, levels=np.arange(175, 205.1, 0.5), cmap=cpt_convert_r, extend='both', zorder=1)
            if if_AEW:
                ax.plot(AEW_lon, AEW_lat, 'x', color='k', markersize=7.5, markeredgewidth=1.0)
                ax.text(AEW_lon-4.5, AEW_lat+4.5, '(c)', ha='center', va='center', color='k', fontsize=10.0, zorder=7)
            else:
                ax.plot(TC_lon, TC_lat, 'x', color='k', markersize=7.5, markeredgewidth=1.0)
                ax.text(TC_lon-4.5, TC_lat+4.5, '(c)', ha='center', va='center', color='k', fontsize=10.0, zorder=7)

            clb_label = '36.5 GHz V BTs (K)'
            clb = fig.colorbar(pcm, ax=ax, ticks=np.arange(175, 205.1, 5), orientation='horizontal', pad=0.060, aspect=25, shrink=0.90)
            clb.set_label(clb_label, fontsize=10.0, labelpad=4.0)
            clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

            ax = axs[1, 1]

            m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
            m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
            m.drawparallels(np.arange(-10,  36, 5), labels=[1,0,0,0], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)
            m.drawmeridians(np.arange(-95, -29, 5), labels=[0,0,0,1], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)

            x_s2_lon, y_s2_lat = m(S2_Longitude, S2_Latitude, inverse=False)
            pcm = ax.contourf(x_s2_lon, y_s2_lat, S2_earthView[:,:,3]/100.0, levels=np.arange(230, 290.1, 1.0), cmap=cpt_convert, extend='both', zorder=1)
            if if_AEW:
                ax.plot(AEW_lon, AEW_lat, 'x', color='k', markersize=7.5, markeredgewidth=1.0)
                ax.text(AEW_lon-4.5, AEW_lat+4.5, '(d)', ha='center', va='center', color='k', fontsize=10.0, zorder=7)
            else:
                ax.plot(TC_lon, TC_lat, 'x', color='k', markersize=7.5, markeredgewidth=1.0)
                ax.text(TC_lon-4.5, TC_lat+4.5, '(d)', ha='center', va='center', color='k', fontsize=10.0, zorder=7)

            clb_label = '183.31_7 V BTs (K)'
            clb = fig.colorbar(pcm, ax=ax, ticks=np.arange(230, 290.1, 10), orientation='horizontal', pad=0.060, aspect=25, shrink=0.90)
            clb.set_label(clb_label, fontsize=10.0, labelpad=4.0)
            clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

            pdf.savefig(fig)
            plt.cla()
            plt.clf()
            plt.close()
