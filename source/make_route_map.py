import random
import osmnx as ox
import networkx as nx
import numpy as np
import pandas as pd
from get_trip_and_station_data import get_and_format_trip_data, get_station_list


def add_station_locations_to_trips(trips, stations):
    trips_with_start_locations = trips.merge(stations, left_on='from_station_id',
                                             right_on='id', copy=False).rename(
        columns={'latitude': 'Start_Latitude', 'longitude': 'Start_Longitude'}).drop(
        columns=['altitude', 'availableBikes', 'availableDocks', 'city', 'is_renting', 'kioskType',
                 'landMark', 'lastCommunicationTime', 'location', 'postalCode', 'stAddress1', 'stAddress2', 'stationName',
                 'status', 'statusKey', 'statusValue', 'testStation', 'totalDocks'])
    trips_with_start_and_stop_locations = trips_with_start_locations.merge(stations,
                                                                           left_on='to_station_id',
                                                                           right_on='id', copy=False).rename(
        columns={'latitude': 'End_Latitude', 'longitude': 'End_Longitude'}).drop(
        columns=['altitude', 'availableBikes', 'availableDocks', 'city', 'is_renting', 'kioskType',
                 'landMark', 'lastCommunicationTime', 'location', 'postalCode', 'stAddress1', 'stAddress2', 'stationName',
                 'status', 'statusKey', 'statusValue', 'testStation', 'totalDocks'])

    return trips_with_start_and_stop_locations

def pick_trip_at_random(trips):
    return trips.iloc[random.randint(0, (len(trips.index) + 1))]

def find_extent_of_area(stations):
    westernmost_station = stations.loc[stations['longitude'].idxmin()]
    easternmost_station = stations.loc[stations['longitude'].idxmax()]
    southernmost_station = stations.loc[stations['latitude'].idxmin()]
    northernmost_station = stations.loc[stations['latitude'].idxmax()]
    return {
        'west_lon': westernmost_station.at['longitude'],
        'east_lon': easternmost_station.at['longitude'],
        'north_lat': northernmost_station.at['latitude'],
        'south_lat': southernmost_station.at['latitude']
    }

def get_ox_graph_from_bbox(station_extremes, type):
    return ox.graph_from_bbox(station_extremes['north_lat'], station_extremes['south_lat'],
                              station_extremes['east_lon'], station_extremes['west_lon'],
                              network_type=type)

def find_nearest_nodes(graph, trip):
    orig_lat_lon = (trip.at['Start_Latitude'], trip.at['Start_Longitude'])
    target_lat_lon = (trip.at['End_Latitude'], trip.at['End_Longitude'])
    return {
        'orig_node': ox.get_nearest_node(graph, orig_lat_lon, method='euclidean'),
        'target_node': ox.get_nearest_node(graph, target_lat_lon, method='euclidean')
    }

def route_trip_on_folium_map(graph, route):
    return ox.plot_route_folium(graph, route)

def save_route_map_to_html(folium_route, filename):
    folium_route.save(filename)

def make_graph(stations):
    station_extremes = find_extent_of_area(stations)
    return get_ox_graph_from_bbox(station_extremes, 'bike')

def find_route(graph, trip):
    endpoints = find_nearest_nodes(graph, trip)
    return nx.shortest_path(G=graph, source=endpoints['orig_node'], target=endpoints['target_node'], weight='length')

# could probably refactor this function a bit or something // or SOMETHING

def add_routes_to_trips():
    trips = get_and_format_trip_data('/Users/Drevets/PycharmProjects/hot-bikes/resources/Divvy_Trips_2018_06.csv')
    stations = get_station_list()
    trips_with_start_and_stop_locations = add_station_locations_to_trips(trips, stations)
    graph = make_graph(stations)
    routes_array = []
    for index, trip in trips_with_start_and_stop_locations.iterrows():
        routes_array.append({'trip_id': trip['trip_id'], 'route': find_route(graph, trip)})
        print('one done')
    routes_df = pd.DataFrame(routes_array)
    trips_with_routes = trips_with_start_and_stop_locations.merge(routes_df, on='trip_id')
    return trips_with_routes

def route_random_trip_on_folium_map():
    trips = get_and_format_trip_data('/Users/Drevets/PycharmProjects/hot-bikes/resources/Divvy_Trips_2018_06.csv')
    stations = get_station_list()
    trips_with_start_and_stop_locations = add_station_locations_to_trips(trips, stations)
    trip = pick_trip_at_random(trips_with_start_and_stop_locations)
    graph = make_graph(stations)
    route = find_route(graph, trip)
    folium_route = route_trip_on_folium_map(graph, route)
    save_route_map_to_html(folium_route, '/Users/Drevets/PycharmProjects/hot-bikes/app/templates/one_trip.html')

def find_intersecting_trip(selected_trip, trips):
    '''takes a series object, or whatever the pandas term is for just a row'''
    route = selected_trip['route']
    print('looking for this route', route)
    for index, trip in trips.iterrows():
        route_set = set(route)
        target_route_set = set(trip['route'])
        print('target_route_set', target_route_set)
        intersecting_nodes = route_set.intersection(target_route_set)
        if bool(intersecting_nodes):
            print('match found')
            return {'trip': trip, 'matching_nodes': intersecting_nodes}
    return False

def make_route(start_station, end_station, graph):
    stations = pd.DataFrame(get_station_list())
    start_station_lat_and_lon = (stations.loc[stations['stationName'] == start_station, 'latitude'].values[0],
                                 stations.loc[stations['stationName'] == start_station, 'longitude'].values[0])
    end_station_lat_and_lon = (stations.loc[stations['stationName'] == end_station, 'latitude'].values[0],
                                 stations.loc[stations['stationName'] == end_station, 'longitude'].values[0])
    start_node = ox.get_nearest_node(graph, start_station_lat_and_lon, method='euclidean')
    end_node = ox.get_nearest_node(graph, end_station_lat_and_lon, method='euclidean')
    route = nx.shortest_path(G=graph, source=start_node, target=end_node, weight='length')
    return route

trips = get_and_format_trip_data('/Users/Drevets/PycharmProjects/hot-bikes/resources/Divvy_Trips_2018_06.csv')
stations = get_station_list()
trips_with_start_and_stop_locations = add_station_locations_to_trips(trips, stations)

def filter_trips(trips, hour, gender, age):
    trips = trips.loc[trips['hour'] == hour]
    trips = trips.loc[trips['gender'] == gender]
    now = pd.Timestamp.now().year
    oldest_birthyear = now - age
    trips = trips.loc[trips['birthyear'] >= oldest_birthyear]
    print(trips.head(5))

filter_trips(trips_with_start_and_stop_locations, 9, 'Female', 45)