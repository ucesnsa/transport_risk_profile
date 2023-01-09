SELECT nlc, tfl_station_nm, station_nm, inner_zone_cd, outer_zone_cd, 
       easting_amt, northing_amt, longitude, latitude
  FROM tbl_station
  where nlc in ( '747','746')

-- line numbers 
idline:  "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"

-- count 18,169,286
select count(*) from tbl_oyster 


-- count 18, 169, 286
select * from tbl_oyster limit 100 


