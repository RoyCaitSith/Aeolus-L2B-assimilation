import os
import datetime
import numpy as np
from netCDF4 import Dataset

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/15_ENS'
dir_main = '/'.join([dir_CPEX, 'display_bufr'])

#case = 'CON6h_Aeolus6h_082406_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082412_Hybrid_C08'
#case = 'CON6h_Aeolus6h_082418_Hybrid_C08'
case = 'CON6h_Aeolus6h_082500_Hybrid_C08'
status = ['ges', 'anl']
#domains = ['d01']
domains = ['d02']
cycling_interval = 6.0

#anl_start_time = datetime.datetime(2021, 8, 24, 12, 0, 0)
#anl_end_time   = datetime.datetime(2021, 8, 26,  6, 0, 0)
#anl_start_time = datetime.datetime(2021, 8, 24, 18, 0, 0)
#anl_end_time   = datetime.datetime(2021, 8, 26, 12, 0, 0)
#anl_start_time = datetime.datetime(2021, 8, 25,  0, 0, 0)
#anl_end_time   = datetime.datetime(2021, 8, 26, 18, 0, 0)
anl_start_time = datetime.datetime(2021, 8, 25,  6, 0, 0)
anl_end_time   = datetime.datetime(2021, 8, 27,  0, 0, 0)

for dom in domains:

    dir_save = '/'.join([dir_CPEX, 'cycling_da', 'Data', case, 'da'])
    dir_out = '/'.join([dir_main, case])
    os.system('mkdir ' + dir_out)

    time_now = anl_start_time
    while time_now <= anl_end_time:

        time_now_str = time_now.strftime('%Y%m%d%H')

        for stat in status:

            results_conv = dir_save + '/results_conv_' + stat + '.' + time_now_str + '.' + dom
            print(results_conv)

            tmp = np.array([])
            with open(results_conv) as f:
                lines = np.array(f.readlines())

            if len(lines) > 0:
                index = np.char.find(lines, 'uv')
                lines = lines[index == -1]
                lines = ' '.join(lines)
                tmp = np.append(tmp, np.array(lines.split()).astype(np.float64))
                print(len(tmp))

            n_obs = int(len(tmp)/27)
            print(n_obs)
            tmp = np.array(tmp)
            tmp = np.reshape(tmp, (n_obs, 27))
            index = (tmp[:,0]==101.0)
            tmp = tmp[index, :]
            n_obs = int(len(tmp[:,0]))
            print(n_obs)

            if n_obs != 0:

                print(tmp[0,:])

                filename = dir_out + '/' + time_now_str + '_' + stat + '_' + dom + '.nc'
                print(filename)

                os.system('rm -rf ' + filename)
                ncfile = Dataset(filename, 'w', format='NETCDF4')
                ncfile.createDimension('n_obs',  n_obs)
                ncfile.createVariable('observation_type',             'f8', ('n_obs'))
                ncfile.createVariable('observation_subtype',          'f8', ('n_obs'))
                ncfile.createVariable('latitude',                     'f8', ('n_obs'))
                ncfile.createVariable('longitude',                    'f8', ('n_obs'))
                ncfile.createVariable('station_elevation',            'f8', ('n_obs'))
                ncfile.createVariable('pressure',                     'f8', ('n_obs'))
                ncfile.createVariable('height',                       'f8', ('n_obs'))
                ncfile.createVariable('observation_time',             'f8', ('n_obs'))
                ncfile.createVariable('input_prepbufr_qc',            'f8', ('n_obs'))
                ncfile.createVariable('setup_qc',                     'f8', ('n_obs'))
                ncfile.createVariable('data_usage_flag',              'f8', ('n_obs'))
                ncfile.createVariable('analysis_usage_flag',          'f8', ('n_obs'))
                ncfile.createVariable('nonlinear_qc_relative_weight', 'f8', ('n_obs'))
                ncfile.createVariable('inverse_obs_error_input',      'f8', ('n_obs'))
                ncfile.createVariable('inverse_obs_error_adjust',     'f8', ('n_obs'))
                ncfile.createVariable('inverse_obs_error_final',      'f8', ('n_obs'))
                ncfile.createVariable('observation',                  'f8', ('n_obs'))
                ncfile.createVariable('obs_minus_ges_analysis',       'f8', ('n_obs'))
                ncfile.createVariable('obs_minus_ges_without_BC',     'f8', ('n_obs'))
                ncfile.createVariable('10m_wind_reduction_factor',    'f8', ('n_obs'))
                ncfile.createVariable('elevation_angle',              'f8', ('n_obs'))
                ncfile.createVariable('azimuth',                      'f8', ('n_obs'))
                ncfile.createVariable('receiver_channel',             'f8', ('n_obs'))
                ncfile.createVariable('classification_type',          'f8', ('n_obs'))
                ncfile.createVariable('confidence_flag',              'f8', ('n_obs'))
                ncfile.createVariable('LOS_component_of_wind',        'f8', ('n_obs'))
                ncfile.createVariable('ges_ensemble_spread',          'f8', ('n_obs'))

                ncfile.variables['observation_type'][:] = tmp[:, 0]
                ncfile.variables['observation_subtype'][:] = tmp[:, 1]
                ncfile.variables['latitude'][:] = tmp[:, 2]
                ncfile.variables['longitude'][:] = tmp[:, 3]
                ncfile.variables['station_elevation'][:] = tmp[:, 4]
                ncfile.variables['pressure'][:] = tmp[:, 5]
                ncfile.variables['height'][:] = tmp[:, 6]
                ncfile.variables['observation_time'][:] = tmp[:, 7]
                ncfile.variables['input_prepbufr_qc'][:] = tmp[:, 8]
                ncfile.variables['setup_qc'][:] = tmp[:, 9]
                ncfile.variables['data_usage_flag'][:] = tmp[:, 10]
                ncfile.variables['analysis_usage_flag'][:] = tmp[:, 11]
                ncfile.variables['nonlinear_qc_relative_weight'][:] = tmp[:, 12]
                ncfile.variables['inverse_obs_error_input'][:] = tmp[:, 13]
                ncfile.variables['inverse_obs_error_adjust'][:] = tmp[:, 14]
                ncfile.variables['inverse_obs_error_final'][:] = tmp[:, 15]
                ncfile.variables['observation'][:] = tmp[:, 16]
                ncfile.variables['obs_minus_ges_analysis'][:] = tmp[:, 17]
                ncfile.variables['obs_minus_ges_without_BC'][:] = tmp[:, 18]
                ncfile.variables['10m_wind_reduction_factor'][:] = tmp[:, 19]
                ncfile.variables['elevation_angle'][:] = tmp[:, 20]
                ncfile.variables['azimuth'][:] = tmp[:, 21]
                ncfile.variables['receiver_channel'][:] = tmp[:, 22]
                ncfile.variables['classification_type'][:] = tmp[:, 23]
                ncfile.variables['confidence_flag'][:] = tmp[:, 24]
                ncfile.variables['LOS_component_of_wind'][:] = tmp[:, 25]
                ncfile.variables['ges_ensemble_spread'][:] = tmp[:, 26]

                ncfile.close()

        time_now = time_now + datetime.timedelta(hours=cycling_interval)
