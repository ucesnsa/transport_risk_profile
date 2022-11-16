from dataclasses import dataclass
from datetime import datetime
from dataclasses import field


@dataclass
class RawRow:
    id: str
    idoyster: str
    idday: str
    idline: str
    si: str
    so: str
    tii: str
    tio: str


@dataclass(frozen=False, order=True)
class JourneyTimeMatrix:
    raw: RawRow = field(repr=False, metadata={"include_in_dict": False})
    id: str = field(init=False)
    id_oyster: str = field(init=False)
    id_day: int = field(init=False)
    id_tube_line: int = field(init=False)
    station_in: int = field(init=False)                 # from SCD
    station_out: int = field(init=False)                # from SCD
    time_in: datetime = field(init=False)
    time_out: datetime = field(init=False)
    tube_line_name: str = field(init=False)

    time_in_on_platform: datetime = field(init=False)   # a) this is the time_in + time_to_platform
    time_in_on_train: datetime = field(init=False)      # b) this is from the train time table, a), next train
    time_out_train: datetime = field(init=False)        # c) this b + journey time
    time_out_platform_forward: datetime = field(init=False)     # d calculate forward by adding time_out_train + platform
    time_out_platform_backward: datetime = field(init=False)    # e calculate backwards by subtracting time_time - platform
    #d and e should in theory be same/similar but e is more reliable indicator, and difference between the two
    # suggest more time has been spent on the platform_in or during the journey


    # there can be two possibilities of c) and d) to not match/close enough
    # 1. the passenger couldn't get on the next train, too busy
    # 2. the train took longer in the transit
    ###Possible idea: how much train distruction happened can be GISRUK paper, if you are interested. Or if you have another idea,
    ###we can incooperate this from this paper.

    def __post_init__(self):
        self.id = self.raw.id
        self.id_oyster = self.raw.idoyster
        self.id_day = self.raw.idday
        self.id_tube_line = self.raw.idline
        self.station_in = int(self.raw.si)
        self.station_out = int(self.raw.so)
        try:
            self.time_in = datetime.strptime('{:02d}:{:02d}'.format(*divmod(int(self.raw.tii), 60)),'%H:%M')
            self.time_out = datetime.strptime('{:02d}:{:02d}'.format(*divmod(int(self.raw.tio), 60)),'%H:%M')
        except ValueError as e:
            print ('time value great than 2400')
            self.time_in = datetime.strptime('00:00','%H:%M')
            self.time_out = datetime.strptime('00:00','%H:%M')

        self.tube_line_name = ''
        self.time_in_on_platform = ''
        self.time_in_on_train = ''
        self.time_out_train = ''
        self.time_out_platform_forward = ''
        self.time_out_platform_backward = ''

    def as_dict(self):
       return {
          k: v
          for k, v in self.__dict__.items() if k != 'raw'
       }

    @staticmethod
    def as_dict_keys() -> list:
        return [k for k in JourneyTimeMatrix.__annotations__.keys() if k != 'raw']