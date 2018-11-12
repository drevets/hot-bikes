import osmnx as ox
import networkx as nx
import pandas as pd
import folium
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


def make_graph(stations):
    station_extremes = find_extent_of_area(stations)
    return get_ox_graph_from_bbox(station_extremes, 'bike')


def find_route(graph, trip):
    endpoints = find_nearest_nodes(graph, trip)
    return nx.shortest_path(G=graph, source=endpoints['orig_node'], target=endpoints['target_node'], weight='length')


def find_intersecting_route(trips, graph, user_route):
    for index, trip in trips.iterrows():
        candidate_route = find_route(graph, trip)
        if does_route_intersect(user_route, candidate_route):
            return candidate_route
    else:
        raise Exception('No intersecting route found')


def does_route_intersect(user_route, candidate_route):
    route_set = set(user_route)
    candidate_set= set(candidate_route)
    intersecting_nodes = route_set.intersection(candidate_set)
    return bool(intersecting_nodes)


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


def filter_trips(trips, hour, gender):
    trips = trips.loc[trips['hour'] == hour]
    trips = trips.loc[trips['gender'] == gender]
    return trips


def convert_nodes_to_lat_and_lon(graph, route):
    route_coords = []
    for node in route:
        route_coords.append((graph.node[node]['y'], graph.node[node]['x']))
    return route_coords


def create_folium_polylines(route_array):
    return folium.PolyLine(route_array)


def find_center_of_route(route):
    avg_lat = 0
    avg_lon = 0
    for lat, lon in route:
        avg_lat += lat
        avg_lon += lon
    return (avg_lat / len(route), avg_lon / len(route))


def create_folium_map(map_center):
    folium_map = folium.Map(location=map_center,
               zoom_start=13,
               tiles="CartoDB dark_matter")
    return folium_map


def add_lines_to_folium_map(map, lines):
    lines.add_to(map)
    return map


def find_intersecting_routes_and_save_map_hmtl():
    trips = get_and_format_trip_data('/Users/Drevets/PycharmProjects/hot-bikes/resources/Divvy_Trips_2018_06.csv')
    stations = get_station_list()
    trips_with_start_and_stop_locations = add_station_locations_to_trips(trips, stations) # might be able to switch these steps
    trips = filter_trips(trips_with_start_and_stop_locations, 9, 'Female')
    graph = make_graph(stations)
    user_route = make_route("Buckingham Fountain", "Greenview Ave & Fullerton Ave", graph)
    intersecting_route = find_intersecting_route(trips, graph, user_route)
    intersecting_route_coords = convert_nodes_to_lat_and_lon(graph, intersecting_route)
    user_route_coords = convert_nodes_to_lat_and_lon(graph, user_route)
    intersecting_route_center = find_center_of_route(intersecting_route_coords)
    user_route_center = find_center_of_route(user_route_coords)
    center_of_intersecting_routes = find_center_of_route([intersecting_route_center, user_route_center])
    polylines = create_folium_polylines([[intersecting_route_coords], [user_route_coords]])
    folium_map = create_folium_map(center_of_intersecting_routes)
    line_map = add_lines_to_folium_map(folium_map, polylines)
    line_map.save('/Users/Drevets/PycharmProjects/hot-bikes/app/templates/line_map.html')

find_intersecting_routes_and_save_map_hmtl()