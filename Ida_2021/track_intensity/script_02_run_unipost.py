import os
import re
import sys
import time
import shutil
import datetime
import numpy as np

#case = 'CON6h_082406_Hybrid_C08'
#case = 'CON6h_082412_Hybrid_C08'
#case = 'CON6h_082418_Hybrid_C08'
#case = 'CON6h_082500_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082406_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082412_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082418_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082500_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082500_H1_Hybrid_C05'
#case = 'CON6h_Aeolus6h_082500_H2_Hybrid_C05'
#case = 'CON6h_Aeolus6h_082500_V1_Hybrid_C05'
case = 'CON6h_Aeolus6h_082500_V2_Hybrid_C05'

dir_exp = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS/track_intensity'
folder_in  = dir_exp + '/CON6h_Aeolus6h_082500_Hybrid_C05'
folder_out = dir_exp + '/' + case

print('Create a folder: multi')
folder_multi_in  = folder_in  + '/multi'
folder_multi_out = folder_out + '/multi'
os.system('mkdir ' + folder_multi_out)

print('Copy the files from ', folder_multi_in, ' to ', folder_multi_out)
os.system('cp ' + folder_multi_in + '/fort.* ' + folder_multi_out)
os.system('cp ' + folder_multi_in + '/gettrk.exe ' + folder_multi_out)
os.system('cp ' + folder_multi_in + '/grbindex.exe ' + folder_multi_out)
os.system('cp ' + folder_multi_in + '/input.nml ' + folder_multi_out)
os.system('cp ' + folder_multi_in + '/tcvit_rsmc_storms.txt ' + folder_multi_out)

print('Create a folder: parm')
folder_parm_in  = folder_in  + '/parm'
folder_parm_out = folder_out + '/parm'
os.system('mkdir ' + folder_parm_out)

print('Copy the files from ', folder_parm_in, ' to ', folder_parm_out)
os.system('cp ' + folder_parm_in + '/wrf_cntrl.parm ' + folder_parm_out)

print('Create a folder: postprd')
folder_postprd_in  = folder_in  + '/postprd'
folder_postprd_out = folder_out + '/postprd'
os.system('mkdir ' + folder_postprd_out)

print('Copy the files from ', folder_postprd_in, ' to ', folder_postprd_out)
os.system('cp ' + folder_postprd_in + '/run_unipost ' + folder_postprd_out)

print('Please revise fort.15 in ', folder_multi_out)
print('Please revise input.nml in ', folder_multi_out)
print('Please revise tcvit_rsmc_storms.txt in ', folder_multi_out)
print('Please revise run_unipost in ', folder_postprd_out)
print('Please run run_unipost!')
