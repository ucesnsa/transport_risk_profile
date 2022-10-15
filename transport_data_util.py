from reference_data_loader import RefDataLoader

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


# time2plat - load the time to the platform data i.e. Station Number	station name 	LineNumber	To to platform mins
# return mins from tap in to platform
def time2plat(station, line_name) -> int:
    pass


# time2train - Time2train will tell you the difference between next train and time2platform
# use the train timetable(ref data), station, line and current time to get the next train time
def time2train(station, line_name, current_time):
    pass


# getTime2out - Select travel time between data.StationIn and data.StationOut
def getTime2out(station_in, station_out):
    pass
