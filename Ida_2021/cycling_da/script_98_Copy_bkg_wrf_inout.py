import os
import re
import time
import datetime
from subroutine import file_operations as fo

#case = 'CON6h_082406_Hybrid_C08'
#case = 'CON6h_082412_Hybrid_C08'
#case = 'CON6h_082418_Hybrid_C08'
#case = 'CON6h_082500_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082406_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082412_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082418_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082500_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082500_H1_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082500_H2_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082500_V1_Hybrid_C08'
case = 'CON6h_Aeolus6h_082500_V2_Hybrid_C08'

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN'
dir_exp  = dir_CPEX + '/15_ENS/cycling_da'
dir_bkg  = dir_exp + '/Data/' + case + '/bkg'
dir_da   = dir_exp + '/Data/' + case + '/da'

#initial_time   = datetime.datetime(2021, 8, 24,  6, 0, 0)
#anl_start_time = datetime.datetime(2021, 8, 24, 12, 0, 0)
#initial_time   = datetime.datetime(2021, 8, 24, 12, 0, 0)
#anl_start_time = datetime.datetime(2021, 8, 24, 18, 0, 0)
#initial_time   = datetime.datetime(2021, 8, 24, 18, 0, 0)
#anl_start_time = datetime.datetime(2021, 8, 25,  0, 0, 0)
initial_time   = datetime.datetime(2021, 8, 25,  0, 0, 0)
anl_start_time = datetime.datetime(2021, 8, 25,  6, 0, 0)

domains = ['d01', 'd02']
cycling_interval = 6.0
max_dom = len(domains)
n_cycle = int(case[-2:])-1

for idc in range(0, n_cycle):

    dir_cycle = dir_exp + '/Data/' + case[0:len(case)-2] + str(idc+1).zfill(2)
    dir_bkg_out = dir_cycle + '/bkg'
    dir_da_out = dir_cycle + '/da'
    os.system('mkdir ' + dir_cycle)
    os.system('mkdir ' + dir_bkg_out)
    os.system('mkdir ' + dir_da_out)

    #Copy bkg files
    ctime = initial_time
    anl_end_time = anl_start_time + datetime.timedelta(hours=6.0*idc)
    while ctime <= anl_end_time:
        for dom in domains:
            wrfout_at_dir_bkg = dir_bkg + '/wrfout_' + dom + '_' + ctime.strftime('%Y-%m-%d_%H:%M:00')
            wrfout_at_dir_bkg_out = dir_bkg_out + '/wrfout_' + dom + '_' + ctime.strftime('%Y-%m-%d_%H:%M:00')
            os.system('cp ' + wrfout_at_dir_bkg + ' ' + wrfout_at_dir_bkg_out)
            print(wrfout_at_dir_bkg_out)
        ctime = ctime + datetime.timedelta(hours = cycling_interval)

    #Copy da files
    ctime = anl_start_time
    anl_end_time = anl_start_time + datetime.timedelta(hours=6.0*idc)
    while ctime <= anl_end_time:
        for dom in domains:
            wrfout_at_dir_da = dir_da + '/wrf_inout.' + ctime.strftime('%Y%m%d%H') + '.' + dom
            wrfout_at_dir_da_out = dir_da_out + '/wrf_inout.' + ctime.strftime('%Y%m%d%H') + '.' + dom
            os.system('cp ' + wrfout_at_dir_da + ' ' + wrfout_at_dir_da_out)
            print(wrfout_at_dir_da_out)
        ctime = ctime + datetime.timedelta(hours = cycling_interval)
