# fetch_river_gauges
Fetch river data from USGS API and send to groupme

Using the [USGS Water Data APIs](https://api.waterdata.usgs.gov/), extract water levels from the desired rivers, check to see if it is over a preset limit, send a groupme message if the limit is succeeded. 

An optional ```--test/-t``` mode is included to report on all levels regardless of limit.

Configuration parameters: station_id, label (human readable name), and limit, are stored in "river_guage.json" which is assumed to be in the same directory as the python script.

```usage: fetch_river_guages.py [-h] [-t] bot_id```
Where "bot_id" is the id of the groupme group
