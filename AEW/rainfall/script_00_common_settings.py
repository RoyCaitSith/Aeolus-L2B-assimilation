import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import re
import datetime
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from matplotlib import ticker
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.basemap import Basemap

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021'
dir_main = dir_CPEX + '/rainfall'

draw_scheme = 4

if draw_scheme == 1:
    time = '20210820'
    cases = ['CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', \
             'CON6h_DAWN1hOE1p5', 'CON6h_HALO1h', 'CON6h_HALO1hOE0p2', \
             'CON6h_DS1h', 'CON6h_Aeolus6h', 'CON6h_DAWN1h_HALO1h_DS1h']
    dir_pdf = dir_main + '/' + time + '/figures_OE'
    wrfout = '2021-08-20_18:00:00'
    (fig_width, fig_height, n_row, n_col) = (9.00, 7.50, 3, 3)
    (fig_left, fig_bottom, fig_right, fig_top, fig_wspace, fig_hspace) = (0.075, -0.050, 0.985, 0.925, 0.200, 0.200)
    lb_pad = 0.050
if draw_scheme == 2:
    time = '20210821'
    cases = ['CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', \
             'CON6h_DAWN1hOE1p5', 'CON6h_HALO1h', 'CON6h_DS1h', \
             'CON6h_Aeolus6h', 'CON6h_DAWN1h_HALO1h_DS1h', 'CON6h_DAWN1h_HALO1h_DS1h_Aeolus6h']
    dir_pdf = dir_main + '/' + time + '/figures_OE'
    wrfout = '2021-08-21_18:00:00'
    (fig_width, fig_height, n_row, n_col) = (9.00, 7.50, 3, 3)
    (fig_left, fig_bottom, fig_right, fig_top, fig_wspace, fig_hspace) = (0.075, -0.050, 0.985, 0.925, 0.200, 0.200)
    lb_pad = 0.050
if draw_scheme == 3:
    time = '20210828'
    cases = ['CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', \
             'CON6h_DAWN1hOE1p5', 'CON6h_HALO1h', 'CON6h_HALO1hOE0p2', \
             'CON6h_DS1h', 'CON6h_Aeolus6h', 'CON6h_DAWN1h_HALO1h_DS1h']
    dir_pdf = dir_main + '/' + time + '/figures_OE'
    wrfout = '2021-08-28_18:00:00'
    (fig_width, fig_height, n_row, n_col) = (9.00, 7.50, 3, 3)
    (fig_left, fig_bottom, fig_right, fig_top, fig_wspace, fig_hspace) = (0.075, -0.050, 0.985, 0.925, 0.200, 0.200)
    lb_pad = 0.050
if draw_scheme == 4:
    time = '20210904'
    cases = ['CON6h', 'CON6h_DAWN1h', 'CON6h_DAWN1hOE1', \
             'CON6h_DAWN1hOE1p5', 'CON6h_HALO1h', 'CON6h_HALO1hOE0p2', \
             'CON6h_DS1h', 'CON6h_Aeolus6h', 'CON6h_DAWN1h_HALO1h_DS1h']
    dir_pdf = dir_main + '/' + time + '/figures_OE'
    wrfout = '2021-09-04_18:00:00'
    (fig_width, fig_height, n_row, n_col) = (9.00, 7.50, 3, 3)
    (fig_left, fig_bottom, fig_right, fig_top, fig_wspace, fig_hspace) = (0.075, -0.050, 0.985, 0.925, 0.200, 0.200)
    lb_pad = 0.050

if '20210820' in time:
    forecast_start_time = datetime.datetime(2021, 8, 21,  0, 0, 0)
    forecast_end_time   = datetime.datetime(2021, 8, 22,  0, 0, 0)
    n_time = 5
if '20210821' in time:
    forecast_start_time = datetime.datetime(2021, 8, 22,  0, 0, 0)
    forecast_end_time   = datetime.datetime(2021, 8, 23,  0, 0, 0)
    n_time = 5
if '20210828' in time:
    forecast_start_time = datetime.datetime(2021, 8, 29,  0, 0, 0)
    forecast_end_time   = datetime.datetime(2021, 8, 31,  0, 0, 0)
    n_time = 9
if '20210904' in time:
    forecast_start_time = datetime.datetime(2021, 9,  5,  0, 0, 0)
    forecast_end_time   = datetime.datetime(2021, 9,  7,  0, 0, 0)
    n_time = 9

domains = ['d01', 'd02']
cycling_interval = 6

rain_levels = [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.6, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, \
               6.0, 8.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0]
rain_labels = ['0.1', '0.15', '0.2', '0.25', '0.3', '0.4', '0.6', '1.0', '1.5', \
               '2', '3', '4', '5', '6', '8', '10', '15', '20', '25', '30', '35', '40']
