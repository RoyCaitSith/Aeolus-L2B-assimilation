import os
import re
import sys
import time
import shutil
import datetime
import numpy as np
from wrf import getvar, interplevel, latlon_coords
from netCDF4 import Dataset

#case = 'CON6h_082406_Hybrid_C08'
#case = 'CON6h_082412_Hybrid_C08'
#case = 'CON6h_082418_Hybrid_C08'
#case = 'CON6h_082500_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082406_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082412_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082418_Hybrid_C08'
case = 'CON6h_Aeolus6h_082500_Hybrid_C05'

dir_exp = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS'
dir_in  = dir_exp + '/cycling_da/Data/' + case + '/bkg'
dir_out = dir_exp + '/track_intensity/' + case
print(dir_in)
print(dir_out)

cycling_interval = 6
domain = 'd01'

#forecast_time_str = datetime.datetime(2021, 8, 24,  6, 0, 0)
#forecast_time_end = datetime.datetime(2021, 8, 28, 12, 0, 0)
#forecast_time_str = datetime.datetime(2021, 8, 24, 12, 0, 0)
#forecast_time_end = datetime.datetime(2021, 8, 28, 18, 0, 0)
#forecast_time_str = datetime.datetime(2021, 8, 24, 18, 0, 0)
#forecast_time_end = datetime.datetime(2021, 8, 29,  0, 0, 0)
forecast_time_str = datetime.datetime(2021, 8, 25,  0, 0, 0)
forecast_time_end = datetime.datetime(2021, 8, 28, 12, 0, 0)

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
