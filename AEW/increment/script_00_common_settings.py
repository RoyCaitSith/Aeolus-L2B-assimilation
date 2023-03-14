import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import datetime
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.basemap import Basemap

#cases = ['CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', 'CON6h_DAWN1hOE1p5', \
          #'CON6h_HALO1h', 'CON6h_HALO1hOE0p2', 'CON6h_DS1h', 'CON6h_Aeolus6h', \
          #'CON6h_DAWN1h_HALO1h_DS1h', 'CON6h_DAWN1h_HALO1h_DS1h_Aeolus6h']
#cases = ['20210824_CON6h', '20210824_CON6h_Aeolus6h', '20210824_CON6h_DS1h', \
         #'20210824_CON6h_DS1h_UV', '20210824_CON6h_DS1h_T', '20210824_CON6h_DS1h_Q']
#cases = ['20210824_CON6h_082500', '20210824_CON6h_Aeolus6h_082500', '20210824_CON6h_DS1h_082500', \
         #'20210824_CON6h_DS1h_UV_082500', '20210824_CON6h_DS1h_T_082500', '20210824_CON6h_DS1h_Q_082500']
#cases = ['20210824_CON6h_082512', '20210824_CON6h_Aeolus6h_082512', '20210824_CON6h_DS1h_082512', \
         #'20210824_CON6h_DS1h_UV_082512', '20210824_CON6h_DS1h_T_082512', '20210824_CON6h_DS1h_Q_082512']
#cases = ['20210904_CON6h_DAWN1h_Aeolus6h']
#cases = ['20210904_CON6h_DS1h', '20210904_CON6h_DS1h_UV', '20210904_CON6h_DS1h_T', '20210904_CON6h_DS1h_Q']
#cases = ['20210824_CON6h_Hybrid_082500']

draw_scheme = 3

if draw_scheme == 1:
    cases    = ['20210820_CON6h_DS1h_UV', '20210820_CON6h_DS1h_T', '20210820_CON6h_DS1h_Q']
    dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021'
    dir_main = dir_CPEX + '/increment/' + cases[0][0:8]
    dir_pdf  = dir_main
    lb_pad   = 0.100
    (fig_width, fig_height, n_row, n_col) = (9.00, 2.90, 1, 3)
    (fig_left, fig_bottom, fig_right, fig_top, fig_wspace, fig_hspace) = (0.050, 0.025, 0.985, 0.950, 0.200, 0.250)
if draw_scheme == 2:
    cases    = ['20210821_CON6h_DS1h_UV', '20210821_CON6h_DS1h_T', '20210821_CON6h_DS1h_Q']
    dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021'
    dir_main = dir_CPEX + '/increment/' + cases[0][0:8]
    dir_pdf  = dir_main
    lb_pad   = 0.100
    (fig_width, fig_height, n_row, n_col) = (9.00, 2.90, 1, 3)
    (fig_left, fig_bottom, fig_right, fig_top, fig_wspace, fig_hspace) = (0.050, 0.025, 0.985, 0.950, 0.200, 0.250)
if draw_scheme == 3:
    cases = ['20210824_CON6h_DS1h_Q_Hybrid_082500']
    dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021'
    dir_main = dir_CPEX + '/increment/' + cases[0][0:8]
    dir_pdf  = dir_main
    lb_pad   = 0.100
    (fig_width, fig_height, n_row, n_col) = (9.00, 2.90, 1, 3)
    (fig_left, fig_bottom, fig_right, fig_top, fig_wspace, fig_hspace) = (0.050, 0.025, 0.985, 0.950, 0.200, 0.250)
if draw_scheme == 4:
    cases    = ['20210828_CON6h_DS1h_UV', '20210828_CON6h_DS1h_T', '20210828_CON6h_DS1h_Q']
    dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021'
    dir_main = dir_CPEX + '/increment/' + cases[0][0:8]
    dir_pdf  = dir_main
    lb_pad   = 0.100
    (fig_width, fig_height, n_row, n_col) = (9.00, 2.90, 1, 3)
    (fig_left, fig_bottom, fig_right, fig_top, fig_wspace, fig_hspace) = (0.050, 0.025, 0.985, 0.950, 0.200, 0.250)
if draw_scheme == 5:
    cases    = ['20210904_2021090412_CON6h_DAWN1h']
    dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021'
    dir_main = dir_CPEX + '/increment/' + cases[0][0:8]
    dir_pdf  = dir_main
    lb_pad   = 0.100
    (fig_width, fig_height, n_row, n_col) = (9.00, 2.90, 1, 3)
    (fig_left, fig_bottom, fig_right, fig_top, fig_wspace, fig_hspace) = (0.050, 0.025, 0.985, 0.950, 0.200, 0.250)

if '20210820' in cases[0]:
    anl_start_time = datetime.datetime(2021, 8, 20, 18, 0, 0)
    anl_end_time   = datetime.datetime(2021, 8, 21,  0, 0, 0)
    lon_limit = {'d01': [-89.9017, -45.0983], \
                 'd02': [-84.4232, -52.1528]}
    lat_limit = {'d01': [-0.603058, 32.2223], \
                 'd02': [  4.19621, 29.0591]}
if '20210821' in cases[0]:
    anl_start_time = datetime.datetime(2021, 8, 21, 18, 0, 0)
    anl_end_time   = datetime.datetime(2021, 8, 22,  0, 0, 0)
    lon_limit = {'d01': [-72.0007, -27.9993], \
                 'd02': [-66.6203, -34.9275]}
    lat_limit = {'d01': [-4.42091, 28.3878], \
                 'd02': [0.291763, 25.1641]}
if '20210824' in cases[0]:
    anl_start_time = datetime.datetime(2021, 8, 24, 18, 0, 0)
    anl_end_time   = datetime.datetime(2021, 8, 25,  0, 0, 0)
    lon_limit = {'d01': [-97.5707, -46.4293], \
                 'd02': [-92.0152, -53.5830]}
    lat_limit = {'d01': [ 1.77797, 34.6167], \
                 'd02': [ 6.63398, 31.4919]}
if '20210828' in cases[0]:
    anl_start_time = datetime.datetime(2021, 8, 28, 18, 0, 0)
    anl_end_time   = datetime.datetime(2021, 8, 29,  0, 0, 0)
    lon_limit = {'d01': [-77.9314, -32.0686], \
                 'd02': [-72.3234, -39.2899]}
    lat_limit = {'d01': [3.20438, 36.0523], \
                 'd02': [8.09558, 32.9509]}
if '20210904' in cases[0]:
    anl_start_time = datetime.datetime(2021, 9,  4, 18, 0, 0)
    anl_end_time   = datetime.datetime(2021, 9,  5,  0, 0, 0)
    lon_limit = {'d01': [-72.5215, -27.4785], \
                 'd02': [-67.0138, -34.5707]}
    lat_limit = {'d01': [0.349884, 33.1803], \
                 'd02': [ 5.17158, 30.0324]}

status = ['bkg', 'anl', 'anl-bkg']
domains = ['d01']

cycling_interval = 1
analysis_time  = anl_end_time - anl_start_time
analysis_hours = analysis_time.days*24.0 + analysis_time.seconds/3600.0
n_time = int(analysis_hours/cycling_interval) + 1

def set_parameters(var):

    levels = {}

    if 'ua' in var:
        lb_title = 'ua (m/s)'
        factor   = 1.0
        levels.update({925: [-18.0, 20.0, 4.0, 'RdBu_r', -7.0, 8.0, 2.0, 'RdBu_r']})
        levels.update({850: [-18.0, 20.0, 4.0, 'RdBu_r', -7.0, 8.0, 2.0, 'RdBu_r']})
        levels.update({700: [-22.5, 25.0, 5.0, 'RdBu_r', -7.0, 8.0, 2.0, 'RdBu_r']})
        levels.update({500: [-22.5, 25.0, 5.0, 'RdBu_r', -7.0, 8.0, 2.0, 'RdBu_r']})
        levels.update({300: [-36.0, 40.0, 8.0, 'RdBu_r', -7.0, 8.0, 2.0, 'RdBu_r']})
        levels.update({200: [-36.0, 40.0, 8.0, 'RdBu_r', -7.0, 8.0, 2.0, 'RdBu_r']})
    elif 'va' in var:
        lb_title = 'va (m/s)'
        factor   = 1.0
        levels.update({925: [-18.0, 20.0, 4.0, 'RdBu_r', -7.0, 8.0, 2.0, 'RdBu_r']})
        levels.update({850: [-18.0, 20.0, 4.0, 'RdBu_r', -7.0, 8.0, 2.0, 'RdBu_r']})
        levels.update({700: [-13.5, 15.0, 3.0, 'RdBu_r', -7.0, 8.0, 2.0, 'RdBu_r']})
        levels.update({500: [-13.5, 15.0, 3.0, 'RdBu_r', -7.0, 8.0, 2.0, 'RdBu_r']})
        levels.update({300: [-18.0, 20.0, 4.0, 'RdBu_r', -7.0, 8.0, 2.0, 'RdBu_r']})
        levels.update({200: [-18.0, 20.0, 4.0, 'RdBu_r', -7.0, 8.0, 2.0, 'RdBu_r']})
    elif 'temp' in var:
        lb_title = 'T (K)'
        factor   = 1.0
        levels.update({925: [285, 305, 2.0, 'rainbow', -1.4, 1.6, 0.4, 'RdBu_r']})
        levels.update({850: [280, 300, 2.0, 'rainbow', -1.4, 1.6, 0.4, 'RdBu_r']})
        levels.update({700: [275, 290, 1.5, 'rainbow', -1.4, 1.6, 0.4, 'RdBu_r']})
        levels.update({500: [260, 270, 1.0, 'rainbow', -1.4, 1.6, 0.4, 'RdBu_r']})
        levels.update({300: [230, 250, 2.0, 'rainbow', -1.4, 1.6, 0.4, 'RdBu_r']})
        levels.update({200: [210, 225, 1.5, 'rainbow', -1.4, 1.6, 0.4, 'RdBu_r']})
    elif 'QVAPOR' in var:
        lb_title = 'QVAPOR ' + '($\mathregular{gkg^{-1}}$)'
        factor   = 1000.0
        levels.update({925: [0.0, 20.0, 2.00, 'YlGn', -1.4, 1.6, 0.4, 'BrBG']})
        levels.update({850: [0.0, 15.0, 1.50, 'YlGn', -1.4, 1.6, 0.4, 'BrBG']})
        levels.update({700: [0.0, 10.0, 1.00, 'YlGn', -1.4, 1.6, 0.4, 'BrBG']})
        levels.update({500: [0.0, 5.00, 0.50, 'YlGn', -1.4, 1.6, 0.4, 'BrBG']})
        levels.update({300: [0.0, 1.00, 0.10, 'YlGn', -1.4, 1.6, 0.4, 'BrBG']})
        levels.update({200: [0.0, 0.10, 0.01, 'YlGn', -1.4, 1.6, 0.4, 'BrBG']})

    return [lb_title, factor, levels]
