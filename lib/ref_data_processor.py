from datetime import datetime

def get_line_name(refd, station_id) -> list:
    matches = [x for x in refd.station_line_lst if x.station_id == station_id]
    return matches


def get_station_name(refd, station_id) -> str:
    matches = [x for x in refd.station_line_lst if x.station_id == station_id]
    return matches[0].station_name


# time2plat - load the time to the platform data i.e. Station Number	station name 	LineNumber	To to platform mins
# return mins from tap in to platform
def get_time_2_plat(refd, station_id, line_name):
    matches = [x for x in refd.platform_time_lst if x.station_id == station_id and x.line_name == line_name]

    rv = -1
    try:
        rv = int(matches[0].time_taken)
    except ValueError as e:
        print('Error', e)
    except IndexError as e:
        print('Error', e)

    return rv


# time2train - Time2train will tell you the difference between next train and time2platform
# use the train timetable(ref data), station, line and current time to get the next train time
def get_time_2_train(refd, station_id, line_name, current_time):
    matches = [x for x in refd.train_time_table_lst if x.station_id == station_id
               and x.line_name == line_name and datetime.strptime(str(x.arrival_time).zfill(4),
                                                                  '%H%M') >= current_time]

    rv = -1
    try:
        rv = min(matches, key=lambda k: k.arrival_time).arrival_time
        rv = datetime.strptime(str(rv).zfill(4), '%H%M')
    except ValueError as e:
        print('Error', e)
    except IndexError as e:
        print('Error', e)
    return rv


def get_time_2_train_v2(refd, station_id, line_name, current_time):
    rv = -1
    rvt = -1
    try:
        station_lst = refd.station_time_table_dict[station_id]
        station_arrival_time_lst = [x.arrival_time for x in station_lst]
        # matches = [x.arrival_time for x in station_lst if datetime.strptime(str(x.arrival_time).zfill(4),
        #                                                              '%H%M') >= current_time]

        # rv = min(matches, key=lambda k: k.arrival_time).arrival_time

        c_time = str(current_time.hour).zfill(2) + str(current_time.minute).zfill(2)
        rv = min(station_arrival_time_lst, key=lambda x: abs(x - int(c_time)))
        rvt = datetime.strptime(str(rv).zfill(4), '%H%M')
    except ValueError as e:
        print('Error', e)
    except IndexError as e:
        print('Error', e)
    except:
        print('Any error')
    return rvt


# getTime2out - Select travel time between data.StationIn and data.StationOut
def get_time_2_out(refd, station_in_id, station_out_id) -> int:
    matches = [x for x in refd.journey_time_lst if x.start_station_id == station_in_id
               and x.end_station_id == station_out_id]

    if len(matches) == 0:
        matches = [x for x in refd.journey_time_lst if x.end_station_id == station_in_id
                   and x.start_station_id == station_out_id]
    if len(matches) == 0:
        matches = [x for x in refd.journey_time_ex_lst if x.start_station_id == station_in_id
                   and x.end_station_id == station_out_id]
    if len(matches) == 0:
        matches = [x for x in refd.journey_time_ex_lst if x.end_station_id == station_in_id
                   and x.start_station_id == station_out_id]

    rv = -1
    try:
        if len(matches) > 1:
            print('more than one time found selecting the smallest')
            rv_min = matches[0].time_taken
            for a in matches:
                if a.time_taken < rv_min:
                    rv = a.time_taken
                    rv_min = a.time_taken
                else:
                    rv = rv_min
        else:
            rv = int(matches[0].time_taken)
        rv_new = refd.journey_time_dict[station_in_id][station_out_id]
        print('compare journey times', rv, rv_new)
    except ValueError as e:
        print('Error', e)
    except IndexError as e:
        print('Error', e)
    return rv


def get_time_2_out_v2(refd, station_in_id, station_out_id) -> int:
    rv = -1
    try:
        rv = int(refd.journey_time_dict[station_in_id][station_out_id])
    except ValueError as e:
        print('Error', e)
    except IndexError as e:
        print('Error', e)
    except KeyError as e:
        print('KeyError', e)
    return rv
