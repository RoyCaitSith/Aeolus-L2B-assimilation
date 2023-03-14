import datetime
import numpy as np
import pandas as pd
from netCDF4 import Dataset
from scipy import ndimage
from scipy.interpolate import interp1d

time = '20210824'

cases = ['CON6h_Hybrid_082500']

dir_main = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021'
dir_best_track = '/'.join([dir_main, 'track_intensity', 'best_track'])
cycling_interval = 6
domain = 'd01'
dom_res = 12
filter_size = 6
n_small_box = int(108/dom_res)
search_box_size = int(600/dom_res)

if '20210824' in time:
    time_str = datetime.datetime(2021, 8, 24,  6, 0, 0)
    time_end = datetime.datetime(2021, 8, 28, 12, 0, 0)
    file_best_track = '/'.join([dir_best_track, '2021_09L_Ida.csv'])

def vertical_interp(pressure_data, interp_data, order_level):
    nz, ny, nx = np.shape(pressure_data)
    rslt = np.zeros([ny, nx])
    i = 0
    while i < ny:
        j = 0
        while j < nx:
            f = (interp1d(pressure_data[:,i,j], interp_data[:,i,j], kind='linear', fill_value='extrapolate'))
            rslt[i,j] = f(order_level)
            j+=1
        i+=1
    return rslt

def cal_voricity(u,v):
    dudx, dudy = np.gradient(u)
    dvdx, dvdy = np.gradient(v)
    rslt = dvdx-dudy
    return rslt

def find_raw_loc(mslp):
    shp_y, shp_x = np.shape(mslp)
    loc = []
    min_slp = ndimage.filters.minimum_filter(mslp, size=filter_size)
    ny, nx = np.nonzero(mslp == min_slp)
    i = 0
    count = 0
    for cell in ny:
        if n_small_box <= ny[i] <= shp_y-n_small_box and n_small_box <= nx[i] <= shp_x-n_small_box:
            count += 1
            area = mslp[ny[i]-n_small_box:ny[i]+n_small_box, nx[i]-n_small_box:nx[i]+n_small_box]
            area_max = np.max(area)
            idx_y, idx_x = np.nonzero(area == area_max)
            idx_ym, idx_xm = np.nonzero(area == mslp[ny[i],nx[i]])
            dist = np.mean(np.sqrt((idx_y-idx_ym)**2+(idx_x-idx_xm)**2)*dom_res)
            if np.abs((area_max-mslp[ny[i],nx[i]])/dist)/100.0 >= 0.0015:
                loc.append([ny[i],nx[i]])
        i += 1
    return np.asarray(loc)

def find_local_max_vor(u_i, v_i):
    vor = cal_voricity(u_i, v_i)
    max_vor = ndimage.filters.maximum_filter(vor, size=filter_size)
    ny,nx = np.nonzero(vor == max_vor)
    i = 0
    loc = []
    for cell in ny:
        loc.append([ny[i],nx[i]])
        i += 1
    return np.asarray(loc)

def find_local_min_ws(u_i, v_i):
    ws = np.sqrt(u_i**2 + v_i**2)
    min_ws = ndimage.filters.minimum_filter(ws, size=filter_size)
    ny,nx = np.nonzero(ws == min_ws)
    i = 0
    loc = []
    for cell in ny:
        loc.append([ny[i],nx[i]])
        i += 1
    return np.asarray(loc)

def find_local_min_hgt(h_i):
    min_hgt = ndimage.filters.minimum_filter(h_i, size=filter_size)
    ny, nx = np.nonzero(h_i == min_hgt)
    i = 0
    loc = []
    for cell in ny:
        loc.append([ny[i],nx[i]])
        i+=1
    return np.asarray(loc)

for case in cases:

    dir_bkg = '/'.join([dir_main, 'bkg', time, case])
    time_now = time_str
    time_now_str = time_now.strftime('%Y-%m-%d %H:00:00')
    df_best_track = pd.read_csv(file_best_track)
    df_time_now = df_best_track[df_best_track['Date_Time'] == time_now_str]
    last_lat = float(df_time_now['Latitude'])
    last_lon = float(df_time_now['Longitude'])

    while time_now <= time_end:

        print(time_now)

        wrfout_time = time_now.strftime('%Y-%m-%d_%H:00:00')
        wrfout_name = '_'.join(['wrfout', domain, wrfout_time])
        wrfout_file = '/'.join([dir_bkg, wrfout_name])

        ncfile = Dataset(wrfout_file)
        mslp = ncfile.variables['PSFC'][0,:,:]
        u10 = ncfile.variables['U10'][0,:,:]
        v10 = ncfile.variables['V10'][0,:,:]
        u = ncfile.variables['U'][0,:,:,:]
        v = ncfile.variables['V'][0,:,:,:]
        p = (ncfile.variables['P'][0,:,:,:] + ncfile.variables['PB'][0,:,:,:])/100.0
        hgt = (ncfile.variables['PH'][0,:,:,:] + ncfile.variables['PHB'][0,:,:,:])
        xland = ncfile.variables['XLAND'][0,:,:]
        lat = ncfile.variables['XLAT'][0,:,:]
        lon = ncfile.variables['XLONG'][0,:,:]
        ncfile.close()

        u_i_850 = vertical_interp(p, u, 850)
        v_i_850 = vertical_interp(p, v, 850)
        u_i_700 = vertical_interp(p, u, 700)
        v_i_700 = vertical_interp(p, v, 700)
        h_i_850 = vertical_interp(p, hgt[1:,:,:], 850)
        h_i_700 = vertical_interp(p, hgt[1:,:,:], 700)

        print('The guess position:')
        print((last_lat, last_lon))
        last_distance = np.sqrt((last_lat-lat)**2 + (last_lon-lon)**2)
        last_distance_min = np.min(last_distance)
        idx_last_lat, idx_last_lon = np.nonzero(last_distance == last_distance_min)
        idx_last_lat, idx_last_lon = int(idx_last_lat), int(idx_last_lon)
        print('The closet point:')
        print((idx_last_lat, idx_last_lon))
        print((lat[idx_last_lat, idx_last_lon], lon[idx_last_lat, idx_last_lon]))

        ur_lat = idx_last_lat + search_box_size
        ur_lon = idx_last_lon + search_box_size
        ll_lat = idx_last_lat - search_box_size
        ll_lon = idx_last_lon - search_box_size
        mslp_area = mslp[ll_lat:ur_lat, ll_lon:ur_lon]
        lat_area = lat[ll_lat:ur_lat, ll_lon:ur_lon]
        lon_area = lon[ll_lat:ur_lat, ll_lon:ur_lon]
        u10_area = u10[ll_lat:ur_lat, ll_lon:ur_lon]
        v10_area = v10[ll_lat:ur_lat, ll_lon:ur_lon]
        u850_area = u_i_850[ll_lat:ur_lat, ll_lon:ur_lon]
        v850_area = v_i_850[ll_lat:ur_lat, ll_lon:ur_lon]
        h850_area = h_i_850[ll_lat:ur_lat, ll_lon:ur_lon]
        u700_area = u_i_700[ll_lat:ur_lat, ll_lon:ur_lon]
        v700_area = v_i_700[ll_lat:ur_lat, ll_lon:ur_lon]
        h700_area = h_i_700[ll_lat:ur_lat, ll_lon:ur_lon]

        print('Search by MSLP')
        raw_loc = find_raw_loc(mslp_area)
        #print(raw_loc)

        print('Search by Relative Vorticity at 10 m')
        vor10_area = cal_voricity(u10_area, v10_area)
        max_vor10_area = ndimage.filters.maximum_filter(vor10_area, size=filter_size)
        ny, nx = np.nonzero(vor10_area == max_vor10_area)
        loc=[]
        for cell in raw_loc:
            dist = np.sqrt((ny-cell[0])**2+(nx-cell[1])**2)
            if np.min(dist) < n_small_box + 0.5:
                loc.append(cell)
        loc = np.asarray(loc)
        #print(loc)

        print('Search by Relative Vorticity at 850 hPa')
        loc_1 = find_local_max_vor(u850_area, v850_area)
        #print(loc_1)

        print('Search by Relative Vorticity at 700 hPa')
        loc_2 = find_local_max_vor(u700_area, v700_area)
        #print(loc_2)

        print('Search by Geopotential Height at 850 hPa')
        loc_3 = find_local_min_hgt(h850_area)
        #print(loc_3)

        print('Search by Geopotential Height at 700 hPa')
        loc_4 = find_local_min_hgt(h700_area)
        #print(loc_4)

        print('Search by Wind Speed at 10 m')
        loc_5 = find_local_min_ws(u10_area, v10_area)
        #print(loc_5)

        print('Search by Wind Speed at 850 hPa')
        loc_6 = find_local_min_ws(u850_area, v850_area)
        #print(loc_6)

        print('Search by Wind Speed at 700 hPa')
        loc_7 = find_local_min_ws(u700_area, v700_area)
        #print(loc_7)

        possible_loc = []
        for cell in loc:
            dist = [np.min(np.sqrt((loc_1[:,0]-cell[0])**2 + (loc_1[:,1]-cell[1])**2)), \
                    np.min(np.sqrt((loc_2[:,0]-cell[0])**2 + (loc_2[:,1]-cell[1])**2)), \
                    np.min(np.sqrt((loc_3[:,0]-cell[0])**2 + (loc_3[:,1]-cell[1])**2)), \
                    np.min(np.sqrt((loc_4[:,0]-cell[0])**2 + (loc_4[:,1]-cell[1])**2)), \
                    np.min(np.sqrt((loc_5[:,0]-cell[0])**2 + (loc_5[:,1]-cell[1])**2)), \
                    np.min(np.sqrt((loc_6[:,0]-cell[0])**2 + (loc_6[:,1]-cell[1])**2)), \
                    np.min(np.sqrt((loc_7[:,0]-cell[0])**2 + (loc_7[:,1]-cell[1])**2))]
            wind = np.sqrt(u10_area**2 + v10_area**2)
            wind_max = np.max(wind[cell[0]-n_small_box:cell[0]+n_small_box, cell[1]-n_small_box:cell[1]+n_small_box])
            slp_min = np.min(mslp[cell[0]-n_small_box:cell[0]+n_small_box, cell[1]-n_small_box:cell[1]+n_small_box])/100.0
            if all(np.asarray(dist) < n_small_box + 0.5):
                possible_loc += [[lat_area[cell[0],cell[1]], lon_area[cell[0],cell[1]], wind_max, slp_min]
        if time_now == time_str:
            distance = np.sqrt((np.asarray(possible_loc)[:,0] - last_lat)**2 + (np.asarray(possible_loc)[:,1] - last_lon)**2)
        else:
            distance = np.asarray(possible_loc[:,4])
        idx = np.unravel_index(distance.argmin(), distance.shape)[0]
        last_lat = float(possible_loc[idx][0])
        last_lon = float(possible_loc[idx][1])
        print(time_now, possible_loc[idx][0], possible_loc[idx][1], possible_loc[idx][2], possible_loc[idx][3])

        time_now = time_now + datetime.timedelta(hours = cycling_interval)
