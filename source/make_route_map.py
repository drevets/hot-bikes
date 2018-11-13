import osmnx as ox
import networkx as nx
import pandas as pd
import folium
import random


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


def make_graph(stations):
    station_extremes = find_extent_of_area(stations)
    chicago_graph = get_ox_graph_from_bbox(station_extremes, 'bike')
    nx.write_gpickle(chicago_graph, '/Users/Drevets/PycharmProjects/hot-bikes/resources/chicago_graph.pkl')
    return chicago_graph


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

def find_intersecting_trip(trips, graph, user_route):
    for index, trip in trips.iterrows():
        candidate_route = find_route(graph, trip)
        intersecting_node = does_route_intersect(user_route, candidate_route)
        if intersecting_node:
            return [trip, candidate_route, intersecting_node]
    else:
        raise Exception('No intersecting route found')


def does_route_intersect(user_route, candidate_route):
    route_set = set(user_route)
    candidate_set= set(candidate_route)
    return route_set.intersection(candidate_set)


def make_route(stations, start_station, end_station, graph):
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
        print(graph.node[node])
        route_coords.append((graph.node[node]['y'], graph.node[node]['x']))
    return route_coords


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
               tiles="cartodbpositron",
                width='75%',
                height='75%')
    return folium_map


def extract_trip_data(trip):
    start_time = trip['start_time']
    day_name = start_time.day()
    day = start_time.day
    year = start_time.year
    month = start_time.month_name()
    hour = start_time.hour
    minute = start_time.minute
    time = sanitize_time(hour, minute)
    date_string = "{}, {} {}, {}, at approximately {} o'clock".format(day_name, month, day, year, time)
    return {
        'gender': trip['gender'],
        'date_string': date_string,
        'age': pd.Timestamp.now().year - trip['birthyear']
    }

def sanitize_time(hour, minute):
    if hour - 12 > 0:
        return '{}:{} PM'.format(hour - 12, minute)
    return '{}:{} AM'.format(hour, minute)


def make_folium_map_with_polylines(graph, user_route, intersecting_route, user_color, intersecting_route_color):
    intersecting_route_coords = convert_nodes_to_lat_and_lon(graph, intersecting_route)
    user_route_coords = convert_nodes_to_lat_and_lon(graph, user_route)
    user_route_polyline = folium.PolyLine(user_route_coords, color=user_color)
    intersecting_route_polyline = folium.PolyLine(intersecting_route_coords, color=intersecting_route_color)
    intersecting_route_center = find_center_of_route(intersecting_route_coords)
    user_route_center = find_center_of_route(user_route_coords)
    center_of_intersecting_routes = find_center_of_route([intersecting_route_center, user_route_center])
    folium_map = create_folium_map(center_of_intersecting_routes)
    intersecting_route_polyline.add_to(folium_map)
    user_route_polyline.add_to(folium_map)
    return folium_map


def find_intersecting_routes_and_save_map_html(gender, hour, start_station, end_station):
    print('calling and finding intersecting routes and saving the map')
    trips = pd.read_pickle('/Users/Drevets/PycharmProjects/hot-bikes/resources/bike_trips.pkl')
    stations = pd.read_pickle('/Users/Drevets/PycharmProjects/hot-bikes/resources/stations.pkl')
    graph = nx.read_gpickle('/Users/Drevets/PycharmProjects/hot-bikes/resources/chicago_graph.pkl')
    trips_with_start_and_stop_locations = add_station_locations_to_trips(trips, stations)
    trips = filter_trips(trips_with_start_and_stop_locations, hour, gender)
    user_route = make_route(stations, start_station, end_station, graph)
    # intersecting_route = find_intersecting_route(trips, graph, user_route)
    [intersecting_trip, intersecting_route, intersecting_node] = find_intersecting_trip(trips, graph, user_route)
    trip_data = extract_trip_data(intersecting_trip)
    line_map = make_folium_map_with_polylines(graph, user_route, intersecting_route, '#41f4ca', '#d69a2a')
    line_map.save('/Users/Drevets/PycharmProjects/hot-bikes/app/templates/line_map.html')