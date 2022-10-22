from lib.reference_data_loader import RefDataLoader
from lib.risk_profile_model import JourneyTimeMatrix

# Load all reference data
# load the line data i.e. station code, station name, line name
rd = RefDataLoader()


# select the first common train line between the two stations
def get_train_line(station_in, station_out) -> str:
    # get the lines at each station
    stations_line_in = rd.get_line_name(station_in)
    stations_line_out = rd.get_line_name(station_out)

    common_line_list = [ele1 for ele1 in stations_line_in
                        for ele2 in stations_line_out if ele1.line_name == ele2.line_name]

    # it is possible to have one journey station_in and station_out to have more than one common line
    # e.g. Finchley Road and Baker Street stations both have metropolitan line
    # in such case the first match will be picked as the selected line
    # if len(common_line_list) > 1:
    #    print ('more than 1 line',common_line_list)

    print(rd.get_station_name(station_in), '-->', rd.get_station_name(station_out),
          ' on tube line :', common_line_list[0].line_name)

    # print('station in line is', rd.get_line_name(j.station_in)[0].line_name,'station out line is',
    #      rd.get_line_name(j.station_out)[0].line_name)

    return rd.get_line_name(station_out)[0].line_name


def calculate_time_matrix(mt: JourneyTimeMatrix) -> JourneyTimeMatrix:
    j = mt

    j.tube_line_name = get_train_line(j.station_in, j.station_out)

    # test data
    j.time_in_on_platform = int(j.time_in) + rd.get_time_2_plat(670, 'Bakerloo')
    j.time_in_on_train = rd.get_time_2_train(597, 'Bakerloo', 1016)
    j.time_out_train = int(j.time_in_on_train) + rd.get_Time_2_out(597, 620)
    j.time_out_platform = int(j.time_out) - rd.get_time_2_plat(670, 'Bakerloo')


#    j.time_in_on_platform = j.time_in + rd.get_time_2_plat(j.station_in, j.tube_line_name)

#    j.time_in_on_train = rd.get_time_2_train(j.station_in, j.tube_line_name,j.time_in_on_platform)

#    j.time_out_train = rd.get_Time_2_out(j.station_in, j.station_out)

#    j.time_out_platform = j.time_out - rd.get_time_2_plat(j.station_out, j.tube_line_name)

    return j