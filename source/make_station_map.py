import pandas as pd
import folium
import requests


def get_and_format_trip_data(file_name):
    '''
    input: file name
    output: pandas data frame
    '''
    parse_dates = ['start_time', 'end_time']
    bike_trips = pd.read_csv(file_name, parse_dates=parse_dates)
    bike_trips["hour"] = bike_trips["start_time"].map(lambda x: x.hour)
    return bike_trips

def get_station_list():
    '''output: pandas data frame'''
    station_api_key = 'stationBeanList'
    try:
        response = requests.get('https://feeds.divvybikes.com/stations/stations.json')
        station_data = response.json()
        station_list = station_data[station_api_key]
        stations = pd.DataFrame.from_records(station_list, index='id')
    except:
        print('something went wrong')
    return stations

def add_trip_counts_to_stations(stations, trips):
    '''
    input: data frames
    output: data frame
    '''
    departure_counts = trips.groupby('from_station_id').count()
    departure_counts = departure_counts.iloc[:, [0]]
    departure_counts.columns = ['Departure Count']

    arrival_counts = trips.groupby('to_station_id').count()
    arrival_counts = arrival_counts.iloc[:, [0]]
    arrival_counts.columns = ['Arrival Count']

    stations = pd.merge(departure_counts, stations,
                        right_on='id',
                        left_index=True).merge(arrival_counts,
                                               left_on='id',
                                               right_index=True)
    return stations


def add_lat_and_lon_to_trips(trips, stations):
    '''
    input: dataframes
    output: dataframe
    '''

    lat_lon_start = stations[['latitude', 'longitude']]
    lat_lon_start.columns = ['Start_Latitude', 'Start_Longitude']
    lat_lon_end = stations[['latitude', 'longitude']]
    lat_lon_end.columns = ['End_Latitude', 'End_Longitude']
    trips = trips.merge(lat_lon_start,
                        left_on='from_station_id',
                        right_on='id').merge(lat_lon_end,
                                            left_on='to_station_id',
                                            right_on='id')
    return trips


def put_stations_on_map(stations):
    '''
    input: data frame
    output: folium map
    '''
    map = folium.Map(location=[41.88, -87.62],
                            zoom_start=13,
                            tiles="CartoDB dark_matter")
    for index, station in stations.iterrows():
        popup_text = "{}<br> Total departures: {}<br> Total arrivals: {}<br>"
        popup_text = popup_text.format(stations.at[index, "stationName"],
                                       stations.at[index, "Arrival Count"],
                                       stations.at[index, "Departure Count"],
                                       )
        folium.CircleMarker(location=[stations.at[index, 'latitude'],
                                      stations.at[index, 'longitude']],
                            fill=True,
                            popup=popup_text).add_to(map)
    map.save("count_map.html")
    return map

