from __future__ import print_function
import os, sys
import shutil
import string
import numpy as np

#case = 'CON6h_082406_Hybrid_C08'
#case = 'CON6h_082412_Hybrid_C08'
#case = 'CON6h_082418_Hybrid_C08'
#case = 'CON6h_082500_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082406_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082412_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082418_Hybrid_C08'
case = 'CON6h_Aeolus6h_082500_Hybrid_C08'

files_exp  = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS/track_intensity/' + case
#files_hwrf = files_exp + '/multi/hwrf.18x18.AL092021.2021082406.f'
#files_hwrf = files_exp + '/multi/hwrf.18x18.AL092021.2021082412.f'
#files_hwrf = files_exp + '/multi/hwrf.18x18.AL092021.2021082418.f'
files_hwrf = files_exp + '/multi/hwrf.18x18.AL092021.2021082500.f'
n_time     = 18

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
