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


--step 1a - delete summary table  
drop table tbl_time_matrix_summary_fwd;
drop table tbl_time_matrix_summary_bwd;

--step 1b , create a table to summarize results for platforms (in,out), excluding all the journeys not requird to be considered 
-- time on platform in and time on platform out 
-- using platform_out from the forward calculations
create table tbl_time_matrix_summary_fwd as 
with select_jrys as 
( select case when tube_line_name = 'Overground' or station_in = station_out or tube_line_name = 'NA' or time_in = '00:00:00' or time_out = '00:00:00' then 1 else 0 end excl_flag,
* from tbl_time_matrix )
select typ, id_day, station, time_on_platform, cnt from 
(SELECT 'platform_in' as typ, id_day, station_in as station, time_in_on_platform as time_on_platform, count(*) as cnt FROM select_jrys where excl_flag = 0 
group by id_day, station_in, time_in_on_platform
union all 
SELECT 'platform_out' as typ, id_day, station_out, time_out_platform_forward, count(*) as cnt FROM select_jrys where excl_flag = 0 
group by id_day, station_out, time_out_platform_forward
) a

-- using platform_out from the backward calculations
create table tbl_time_matrix_summary_bwd as 
with select_jrys as 
( select case when tube_line_name = 'Overground' or station_in = station_out or tube_line_name = 'NA' or time_in = '00:00:00' or time_out = '00:00:00' then 1 else 0 end excl_flag,
* from tbl_time_matrix )
select typ, id_day, station, time_on_platform, cnt from 
(SELECT 'platform_in' as typ, id_day, station_in as station, time_in_on_platform as time_on_platform, count(*) as cnt FROM select_jrys where excl_flag = 0 
group by id_day, station_in, time_in_on_platform
union all 
SELECT 'platform_out' as typ, id_day, station_out, time_out_platform_backward, count(*) as cnt FROM select_jrys where excl_flag = 0 
group by id_day, station_out, time_out_platform_backward
) a


--step 2 - final analysis using forward and backward platform out 
select typ,id_day, station, time_on_platform, sum(cnt) from tbl_time_matrix_summary_fwd
where excl_flag=0
group by typ,id_day,station, time_on_platform
order by time_on_platform

select typ,id_day, station, time_on_platform, sum(cnt) from tbl_time_matrix_summary_bwd
where excl_flag=0
group by typ,id_day,station, time_on_platform
order by time_on_platform

--step 3 - final analysis 
select id_day, station, time_on_platform, sum(cnt) from tbl_time_matrix_summary_fwd
where excl_flag=0
group by id_day,station, time_on_platform
order by station,time_on_platform

select id_day, station, time_on_platform, sum(cnt) from tbl_time_matrix_summary_bwd
where excl_flag=0
group by id_day,station, time_on_platform
order by station,time_on_platform

with select_jrys as 
( select 
id,id_oyster,id_day, id_tube_line,station_in,station_out, time_in, time_out,
(case when time_in_on_platform ='-1' then '00:00' else time_in_on_platform end)::time without time zone time_in_on_platform,
(case when time_in_on_train ='-1' then '00:00' else time_in_on_train end)::time without time zone time_in_on_train,
(case when time_out_train ='-1' then '00:00' else time_out_train end)::time without time zone time_out_train,
(case when time_out_platform_forward ='-1' then '00:00' else time_out_platform_forward end)::time without time zone time_out_platform_forward,
(case when time_out_platform_backward ='-1' then '00:00' else time_out_platform_backward end)::time without time zone time_out_platform_backward,
case when tube_line_name = 'Overground' or station_in = station_out or tube_line_name = 'NA' or time_in = '00:00:00' or time_out = '00:00:00' then 1 else 0 end excl_flag
from tbl_time_matrix),
w as
(SELECT dd as day_window,date_trunc('minute', tm)::time as min_window FROM 
generate_series ( 1,8,1) dd , 
generate_series
        ( '2022-10-01'::timestamp 
        , '2022-10-02'::timestamp
        , '1 minute'::interval) tm 
where dd=1
        )
select station_in,id_day,w.min_window,
--,w.min_window,b.time_in_on_platform,b.time_in_on_train  
count(*) as j_count from w left join select_jrys as b on 
w.day_window = cast(id_day as int) and w.min_window between b.time_in_on_platform and b.time_in_on_train
where excl_flag=0
group by station_in,id_day,w.min_window
order by station_in,id_day,w.min_window




--select min_window from w 
select * from select_jrys 
limit 100


(SELECT dd as day_window, FROM generate_series ( 1,8,1) dd )
(SELECT date_trunc('minute', tm):: time as min_window
FROM generate_series
        ( '2022-10-01'::timestamp 
        , '2022-10-02'::timestamp
        , '1 minute'::interval) tm)


(SELECT dd as day_window,date_trunc('minute', tm):: time as min_window FROM 
generate_series ( 1,8,1) dd , 
generate_series
        ( '2022-10-01'::timestamp 
        , '2022-10-02'::timestamp
        , '1 minute'::interval) tm) as w
