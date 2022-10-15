import pandas as pd


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

    def get_line_name(self, station_id):
        matches = [x for x in self.station_line_lst if x.station_id == station_id]
        return matches

    def get_station_name(self, station_id):
        matches = [x for x in self.station_line_lst if x.station_id == station_id]
        return matches[0].station_name
