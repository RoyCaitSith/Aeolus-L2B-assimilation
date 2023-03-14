import os
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_pdf import PdfPages
from wrf import to_np, getvar, CoordPair, vertcross, latlon_coords, interplevel
from scipy.interpolate import griddata
from subroutine import cal_polar_to_latlon as clatlon

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS'
dir_main = dir_CPEX + '/increment'

domains = ['d01']

#cases = ['CON6h_082406_Hybrid_C08', 'CON6h_Aeolus6h_082406_Hybrid_C08']
#labels = ['082406_C08', 'Aeolus_082406_C08']
#cases = ['CON6h_082412_Hybrid_C08', 'CON6h_Aeolus6h_082412_Hybrid_C08']
#labels = ['082412_C08', 'Aeolus_082412_C08']
#cases = ['CON6h_082418_Hybrid_C08', 'CON6h_Aeolus6h_082418_Hybrid_C08']
#labels = ['082418_C08', 'Aeolus_082418_C08']
cases = ['CON6h_082500_Hybrid_C08', 'CON6h_Aeolus6h_082500_Hybrid_C08']
labels = ['082500_C08', 'Aeolus_082500_C08']

#anl_start_time = datetime.datetime(2021, 8, 24, 12, 0, 0)
#anl_end_time   = datetime.datetime(2021, 8, 26,  6, 0, 0)
#anl_start_time = datetime.datetime(2021, 8, 24, 18, 0, 0)
#anl_end_time   = datetime.datetime(2021, 8, 26, 12, 0, 0)
#anl_start_time = datetime.datetime(2021, 8, 25,  0, 0, 0)
#anl_end_time   = datetime.datetime(2021, 8, 26, 18, 0, 0)
anl_start_time = datetime.datetime(2021, 8, 25,  6, 0, 0)
anl_end_time   = datetime.datetime(2021, 8, 27,  0, 0, 0)

levels = {}
levels.update({925: [-9.0, 10.0, 2.0, 'BrBG']})
levels.update({850: [-9.0, 10.0, 2.0, 'BrBG']})
levels.update({700: [-9.0, 10.0, 2.0, 'BrBG']})
levels.update({500: [-9.0, 10.0, 2.0, 'BrBG']})
levels.update({300: [-9.0, 10.0, 2.0, 'BrBG']})
levels.update({200: [-9.0, 10.0, 2.0, 'BrBG']})
levels.update({100: [-9.0, 10.0, 2.0, 'BrBG']})

radii = [150.0, 300.0, 450.0]
angles = np.arange(0.0, 360.0, 2.0)
sns_cmap = sns.color_palette('bright')

for dom in domains:
    for idc, case in enumerate(cases):

        label = labels[idc]

        dir_pdf = dir_main + '/rh_tc/' + case
        os.system('mkdir ' + dir_pdf)

        casename = case + '_d01'
        filename = dir_CPEX + '/track_intensity/best_track/' + casename + '.csv'

        df = pd.read_csv(filename)

        time_now = anl_start_time
        while time_now <= anl_end_time:

            time_now_str = time_now.strftime('%Y%m%d%H')

            index = []
            for idx, Date_Time in enumerate(df['Date_Time']):
                time_temp = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
                if time_temp == time_now: index = index + [idx]

            TC_lat = list(df['Latitude'][index])
            TC_lon = list(df['Longitude'][index])
            extent = [TC_lon[0]-5.0, TC_lon[0]+5.0, TC_lat[0]-5.0, TC_lat[0]+5.0]
            #print([TC_lat, TC_lon])

            dir_wrfout_bkg = '/'.join([dir_CPEX, 'cycling_da', 'Data', case, 'bkg'])
            wrfout_bkg = dir_wrfout_bkg + '/wrfout_' + dom + '_' + time_now.strftime('%Y-%m-%d_%H:00:00')
            ncfile_bkg = Dataset(wrfout_bkg)
            p_bkg = getvar(ncfile_bkg, 'pressure')
            ua_bkg = getvar(ncfile_bkg, 'ua', units='ms-1')
            va_bkg = getvar(ncfile_bkg, 'va', units='ms-1')
            var_bkg = getvar(ncfile_bkg, 'rh')
            lat, lon = latlon_coords(p_bkg)
            tmp_bkg = interplevel(var_bkg, p_bkg, list(levels.keys()))
            ncfile_bkg.close()

            dir_wrfout_anl = '/'.join([dir_CPEX, 'cycling_da', 'Data', case, 'da'])
            wrfout_anl = dir_wrfout_anl + '/wrf_inout.' + time_now.strftime('%Y%m%d%H') + '.' + dom
            ncfile_anl = Dataset(wrfout_anl)
            p_anl = getvar(ncfile_anl, 'pressure')
            ua_anl = getvar(ncfile_anl, 'ua', units='ms-1')
            va_anl = getvar(ncfile_anl, 'va', units='ms-1')
            var_anl = getvar(ncfile_anl, 'rh')
            tmp_anl = interplevel(var_anl, p_anl, list(levels.keys()))
            ncfile_anl.close()

            for idl, lev in enumerate(levels.keys()):

                figname = '_'.join([time_now_str, 'rh', case, dom, str(int(lev))])
                pdfname = dir_pdf + '/' + figname + '.pdf'
                print(pdfname)

                with PdfPages(pdfname) as pdf:

                    fig, axs = plt.subplots(1, 1, figsize=(6.0, 6.0))
                    fig.subplots_adjust(left=0.075, bottom=-0.050, right=0.975, top=0.980, wspace=0.100, hspace=0.100)

                    ax = axs
                    m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                    m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                    m.drawparallels(np.arange( -10,  46, 2.5), labels=[1,0,0,0], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)
                    m.drawmeridians(np.arange(-120, -29, 2.5), labels=[0,0,0,1], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)

                    #print(np.max(tmp_anl[idl,:,:]-tmp_bkg[idl,:,:]))
                    #print(np.min(tmp_anl[idl,:,:]-tmp_bkg[idl,:,:]))
                    #print(np.max(tmp_bkg[idl,:,:]))
                    #print(np.min(tmp_bkg[idl,:,:]))

                    inc_contourf = ax.contourf(lon, lat, tmp_anl[idl,:,:]-tmp_bkg[idl,:,:], \
                                               levels=np.arange(levels[lev][0], levels[lev][1], levels[lev][2]), cmap=levels[lev][3], extend='both', zorder=1)
                    pcm = ax.quiver(lon[::2, ::2], lat[::2, ::2], ua_bkg[idl, ::2, ::2], va_bkg[idl, ::2, ::2], color='k', scale=5.0*10.0, scale_units='inches', zorder=2)
                    qk = ax.quiverkey(pcm, 0.050, 0.050, 10.0, '10.0 m/s', labelpos='E', coordinates='figure')
                    ax.plot([-180.0, 180.0], [TC_lat[0], TC_lat[0]], '--', color=sns_cmap[7], linewidth=1.0, zorder=3)
                    ax.plot([TC_lon[0], TC_lon[0]], [-90.0, 90.0],   '--', color=sns_cmap[7], linewidth=1.0, zorder=3)

                    lat_polar = np.zeros((len(radii), len(angles)))
                    lon_polar = np.zeros((len(radii), len(angles)))
                    for idr in range(0, len(radii)):
                        for ida in range(0, len(angles)):
                            lat_polar[idr,ida], lon_polar[idr,ida] = clatlon.Cal_LatLon(TC_lat[0], TC_lon[0], radii[idr], angles[ida])
                        ax.plot(lon_polar[idr,:], lat_polar[idr,:], '--', color=sns_cmap[7], linewidth=1.0, zorder=3)

                    clb = fig.colorbar(inc_contourf, ax=axs, ticks=np.arange(levels[lev][0], levels[lev][1], levels[lev][2]), \
                                       orientation='horizontal', pad=0.050, aspect=50, shrink=1.00)
                    clb.set_label('RH Increment (%) of Exp. ' + label + \
                                  ' on ' + str(int(lev)) + ' hPa at ' + time_now_str, fontsize=7.5, labelpad=4.0)
                    clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
                    #plt.clabel(bkg_contour1, bkg_contour1.levels[::2], fontsize=10.0, inline=1, fmt='%1.0f')
                    #plt.clabel(bkg_contour2, bkg_contour2.levels[::2], fontsize=10.0, inline=1, fmt='%1.0f')

                    plt.savefig(dir_pdf + '/' + figname + '.png')
                    pdf.savefig(fig)
                    plt.cla()
                    plt.clf()
                    plt.close()

            time_now = time_now + datetime.timedelta(hours = 6.0)
