import pandas as pd
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


