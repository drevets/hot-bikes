import pandas as pd
import folium

#why these modules no exist?

bike_data = pd.read_csv("Divvy_Trips_2018_06.csv")

response = requests.get('https://feeds.divvybikes.com/stations/stations.json')

# man there is so much that I'm not understanding about this....

station_data = response.json()

def put_stations_on_map(station_data):
    folium_map = folium.Map(location=[41.881, ‎-87.623],
                zoom_start = 13,
                 tiles = "CartoDB dark_matter")
    for station in station_data:
        folium.CircleMarker(location=[station.latitude, station.longitude], fill=True).add_to(folium_map)
    return folium_map

#so I think this will return a map with stations on it....