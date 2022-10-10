from dataclasses import dataclass
import datetime
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
    station_in: str = field(init=False)
    station_out: str = field(init=False)
    time_in: datetime = field(init=False)
    time_out: datetime = field(init=False)
    time_in_on_platform: datetime = field(init=False)
    time_in_on_train: datetime = field(init=False)
    time_out_train: datetime = field(init=False)
    time_out_platform: datetime = field(init=False)

    def __post_init__(self):
        self.id = self.raw.id
        self.id_oyster = self.raw.idoyster
        self.id_day = self.raw.idday
        self.id_tube_line = self.raw.idline
        self.station_in = self.raw.si
        self.station_out = self.raw.so
        self.time_in = self.raw.tii
        self.time_out = self.raw.tio
        self.time_in_on_platform = ''
        self.time_in_on_train = ''
        self.time_out_train = ''
        self.time_out_platform = ''

    def as_dict(self):
       return {
          k: v
          for k, v in self.__dict__.items() if k != 'raw'
       }

    @staticmethod
    def as_dict_keys() -> list:
        return [k for k in JourneyTimeMatrix.__annotations__.keys() if k != 'raw']