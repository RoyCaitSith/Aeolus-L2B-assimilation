import os
import time
import datetime

dir_main = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/14_ENS_20210824/Aeolus/create_bufr'
dir_bufr = dir_main + '/bufr'
dir_bufr_temp = dir_main + '/bufr_temp'
dir_fortran = dir_main + '/fortran_files'

anl_start_time = datetime.datetime(2021, 8, 23,  0, 0, 0, tzinfo = datetime.timezone.utc)
anl_end_time   = datetime.datetime(2021, 8, 29,  0, 0, 0, tzinfo = datetime.timezone.utc)
time_interval  = 6

time_now = anl_start_time
while time_now <= anl_end_time:

    YYYYMMDD  = time_now.strftime('%Y%m%d')
    HH        = time_now.strftime('%H')
    MM        = time_now.strftime('%M')
    file_bufr = dir_bufr + '/' + YYYYMMDD + '/gdas.t' + HH + 'z.aeolus.tm00.bufr_d'
    print(file_bufr)

    fortran_bufr = dir_fortran + '/gdas.aeolus.bufr'
    os.system('rm -rf ' + fortran_bufr)

    print('Check bufr_temp: ')
    flag = True
    info = os.popen('cd ' + dir_bufr_temp + '/' + YYYYMMDD + HH + ' && ls ./*.txt').readlines()
    if len(info) != 52:
        flag = False
    print(len(info))
    print(flag)

    if flag:

        fdata = ''
        with open(dir_fortran + '/bufr_encode_L2B.f90', 'r') as f:
            for line in f.readlines():
                if(line.find('idate = ') == 4):
                    line = '    idate = ' + YYYYMMDD + HH + '\n'
                fdata += line
        f.close()

        with open(dir_fortran + '/bufr_encode_L2B.f90', 'w') as f:
            f.writelines(fdata)
        f.close()

        os.popen('cd ' + dir_fortran + ' && ./run_encode_L2B.sh > log_out')
        flag      = True
        file_size = 0
        while flag:
            time.sleep(5)
            file_size_temp = os.popen("stat -c '%s' " + fortran_bufr).read()
            if file_size_temp:
                file_size_next = int(file_size_temp)
                if file_size_next == file_size:
                    flag = False
                else:
                    file_size = file_size_next
            print(file_size)

        os.system('mv ' + fortran_bufr + ' ' + file_bufr)

    time_now  = time_now + datetime.timedelta(hours = time_interval)
