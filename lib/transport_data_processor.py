from lib.ref_data_loader import RefDataLoader
from lib.risk_profile_model import JourneyTimeMatrix,JourneySegment
import lib.ref_data_processor as rd
from datetime import datetime, timedelta
import pickle
import pandas as pd
from utils import db_utils as du

# drop table , used to save the results
tbl_name = 'journey_segments'
db_name = 'Roberto_RiskProfile_Oyster'

du.drop_db_table(db_name, tbl_name)
print ('Cleared DB table to sort the results. ')

# Load all reference data
# load the line data i.e. station code, station name, line name
refd = RefDataLoader()

with open('data\stations_dict.pkl', 'rb') as f:
    station_dict = pickle.load(f)
    print('stations dictionary loaded')

with open('data\stations_df.pkl', 'rb') as f:
    station_df = pickle.load(f)
    print('stations data frame loaded')


# select the first common train line between the two stations
def get_train_line(station_in, station_out) -> str:
    # get the lines at each station
    stations_line_in = rd.get_line_name(refd, station_in)
    stations_line_out = rd.get_line_name(refd, station_out)

    stations_line_in = [e1.line_name for e1 in stations_line_in]
    stations_line_out = [e1.line_name for e1 in stations_line_out]

    common_line_list = list(set(stations_line_in) & set(stations_line_out))

    if len(common_line_list) < 1:
        # if there is no common line between the stations train_line can not be
        # determined for the journey should be excluded
        rv = 'NA'
    else:
        rv = common_line_list[0]
    return rv


def get_journey_times(mt: JourneyTimeMatrix):
    key1 = mt.tube_line_name + '-' + str(mt.station_in)
    key2 = mt.tube_line_name + '-' + str(mt.station_out)
    #print(key1, key2)
    lstSegs = list()
    total_journey_time = 0
    try:
        index1 = station_dict[key1]
        index2 = station_dict[key2]
        start_index = index1 if index1 < index2 else index2
        end_index = index2 if index1 < index2 else index1
        #print(key1, key2, start_index,end_index)



        for idx in range(start_index, end_index):
            station_in = station_df.iloc[idx]['start_station']
            station_out = station_df.iloc[idx+1]['start_station']
            time_taken = rd.get_time_2_out_v2(refd, station_in, station_out)
            total_journey_time = total_journey_time + time_taken
            segment_time = mt.time_in_on_train + timedelta(minutes=total_journey_time) \
                if time_taken != -1 and mt.time_in_on_train != -1 else -1

            segment_time = segment_time.time() if time_taken != -1 and mt.time_in_on_train != -1 else ''

            j = JourneySegment(mt.id, station_in, station_out, segment_time)
            lstSegs.append(j)
#            print(j)
        dfJourneyDataAll = pd.DataFrame(lstSegs)
        du.write_to_db_table(dfJourneyDataAll, db_name, tbl_name)
    except KeyError as e:
        print('Error', e)
    return total_journey_time


def calculate_time_matrix(mt: JourneyTimeMatrix) -> JourneyTimeMatrix:
    j = mt

    j.tube_line_name = get_train_line(j.station_in, j.station_out)
    if j.tube_line_name == 'NA':
        return j

    # time_2_plat is the time take to get in to platform from station entry
    time_2_plat = rd.get_time_2_plat(refd, j.station_in, j.tube_line_name)

    j.time_in_on_platform = j.time_in + timedelta(minutes=time_2_plat) \
        if time_2_plat != -1 and j.time_in != -1 else -1

    # if j.time_in_on_platform can not be found use the station time in will be used instead
    j.time_in_on_train = rd.get_time_2_train_v2(refd, j.station_in, j.tube_line_name, j.time_in_on_platform) \
        if j.time_in_on_platform != -1 else rd.get_time_2_train_v2(refd, j.station_in, j.tube_line_name, j.time_in)

    # time_2_out is the time taken for the journey between the stations
    time_2_out = get_journey_times(j)

    j.time_out_train = j.time_in_on_train + timedelta(minutes=time_2_out) \
        if time_2_out != -1 and j.time_in_on_train != -1 else -1

    # time_2_plat2 is the time taken from platform to station exit
    time_2_plat2 = rd.get_time_2_plat(refd, j.station_out, j.tube_line_name)
    j.time_out_platform_forward = -1 \
        if not time_2_plat2 or j.time_out_train == -1 or not j.time_out_train else j.time_out_train + timedelta(
        minutes=time_2_plat2)

    time_2_plat2 = rd.get_time_2_plat(refd, j.station_out, j.tube_line_name)
    j.time_out_platform_backward = j.time_out - timedelta(minutes=time_2_plat2) if time_2_plat2 != -1 else -1

    # strip the date and only use time for the file output.
    j.time_in = j.time_in.time()
    j.time_out = j.time_out.time()
    j.time_in_on_platform = j.time_in_on_platform.time() if j.time_in_on_platform != -1 else -1
    j.time_out_train = j.time_out_train.time() if j.time_out_train != -1 else -1
    j.time_in_on_train = j.time_in_on_train.time() if j.time_in_on_train != -1 else -1
    j.time_out_platform_forward = j.time_out_platform_forward.time() if j.time_out_platform_forward != -1 else -1
    j.time_out_platform_backward = j.time_out_platform_backward.time() if j.time_out_platform_backward != -1 else -1

    return j
