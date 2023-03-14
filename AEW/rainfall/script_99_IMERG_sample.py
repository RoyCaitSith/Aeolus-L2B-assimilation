import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_pdf import PdfPages

dir_IMERG = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/Data/IMERG/20210824'
file_IMERG = dir_IMERG + '/3B-HHR.MS.MRG.3IMERG.20210824-S003000-E005959.0030.V06B.HDF5'

rain_levels = [0.6, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0]
rain_labels = ['0.6', '1', '1.5', '2', '3', '4', '5', '6', '8', '10', '15', '20', '25', '30', '35', '40']

f = h5py.File(file_IMERG)
IMERG_prep = f['Grid']['precipitationCal'][0,:,:]
IMERG_lat = np.tile(f['Grid']['lat'][:], (3600, 1))
IMERG_lon = np.transpose(np.tile(f['Grid']['lon'][:], (1800, 1)))

pdfname = './smaple.pdf'
print(pdfname)

with PdfPages(pdfname) as pdf:

    fig, axs = plt.subplots(1, 1, figsize=(6.0, 5.0))
    fig.subplots_adjust(left=0.075, bottom=-0.040, right=0.975, top=0.980, wspace=0.100, hspace=0.100)

    ax = axs
    extent = [-95, -30, -10, 35]
    m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
    m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
    m.drawparallels(np.arange(-10,  36, 5), labels=[1,0,0,0], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)
    m.drawmeridians(np.arange(-95, -29, 5), labels=[0,0,0,1], fontsize=10.0, linewidth=0.01, dashes=[1,1], color='k', zorder=8)

    IMERG_lon, IMERG_lat = m(IMERG_lon, IMERG_lat, inverse=False)
    pcm = ax.contourf(IMERG_lon, IMERG_lat, IMERG_prep, locator=ticker.LogLocator(), levels=rain_levels, cmap='jet', extend='max', zorder=1)

    clb = fig.colorbar(pcm, ax=axs, orientation='horizontal', pad=0.050, aspect=50, shrink=1.00)
    clb.set_label('IMERG Precipitation (mm/hr)', fontsize=10.0, labelpad=4.0)
    clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
    clb.ax.minorticks_off()
    clb.set_ticks(rain_levels)
    clb.set_ticklabels(rain_labels)

    pdf.savefig(fig)
    plt.cla()
    plt.clf()
    plt.close()
