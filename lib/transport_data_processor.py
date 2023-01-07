from lib.ref_data_loader import RefDataLoader
from lib.risk_profile_model import JourneyTimeMatrix
import lib.ref_data_processor as rd
from datetime import datetime, timedelta
import pickle
import datetime

# Load all reference data
# load the line data i.e. station code, station name, line name
refd = RefDataLoader()


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
    return rd.get_time_2_out_v2(refd, mt.station_in, mt.station_out)


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
