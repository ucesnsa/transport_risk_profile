import pandas as pd
import pickle

INPUT_FILE_NAME = "London_tube_lines v2.xlsx"
OUTPUT_FILE_NAME ="tube_segments_output.xlsx"
PICKLE_DICT_FILE_NAME = '..\data\stations_dict.pkl'
PICKLE_DF_FILE_NAME = '..\data\stations_df.pkl'

def calculate_segments(line_name, df_all):
    # read excel worksheet
    process_line = line_name
    xl = pd.ExcelFile(INPUT_FILE_NAME)
    # print(xl.sheet_names)
    columns = xl.parse(process_line).columns
    converters = {column: str for column in columns}

    df_train = xl.parse(process_line, converters= converters)
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

df_all['index1'] = df_all.index
df_all['key'] = df_all[ 'line_name'] +'-'+ df_all[ 'start_station'].astype(str)

df_all = df_all[['key', 'index1', 'line_name', 'start_station', 'start_station_name']]
print (df_all.columns)

##write to excel file to be used in the main code
#df_all.to_excel(OUTPUT_FILE_NAME, sheet_name='all_lines')

# train time table
stations_dict = dict(zip(df_all.key, df_all.index1))
# write pickle after loading
with open(PICKLE_DICT_FILE_NAME, 'wb') as f:
    pickle.dump(stations_dict, f)

with open(PICKLE_DF_FILE_NAME, 'wb') as f:
    pickle.dump(df_all, f)
