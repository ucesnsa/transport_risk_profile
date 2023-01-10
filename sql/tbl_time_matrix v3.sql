-- pre-filter delete if header is included in the data
delete from tbl_time_matrix where id_day='id_day'

/* exclusion status for the dataset*/
SELECT 
sum( case when time_in = '00:00:00' or time_out = '00:00:00'  then 1 else 0 end ) cnt_24Plus_jrys,
sum( case when tube_line_name = 'NA' then 1 else 0 end ) cnt_connecting_jrys,
sum( case when station_in = station_out then 1 else 0 end ) cnt_same_station_jrys,
sum( case when tube_line_name = 'Overground' then 1 else 0 end ) cnt_overground_jrys,
sum( case when tube_line_name = 'Overground' or station_in = station_out or tube_line_name = 'NA' or time_in = '00:00:00' or time_out = '00:00:00' then 1 else 0 end )as cnt_excl_jrys,
count(*) as total_jrys
from tbl_time_matrix 


--platform in 
-- on the platform is the time between a)time_in_on_platform and b)time_in_on train, e.g. if a passenger was a=1505 and b=1510, he/she spent 5 mins on the platform 
-- the passenger will be counted in for each time slot between 1505 and 1510 i.e 1505, 1506, 1507, 1508, 1509 and 1510
-- on the platform count by min 
with select_jrys as 
( select 
id,id_oyster,id_day, id_tube_line,station_in,station_out, time_in, time_out,
(case when time_in_on_platform ='-1' then '00:00' else time_in_on_platform end)::time without time zone time_in_on_platform,
(case when time_in_on_train ='-1' then '00:00' else time_in_on_train end)::time without time zone time_in_on_train,
(case when time_out_train ='-1' then '00:00' else time_out_train end)::time without time zone time_out_train,
(case when time_out_platform_forward ='-1' then '00:00' else time_out_platform_forward end)::time without time zone time_out_platform_forward,
(case when time_out_platform_backward ='-1' then '00:00' else time_out_platform_backward end)::time without time zone time_out_platform_backward,
case when tube_line_name = 'Overground' or station_in = station_out or tube_line_name = 'NA' or time_in = '00:00:00' or time_out = '00:00:00' then 1 else 0 end excl_flag
from tbl_time_matrix where id_tube_line='12' and tube_line_name='Victoria'),
w as
(SELECT dd as day_window,date_trunc('minute', tm)::time as min_window FROM 
generate_series ( 1,8,1) dd , 
generate_series
        ( '2022-10-01'::timestamp 
        , '2022-10-02'::timestamp
        , '1 minute'::interval) tm 
        )
select 'platform_in' as typ,id_day, station_in, w.min_window,
--,w.min_window,b.time_in_on_platform,b.time_in_on_train  
count(*) as j_count from w left join select_jrys as b on 
w.day_window = cast(id_day as int) and w.min_window between b.time_in_on_platform and b.time_in_on_train 
where excl_flag=0
group by id_day, station_in, w.min_window
union all 
SELECT 'platform_out' as typ, id_day, station_out, time_out_platform_backward,  
count(*) as cnt FROM select_jrys where excl_flag = 0 
group by id_day, station_out, time_out_platform_backward
order by 1,2,3,4



with select_jrys as 
( select 
*,
case when tube_line_name = 'Overground' or station_in = station_out or tube_line_name = 'NA' or time_in = '00:00:00' or time_out = '00:00:00' then 1 else 0 end excl_flag
from tbl_time_matrix)
select 
sum(case when Extract(epoch FROM (time_out_platform_forward::time - time_out::time))/60 <2 then 1 else 0 end) as count_less_than_2, 
sum(case when Extract(epoch FROM (time_out_platform_forward::time - time_out::time))/60 between 3 and 4 then 1 else 0 end) as count_between_2_3
sum(case when Extract(epoch FROM (time_out_platform_forward::time - time_out::time))/60 between 5 and 6 then 1 else 0 end) as count_between_4_5,
sum(case when Extract(epoch FROM (time_out_platform_forward::time - time_out::time))/60 between 7 and 8 then 1 else 0 end) as count_between_6_7,
sum(case when Extract(epoch FROM (time_out_platform_forward::time - time_out::time))/60 > 8 then 1 else 0 end) as count_greater_8
--*
--count(*) 
from select_jrys where excl_flag=0 and id_day='4'
and time_out_platform_forward > time_out


-- 86,173 total (time_out_platform_forward > time_out)
-- 187,355 total 
