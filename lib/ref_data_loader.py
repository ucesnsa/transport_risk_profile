import pandas as pd
import pickle
from pathlib import Path


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
        my_file = Path("data\journey_time_dict.pkl")
        if my_file.is_file():
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

        print("Initialise reference data loader - complete")
        #        cls.train_time_table_lst = list(df_train_time_table.itertuples(index=False, name='tfl_time_table'))
        return super().__new__(cls)