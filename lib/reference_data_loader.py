import pandas as pd
from datetime import datetime
from operator import itemgetter


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

    def __new__(cls, *args, **kwargs):
        print("Initialise reference data loader")
        xl = pd.ExcelFile("data/transport_risk_ref_data.xlsx")
        print(xl.sheet_names)
        df_train = xl.parse("train_location_line_geo")
        df_platform_time = xl.parse("time_to_plat")
        df_journey_time = xl.parse("journey_time")
        df_train_time_table = xl.parse("train_time_table")

        cls.station_line_lst = list(df_train.itertuples(index=False, name='station_line'))
        cls.platform_time_lst = list(df_platform_time.itertuples(index=False, name='platform_time'))
        cls.journey_time_lst = list(df_journey_time.itertuples(index=False, name='journey_time'))
        cls.train_time_table_lst = list(df_train_time_table.itertuples(index=False, name='train_time_table'))
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
    def get_time_2_train(self, station_id, line_name, current_time) :


        matches = [x for x in self.train_time_table_lst if x.station_id == station_id
                   and x.line_name == line_name and datetime.strptime(str(x.arrival_time).zfill(4),'%H%M') >= current_time]

        rv = -1
        try:
            rv = min(matches, key=lambda k: k.arrival_time).arrival_time
            rv = datetime.strptime(str(rv).zfill(4), '%H%M')
        except ValueError as e:
            print('Error', e)
        except IndexError as e:
            print('Error', e)
        return rv

    # getTime2out - Select travel time between data.StationIn and data.StationOut
    def get_time_2_out(self, station_in_id, station_out_id) -> int:
        matches = [x for x in self.journey_time_lst if x.start_station_id == station_in_id
                   and x.end_station_id == station_out_id]

        rv = -1
        try:
            rv = int(matches[0].time_taken)
        except ValueError as e:
            print('Error', e)
        except IndexError as e:
            print('Error', e)
        return rv
