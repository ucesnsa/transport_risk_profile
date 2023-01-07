import pandas as pd


INPUT_FILE_NAME = "London_tube_lines v2.xlsx"
OUTPUT_FILE_NAME ="tube_segments_output.xlsx"

def calculate_segments(line_name, df_all):
    # read excel worksheet
    process_line = line_name
    xl = pd.ExcelFile(INPUT_FILE_NAME)
    # print(xl.sheet_names)
    df_train = xl.parse(process_line)
    df_train = df_train[['station', 'start_station_id']]
    station_line_lst = list(df_train.itertuples(index=False, name=process_line))
    len1 = len(station_line_lst)
    unit_time = 2  # time between two stops , multiple this with number of stops between stations to get journey_time

    lst = []
    for idx, s in enumerate(station_line_lst):
        l1 = [process_line, station_line_lst[idx].start_station_id, station_line_lst[idx].station]
        df_all.loc[len(df_all)] = l1
    # write excel worksheet
    return df_all


## read input xlsx file to get the train line data
xl = pd.ExcelFile(INPUT_FILE_NAME)

df_all = pd.DataFrame(columns=['line_name','start_station','start_station_name'])

## read each worksheet for each train line and calcualted
for line_name in xl.sheet_names:
#for line_name in ['Jubilee','Metropolitan']:
#   line_name = 'Jubilee'
   df_all = calculate_segments(line_name, df_all)
   print (df_all.shape)


##write to excel file to be used in the main code
df_all.to_excel(OUTPUT_FILE_NAME, sheet_name='all_lines')
