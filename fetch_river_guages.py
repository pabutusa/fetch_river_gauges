#!/usr/bin/python3

import requests
import json
import io
import argparse
from datetime import datetime



def send_gm_message(bot_id, message):
   url = "https://api.groupme.com/v3/bots/post"
   payload = {"bot_id": bot_id, "text": message}
   r = requests.post(url, data=json.dumps(payload))

   return

def main(args):
    # USGS OGC API endpoint for latest continuous water data    

    url = "https://api.waterdata.usgs.gov/ogcapi/v1/collections/latest-continuous/items"

    with open('river_guage.json', 'r') as river_guage_file:
        config_data=json.load(river_guage_file)

    stations=','.join([i["station_id"] for i in config_data ])

    # Parameters matching Belvidere, NJ station and gage height (00065)
    params = {
        "monitoring_location_id": stations,
        "parameter_code": "00065",
        "f": "json",
        "lang" : "en-US", 
        "limit" : "10",
        "skipGeometry" : "false",
        "offset" : "0"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        
        # OGC API returns GeoJSON features matching the query
        features = data.get("features", [])
        output_buffer = io.StringIO()

        for feature in features:
            latest_obs = feature["properties"]
            
            station_id = latest_obs.get("monitoring_location_id")
            location_name, limit=[(item["label"],item["limit"]) for item in config_data if item.get("station_id") == station_id ][0]
            value = float(latest_obs.get("value"))
            unit = latest_obs.get("unit_of_measure")
            timestamp=datetime.fromisoformat(latest_obs.get("time")).astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')

            if value >= limit or args.test:
                print(f"Station: {location_name}",file=output_buffer)
                print(f"Current Water Level: {value} {unit} @ {timestamp}",file=output_buffer)
                #print(f"Timestamp: {timestamp}",file=output_buffer)
                print("",file=output_buffer)
    else:
        print(f"Error fetching data: {response.status_code} - {response.text}",file=output_buffer)

    if output_buffer.getvalue() is not None:
        send_gm_message(args.bot_id, output_buffer.getvalue())

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='fetch latest river guages')
    parser.add_argument('bot_id', help="ID of the groupme bot")
    parser.add_argument('-t', '--test', action='store_true', help="force limit to zero")
    args = parser.parse_args()

    main(args)
