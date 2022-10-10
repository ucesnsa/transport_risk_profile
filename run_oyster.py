from typing import Tuple, Iterator
import csv
from risk_profile_model import JourneyTimeMatrix, RawRow


def calculate_time_matrix(mt: JourneyTimeMatrix) -> JourneyTimeMatrix:
    j = mt
    return j


def journey_iter(reader: csv.DictReader) -> Iterator[JourneyTimeMatrix]:
    read_max_count = 100
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

        reader = csv.DictReader(f_in, delimiter=",")
        for journey in journey_iter(reader):
            # write header for output
            wrt = csv.DictWriter(f_out, journey.as_dict().keys())

            # calculate time matrix
            journey = calculate_time_matrix(journey)

            wrt.writerow(journey.as_dict())


if __name__ == '__main__':
    run_all()