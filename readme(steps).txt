Data processing (done in Python )
1- Pick a journey
2- take the tap in station and tap out station , and look through on the TFL network to see if the stations are on the same line 
	a) if the stations are on the same single single line proceed
	b) if the stations are on more than 1 line, pick the first match (this may not be 100 accurate approach), and proceed 
	c) if the stations are on different lines, ignore that journey, (approx x% of the journeys are transit journeys)
	
3. use the walk to platform data to calculate, walk_in time for the journey 
4. use the train time table to calculate, the waiting on the platform time
5. calculate journey time 
	a) this calculation is done for each segment of the journey e.g. baker street to Finchley road  has 3 segments 
	b) calculate the train time taken for the journey for each segment and add it to get the total journey train time 
6. calculate platform out time, by adding the TRAIN_JOURNEY_TIME to the PLATFORM WALK time to calculate STATION_TIME_OUT_FORWARD. 
7. a comparison of actual  time_out vs STATION_TIME_OUT_FORWARD will give you the error rate in the time matrix calculation

Data analysis (in SQL)

