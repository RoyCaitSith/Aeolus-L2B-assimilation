import pygrib
import datetime
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_pdf import PdfPages

time = '20210824'

case = 'CON6h_Aeolus6h_Hybrid_082500'

forecast_start_time = datetime.datetime(2021, 8, 25,  0, 0, 0)
forecast_end_time   = datetime.datetime(2021, 8, 28, 12, 0, 0)

vor_levels = np.arange(-4.8, 4.9, 0.8)
vor_labels = [-4.8, -4.0, -3.2, -2.4, -1.6, -0.8, 0.0, 0.8, 1.6, 2.4, 3.2, 4.0, 4.8]

dir_main = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021/upp'
dir_in = '/'.join([dir_main, time, case, 'postprd'])
dir_fig = '/'.join([dir_main, time, case, 'figure'])

time_now = forecast_start_time
file_name = dir_in + '/WRFPRS_d01.00'
grbs = pygrib.open(file_name)

abs_vor_grb = grbs.select(name='Absolute vorticity', typeOfLevel='isobaricInhPa', level=850)[0]
abs_vor = abs_vor_grb.values*10000.0
lats, lons = abs_vor_grb.latlons()
rel_vor = abs_vor-2.0*7.2921/100000.0*np.sin(lats*np.pi/180.0)
extent = [lons.min(), lons.max(), lats.min(), lats.max()]
print(rel_vor.min())
print(rel_vor.max())

pdfname = dir_fig + '/2021082500_rel_vor.pdf'

with PdfPages(pdfname) as pdf:

    fig, axs = plt.subplots(1, 1, figsize=(6.0, 4.50))
    fig.subplots_adjust(left=0.075, bottom=-0.035, right=0.975, top=0.975, wspace=0.100, hspace=0.100)

    ax = axs
    m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
    m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
    m.drawparallels(np.arange(-10,  36, 5), labels=[1,0,0,0], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)
    m.drawmeridians(np.arange(-95, -29, 5), labels=[0,0,0,1], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)

    pcm = ax.contourf(lons, lats, rel_vor, levels=vor_levels, cmap='RdBu_r', extend='both', zorder=1)

    clb = fig.colorbar(pcm, ax=axs, orientation='horizontal', pad=0.075, aspect=50, shrink=1.00)
    clb.set_label('Relative Vorticity of ' + case + ' at 00 UTC 25 Aug 2021', fontsize=10.0, labelpad=4.0)
    clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
    clb.ax.minorticks_off()
    clb.set_ticks(vor_levels)
    clb.set_ticklabels(vor_labels)

    pdf.savefig(fig)
    plt.cla()
    plt.clf()
    plt.close()
