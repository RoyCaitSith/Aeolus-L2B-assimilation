import os
import datetime

dir_case = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021/bkg/20210904'
cases = ['CON6h_DAWN1h_HALO1h_DS1h', 'CON6h_DAWN1h_HALO1h_DS1h_Aeolus6h']
forecast_time  = datetime.datetime(2021, 9,  5,  0, 0, 0)

for case in cases:

    save_dir = dir_case + '/' + case

    info = os.popen('cd ' + save_dir + ' & ls ' + save_dir).read()
    for wrfout in info.split('\n'):
        if wrfout != '':

            YY = int(wrfout[11:15])
            mm = int(wrfout[16:18])
            dd = int(wrfout[19:21])
            HH = int(wrfout[22:24])
            MM = int(wrfout[25:27])
            ss = int(wrfout[28:30])

            time_now = datetime.datetime(YY, mm, dd, HH, MM, ss)
            time_dif = time_now - forecast_time
            del_hour = time_dif.total_seconds()

            index = del_hour%21600

            if index != 0.0:
                os.system('rm -rf ' + save_dir + '/' + wrfout)
