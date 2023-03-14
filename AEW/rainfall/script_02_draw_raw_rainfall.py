from script_00_common_settings import *

for dom in domains:

    domain_file = dir_CPEX + '/bkg/' + time + '/' + cases[-2] + '/wrfout_' + dom + '_' + wrfout
    domain_data = Dataset(domain_file)
    domain_lat  = domain_data.variables['XLAT'][0,:,:]
    domain_lon  = domain_data.variables['XLONG'][0,:,:]
    domain_data.close()

    extent = [domain_lon[0,0], domain_lon[-1,-1], domain_lat[0,0], domain_lat[-1,-1]]

    for idt in range(0, n_time):

        time_now     = forecast_start_time + datetime.timedelta(hours = idt*cycling_interval)
        time_now_str = time_now.strftime('%Y%m%d%H')
        print(time_now)

        pdfname = dir_pdf + '/' + time_now_str + '_rainfall_6h_' + dom + '.pdf'

        with PdfPages(pdfname) as pdf:

            fig, axs   = plt.subplots(n_row, n_col, figsize=(fig_width, fig_height))
            fig.subplots_adjust(left=fig_left, bottom=fig_bottom, right=fig_right, top=fig_top, wspace=fig_wspace, hspace=fig_hspace)

            suptitle_str = time_now_str + ', ' + dom + ', 6-hr accumulated precipitation'
            fig.suptitle(suptitle_str, fontsize=7.5)

            for idc, case in enumerate(cases):

                print(case)

                var = 'rainfall'
                filename = dir_main + '/' + time + '/' + case + '/rainfall_6h_' + dom + '.nc'
                ncfile   = Dataset(filename)
                rain     = ncfile.variables[var][idt,:,:]
                rain_lat = ncfile.variables['lat'][:,:]
                rain_lon = ncfile.variables['lon'][:,:]
                ncfile.close()

                row = idc//n_col
                col = idc%n_col
                #print(row, col)

                ax = axs[row, col]
                m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                m.drawcoastlines(linewidth=0.2, color='k')
                m.drawparallels(np.arange(int(extent[2]), int(extent[3])+1, 10), labels=[1,0,0,0], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])
                m.drawmeridians(np.arange(int(extent[0]), int(extent[1])+1, 10), labels=[0,0,0,1], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])

                rain[rain<=0] = 0
                rain_lon, rain_lat = m(rain_lon, rain_lat, inverse=False)
                pcm1 = ax.contourf(rain_lon, rain_lat, rain, locator=ticker.LogLocator(), levels=rain_levels, cmap='jet', extend='max', zorder=0)

                mtitle = '(' + chr(97+idc) + ') ' + case
                ax.set_title(mtitle, fontsize=7.5, pad=4.0)

            clb = fig.colorbar(pcm1, ax=axs, orientation='horizontal', pad=lb_pad, aspect=75, shrink=0.95)
            clb.set_label('6-hr Accumulated Precipitation (mm/hr)', fontsize=7.5, labelpad=4.0)
            clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=7.5)
            clb.ax.minorticks_off()
            clb.set_ticks(rain_levels)
            clb.set_ticklabels(rain_labels)

            pdf.savefig(fig)
            plt.cla()
            plt.clf()
            plt.close()
