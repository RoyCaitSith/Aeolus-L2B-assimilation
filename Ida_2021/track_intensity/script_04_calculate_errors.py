import datetime
import numpy as np
import pandas as pd
from geopy.distance import great_circle

dir_CPEX = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN'
dir_main = dir_CPEX + '/15_ENS/track_intensity'
dir_best_track = dir_main + '/best_track'

#cases = ['CON6h_082406_Hybrid_C05', 'CON6h_082406_Hybrid_C06', 'CON6h_082406_Hybrid_C07', 'CON6h_082406_Hybrid_C08']
#cases = ['CON6h_082412_Hybrid_C05', 'CON6h_082412_Hybrid_C06', 'CON6h_082412_Hybrid_C07', 'CON6h_082412_Hybrid_C08']
#cases = ['CON6h_082418_Hybrid_C05', 'CON6h_082418_Hybrid_C06', 'CON6h_082418_Hybrid_C07', 'CON6h_082418_Hybrid_C08']
#cases = ['CON6h_082500_Hybrid_C05', 'CON6h_082500_Hybrid_C06', 'CON6h_082500_Hybrid_C07', 'CON6h_082500_Hybrid_C08']
#cases = ['CON6h_Aeolus6h_082406_Hybrid_C05', 'CON6h_Aeolus6h_082406_Hybrid_C06', 'CON6h_Aeolus6h_082406_Hybrid_C07', 'CON6h_Aeolus6h_082406_Hybrid_C08']
#cases = ['CON6h_Aeolus6h_082412_Hybrid_C05', 'CON6h_Aeolus6h_082412_Hybrid_C06', 'CON6h_Aeolus6h_082412_Hybrid_C07', 'CON6h_Aeolus6h_082412_Hybrid_C08']
#cases = ['CON6h_Aeolus6h_082418_Hybrid_C05', 'CON6h_Aeolus6h_082418_Hybrid_C06', 'CON6h_Aeolus6h_082418_Hybrid_C07', 'CON6h_Aeolus6h_082418_Hybrid_C08']
cases = ['CON6h_Aeolus6h_082500_Hybrid_C05', 'CON6h_Aeolus6h_082500_Hybrid_C06', 'CON6h_Aeolus6h_082500_Hybrid_C07', 'CON6h_Aeolus6h_082500_Hybrid_C08']

domain = 'd01'
file_best_track = dir_best_track + '/2021_09L_Ida.csv'
#forecast_start_time = datetime.datetime(2021, 8, 24,  6, 0, 0)
#forecast_start_time = datetime.datetime(2021, 8, 24, 12, 0, 0)
#forecast_start_time = datetime.datetime(2021, 8, 24, 18, 0, 0)
forecast_start_time = datetime.datetime(2021, 8, 25,  0, 0, 0)

BT_df = pd.read_csv(file_best_track)
for case in cases:

    forecast_hours = 54 + 6*int(case[-2:])
    n_lead_time = int(forecast_hours/6 + 1)
    error_df = pd.DataFrame(0.0, index=np.arange(n_lead_time), columns=['Forecast_Hour', 'Track_Error (km)', 'MSLP_Error (hPa)', 'MWS_Error (Knot)'])

    filename = dir_main + '/' + case + '/multi/fort.69'
    df = pd.read_csv(filename, header=None, usecols=[2, 5, 6, 7, 8, 9])
    df.columns = ['Initial_Time', 'Forecast_Hour', 'Latitude', 'Longitude', 'MWS (Knot)', 'MSLP (hPa)']
    df.drop_duplicates(subset=['Forecast_Hour'], keep='last', inplace=True)

    Date_Time = []
    for it, fh in zip(df['Initial_Time'], df['Forecast_Hour']):
        Date_Time = Date_Time + [datetime.datetime.strptime(str(it), '%Y%m%d%H') + datetime.timedelta(hours = fh/100.0)]
    df.insert(loc=0, column='Date_Time', value=Date_Time)
    df.drop(columns=['Initial_Time', 'Forecast_Hour'], inplace=True)
    df.reset_index(drop=True, inplace=True)

    lat = list(df['Latitude'])
    lat = [x.split('N')[0] for x in lat]
    lat = pd.Series(map(float, lat))
    df['Latitude'] = 0.1*lat

    lon = list(df['Longitude'])
    lon = [x.split('W')[0] for x in lon]
    lon = pd.Series(map(float, lon))
    df['Longitude'] = -0.1*lon

    df.to_csv(dir_best_track + '/' + case + '_' + domain + '.csv', index=False)

    for idx, DT in enumerate(BT_df['Date_Time']):
        if datetime.datetime.strptime(DT, '%Y-%m-%d %H:%M:%S') == forecast_start_time: BT_str_index = idx
    for idx, DT in enumerate(df['Date_Time']):
        if DT == forecast_start_time: str_index = idx

    for idl in range(0, n_lead_time):

        index = idl
        error_df['Forecast_Hour'][index] = 6.0*idl

        loc = (df['Latitude'][str_index+idl], df['Longitude'][str_index+idl])
        BT_loc = (BT_df['Latitude'][BT_str_index+idl], BT_df['Longitude'][BT_str_index+idl])
        error_df['Track_Error (km)'][index] = great_circle(loc, BT_loc).kilometers
        error_df['MSLP_Error (hPa)'][index] = df['MSLP (hPa)'][str_index+idl] - BT_df['MSLP (hPa)'][BT_str_index+idl]
        error_df['MWS_Error (Knot)'][index] = df['MWS (Knot)'][str_index+idl] - BT_df['MWS (Knot)'][BT_str_index+idl]

    error_df.to_csv(dir_best_track + '/Error_' + case + '_' + domain + '.csv', index=False)
