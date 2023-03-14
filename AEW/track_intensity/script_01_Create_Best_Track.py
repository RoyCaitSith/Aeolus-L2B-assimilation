import datetime
import pandas as pd

dir_main            = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021/track_intensity'
dir_best_track      = dir_main + '/best_track'
file_raw_best_track = dir_best_track + '/syndat_tcvitals.2020'
file_best_track     = dir_best_track + '/2020_Laura.csv'

print(miao)

df = pd.read_csv(file_raw_best_track, sep='\s+', header=None, usecols=[0, 1, 2, 3, 4, 5, 6, 9, 12])
df.columns = ['Organization', 'Number', 'Name', 'Date', 'Time', 'Latitude', 'Longitude', 'MSLP (hPa)', 'MWS (Knot)']
df = df[(df['Organization'] == 'NHC') & (df['Number'] == '13L')]
df.drop_duplicates(subset=['Date', 'Time'], keep='last', inplace=True)
df.drop(columns=['Number', 'Name'], inplace=True)
df.reset_index(drop=True, inplace=True)

Date_Time = []
for date, time in zip(df['Date'], df['Time']):
    Date_Time = Date_Time + [datetime.datetime.strptime(str(date)+str(time).zfill(4), '%Y%m%d%H%M')]
df.insert(loc=2, column='Date_Time', value=Date_Time)
df.drop(columns=['Date', 'Time'], inplace=True)

Latitude = list(df['Latitude'])
Latitude = [x.split('N')[0] for x in Latitude]
Latitude = pd.Series(map(float, Latitude))
df['Latitude'] = 0.1*Latitude

Longitude = list(df['Longitude'])
Longitude = [x.split('W')[0] for x in Longitude]
Longitude = pd.Series(map(float, Longitude))
df['Longitude'] = -0.1*Longitude

MWS = list(1.94384*df['MWS (Knot)'])
MWS = [5.0*round(x/5) for x in MWS]
df['MWS (Knot)'] = MWS

df.to_csv(file_best_track, index=False)

print(df)
