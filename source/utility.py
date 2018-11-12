import folium
from source.get_trip_and_station_data import get_and_format_trip_data, get_station_list
import pandas as pd


def make_chicago_map():
    folium_map = folium.Map(location=[41.88, -87.62],
                            zoom_start=13,
                            tiles="cartodbpositron",
                            width='75%',
                            height='75%')
    folium_map.save('/Users/Drevets/PycharmProjects/hot-bikes/app/templates/chicago_map.html')


def make_station_list():
    station_df = pd.read_pickle('/Users/Drevets/PycharmProjects/hot-bikes/resources/stations.pkl')
    station_list = []
    for index, station in station_df.iterrows():
        station_list.append(station['stationName'])
    print(sorted(station_list))
    return station_list

def get_hour_from_time_string(time_str):
    [hour, minute] = time_str.split(':')
    return int(hour)