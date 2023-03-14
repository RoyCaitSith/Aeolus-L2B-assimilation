import os
import re
import time
import datetime
from subroutine import file_operations as fo

#case = 'CON6h_082406_Hybrid_C08'
#case = 'CON6h_082412_Hybrid_C08'
#case = 'CON6h_082418_Hybrid_C08'
#case = 'CON6h_082418_H1_Hybrid_C08'
#case = 'CON6h_082418_H2_Hybrid_C08'
#case = 'CON6h_082418_V1_Hybrid_C08'
#case = 'CON6h_082418_V2_Hybrid_C08'
#case = 'CON6h_082500_Hybrid_C08'
#case = 'CON6h_082500_H1_Hybrid_C08'
#case = 'CON6h_082500_H2_Hybrid_C08'
#case = 'CON6h_082500_V1_Hybrid_C08'
#case = 'CON6h_082500_V2_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082406_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082412_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082418_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082418_H1_Hybrid_C08'
case = 'CON6h_Aeolus6h_082418_H2_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082418_V1_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082418_V2_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082500_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082500_H1_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082500_H2_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082500_V1_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082500_V2_Hybrid_C08'

dir_GOES   = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_CPEX   = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS'
dir_exp    = dir_CPEX + '/cycling_da'
dir_ens    = dir_GOES + '/Data/ensemble'
dir_prep   = dir_GOES + '/Data/prepbufr'
dir_obs    = dir_CPEX + '/Aeolus/create_bufr/bufr'
dir_main   = dir_exp + '/' + case
dir_bkg    = dir_exp + '/Data/' + case + '/bkg'
dir_option = dir_exp + '/Data/' + case + '/option'
dir_da     = dir_exp + '/Data/' + case + '/da'
dir_case   = '/scratch/general/lustre/u1237353/' + case

#initial_time   = datetime.datetime(2021, 8, 24,  6, 0, 0)
#anl_start_time = datetime.datetime(2021, 8, 24, 12, 0, 0)
#anl_end_time   = datetime.datetime(2021, 8, 24, 12, 0, 0)
#initial_time   = datetime.datetime(2021, 8, 24, 12, 0, 0)
#anl_start_time = datetime.datetime(2021, 8, 24, 18, 0, 0)
#anl_end_time   = datetime.datetime(2021, 8, 24, 18, 0, 0)
initial_time   = datetime.datetime(2021, 8, 24, 18, 0, 0)
anl_start_time = datetime.datetime(2021, 8, 25,  0, 0, 0)
anl_end_time   = datetime.datetime(2021, 8, 25,  0, 0, 0)
#initial_time   = datetime.datetime(2021, 8, 25,  0, 0, 0)
#anl_start_time = datetime.datetime(2021, 8, 25,  6, 0, 0)
#anl_end_time   = datetime.datetime(2021, 8, 25,  6, 0, 0)
anl_end_time   = anl_start_time + datetime.timedelta(hours=6.0*(int(case[-2:])-1))

n_ens = 80
cycling_interval = 6
history_interval = 360
domains = ['d01', 'd02']
wps_interval   = 6
max_dom = len(domains)

time_last = initial_time
time_now = anl_start_time
initial_time_str = initial_time.strftime('%Y%m%d%H')
time_last_str = time_last.strftime('%Y%m%d%H')
time_now_str = time_now.strftime('%Y%m%d%H')

print(dir_main)
os.system('mkdir ' + dir_main)

while time_now <= anl_end_time:

    #Run GSI
    print('Run GSI at: ', time_now_str)
    for dom in domains:

        print('Check wrfinput file for ', dom)

        wrf_inout = dir_da + '/wrf_inout.' + time_now_str + '.' + dom
        if not os.path.exists(wrf_inout):

            print('Copy satbias_out to satbias_out')
            diag_satbias = dir_da + "/satbias_out." + time_last_str + "." + dom
            os.system('cp ' + diag_satbias + ' ' + dir_option + '/comgsi_satbias_in')

            print('Copy satbias_pc.out to satbias_pc.out')
            diag_satbias = dir_da + "/satbias_pc.out." + time_last_str + "." + dom
            os.system('cp ' + diag_satbias + ' ' + dir_option + '/comgsi_satbias_pc_in')

            print(time_now_str)
            run_gsi_dir  = dir_main + '/' + time_now_str
            os.system('mkdir ' + run_gsi_dir)

            print('Create bkg folder, and copy wrfout to bkg')
            bkg_dir = run_gsi_dir + '/bkg'
            wrfout  = dir_bkg + '/wrfout_' + dom + '_' + time_now.strftime('%Y-%m-%d_%H:00:00')
            os.system('mkdir ' + bkg_dir)
            os.system('cp ' + wrfout + ' ' + bkg_dir)

            print('Create obs folder, and copy bufr to obs')
            obs_dir = run_gsi_dir + '/obs'
            os.system('mkdir ' + obs_dir)
            if 'CON' in case:
                bufr = dir_prep + '/' + time_now_str[0:8] + '/prepbufr.gdas.' + time_now.strftime('%Y%m%d') + '.t' + time_now.strftime('%H') + 'z.nr.48h'
                print(bufr)
                os.system('cp ' + bufr + ' ' + obs_dir + '/gdas.t' + time_now.strftime('%H') + 'z.prepbufr')

            if 'Aeolus' in case:
                bufr = dir_obs + '/' + time_now_str[0:8] + '/gdas.t' + time_now.strftime('%H') + 'z.aeolus.tm00.bufr_d'
                if os.path.exists(bufr):
                    print(bufr)
                    os.system('cp ' + bufr + ' ' + obs_dir)

            print('Create gfsens folder, and copy wrfout to gfsens')
            ens_time = time_last
            ens_time_str = ens_time.strftime('%Y%m%d%H')
            gfsens_dir = run_gsi_dir + '/gfsens'
            os.system('mkdir ' + gfsens_dir)
            for idens in range(n_ens):
                dir_gfsens = dir_ens + '/' + ens_time_str[0:8] + '/' + ens_time_str[8:10] + '/atmos/mem' + str(idens+1).zfill(3) + '/*'
                gfsens_dir = run_gsi_dir + '/gfsens/gdas.t' + ens_time_str[8:10] + 'z.atmf006s.mem' + str(idens+1).zfill(3)
                os.system('ln -sf ' + dir_gfsens + ' ' + gfsens_dir)
                if idens == 0:
                    print(dir_gfsens)
                    print(gfsens_dir)

            print('Copy, revise, and the script of running gsi at ', time_now_str)
            run_gsi_input = fo.change_content(dir_option + '/run_GSI.sh')
            run_gsi_input.substitude_string('ANAL_TIME', '=', time_now_str)
            run_gsi_input.substitude_string('DOMAIN_NAME', '=', dom)
            run_gsi_input.save_content()

            info = os.popen('grep "ENDING DATE-TIME" ' + run_gsi_dir + '/case_' + dom + '/stdout').readlines()
            if len(info) == 0:
                info = os.popen('cd ' + dir_option + ' && sbatch ./run_GSI.sh').read()
                jobid = re.findall(r"\d+\.?\d*", info)
                print('Run gsi for domain ', dom, ' at ', time_now_str, ', jobid: ', jobid)
                flag = True
                while flag:
                    time.sleep(30)
                    flag = False
                    info = os.popen('squeue -u u1237353').read()
                    number_in_info = re.findall(r"\d+\.?\d*", info)
                    for num in number_in_info:
                        if num == jobid[0]:
                            flag = True

            info = os.popen('grep "ENDING DATE-TIME" ' + run_gsi_dir + '/case_' + dom + '/stdout').readlines()
            if len(info) == 1:

                print('Finish running gsi at ', time_now_str, ' for ', dom)

                diag_ges    = dir_da + "/diag_conv_ges." + time_now_str + "." + dom
                results_ges = dir_da + "/results_conv_ges." + time_now_str + "." + dom
                f = open(dir_option + '/namelist.conv', 'w')
                f.write("&iosetup\n")
                f.write(" infilename='" + diag_ges + "',\n")
                f.write(" outfilename='" + results_ges + "',\n")
                f.write("/")
                f.close()

                print('Copy ges diag files')
                os.system('cp ' + dir_option + '/namelist.conv ' + dir_da)
                os.system('cp ' + dir_option + '/read_diag_conv.x ' + dir_da)
                os.system('cp ' + run_gsi_dir + '/case_' + dom + '/diag_conv_ges.* ' + diag_ges)

                print('Run read_diag_conv.x')
                os.system('cd ' + dir_da + ' && ./read_diag_conv.x')
                os.system('rm -rf ' + dir_da + '/namelist.conv')
                os.system('rm -rf ' + dir_da + '/read_diag_conv.x')

                diag_anl    = dir_da + "/diag_conv_anl." + time_now_str + "." + dom
                results_anl = dir_da + "/results_conv_anl." + time_now_str + "." + dom
                f = open(dir_option + '/namelist.conv', 'w')
                f.write("&iosetup\n")
                f.write(" infilename='" + diag_anl + "',\n")
                f.write(" outfilename='" + results_anl + "',\n")
                f.write("/")
                f.close()

                print('Copy anl diag files')
                os.system('cp ' + dir_option + '/namelist.conv ' + dir_da)
                os.system('cp ' + dir_option + '/read_diag_conv.x ' + dir_da)
                os.system('cp ' + run_gsi_dir + '/case_' + dom + '/diag_conv_anl.* ' + diag_anl)

                print('Run read_diag_conv.x')
                os.system('cd ' + dir_da + ' && ./read_diag_conv.x')
                os.system('rm -rf ' + dir_da + '/namelist.conv')
                os.system('rm -rf ' + dir_da + '/read_diag_conv.x')

                if 'Hybrid' in case:
                    print('Save ens_spread.grd')
                    ens_spread = dir_da + '/ens_spread_' + time_now_str + '_' + dom + '.grd'
                    os.system('cp ' + run_gsi_dir + '/case_' + dom + '/ens_spread.grd ' + ens_spread)

                print('Copy satbias_out')
                diag_satbias = dir_da + "/satbias_out." + time_now_str + "." + dom
                os.system('cp ' + run_gsi_dir + '/case_' + dom + '/satbias_out ' + diag_satbias)

                print('Copy satbias_pc.out')
                diag_satbias = dir_da + "/satbias_pc.out." + time_now_str + "." + dom
                os.system('cp ' + run_gsi_dir + '/case_' + dom + '/satbias_pc.out ' + diag_satbias)

                print('Save wrf_inout of domain ', dom)
                os.system('cp ' + run_gsi_dir + '/case_' + dom + '/wrf_inout ' + wrf_inout)

                print('Delete slurm...')
                os.system('rm -rf ' + dir_option + '/slurm*')

            else:

                print('GSI failed at ', time_now_str, ', exit!')
                print('Delete slurm...')
                os.system('rm -rf ' + dir_option + '/slurm*')
                os._exit(0)

    time_last = time_now
    time_now = time_now + datetime.timedelta(hours = cycling_interval)

    time_last_str = time_last.strftime('%Y%m%d%H')
    time_now_str  = time_now.strftime('%Y%m%d%H')

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

    if not wrfout_exist and time_last < anl_end_time:

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
