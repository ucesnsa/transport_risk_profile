from typing import Iterator
import csv
from lib.risk_profile_model import JourneyTimeMatrix, RawRow
from lib.transport_data_processor import calculate_time_matrix, get_train_line

import pandas as pd
import datetime


def journey_iter(reader: csv.DictReader) -> Iterator[JourneyTimeMatrix]:
    read_max_count = 200_000
    for index, row in enumerate(reader):
        raw = RawRow(**row)  # same **kwargs i.e.  variable-length argument dictionary
        if index >= read_max_count:
            return
        yield JourneyTimeMatrix(raw)


def run_all():
    file_write = 'C:/Users/ucesnsa/Downloads/Roberto_RiskProfiles/oyster_time_matrix.csv'
    file_read = 'C:/Users/ucesnsa/Downloads/Roberto_RiskProfiles/oyster.csv'


    with open(file_read, "r") as f_in, open(file_write, "w", newline='') as f_out:
        # write output file header using the data class static method
        wrt = csv.DictWriter(f_out, JourneyTimeMatrix.as_dict_keys())
        wrt.writeheader()
        a = datetime.datetime.now()
        reader = csv.DictReader(f_in, delimiter=",")
        for i, journey in enumerate( journey_iter(reader) ):
            # write header for output
            wrt = csv.DictWriter(f_out, journey.as_dict().keys())

            if 1 == 1: #journey.raw.idday == '4':
                # calculate time matrix
                journey = calculate_time_matrix(journey)
                # write in file the risk_profile object with the additional information calculated using the
                # calculate_time_matrix function
                wrt.writerow(journey.as_dict())
                #b = datetime.datetime.now()
                #print('b-a', b - a)
if __name__ == '__main__':
    #get_train_line(796, 511)
    #print (get_time_2_out(578,643))
    run_all()

