import pandas as pd
import pandas as pd
import openpyxl


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


#change time vales in 24h format
#look at the arrival time and departure time
#you may add weekend and weekday column too/ask Roberto

#print(convert_to_preferred_format(90480))


def calculate_line_times(line_name, df_all):
   # read excel worksheet
   process_line = line_name
   xl = pd.ExcelFile("London_tube_lines v2.xlsx")
   #print(xl.sheet_names)
   df_train = xl.parse(process_line)
   df_train = df_train[['station','start_station_id']]
   station_line_lst = list(df_train.itertuples(index=False, name=process_line))
   len1 = len(station_line_lst)
   unit_time = 2 # time between two stops , multiple this with number of stops between stations to get journey_time

   lst = []
   for idx, s in enumerate (station_line_lst):
         for i in range(0, idx):
            l1 = [process_line,station_line_lst[idx].start_station_id,station_line_lst[idx].station,
                  station_line_lst[i].start_station_id,station_line_lst[i].station, (idx-i)*unit_time]
            #lst.append(l1)
            df_all.loc[len(df_all)] = l1
            #print(station_line_lst[idx].start_station_id, station_line_lst[i].start_station_id,'cost:', (idx-i)*unit_time )

         for j in range(idx, len1):
            l2 = [process_line,station_line_lst[idx].start_station_id,station_line_lst[idx].station,
                  station_line_lst[j].start_station_id,station_line_lst[j].station, (j-idx) * unit_time]
            df_all.loc[len(df_all)] = l2
            #print(station_line_lst[idx].start_station_id, station_line_lst[j].start_station_id,'cost:', (j-idx)*unit_time )

   # write excel worksheet
   return df_all

df_all = pd.DataFrame(columns=['line_name','start_station','start_station_name','end_station','end_station_name','time_cost'])

## read input xlsx file to get the train line data
xl = pd.ExcelFile("London_tube_lines v2.xlsx")

## read each worksheet for each train line and calcualted
for line_name in xl.sheet_names:
#for line_name in ['Jubilee','Metropolitan']:
#   line_name = 'Jubilee'
   df_all = calculate_line_times(line_name, df_all)
   print (df_all.shape)


##write to excel file to be used in the main code
df_all.to_excel("London_tube_lines_output.xlsx", sheet_name='all_lines')


## test stub
def test():
   unit_time =2
   idx = 5
   len1 = 10
   for i in range(0, idx):
      print('going up cost:', i, (idx-i)*unit_time)

   for j in range(idx, len1):
      print('going down cost', j, (j-idx)*unit_time)
#test()