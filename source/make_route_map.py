import random
import osmnx as ox
import networkx as nx
from source.get_trip_and_station_data import get_and_format_trip_data, get_station_list


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
    print('trip type in find nearest nodes:', type(trip))
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

def route_random_trip_on_folium_map():
    trips = get_and_format_trip_data('/Users/Drevets/PycharmProjects/hot-bikes/resources/Divvy_Trips_2018_06.csv')
    stations = get_station_list()
    trips_with_start_and_stop_locations = add_station_locations_to_trips(trips, stations)
    trip = pick_trip_at_random(trips_with_start_and_stop_locations)
    graph = make_graph(stations)
    route = find_route(graph, trip)
    folium_route = route_trip_on_folium_map(graph, route)
    save_route_map_to_html(folium_route, '/Users/Drevets/PycharmProjects/hot-bikes/app/templates/one_trip.html')


route_random_trip_on_folium_map()