from netCDF4 import Dataset

wrfrsts = ['wrfrst_d01_2021-08-20_18:00:00', 'wrfrst_d02_2021-08-20_18:00:00']

for wrfrst in wrfrsts:

    wrfrst_read = Dataset('./' + wrfrst, 'r+')
    wrfrst_read.WRF_ALARM_SECS_TIL_NEXT_RING_01 = '3600'
    wrfrst_read.close()
