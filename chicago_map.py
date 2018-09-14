import pandas as pd
import folium
import requests
import numpy as np

# shadowing bad?
def get_and_format_bike_data(csv_string):
    bike_data = pd.read_csv(csv_string)

    #this time below might not be necessary if not working  with time

    bike_data["start_time"] = pd.to_datetime(bike_data["start_time"])
    bike_data["end_time"] = pd.to_datetime(bike_data["end_time"])
    bike_data["hour"] = bike_data["start_time"].map(lambda x: x.hour) #what is this lambda expression doing?
    bike_data['start_station_longitude'] = np.nan
    bike_data['start_station_latitude'] = np.nan
    bike_data['end_station_longitude'] = np.nan
    bike_data['end_station_latitude'] = np.nan
    return bike_data

#async programming in Python?

bike_data = get_and_format_bike_data("Divvy_Trips_2018_06.csv")

def get_station_list():
    response = requests.get('https://feeds.divvybikes.com/stations/stations.json')

    station_data = response.json()
    station_list = station_data['stationBeanList']
    station_data_frame = pd.DataFrame.from_records(station_list, index='id')
    return station_data_frame


station_data_frame = get_station_list()
# need a way to weed out the bike trips that are not from current stations...


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


def add_counts_to_stations(station_data_frame, bike_data):
    departure_counts = bike_data.groupby('from_station_id').count()
    departure_counts = departure_counts.iloc[:, [0]] # so this does something magical....
    departure_counts.columns = ['Departure Count']

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
    return station_data_frame

station_data_frame = add_counts_to_stations(station_data_frame, bike_data)


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


def put_stations_on_map(station_list):
    folium_map = folium.Map(location=[41.88, -87.62],
                            zoom_start=13,
                            tiles="CartoDB dark_matter")
    for station in station_list:
        folium.CircleMarker(location=[station['latitude'], station['longitude']], fill=True).add_to(folium_map)
    folium_map.save("marker_map.html")
    return folium_map


