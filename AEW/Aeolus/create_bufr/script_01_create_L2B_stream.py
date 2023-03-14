import os
os.putenv('CODA_DEFINITION', './')

import coda
import datetime
import numpy as np

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021/Aeolus/create_bufr'
dir_bufr = dir_main + '/bufr_temp'
dir_aeolus = dir_GOES + '/Data/aeolus'

anl_start_time = datetime.datetime(2021, 8, 24,  0, 0, 0)
anl_end_time   = datetime.datetime(2021, 8, 26,  0, 0, 0)
time_interval  = 6
window_time    = 6
J2000 = datetime.datetime(2000, 1, 1, 0, 0, 0, tzinfo = datetime.timezone.utc)

filenames = os.popen('ls ' + dir_aeolus + '/*/*DBL').read().split()

time_now = anl_start_time
while time_now <= anl_end_time:

    time_now_str = time_now.strftime('%Y%m%d%H')
    time_now_s = time_now - datetime.timedelta(hours = window_time/2.0)
    time_now_e = time_now + datetime.timedelta(hours = window_time/2.0)
    new_flag = True
    print(time_now_str)

    for filename in filenames:

        date_s_str = filename.split('_')[-3][0:8] + filename.split('_')[-3][9:15]
        date_e_str = filename.split('_')[-2][0:8] + filename.split('_')[-2][9:15]
        date_s = datetime.datetime.strptime(date_s_str, '%Y%m%d%H%M%S')
        date_e = datetime.datetime.strptime(date_e_str, '%Y%m%d%H%M%S')

        if date_s <= time_now_e and date_e >= time_now_s:

            if new_flag == True:

                new_flag = False
                dir_out = dir_bufr + '/' + time_now_str
                os.system('rm -rf ' + dir_out)
                os.system('mkdir ' + dir_out)
                n_data_total = 0

            print(filename)
            product = coda.open(filename)

            mie_latitude_start = coda.fetch(product, 'mie_geolocation', -1, 'windresult_geolocation/latitude_start')
            mie_latitude_cog = coda.fetch(product, 'mie_geolocation', -1, 'windresult_geolocation/latitude_cog')
            mie_latitude_stop = coda.fetch(product, 'mie_geolocation', -1, 'windresult_geolocation/latitude_stop')
            mie_longitude_start = coda.fetch(product, 'mie_geolocation', -1, 'windresult_geolocation/longitude_start')
            mie_longitude_cog = coda.fetch(product, 'mie_geolocation', -1, 'windresult_geolocation/longitude_cog')
            mie_longitude_stop = coda.fetch(product, 'mie_geolocation', -1, 'windresult_geolocation/longitude_stop')
            mie_datetime_start = coda.fetch(product, 'mie_geolocation', -1, 'windresult_geolocation/datetime_start')
            mie_datetime_cog = coda.fetch(product, 'mie_geolocation', -1, 'windresult_geolocation/datetime_cog')
            mie_datetime_stop = coda.fetch(product, 'mie_geolocation', -1, 'windresult_geolocation/datetime_stop')
            mie_altitude_bottom = coda.fetch(product, 'mie_geolocation', -1, 'windresult_geolocation/altitude_bottom')
            mie_altitude_vcog = coda.fetch(product, 'mie_geolocation', -1, 'windresult_geolocation/altitude_vcog')
            mie_altitude_top = coda.fetch(product, 'mie_geolocation', -1, 'windresult_geolocation/altitude_top')
            mie_los_azimuth = coda.fetch(product, 'mie_geolocation', -1, 'windresult_geolocation/los_azimuth')
            mie_los_elevation_bottom = coda.fetch(product, 'mie_geolocation', -1, 'windresult_geolocation/los_elevation_bottom')
            mie_los_elevation_vcog = coda.fetch(product, 'mie_geolocation', -1, 'windresult_geolocation/los_elevation_vcog')
            mie_los_elevation_top = coda.fetch(product, 'mie_geolocation', -1, 'windresult_geolocation/los_elevation_top')
            mie_satrange_bottom = coda.fetch(product, 'mie_geolocation', -1, 'windresult_geolocation/satrange_bottom')
            mie_satrange_vcog = coda.fetch(product, 'mie_geolocation', -1, 'windresult_geolocation/satrange_vcog')
            mie_satrange_top = coda.fetch(product, 'mie_geolocation', -1, 'windresult_geolocation/satrange_top')
            mie_start_of_obs_time = coda.fetch(product, 'mie_geolocation', -1, 'start_of_obs_time')
            mie_hlos_error_estimate = coda.fetch(product, 'mie_wind_prod_conf_data', -1, 'mie_wind_QC/hlos_error_estimate')/100.0
            mie_profile_id_number = coda.fetch(product, 'mie_profile', -1, 'l2b_wind_profiles/profile_id_number')
            mie_wind_result_id_number = coda.fetch(product, 'mie_profile', -1, 'l2b_wind_profiles/wind_result_id_number')
            mie_integration_length = coda.fetch(product, 'mie_hloswind', -1, 'windresult/integration_length')
            mie_wind_result_id = coda.fetch(product, 'mie_hloswind', -1, 'wind_result_id')
            mie_observation_type = coda.fetch(product, 'mie_hloswind', -1, 'windresult/observation_type')
            mie_validity_flag = coda.fetch(product, 'mie_hloswind', -1, 'windresult/validity_flag')
            mie_wind_velocity = coda.fetch(product, 'mie_hloswind', -1, 'windresult/mie_wind_velocity')/100.0
            #mie_reference_pressure = coda.fetch(product, 'mie_hloswind', -1, 'windresult/reference_pressure')
            #mie_reference_temperature = coda.fetch(product, 'mie_hloswind', -1, 'windresult/reference_temperature')/100.0
            #mie_reference_backscatter_ratio = coda.fetch(product, 'mie_hloswind', -1, 'windresult/reference_backscatter_ratio')/1000000.0
            #mie_wind_to_pressure = coda.fetch(product, 'mie_hloswind', -1, 'windresult/mie_wind_to_pressure')/1000000.0
            #mie_wind_to_temperature = coda.fetch(product, 'mie_hloswind', -1, 'windresult/mie_wind_to_temperature')/100.0
            #mie_wind_to_backscatter_ratio = coda.fetch(product, 'mie_hloswind', -1, 'windresult/mie_wind_to_backscatter_ratio')/100.0

            rayleigh_latitude_start = coda.fetch(product, 'rayleigh_geolocation', -1, 'windresult_geolocation/latitude_start')
            rayleigh_latitude_cog = coda.fetch(product, 'rayleigh_geolocation', -1, 'windresult_geolocation/latitude_cog')
            rayleigh_latitude_stop = coda.fetch(product, 'rayleigh_geolocation', -1, 'windresult_geolocation/latitude_stop')
            rayleigh_longitude_start = coda.fetch(product, 'rayleigh_geolocation', -1, 'windresult_geolocation/longitude_start')
            rayleigh_longitude_cog = coda.fetch(product, 'rayleigh_geolocation', -1, 'windresult_geolocation/longitude_cog')
            rayleigh_longitude_stop = coda.fetch(product, 'rayleigh_geolocation', -1, 'windresult_geolocation/longitude_stop')
            rayleigh_datetime_start = coda.fetch(product, 'rayleigh_geolocation', -1, 'windresult_geolocation/datetime_start')
            rayleigh_datetime_cog = coda.fetch(product, 'rayleigh_geolocation', -1, 'windresult_geolocation/datetime_cog')
            rayleigh_datetime_stop = coda.fetch(product, 'rayleigh_geolocation', -1, 'windresult_geolocation/datetime_stop')
            rayleigh_altitude_bottom = coda.fetch(product, 'rayleigh_geolocation', -1, 'windresult_geolocation/altitude_bottom')
            rayleigh_altitude_vcog = coda.fetch(product, 'rayleigh_geolocation', -1, 'windresult_geolocation/altitude_vcog')
            rayleigh_altitude_top = coda.fetch(product, 'rayleigh_geolocation', -1, 'windresult_geolocation/altitude_top')
            rayleigh_los_azimuth = coda.fetch(product, 'rayleigh_geolocation', -1, 'windresult_geolocation/los_azimuth')
            rayleigh_los_elevation_bottom = coda.fetch(product, 'rayleigh_geolocation', -1, 'windresult_geolocation/los_elevation_bottom')
            rayleigh_los_elevation_vcog = coda.fetch(product, 'rayleigh_geolocation', -1, 'windresult_geolocation/los_elevation_vcog')
            rayleigh_los_elevation_top = coda.fetch(product, 'rayleigh_geolocation', -1, 'windresult_geolocation/los_elevation_top')
            rayleigh_satrange_bottom = coda.fetch(product, 'rayleigh_geolocation', -1, 'windresult_geolocation/satrange_bottom')
            rayleigh_satrange_vcog = coda.fetch(product, 'rayleigh_geolocation', -1, 'windresult_geolocation/satrange_vcog')
            rayleigh_satrange_top = coda.fetch(product, 'rayleigh_geolocation', -1, 'windresult_geolocation/satrange_top')
            rayleigh_start_of_obs_time = coda.fetch(product, 'rayleigh_geolocation', -1, 'start_of_obs_time')
            rayleigh_hlos_error_estimate = coda.fetch(product, 'rayleigh_wind_prod_conf_data', -1, 'rayleigh_wind_QC/hlos_error_estimate')/100.0
            rayleigh_profile_id_number = coda.fetch(product, 'rayleigh_profile', -1, 'l2b_wind_profiles/profile_id_number')
            rayleigh_wind_result_id_number = coda.fetch(product, 'rayleigh_profile', -1, 'l2b_wind_profiles/wind_result_id_number')
            rayleigh_integration_length = coda.fetch(product, 'rayleigh_hloswind', -1, 'windresult/integration_length')
            rayleigh_wind_result_id = coda.fetch(product, 'rayleigh_hloswind', -1, 'wind_result_id')
            rayleigh_observation_type = coda.fetch(product, 'rayleigh_hloswind', -1, 'windresult/observation_type')
            rayleigh_validity_flag = coda.fetch(product, 'rayleigh_hloswind', -1, 'windresult/validity_flag')
            rayleigh_wind_velocity = coda.fetch(product, 'rayleigh_hloswind', -1, 'windresult/rayleigh_wind_velocity')/100.0
            #rayleigh_reference_pressure = coda.fetch(product, 'rayleigh_hloswind', -1, 'windresult/reference_pressure')
            #rayleigh_reference_temperature = coda.fetch(product, 'rayleigh_hloswind', -1, 'windresult/reference_temperature')/100.0
            #rayleigh_reference_backscatter_ratio = coda.fetch(product, 'rayleigh_hloswind', -1, 'windresult/reference_backscatter_ratio')/1000000.0
            #rayleigh_wind_to_pressure = coda.fetch(product, 'rayleigh_hloswind', -1, 'windresult/rayleigh_wind_to_pressure')/1000000.0
            #rayleigh_wind_to_temperature = coda.fetch(product, 'rayleigh_hloswind', -1, 'windresult/rayleigh_wind_to_temperature')/100.0
            #rayleigh_wind_to_backscatter_ratio = coda.fetch(product, 'rayleigh_hloswind', -1, 'windresult/rayleigh_wind_to_backscatter_ratio')/100.0

            coda.close(product)

            mie_wind_result_id_number = np.vstack(mie_wind_result_id_number)
            mie_profile_id = np.zeros(mie_wind_result_id_number.shape, dtype='int64')
            for idp, profile_id in enumerate(mie_profile_id_number):
                mie_profile_id[idp, :] = profile_id
            rayleigh_wind_result_id_number = np.vstack(rayleigh_wind_result_id_number)
            rayleigh_profile_id = np.zeros(rayleigh_wind_result_id_number.shape, dtype='int64')
            for idp, profile_id in enumerate(rayleigh_profile_id_number):
                rayleigh_profile_id[idp, :] = profile_id

            mie_year = np.array([(J2000 + datetime.timedelta(seconds = d)).year for d in mie_start_of_obs_time], dtype='int64')
            mie_mnth = np.array([(J2000 + datetime.timedelta(seconds = d)).month for d in mie_start_of_obs_time], dtype='int64')
            mie_days = np.array([(J2000 + datetime.timedelta(seconds = d)).day for d in mie_start_of_obs_time], dtype='int64')
            mie_hour = np.array([(J2000 + datetime.timedelta(seconds = d)).hour for d in mie_start_of_obs_time], dtype='int64')
            mie_minu = np.array([(J2000 + datetime.timedelta(seconds = d)).minute for d in mie_start_of_obs_time], dtype='int64')
            mie_secw = np.array([(J2000 + datetime.timedelta(seconds = d)).second for d in mie_start_of_obs_time])
            mie_microsecond = np.array([(J2000 + datetime.timedelta(seconds = d)).microsecond for d in mie_start_of_obs_time])
            mie_secw = mie_secw + mie_microsecond/1000000.0
            mie_tise_start = mie_datetime_start - mie_start_of_obs_time
            mie_tise_cog = mie_datetime_cog - mie_start_of_obs_time
            mie_tise_stop = mie_datetime_stop - mie_start_of_obs_time

            rayleigh_year = np.array([(J2000 + datetime.timedelta(seconds = d)).year for d in rayleigh_start_of_obs_time], dtype='int64')
            rayleigh_mnth = np.array([(J2000 + datetime.timedelta(seconds = d)).month for d in rayleigh_start_of_obs_time], dtype='int64')
            rayleigh_days = np.array([(J2000 + datetime.timedelta(seconds = d)).day for d in rayleigh_start_of_obs_time], dtype='int64')
            rayleigh_hour = np.array([(J2000 + datetime.timedelta(seconds = d)).hour for d in rayleigh_start_of_obs_time], dtype='int64')
            rayleigh_minu = np.array([(J2000 + datetime.timedelta(seconds = d)).minute for d in rayleigh_start_of_obs_time], dtype='int64')
            rayleigh_secw = np.array([(J2000 + datetime.timedelta(seconds = d)).second for d in rayleigh_start_of_obs_time])
            rayleigh_microsecond = np.array([(J2000 + datetime.timedelta(seconds = d)).microsecond for d in rayleigh_start_of_obs_time])
            rayleigh_secw = rayleigh_secw + rayleigh_microsecond/1000000.0
            rayleigh_tise_start = rayleigh_datetime_start - rayleigh_start_of_obs_time
            rayleigh_tise_cog = rayleigh_datetime_cog - rayleigh_start_of_obs_time
            rayleigh_tise_stop = rayleigh_datetime_stop - rayleigh_start_of_obs_time

            n_data = len(mie_wind_velocity) + len(rayleigh_wind_velocity)

            SAID = np.full((n_data), 48, dtype='int64')
            SIID = np.full((n_data), 130, dtype='int64')
            OGCE = np.full((n_data), 0, dtype='int64')
            GSES = np.full((n_data), 0, dtype='int64')
            YEAR = np.concatenate((mie_year, rayleigh_year))
            MNTH = np.concatenate((mie_mnth, rayleigh_mnth))
            DAYS = np.concatenate((mie_days, rayleigh_days))
            HOUR = np.concatenate((mie_hour, rayleigh_hour))
            MINU = np.concatenate((mie_minu, rayleigh_minu))
            SECW = np.concatenate((mie_secw, rayleigh_secw))

            #2: Start of observation
            CRDSIG_2 = np.full((n_data), 2, dtype='int64')
            CLATH_2 = np.concatenate((mie_latitude_start, rayleigh_latitude_start))
            CLONH_2 = np.concatenate((mie_longitude_start, rayleigh_longitude_start))
            TISE_2 = np.concatenate((mie_tise_start, rayleigh_tise_start))
            #3: End of observation
            CRDSIG_3 = np.full((n_data), 3, dtype='int64')
            CLATH_3 = np.concatenate((mie_latitude_stop, rayleigh_latitude_stop))
            CLONH_3 = np.concatenate((mie_longitude_stop, rayleigh_longitude_stop))
            TISE_3 = np.concatenate((mie_tise_stop, rayleigh_tise_stop))
            #4: Horizontal Centre of gravity of observation
            CRDSIG_4 = np.full((n_data), 4, dtype='int64')
            CLATH_4 = np.concatenate((mie_latitude_cog, rayleigh_latitude_cog))
            CLONH_4 = np.concatenate((mie_longitude_cog, rayleigh_longitude_cog))
            TISE_4 = np.concatenate((mie_tise_cog, rayleigh_tise_cog))
            #6: Top of observation
            CRDSIG_6 = np.full((n_data), 6, dtype='int64')
            HEITH_6 = np.concatenate((mie_altitude_top, rayleigh_altitude_top))
            BEARAZ_6 = np.concatenate((mie_los_azimuth, rayleigh_los_azimuth))
            ELEV_6 = np.concatenate((mie_los_elevation_top, rayleigh_los_elevation_top))
            SATRG_6 = np.concatenate((mie_satrange_top, rayleigh_satrange_top))
            #7: Bottom of observation
            CRDSIG_7 = np.full((n_data), 7, dtype='int64')
            HEITH_7 = np.concatenate((mie_altitude_bottom, rayleigh_altitude_bottom))
            BEARAZ_7 = np.concatenate((mie_los_azimuth, rayleigh_los_azimuth))
            ELEV_7 = np.concatenate((mie_los_elevation_bottom, rayleigh_los_elevation_bottom))
            SATRG_7 = np.concatenate((mie_satrange_bottom, rayleigh_satrange_bottom))
            #5: Vertical centre of Gravity of the observation
            CRDSIG_5 = np.full((n_data), 5, dtype='int64')
            HEITH_5 = np.concatenate((mie_altitude_vcog, rayleigh_altitude_vcog))
            BEARAZ_5 = np.concatenate((mie_los_azimuth, rayleigh_los_azimuth))
            ELEV_5 = np.concatenate((mie_los_elevation_vcog, rayleigh_los_elevation_vcog))
            SATRG_5 = np.concatenate((mie_satrange_vcog, rayleigh_satrange_vcog))

            PFNUM = np.concatenate((mie_profile_id[mie_wind_result_id_number != 0], rayleigh_profile_id[rayleigh_wind_result_id_number != 0]))
            OBSID = np.concatenate((mie_wind_result_id, rayleigh_wind_result_id))
            RCVCH = np.concatenate((np.full((len(mie_wind_velocity)), 0, dtype='int64'), np.full((len(rayleigh_wind_velocity)), 1, dtype='int64')))
            LL2BCT = np.concatenate((mie_observation_type, rayleigh_observation_type))
            LL2BCT = np.where(LL2BCT == 0, 15, LL2BCT)
            LL2BCT = np.where(LL2BCT == 2, 0, LL2BCT)
            HOIL = np.concatenate((mie_integration_length, rayleigh_integration_length))
            HLSW = np.concatenate((mie_wind_velocity, rayleigh_wind_velocity))
            HLSWEE = np.concatenate((mie_hlos_error_estimate, rayleigh_hlos_error_estimate))
            CONFLG = np.concatenate((mie_validity_flag, rayleigh_validity_flag))
            CONFLG = np.where(CONFLG == 1, 0, 1)
            PRES = np.full((n_data), 0.0, dtype='float64')
            TMDBST = np.full((n_data), 0.0, dtype='float64')
            BKSTR = np.full((n_data), 0.0, dtype='float64')
            DWPRS = np.full((n_data), 0.0, dtype='float64')
            DWTMP = np.full((n_data), 0.0, dtype='float64')
            DWBR = np.full((n_data), 0.0, dtype='float64')
            #PRES = np.concatenate((mie_reference_pressure, rayleigh_reference_pressure))
            #TMDBST = np.concatenate((mie_reference_temperature, rayleigh_reference_temperature))
            #BKSTR = np.concatenate((mie_reference_backscatter_ratio, rayleigh_reference_backscatter_ratio))
            #DWPRS = np.concatenate((mie_wind_to_pressure, rayleigh_wind_to_pressure))
            #DWTMP = np.concatenate((mie_wind_to_temperature, rayleigh_wind_to_temperature))
            #DWBR = np.concatenate((mie_wind_to_backscatter_ratio, rayleigh_wind_to_backscatter_ratio))

            n_data_total = n_data_total + n_data

            with open(dir_out + '/1.txt', 'ab') as f:
                np.savetxt(f, SAID)
            with open(dir_out + '/2.txt', 'ab') as f:
                np.savetxt(f, SIID)
            with open(dir_out + '/3.txt', 'ab') as f:
                np.savetxt(f, OGCE)
            with open(dir_out + '/4.txt', 'ab') as f:
                np.savetxt(f, GSES)
            with open(dir_out + '/5.txt', 'ab') as f:
                np.savetxt(f, YEAR)
            with open(dir_out + '/6.txt', 'ab') as f:
                np.savetxt(f, MNTH)
            with open(dir_out + '/7.txt', 'ab') as f:
                np.savetxt(f, DAYS)
            with open(dir_out + '/8.txt', 'ab') as f:
                np.savetxt(f, HOUR)
            with open(dir_out + '/9.txt', 'ab') as f:
                np.savetxt(f, MINU)
            with open(dir_out + '/10.txt', 'ab') as f:
                np.savetxt(f, SECW)
            with open(dir_out + '/11.txt', 'ab') as f:
                np.savetxt(f, CRDSIG_2)
            with open(dir_out + '/12.txt', 'ab') as f:
                np.savetxt(f, CLATH_2)
            with open(dir_out + '/13.txt', 'ab') as f:
                np.savetxt(f, CLONH_2)
            with open(dir_out + '/14.txt', 'ab') as f:
                np.savetxt(f, TISE_2)
            with open(dir_out + '/15.txt', 'ab') as f:
                np.savetxt(f, CRDSIG_3)
            with open(dir_out + '/16.txt', 'ab') as f:
                np.savetxt(f, CLATH_3)
            with open(dir_out + '/17.txt', 'ab') as f:
                np.savetxt(f, CLONH_3)
            with open(dir_out + '/18.txt', 'ab') as f:
                np.savetxt(f, TISE_3)
            with open(dir_out + '/19.txt', 'ab') as f:
                np.savetxt(f, CRDSIG_4)
            with open(dir_out + '/20.txt', 'ab') as f:
                np.savetxt(f, CLATH_4)
            with open(dir_out + '/21.txt', 'ab') as f:
                np.savetxt(f, CLONH_4)
            with open(dir_out + '/22.txt', 'ab') as f:
                np.savetxt(f, TISE_4)
            with open(dir_out + '/23.txt', 'ab') as f:
                np.savetxt(f, CRDSIG_6)
            with open(dir_out + '/24.txt', 'ab') as f:
                np.savetxt(f, HEITH_6)
            with open(dir_out + '/25.txt', 'ab') as f:
                np.savetxt(f, BEARAZ_6)
            with open(dir_out + '/26.txt', 'ab') as f:
                np.savetxt(f, ELEV_6)
            with open(dir_out + '/27.txt', 'ab') as f:
                np.savetxt(f, SATRG_6)
            with open(dir_out + '/28.txt', 'ab') as f:
                np.savetxt(f, CRDSIG_7)
            with open(dir_out + '/29.txt', 'ab') as f:
                np.savetxt(f, HEITH_7)
            with open(dir_out + '/30.txt', 'ab') as f:
                np.savetxt(f, BEARAZ_7)
            with open(dir_out + '/31.txt', 'ab') as f:
                np.savetxt(f, ELEV_7)
            with open(dir_out + '/32.txt', 'ab') as f:
                np.savetxt(f, SATRG_7)
            with open(dir_out + '/33.txt', 'ab') as f:
                np.savetxt(f, CRDSIG_5)
            with open(dir_out + '/34.txt', 'ab') as f:
                np.savetxt(f, HEITH_5)
            with open(dir_out + '/35.txt', 'ab') as f:
                np.savetxt(f, BEARAZ_5)
            with open(dir_out + '/36.txt', 'ab') as f:
                np.savetxt(f, ELEV_5)
            with open(dir_out + '/37.txt', 'ab') as f:
                np.savetxt(f, SATRG_5)
            with open(dir_out + '/38.txt', 'ab') as f:
                np.savetxt(f, PFNUM)
            with open(dir_out + '/39.txt', 'ab') as f:
                np.savetxt(f, OBSID)
            with open(dir_out + '/40.txt', 'ab') as f:
                np.savetxt(f, RCVCH)
            with open(dir_out + '/41.txt', 'ab') as f:
                np.savetxt(f, LL2BCT)
            with open(dir_out + '/42.txt', 'ab') as f:
                np.savetxt(f, HOIL)
            with open(dir_out + '/43.txt', 'ab') as f:
                np.savetxt(f, HLSW)
            with open(dir_out + '/44.txt', 'ab') as f:
                np.savetxt(f, HLSWEE)
            with open(dir_out + '/45.txt', 'ab') as f:
                np.savetxt(f, CONFLG)
            with open(dir_out + '/46.txt', 'ab') as f:
                np.savetxt(f, PRES)
            with open(dir_out + '/47.txt', 'ab') as f:
                np.savetxt(f, TMDBST)
            with open(dir_out + '/48.txt', 'ab') as f:
                np.savetxt(f, BKSTR)
            with open(dir_out + '/49.txt', 'ab') as f:
                np.savetxt(f, DWPRS)
            with open(dir_out + '/50.txt', 'ab') as f:
                np.savetxt(f, DWTMP)
            with open(dir_out + '/51.txt', 'ab') as f:
                np.savetxt(f, DWBR)

    np.savetxt(dir_out + '/0.txt', [n_data_total])
    time_now = time_now + datetime.timedelta(hours = time_interval)
