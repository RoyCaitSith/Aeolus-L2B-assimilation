import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import re
import sys
import time
import shutil
import datetime
import numpy as np
from wrf import getvar, interplevel, latlon_coords
from netCDF4 import Dataset

time = '20210824'

#case = 'CON6h_Hybrid_082500'
#case = 'CON6h_DS1h_Hybrid_082500'
#case = 'CON6h_DS1h_UV_Hybrid_082500'
#case = 'CON6h_DS1h_T_Hybrid_082500'
#case = 'CON6h_DS1h_Q_Hybrid_082500'
#case = 'CON6h_Aeolus6h_Hybrid_082500'
#case = 'CON6h_Aeolus6h_L2B_Hybrid_082500'
#case = 'CON6h_Hybrid_082512'
#case = 'CON6h_DS1h_Hybrid_082512'
#case = 'CON6h_DS1h_UV_Hybrid_082512'
#case = 'CON6h_DS1h_T_Hybrid_082512'
#case = 'CON6h_DS1h_Q_Hybrid_082512'
#case = 'CON6h_Aeolus6h_Hybrid_082512'
case = 'CON6h_Aeolus6h_L2B_Hybrid_082512'

dir_exp = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021'
dir_in  = dir_exp + '/bkg/' + time + '/' + case
dir_out = dir_exp + '/track_intensity/' + time + '/' + case

cycling_interval = 6
domain = 'd01'

if '20210824' in time:
    forecast_time_str = datetime.datetime(2021, 8, 24,  6, 0, 0)
    forecast_time_end = datetime.datetime(2021, 8, 28, 12, 0, 0)
    #forecast_time_str = datetime.datetime(2021, 8, 24,  6, 0, 0)
    #forecast_time_end = datetime.datetime(2021, 8, 27, 12, 0, 0)
if '20210828' in time:
    forecast_time_str = datetime.datetime(2021, 8, 28, 12, 0, 0)
    forecast_time_end = datetime.datetime(2021, 8, 31,  0, 0, 0)
if '20210904' in time:
    #forecast_time_str = datetime.datetime(2021, 9,  3, 18, 0, 0)
    #forecast_time_end = datetime.datetime(2021, 9,  7,  0, 0, 0)
    forecast_time_str = datetime.datetime(2021, 9,  4, 12, 0, 0)
    forecast_time_end = datetime.datetime(2021, 9,  7, 18, 0, 0)

os.system('mkdir ' + dir_out)
dir_out = dir_out + '/wrfprd'
os.system('mkdir ' + dir_out)

time_str = forecast_time_str.strftime('%Y-%m-%d_%H:00:00')
print('time start: ', time_str)
forecast_time_now = forecast_time_str
while forecast_time_now <= forecast_time_end:

    print('Copy the wrfout files to wrfprd at ', forecast_time_now)
    time        = forecast_time_now.strftime('%Y%m%d%H')
    wrfout_time = forecast_time_now.strftime('%Y-%m-%d_%H:00:00')
    wrfout_name = 'wrfout_' + domain + '_' + wrfout_time
    wrfout      = dir_in + '/' + wrfout_name
    os.system('cp ' + wrfout + ' ' + dir_out)

    wrfout_read = Dataset(dir_out + '/' + wrfout_name, 'r+')
    wrfout_read.START_DATE = time_str
    wrfout_read.SIMULATION_START_DATE = time_str

    forecast_time_now = forecast_time_now + datetime.timedelta(hours = cycling_interval)
