from typing import Tuple, Iterator
import csv
from risk_profile_model import JourneyTimeMatrix, RawRow
from reference_data_loader import RefDataLoader


def calculate_time_matrix(mt: JourneyTimeMatrix) -> JourneyTimeMatrix:
    j = mt

    # get the lines at each station
    stations_line_in = rd.get_line_name(j.station_in)
    stations_line_out = rd.get_line_name(j.station_out)

    common_line_list = [ele1 for ele1 in stations_line_in
                        for ele2 in stations_line_out if ele1.line_name == ele2.line_name]

    # it is possible to have one journey station_in and station_out to have more than one common line
    # e.g. Finchley Road and Baker Street stations both have metropolitan line
    # in such case the first match will be picked as the selected line
    #if len(common_line_list) > 1:
    #    print ('more than 1 line',common_line_list)

    print(rd.get_station_name(j.station_in),'-->',rd.get_station_name(j.station_out),
          ' on tube line :', common_line_list[0].line_name)

    # print('station in line is', rd.get_line_name(j.station_in)[0].line_name,'station out line is',
    #      rd.get_line_name(j.station_out)[0].line_name)

    return j


def journey_iter(reader: csv.DictReader) -> Iterator[JourneyTimeMatrix]:
    read_max_count = 10000
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
    # Load all reference data
    # load the line data i.e. station code, station name, line name
    # time2plat - load the time to the platform data i.e. Station Number	station name 	LineNumber	To to platform mins
    # time2train - Time2train will tell you the difference between next train and time2platform
    # getTime2out - Select travel time between data.StationIn and data.StationOut
    rd = RefDataLoader()

    run_all()
