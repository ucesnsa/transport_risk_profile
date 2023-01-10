-- pre-filter delete if header is included in the data
delete from tbl_time_matrix where id_day='id_day'

/* exclusion status for the dataset*/
SELECT 
sum( case when time_in = '00:00:00' or time_out = '00:00:00'  then 1 else 0 end ) cnt_24Plus_jrys,
sum( case when tube_line_name = 'NA' then 1 else 0 end ) cnt_connecting_jrys,
sum( case when station_in = station_out then 1 else 0 end ) cnt_same_station_jrys,
sum( case when tube_line_name = 'Overground' then 1 else 0 end ) cnt_overground_jrys,
sum( case when tube_line_name = 'Overground' or station_in = station_out or tube_line_name = 'NA' or time_in = '00:00:00' or time_out = '00:00:00' then 1 else 0 end )as cnt_excl_jrys,
sum( case when time_out_train = '-1' then 1 else 0 end ) as cnt_time_out_train_na, 
count(*) as total_jrys
from tbl_time_matrix 


select id_day, tube_line_name, count(*) 
from tbl_time_matrix 
group by id_day, tube_line_name


-- Counting people exiting the station (count people from A to B) as walk_in_platform 
-- Counting people exiting the station (count people from B to C) as platform_wait_in
-- Counting people exiting the station (count people from D to E) as walk_out_platform - v1
-- Counting people exiting the station (count people from D to E) as walk_out_platform, -v2  excluding people leaving out based on calculated time_out

with select_jrys as 
( select 
id,id_oyster,id_day, id_tube_line,station_in,station_out,tube_line_name,time_in::time without time zone as time_in, 
time_out::time without time zone as time_out,
(case when time_in_on_platform ='-1' then '00:00' else time_in_on_platform end)::time without time zone time_in_on_platform,
(case when time_in_on_train ='-1' then '00:00' else time_in_on_train end)::time without time zone time_in_on_train,
(case when time_out_train ='-1' then '00:00' else time_out_train end)::time without time zone time_out_train,
(case when time_out_platform_forward ='-1' then '00:00' else time_out_platform_forward end)::time without time zone time_out_platform_forward,
(case when time_out_platform_backward ='-1' then '00:00' else time_out_platform_backward end)::time without time zone time_out_platform_backward,
case when tube_line_name = 'Overground' or station_in = station_out or tube_line_name = 'NA' or time_in = '00:00:00' or time_out = '00:00:00' then 1 else 0 end excl_flag
from tbl_time_matrix where 
--id_tube_line='12' and
 tube_line_name='Victoria' and 
id_day='4'
and time_out_train != '-1'
),
w as
(SELECT dd as day_window,date_trunc('minute', tm)::time as min_window FROM 
generate_series ( 1,8,1) dd , 
generate_series
        ( '2022-10-01'::timestamp 
        , '2022-10-02'::timestamp
        , '1 minute'::interval) tm 
        )
        
select 'walk_in_platform' as typ,id_day, station_in as station,tube_line_name, w.min_window,
count(*) as j_count from w left join select_jrys as b on 
w.day_window = cast(id_day as int) and w.min_window between b.time_in and b.time_in_on_platform 
where excl_flag=0
group by id_day, station_in,tube_line_name, w.min_window

union all 
select 'platform_wait_in' as typ,id_day, station_in as station, tube_line_name,w.min_window,
count(*) as j_count from w left join select_jrys as b on 
w.day_window = cast(id_day as int) and w.min_window between b.time_in_on_platform and b.time_in_on_train 
where excl_flag=0
group by id_day, station_in,tube_line_name, w.min_window

union all 
select 'walk_out_platform' as typ,id_day, station_out as station, tube_line_name,w.min_window,
count(*) as j_count from w left join select_jrys as b on 
w.day_window = cast(id_day as int) and w.min_window between b.time_out_train and b.time_out 
where excl_flag=0
group by id_day, station_out,tube_line_name, w.min_window

union all 

select 'on_train' as typ,id_day, s.end_station as station, b.tube_line_name,s.segment_time as min_window,
count(*) as j_count from journey_segments s inner join select_jrys as b on s.id = b.id 
where excl_flag=0
--and s.end_station='511'
group by id_day, s.end_station, tube_line_name,s.segment_time
--order by s.segment_time







--*****************************************************
-- this is a test query to analyze individual journeys
with select_jrys as 
( select 
id,id_oyster,id_day, id_tube_line,tube_line_name,station_in,station_out, time_in::time without time zone as time_in, 
time_out::time without time zone as time_out,
(case when time_in_on_platform ='-1' then '00:00:00' else time_in_on_platform end)::time without time zone time_in_on_platform,
(case when time_in_on_train ='-1' then '00:00:00' else time_in_on_train end)::time without time zone time_in_on_train,
(case when time_out_train ='-1' then '00:00:00' else time_out_train end)::time without time zone time_out_train,
(case when time_out_platform_forward ='-1' then '00:00:00' else time_out_platform_forward end)::time without time zone time_out_platform_forward,
(case when time_out_platform_backward ='-1' then '00:00:00' else time_out_platform_backward end)::time without time zone time_out_platform_backward,
case when tube_line_name = 'Overground' or station_in = station_out or tube_line_name = 'NA' or time_in = '00:00:00' or time_out = '00:00:00' then 1 else 0 end excl_flag
from tbl_time_matrix 
where --id_tube_line='12' and tube_line_name='Victoria' and id_day='4' and 
time_out_train != '-1'
)

select id_day, tube_line_name, 
 (CASE WHEN (time_out-time_out_platform_forward < INTERVAL '0') THEN (-(time_out-time_out_platform_forward)) ELSE time_out-time_out_platform_forward END) AS abs_diff,
count(*)
from select_jrys 
group by id_day, tube_line_name, (CASE WHEN (time_out-time_out_platform_forward < INTERVAL '0') THEN (-(time_out-time_out_platform_forward)) ELSE time_out-time_out_platform_forward END)

--*****************************************************


-- 86,173 total (time_out_platform_forward > time_out)
-- 187,355 total , Wed Victoria line 
-- 166,313 total , Wed Victoria line  exlude where no train time out could be calucated i.e. train journey time was not in the refernece data
-- train time calculations 
SELECT count(*) FROM journey_segments;

SELECT * FROM journey_segments s limit 10 
  

