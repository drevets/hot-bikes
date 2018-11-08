from client.src.script.source.transform_trip_data import get_trips, identify_discrete_trips, filter_trips_by_hour, \
    get_and_format_station_data, format_and_clean_path_data, add_lat_and_lon_to_path_data_frame, count_trips, filter_trips_by_count

from client.src.script.source.create_and_manipulate_map_image_data import find_max_and_min_lat_and_lon, create_map_image_data, make_map_image_overlay, \
    get_aspect_ratio_and_return_delta_lat, make_folium_map


def create_html_map_with_path_data():
    trips = get_and_format_path_data()
    folium_map = create_folium_image_with_paths(trips)
    generate_html(folium_map)

def get_and_format_path_data():
    trips = get_trips()
    trips = identify_discrete_trips(trips)
    trips = filter_trips_by_hour(trips, 12)
    trips = count_trips(trips)
    trips = filter_trips_by_count(trips, 5)
    stations = get_and_format_station_data()
    trips = format_and_clean_path_data(trips)
    trips = add_lat_and_lon_to_path_data_frame(trips, stations)
    return trips

def create_folium_image_with_paths(trips):
    min_lat, max_lat, max_lon, min_lon = find_max_and_min_lat_and_lon(trips)
    image_data = create_map_image_data(trips)
    map_overlay = make_map_image_overlay(image_data)
    delta_lat = get_aspect_ratio_and_return_delta_lat(map_overlay, max_lon, min_lon, min_lat)
    folium_map = make_folium_map(map_overlay, max_lat, delta_lat, min_lon, max_lon)
    return folium_map

def generate_html(folium_map):
    folium_map.save('path_map2.html')
