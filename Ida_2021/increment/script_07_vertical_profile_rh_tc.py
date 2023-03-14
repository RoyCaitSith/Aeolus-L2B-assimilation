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
from metpy.units import units
from metpy.calc import divergence
from geopy.distance import great_circle

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS'
dir_main = dir_CPEX + '/increment'

domains = ['d01']
resolutions = [12000.0, 4000.0]

#cases = ['CON6h_082406_Hybrid_C08', 'CON6h_Aeolus6h_082406_Hybrid_C08']
#labels = ['082406_C08', 'Aeolus_082406_C08']
#cases = ['CON6h_082412_Hybrid_C08', 'CON6h_Aeolus6h_082412_Hybrid_C08']
#labels = ['082412_C08', 'Aeolus_082412_C08']
cases = ['CON6h_082418_Hybrid_C08', 'CON6h_Aeolus6h_082418_Hybrid_C08']
labels = ['082418_C08', 'Aeolus_082418_C08']
#cases = ['CON6h_082500_Hybrid_C08', 'CON6h_Aeolus6h_082500_Hybrid_C08']
#labels = ['082500_C08', 'Aeolus_082500_C08']

sns_cmap = sns.color_palette('bright')
sns_paired = sns.color_palette('Paired')
colors = [sns_paired[1], sns_paired[5]]

#anl_start_time = datetime.datetime(2021, 8, 24, 12, 0, 0)
#anl_end_time   = datetime.datetime(2021, 8, 26,  6, 0, 0)
#anl_start_time = datetime.datetime(2021, 8, 24, 18, 0, 0)
#anl_end_time   = datetime.datetime(2021, 8, 26, 12, 0, 0)
anl_start_time = datetime.datetime(2021, 8, 25,  0, 0, 0)
anl_end_time   = datetime.datetime(2021, 8, 26, 18, 0, 0)
#anl_start_time = datetime.datetime(2021, 8, 25,  6, 0, 0)
#anl_end_time   = datetime.datetime(2021, 8, 27,  0, 0, 0)

r = 300.0
levels = np.arange(100, 1000.1, 100.0)

for idd, dom in enumerate(domains):

    dir_pdf = dir_main + '/vp_rh_tc/' + cases[0]
    os.system('mkdir ' + dir_pdf)

    time_now = anl_start_time
    while time_now <= anl_end_time:

        time_now_str = time_now.strftime('%Y%m%d%H')
        figname = '_'.join([time_now_str, 'vertical_profile_rh', dom])
        pdfname = dir_pdf + '/' + figname + '.pdf'
        print(pdfname)

        with PdfPages(pdfname) as pdf:

            fig, axs = plt.subplots(1, 1, figsize=(4.5, 6.0))
            fig.subplots_adjust(left=0.150, bottom=0.075, right=0.975, top=0.980, wspace=0.100, hspace=0.100)
            ax = axs

            for idc, case in enumerate(cases):

                label = labels[idc]

                casename = case + '_d01'
                filename = dir_CPEX + '/track_intensity/best_track/' + casename + '.csv'

                df = pd.read_csv(filename)

                index = []
                for idx, Date_Time in enumerate(df['Date_Time']):
                    time_temp = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
                    if time_temp == time_now: index = index + [idx]

                TC_lat = list(df['Latitude'][index])
                TC_lon = list(df['Longitude'][index])

                dir_wrfout_bkg = '/'.join([dir_CPEX, 'cycling_da', 'Data', case, 'bkg'])
                wrfout_bkg = dir_wrfout_bkg + '/wrfout_' + dom + '_' + time_now.strftime('%Y-%m-%d_%H:00:00')
                ncfile_bkg = Dataset(wrfout_bkg)
                p_bkg = getvar(ncfile_bkg, 'pressure')
                var_bkg = getvar(ncfile_bkg, 'rh')
                lat, lon = latlon_coords(p_bkg)
                tmp_var_bkg = interplevel(var_bkg, p_bkg, levels)
                ncfile_bkg.close()

                dir_wrfout_anl = '/'.join([dir_CPEX, 'cycling_da', 'Data', case, 'da'])
                wrfout_anl = dir_wrfout_anl + '/wrf_inout.' + time_now.strftime('%Y%m%d%H') + '.' + dom
                ncfile_anl = Dataset(wrfout_anl)
                p_anl = getvar(ncfile_bkg, 'pressure')
                var_anl = getvar(ncfile_anl, 'rh')
                tmp_var_anl = interplevel(var_anl, p_anl, levels)
                ncfile_anl.close()

                (n_lat, n_lon) = lat.shape
                mask_latlon = np.ones((n_lat, n_lon), dtype=bool)
                for idlat in range(n_lat):
                    for idlon in range(n_lon):
                        distance = great_circle((float(lat[idlat, idlon]), float(lon[idlat, idlon])), (TC_lat[0], TC_lon[0])).kilometers
                        if distance <= r:
                            mask_latlon[idlat, idlon] = False

                rhs = []
                for idl, lev in enumerate(levels):
                    tmp_bkg = tmp_var_bkg[idl,:,:]
                    tmp_anl = tmp_var_anl[idl,:,:]
                    tmp_inc = tmp_anl-tmp_bkg
                    tmp_inc_masked = np.ma.array(tmp_inc, mask=mask_latlon)
                    np.ma.masked_invalid(tmp_inc_masked)
                    rhs.append(np.nanmean(tmp_inc_masked))

                ax.plot(rhs, levels, '-', color=colors[idc], ms=0.25)
                ax.plot([0, 0], [0, 2000.0], '-', color='k')

            ax.set_xlabel('Increment of RH (%)', fontsize=10.0)
            ax.set_ylabel('Pressure (hPa)', fontsize=10.0)
            ax.set_xticks(np.arange(-6.0, 6.1, 2.0))
            ax.set_yticks(np.arange(0.0, 1100.0, 200.0))
            ax.tick_params('both', direction='in', labelsize=10.0)
            ax.grid(True, linewidth=0.5, color=sns_cmap[7])
            ax.axis([-6.0, 6.0, 0, 1000])

            plt.gca().invert_yaxis()
            plt.savefig(dir_pdf + '/' + figname + '.png', dpi=600)
            pdf.savefig(fig)
            plt.cla()
            plt.clf()
            plt.close()

        time_now = time_now + datetime.timedelta(hours = 6.0)
