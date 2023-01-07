import pandas as pd
from datetime import datetime
import pickle


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class RefDataLoader(object):
    def __repr__(self):
        return 'Reference data loader'

    __metaclass__ = Singleton
    station_line_lst = None
    platform_time_lst = None
    journey_time_lst = None
    train_time_table_lst = None
    station_time_table_dict = None
    train_time_table_lst = None
    journey_time_dict = None

    def __new__(cls, *args, **kwargs):
        t1 = datetime.now()
        print("Initialise reference data loader")
        xl = pd.ExcelFile("data/transport_risk_ref_data.xlsx")

        print(xl.sheet_names)
        df_train = xl.parse("train_location_line_geo")
        df_platform_time = xl.parse("time_to_plat")
        df_journey_time = xl.parse("journey_time")
        columns = xl.parse("journey_time_ex").columns
        converters = {column: int for column in columns}
        df_journey_time_ex = xl.parse("journey_time_ex", converters=converters)
        df_train_time_table = xl.parse("train_time_table")

        cls.station_line_lst = list(df_train.itertuples(index=False, name='station_line'))
        cls.platform_time_lst = list(df_platform_time.itertuples(index=False, name='platform_time'))
        cls.journey_time_lst = list(df_journey_time.itertuples(index=False, name='journey_time'))
        cls.journey_time_ex_lst = list(df_journey_time_ex.itertuples(index=False, name='journey_time_ex'))

        # train time table
        unique_station_ids = df_train_time_table.station_id.unique()
        cls.station_time_table_dict = {elem: list() for elem in unique_station_ids}

        # create a 1D dictionary of to lookup train time from train timetable
        for key in cls.station_time_table_dict.keys():
            cls.station_time_table_dict[key] = \
                list(df_train_time_table[:][df_train_time_table.station_id == key].itertuples(index=False))

        # create a 2D dictionary to lookup journey time
        # read pickle
        with open('data\journey_time_dict.pkl', 'rb') as f:
            cls.journey_time_dict = pickle.load(f)

        if cls.journey_time_dict is None:
            cls.journey_time_dict = {elem: dict() for elem in unique_station_ids}
            for key in cls.station_time_table_dict.keys():
                for key2 in cls.station_time_table_dict.keys():
                    temp = df_journey_time_ex.loc[((df_journey_time_ex['start_station_id'] == key) & (
                            df_journey_time_ex['end_station_id'] == key2)), 'time_taken']
                    try:
                        tm = min(temp.tolist())
                        cls.journey_time_dict[key][key2] = tm
                    except ValueError as e:
                        cls.journey_time_dict[key][key2] = -1
            # write pickle after loading
            with open('data\journey_time_dict.pkl', 'wb') as f:
                pickle.dump(cls.journey_time_dict, f)

        t2 = datetime.now()
        print('loading train time reference data  (t2 - t1) : ', t2 - t1)
        print("Initialise reference data loader")

        #        cls.train_time_table_lst = list(df_train_time_table.itertuples(index=False, name='tfl_time_table'))
        return super().__new__(cls)

    def get_line_name(self, station_id) -> list:
        matches = [x for x in self.station_line_lst if x.station_id == station_id]
        return matches

    def get_station_name(self, station_id) -> str:
        matches = [x for x in self.station_line_lst if x.station_id == station_id]
        return matches[0].station_name

    # time2plat - load the time to the platform data i.e. Station Number	station name 	LineNumber	To to platform mins
    # return mins from tap in to platform
    def get_time_2_plat(self, station_id, line_name):
        matches = [x for x in self.platform_time_lst if x.station_id == station_id and x.line_name == line_name]

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
    def get_time_2_train(self, station_id, line_name, current_time):
        matches = [x for x in self.train_time_table_lst if x.station_id == station_id
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

    def get_time_2_train_v2(self, station_id, line_name, current_time):
        rv = -1
        rvt = -1
        try:
            station_lst = self.station_time_table_dict[station_id]
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
    def get_time_2_out(self, station_in_id, station_out_id) -> int:
        matches = [x for x in self.journey_time_lst if x.start_station_id == station_in_id
                   and x.end_station_id == station_out_id]

        if len(matches) == 0:
            matches = [x for x in self.journey_time_lst if x.end_station_id == station_in_id
                       and x.start_station_id == station_out_id]
        if len(matches) == 0:
            matches = [x for x in self.journey_time_ex_lst if x.start_station_id == station_in_id
                       and x.end_station_id == station_out_id]
        if len(matches) == 0:
            matches = [x for x in self.journey_time_ex_lst if x.end_station_id == station_in_id
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
            rv_new = self.journey_time_dict[station_in_id][station_out_id]
            print('compare journey times', rv, rv_new)
        except ValueError as e:
            print('Error', e)
        except IndexError as e:
            print('Error', e)
        return rv

    def get_time_2_out_v2(self, station_in_id, station_out_id) -> int:
        rv = -1
        try:
            rv = int(self.journey_time_dict[station_in_id][station_out_id])
        except ValueError as e:
            print('Error', e)
        except IndexError as e:
            print('Error', e)
        except KeyError as e:
            print('KeyError', e)
        return rv