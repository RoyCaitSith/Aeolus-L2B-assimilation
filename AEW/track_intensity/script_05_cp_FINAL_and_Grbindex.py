from __future__ import print_function
import os, sys
import shutil
import string
import numpy as np

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

files_exp  = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021/track_intensity/' + time + '/' + case

if '20210824' in time:
    files_hwrf = files_exp + '/multi/hwrf.18x18.AL092021.2021082406.f'
    n_time     = 18
if '20210828' in time:
    files_hwrf = files_exp + '/multi/hwrf.18x18.AL102021.2021082812.f'
    n_time     = 11
if '20210904' in time:
    #files_hwrf = files_exp + '/multi/hwrf.18x18.AL122021.2021090318.f'
    files_hwrf = files_exp + '/multi/hwrf.18x18.AL122021.2021090412.f'
    n_time     = 14

files_dir = files_exp + '/postprd'
files_out = files_exp + '/multi'
dh        = 6
dtime     = 360
input_domain = 'd01'

for i in range(0, n_time, 1):

    input_file = files_dir + '/FINAL_' + input_domain + '.' + str(i*dh).zfill(2)
    out_file   = files_dir + '/FINAL.' + str(i*dh).zfill(2)
    print(input_file)
    print(out_file)

    print('Simply copy ', input_file)
    os.system('cp ' + input_file + ' ' + out_file)

    flnm_hwrf = files_hwrf + str(i*dtime).zfill(5)
    flnm_hwrf_ix = flnm_hwrf + '.ix'
    shutil.copyfile(out_file, flnm_hwrf)
    os.system(files_out + '/grbindex.exe ' + flnm_hwrf + ' ' + flnm_hwrf_ix)
