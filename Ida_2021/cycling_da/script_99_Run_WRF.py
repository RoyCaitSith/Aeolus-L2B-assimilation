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
case = 'CON6h_Aeolus6h_082500_Hybrid_C08'

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN'
dir_exp    = dir_CPEX + '/15_ENS/cycling_da'

dir_main   = dir_exp + '/' + case
dir_bkg    = dir_exp + '/Data/' + case + '/bkg'
dir_option = dir_exp + '/Data/' + case + '/option'
dir_da     = dir_exp + '/Data/' + case + '/da'
dir_case   = '/scratch/general/lustre/u1237353/' + case
print(dir_case)

#initial_time   = datetime.datetime(2021, 8, 24,  6, 0, 0)
#anl_start_time = datetime.datetime(2021, 8, 24, 12, 0, 0)
#anl_end_time   = datetime.datetime(2021, 8, 24, 12, 0, 0)
#initial_time   = datetime.datetime(2021, 8, 24, 12, 0, 0)
#anl_start_time = datetime.datetime(2021, 8, 24, 18, 0, 0)
#anl_end_time   = datetime.datetime(2021, 8, 24, 18, 0, 0)
#initial_time   = datetime.datetime(2021, 8, 24, 18, 0, 0)
#anl_start_time = datetime.datetime(2021, 8, 25,  0, 0, 0)
#anl_end_time   = datetime.datetime(2021, 8, 25,  0, 0, 0)
initial_time   = datetime.datetime(2021, 8, 25,  0, 0, 0)
anl_start_time = datetime.datetime(2021, 8, 25,  6, 0, 0)
anl_end_time   = datetime.datetime(2021, 8, 25,  6, 0, 0)
anl_end_time = anl_start_time + datetime.timedelta(hours=6.0*(int(case[-2:])-1))

forecast_hours = 48
history_interval = 360
domains = ['d01', 'd02']
wps_interval = 6
max_dom = len(domains)
forecast_hours = forecast_hours + wps_interval
cycling_interval = forecast_hours

time_last        = anl_end_time
time_now         = anl_end_time + datetime.timedelta(hours=cycling_interval)
initial_time_str = initial_time.strftime('%Y%m%d%H')
time_last_str    = time_last.strftime('%Y%m%d%H')
time_now_str     = time_now.strftime('%Y%m%d%H')

wrf_inout = dir_da + '/wrf_inout.' + time_last_str + '.d01'
print('Check wrfinput file for ', wrf_inout)
wrf_inout_flag = os.path.exists(wrf_inout)

if wrf_inout_flag:

    #Run WRF
    print('Check wrfout at ', dir_case + '/' + initial_time_str)
    print('Check wrfout at ', dir_bkg)

    wrfout_exist = True
    ctime = time_last
    while ctime <= time_now:
        for dom in domains:
            wrfout_at_dir_case = dir_case + '/' + initial_time_str + '/wrfout_' + dom + '_' + ctime.strftime('%Y-%m-%d_%H:%M:00')
            wrfout_at_dir_bkg  = dir_bkg + '/wrfout_' + dom + '_' + ctime.strftime('%Y-%m-%d_%H:%M:00')
            if (not os.path.exists(wrfout_at_dir_case)) and (not os.path.exists(wrfout_at_dir_bkg)):
                wrfout_exist = False
        ctime = ctime + datetime.timedelta(hours = history_interval/60)

    if not wrfout_exist:

        namelist_input_dir = dir_case + '/Run_WRF/namelist.input'
        namelist_input = fo.change_content(namelist_input_dir)

        #Time_Control
        namelist_input.substitude_string('max_dom', ' = ', str(max_dom))
        namelist_input.substitude_string('run_days',  ' = ', str(cycling_interval//24) + ',')
        namelist_input.substitude_string('run_hours', ' = ', str(cycling_interval%24) + ',')
        namelist_input.substitude_string('input_from_file', ' = ', '.true., ' * max_dom)

        YYYY_str = time_last.strftime('%Y') + ', '
        MM_str   = time_last.strftime('%m') + ', '
        DD_str   = time_last.strftime('%d') + ', '
        HH_str   = time_last.strftime('%H') + ', '
        YYYY_str = YYYY_str * max_dom
        MM_str   = MM_str * max_dom
        DD_str   = DD_str * max_dom
        HH_str   = HH_str * max_dom
        namelist_input.substitude_string('start_year', ' = ', YYYY_str)
        namelist_input.substitude_string('start_month', ' = ', MM_str)
        namelist_input.substitude_string('start_day', ' = ', DD_str)
        namelist_input.substitude_string('start_hour', ' = ', HH_str)

        YYYY_str = time_now.strftime('%Y') + ', '
        MM_str   = time_now.strftime('%m') + ', '
        DD_str   = time_now.strftime('%d') + ', '
        HH_str   = time_now.strftime('%H') + ', '
        YYYY_str = YYYY_str * max_dom
        MM_str   = MM_str * max_dom
        DD_str   = DD_str * max_dom
        HH_str   = HH_str * max_dom
        namelist_input.substitude_string('end_year', ' = ', YYYY_str)
        namelist_input.substitude_string('end_month', ' = ', MM_str)
        namelist_input.substitude_string('end_day', ' = ', DD_str)
        namelist_input.substitude_string('end_hour', ' = ', HH_str)

        history_interval_str = str(history_interval) + ', '
        history_interval_str = history_interval_str * max_dom
        namelist_input.substitude_string('history_interval', ' = ', history_interval_str)
        namelist_input.save_content()

        print('Copy wrfinput')
        for dom in domains:
            wrf_inout = dir_da + '/wrf_inout.' + time_last_str + '.' + dom
            print(wrf_inout)
            os.system('cp ' + wrf_inout + ' ' + dir_case + '/Run_WRF/wrfinput_' + dom)

        #run wrf to get the forecast
        info = os.popen('cd ' + dir_case + '/Run_WRF && sbatch run_wrf.sh').read()
        jobid = re.findall(r"\d+\.?\d*", info)
        print('Run wrf from ', time_last, ' to ', time_now, ', jobid: ', jobid)
        flag = True
        while flag:
            time.sleep(30)
            flag = False
            info = os.popen('squeue -u u1237353').read()
            number_in_info = re.findall(r"\d+\.?\d*", info)
            for num in number_in_info:
                if num == jobid[0]:
                    flag = True

        print('Finish running wrf from ', time_last, ' to ', time_now)

    #move the forecast files to the bkg folder
    print('move the forecast files to the bkg folder at ', time_now)
    ctime = time_last
    while ctime <= time_now:
        for dom in domains:
            wrfout_at_dir_case = dir_case + '/' + initial_time_str + '/wrfout_' + dom + '_' + ctime.strftime('%Y-%m-%d_%H:%M:00')
            wrfout_at_dir_bkg  = dir_bkg + '/wrfout_' + dom + '_' + ctime.strftime('%Y-%m-%d_%H:%M:00')
            if os.path.exists(wrfout_at_dir_case) and not os.path.exists(wrfout_at_dir_bkg):
                os.system('mv ' + wrfout_at_dir_case + ' ' + wrfout_at_dir_bkg)
                print(wrfout_at_dir_case)
        ctime = ctime + datetime.timedelta(hours = history_interval/60)

    print('remove wrfout files at initial time')
    ctime = time_last
    for dom in domains:
        wrfout_at_dir_case = dir_case + '/' + initial_time_str + '/wrfout_' + dom + '_' + ctime.strftime('%Y-%m-%d_%H:%M:00')
        if os.path.exists(wrfout_at_dir_case):
            os.system('rm -rf ' + wrfout_at_dir_case)
