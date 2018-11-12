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
    bike_trips.to_pickle('/Users/Drevets/PycharmProjects/hot-bikes/resources/bike_trips.pkl')
    return bike_trips

def get_station_list():
    '''output: pandas data frame'''
    station_api_key = 'stationBeanList'
    try:
        response = requests.get('https://feeds.divvybikes.com/stations/stations.json')
        station_data = response.json()
        station_list = station_data[station_api_key]
        stations = pd.DataFrame.from_records(station_list, index='id')
        stations.to_pickle('/Users/Drevets/PycharmProjects/hot-bikes/resources/stations.pkl')
    except:
        print('something went wrong')
    return stations



