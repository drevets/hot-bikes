import pandas as pd
import folium
import requests
import numpy as np

bike_data = pd.read_csv("Divvy_Trips_2018_06.csv")

#this stuff below might not be necessary if not doing stuff with time

bike_data["start_time"] = pd.to_datetime(bike_data["start_time"])
bike_data["end_time"] = pd.to_datetime(bike_data["end_time"])
bike_data["hour"] = bike_data["start_time"].map(lambda x: x.hour)

response = requests.get('https://feeds.divvybikes.com/stations/stations.json')

station_data = response.json()
station_list = station_data['stationBeanList']
station_data_frame = pd.DataFrame.from_records(station_list, index='id')


#print(station_data_frame.loc[station_data_frame.id.eq(2), ['id', 'latitude', 'longitude']])
#print(station_data_frame.loc[4, ['latitude', 'longitude']])

#I wonder if I could do something with mapping....

bike_data['start_station_longitude'] = np.nan
bike_data['start_station_latitude'] = np.nan
bike_data['end_station_longitude'] = np.nan
bike_data['end_station_latitude'] = np.nan

#now I want to iterate over bike data
#need a way to weed out the bike trips that are not from current stations...

def add_location_to_bike_trips(bike_data, station_data_frame):
    for index, row in bike_data.iterrows():
        start_station = row.from_station_id
        end_station = row.to_station_id
        try:
            end_station_info = station_data_frame.loc[end_station, ['latitude', 'longitude']]
            start_station_info = station_data_frame.loc[start_station, ['latitude', 'longitude']]
        except:
            print('start or end station not found')
            continue
        bike_data.at[index, 'start_station_longitude'] = start_station_info.longitude
        bike_data.at[index, 'start_station_latitude'] = start_station_info.latitude
        bike_data.at[index, 'end_station_longitude'] = end_station_info.longitude
        bike_data.at[index, 'end_station_longitude'] = end_station_info.longitude
    return bike_data

#lat_and_lon = add_location_to_bike_trips(bike_data, station_data_frame)
#print(lat_and_lon.head(10))

#now I want to do a count....so, count the rows and then add that to the station id

#this is a new data frame
departure_counts = bike_data.groupby('from_station_id').count()
departure_counts = departure_counts.iloc[:, [0]] # so this does something magical....
departure_counts.columns = ['Departure Count']

#this is also a new data frame
arrival_counts = bike_data.groupby('to_station_id').count()
arrival_counts = arrival_counts.iloc[:, [0]]
arrival_counts.columns = ['Arrival Count']


station_data_frame['Arrival Count'] = np.nan
station_data_frame['Departure Count'] = np.nan

for index, row in station_data_frame.iterrows():
    try:
        station_data_frame.at[index, 'Departure Count'] = departure_counts.at[index, 'Departure Count']
        station_data_frame.at[index, 'Arrival Count'] = arrival_counts.at[index, 'Arrival Count']
    except:
        print('key error')

def put_stations_and_counts_on_map(station_list):
    folium_map = folium.Map(location=[41.88, -87.62],
                            zoom_start=13,
                            tiles="CartoDB dark_matter")
    for index, station in station_list.iterrows():
        popup_text = "{}<br> Total departures: {}<br> Total arrivals: {}<br>"
        popup_text = popup_text.format(station_list.at[index, "stationName"],
                                       station_list.at[index, "Arrival Count"],
                                       station_list.at[index, "Departure Count"],
                                       )
        folium.CircleMarker(location=[station_list.at[index, 'latitude'], station_list.at[index, 'longitude']], fill=True, popup=popup_text).add_to(folium_map)
    folium_map.save("count_map.html")
    return folium_map

map = put_stations_and_counts_on_map(station_data_frame)

def count_trips_and_add_to_station(bike_data, station_data):
    locations = bike_data.groupby('from_station_id').first()  # not sure what this code is really doing
    locations = locations.loc[:, ["Start Station Latitude",
                                  "Start Station Longitude",
                                  "Start Station Name"]]  # and here is where I'm going to need to figure out how
    # to join the data that I have with this data

    departure_counts = locations.groupby('from_station_id').count()
    departure_counts = departure_counts.iloc[:, [0]]  # again, no idea what this is doing right now
    departure_counts.columns = ['Departure Count']

    arrival_counts = locations.groupby('to_station_id').count.iloc[:, [0]]
    arrival_counts.columns = ['Arrival Count']

    trip_counts = departure_counts.join(locations).join(arrival_counts)
    return trip_counts


def put_stations_on_map(station_list):
    folium_map = folium.Map(location=[41.88, -87.62],
                            zoom_start=13,
                            tiles="CartoDB dark_matter")
    for station in station_list:
        folium.CircleMarker(location=[station['latitude'], station['longitude']], fill=True).add_to(folium_map)
    folium_map.save("marker_map.html")
    return folium_map


marker_map = put_stations_on_map(station_list)

def get_trip_counts_by_station(station_id):
    locations = bike_data.groupby('from_station_id').first() #not sure what this code is really doing
    locations = locations.loc[:, ["Start Station Latitude",
                                 "Start Station Longitude",
                                 "Start Station Name"]] # and here is where I'm going to need to figure out how
                                                        #to join the data that I have with this data

    departure_counts = locations.groupby('from_station_id').count()
    departure_counts = departure_counts.iloc[:,[0]] #again, no idea what this is doing right now
    departure_counts.columns = ['Departure Count']

    arrival_counts = locations.groupby('to_station_id').count.iloc[:, [0]]
    arrival_counts.columns = ['Arrival Count']

    trip_counts = departure_counts.join(locations).join(arrival_counts)
    return trip_counts



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


