import pandas as pd
import folium
import requests

#should probably put all of this into a method or something..?

bike_data = pd.read_csv("Divvy_Trips_2018_06.csv")

response = requests.get('https://feeds.divvybikes.com/stations/stations.json')

station_data = response.json()
station_list = station_data['stationBeanList']

def put_stations_on_map(station_list):
    folium_map = folium.Map(location=[41.88, -87.62],
                            zoom_start=13,
                            tiles="CartoDB dark_matter")
    for station in station_list:
        folium.CircleMarker(location=[station['latitude'], station['longitude']], fill=True).add_to(folium_map)
    folium_map.save("marker_map.html")
    return folium_map


marker_map = put_stations_on_map(station_list)

#how do I display the map without a web browser? where do I host this in general?

# #so I think this will return a map with stations on it....
#
# #so now I want to take that map and count the number of trips from each station. This will be harder.
# #or, I think what I really want to do is add the station latitude and longitude to the map, and then
# #add station latitude and longitude to the map that I have, based on station id, so that I can then group by total number of
# #depatures.
#
# def get_trip_counts_by_station(station_id):
#     departure_counts = subset.groupby('from_station_id').count()
#     departure_counts.columns = ['Departure Count']


