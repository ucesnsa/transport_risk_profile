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

    def __new__(cls, *args, **kwargs):
        print("Initialise reference data loader")
        xl = pd.ExcelFile("data/train_location_line_geo.xlsx")
        print(xl.sheet_names)
        df = xl.parse("train_location_line_geo")

        cls.station_line_lst = list(df.itertuples(index=False, name='station_line'))
        return super().__new__(cls)

    def get_line_name(self, station_id):
        matches = [x for x in self.station_line_lst if x.station_id == station_id]
        return matches

    def get_station_name(self, station_id):
        matches = [x for x in self.station_line_lst if x.station_id == station_id]
        return matches[0].station_name
