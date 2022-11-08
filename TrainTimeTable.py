import pandas as pd

#read station nlc and code match data
df_station_nlc_code = pd.read_csv('C:/Users/ucesnsa/Downloads/Roberto_RiskProfiles/London_stations_NLC_CODE.csv')
#drop the columns which are not necessary
df_station_nlc_code = df_station_nlc_code.drop(columns=['tfl_station_nm', 'station_nm', 'train_time_table_station_name'])
print(df_station_nlc_code.head(3))


#read clean files, add headers for the columns in each file

df_jubilee = pd.read_csv('C:/Users/ucesnsa/Downloads/Roberto_RiskProfiles/timetables/mondayFriday/MTF/jubilee_clean.txt', header=None)
df_bakerloo = pd.read_csv('C:/Users/ucesnsa/Downloads/Roberto_RiskProfiles/timetables/mondayFriday/MTF/bakerloo_clean.txt',header=None)
df_central = pd.read_csv('C:/Users/ucesnsa/Downloads/Roberto_RiskProfiles/timetables/mondayFriday/MTF/central_clean.txt', header=None)
df_circle = pd.read_csv('C:/Users/ucesnsa/Downloads/Roberto_RiskProfiles/timetables/mondayFriday/MTF/circle_clean.txt', header=None)
df_district = pd.read_csv('C:/Users/ucesnsa/Downloads/Roberto_RiskProfiles/timetables/mondayFriday/MTF/district_clean.txt', header=None)
df_metropolitan = pd.read_csv('C:/Users/ucesnsa/Downloads/Roberto_RiskProfiles/timetables/mondayFriday/MTF/metropolitan_clean.txt', header=None)
df_northern = pd.read_csv('C:/Users/ucesnsa/Downloads/Roberto_RiskProfiles/timetables/mondayFriday/MTF/northern_clean.txt', header=None)
df_picadilly = pd.read_csv('C:/Users/ucesnsa/Downloads/Roberto_RiskProfiles/timetables/mondayFriday/MTF/picadilly_clean.txt', header=None)
df_victoria =pd.read_csv('C:/Users/ucesnsa/Downloads/Roberto_RiskProfiles/timetables/mondayFriday/MTF/victoria_clean.txt', header=None)
df_waterloo =pd.read_csv('C:/Users/ucesnsa/Downloads/Roberto_RiskProfiles/timetables/mondayFriday/MTF/waterloo_clean.txt', header=None)

col_Names = ['TripNumber', 'Record Identifier', '(Trip Start)Site','LocationType', 'Direction', 'ArrivalTime', 'DepartureTime', 'Mode','Facility Number']
df_jubilee.columns = col_Names
df_bakerloo.columns = col_Names
df_central.columns = col_Names
df_circle.columns = col_Names
df_district.columns = col_Names
df_metropolitan.columns = col_Names
df_northern.columns = col_Names
df_picadilly.columns = col_Names
df_victoria.columns = col_Names
df_waterloo.columns = col_Names

#add column to represent the line name
df_jubilee['line_name'] = 'jubilee'
df_bakerloo['line_name'] = 'bakerloo'
df_central['line_name'] = 'central'
df_circle['line_name'] = 'circle'
df_district['line_name'] = 'district'
df_metropolitan['line_name'] = 'metropolitan'
df_northern['line_name'] = 'northern'
df_picadilly['line_name'] = 'picadilly'
df_victoria['line_name'] = 'victoria'
df_waterloo['line_name'] = 'waterloo'

#drop the columns which are not necessary
df_jubilee = df_jubilee.drop(columns=['TripNumber', 'Record Identifier','LocationType', 'Direction','Mode','Facility Number'])
df_bakerloo = df_bakerloo.drop(columns=['TripNumber', 'Record Identifier','LocationType', 'Direction','Mode','Facility Number'])
df_central = df_central.drop(columns=['TripNumber', 'Record Identifier','LocationType', 'Direction','Mode','Facility Number'])
df_circle = df_circle.drop(columns=['TripNumber', 'Record Identifier','LocationType', 'Direction','Mode','Facility Number'])
df_district = df_district.drop(columns=['TripNumber', 'Record Identifier','LocationType', 'Direction','Mode','Facility Number'])
df_metropolitan = df_metropolitan.drop(columns=['TripNumber', 'Record Identifier','LocationType', 'Direction','Mode','Facility Number'])
df_northern = df_northern.drop(columns=['TripNumber', 'Record Identifier','LocationType', 'Direction','Mode','Facility Number'])
df_picadilly = df_picadilly.drop(columns=['TripNumber', 'Record Identifier','LocationType', 'Direction','Mode','Facility Number'])
df_victoria = df_victoria.drop(columns=['TripNumber', 'Record Identifier','LocationType', 'Direction','Mode','Facility Number'])
df_waterloo = df_waterloo.drop(columns=['TripNumber', 'Record Identifier','LocationType', 'Direction','Mode','Facility Number'])

print(df_jubilee.head(3))
print(df_bakerloo.head(3))
print(df_central.head(3))
print(df_circle.head(3))
print(df_district.head(3))
print(df_northern.head(3))
print(df_victoria.head(3))
print(df_waterloo.head(3))

count_row_jubilee = df_jubilee.shape[0]  # Gives number of rows
count_row_bakerloo = df_bakerloo.shape[0]  # Gives number of rows
count_row_central = df_central.shape[0]  # Gives number of rows
count_row_circle = df_circle.shape[0]  # Gives number of rows
count_row_district = df_district.shape[0]  # Gives number of rows
count_row_northern = df_northern.shape[0]  # Gives number of rows
count_row_victoria = df_victoria.shape[0]  # Gives number of rows
count_row_waterloo = df_waterloo.shape[0]  # Gives number of rows

print(count_row_jubilee)
print(count_row_bakerloo)
print(count_row_central)
print(count_row_circle)
print(count_row_district)
print(count_row_northern)
print(count_row_victoria)
print(count_row_waterloo)

#Combining Data Across Rows or Columns
df_all_lines = pd.concat([df_jubilee, df_bakerloo, df_central, df_circle, df_district, df_northern, df_victoria, df_waterloo])
count_row_all_lines = df_all_lines.shape[0]  # Gives number of rows
print(count_row_all_lines)
print(df_all_lines.head(3))

#find the unique values in Trip Start Side
print(df_all_lines["(Trip Start)Site"].unique())
#count unique values as a station code
uniqueValues = df_all_lines['(Trip Start)Site'].nunique()
print(uniqueValues)


#left join to clarify nlc code from the data
#df_all_lines.merge(df_station_nlc_code, on='(Trip Start)Site', how='left')
df_TrainTimeTable=pd.merge(df_all_lines,df_station_nlc_code, on='(Trip Start)Site', how='left')
print(df_TrainTimeTable)
#show NAN values
print(df_TrainTimeTable[df_TrainTimeTable['ArrivalTime'].isnull()])
print(df_TrainTimeTable[df_TrainTimeTable['nlc'].isnull()])

##################
#drop NAN values from nlc, because the data captured from overground stations
#################
df_TrainTimeTable = df_TrainTimeTable.dropna(subset=['nlc'])
print(df_TrainTimeTable.head(3))

#df_TrainTimeTable = df_TrainTimeTable.fillna(subset=['ArrivalTime'])
df_TrainTimeTable['ArrivalTime'] = df_TrainTimeTable['ArrivalTime'].fillna(0).astype(int)
df_TrainTimeTable['DepartureTime'] = df_TrainTimeTable['DepartureTime'].fillna(0).astype(int)
print(df_TrainTimeTable.head(3))


def convert_to_preferred_format(sec):
   sec = sec % (24 * 3600)
   hour = sec // 3600
   sec %= 3600
   min = sec // 60
   sec %= 60
   print("seconds value in hours:",hour)
   print("seconds value in minutes:",min)
   ##return "%02d:%02d:%02d" % (hour, min, sec)
   return "%02d%02d" % (hour, min)

df_TrainTimeTable['ArrivalTime'] = df_TrainTimeTable['ArrivalTime'].apply(convert_to_preferred_format)
df_TrainTimeTable['DepartureTime'] = df_TrainTimeTable['DepartureTime'].apply(convert_to_preferred_format)

print(df_TrainTimeTable.head(3))
df_TrainTimeTable.to_csv("C:/Users/ucesnsa/Downloads/Roberto_RiskProfiles/df_TrainTimeTable.csv")


