import numpy as np

from source.make_station_map import get_and_format_trip_data, get_station_list, add_lat_and_lon_to_trips
from source.draw_paths import to_image, get_image_data, add_alpha
from source.make_heatmap import *

def add_path_station_locations(paths, locations):
    """
    -`paths` is a DataFrame with three columns: "Trip Count", "from_station_id" and "to_station_id"
    -`locations` is a DataFrame with three columns: "station_id", "Latitude" and "Longitude"
    -Return value is a DataFrame with five columns: "Trip Count", "from_station_id", "to_station_id",
     "Start_Latitude", "Start_Longitude", "End_Latitude" and "End_Longitude"
    """
    # Ideally we could use static type checking with Python type-hinting and mypy, however pandas
    # support is currently stalled: https://github.com/pandas-dev/pandas/issues/14468
    # so we use check_data_frame instead
    paths_spec = {"Trip Count": "int64", "from_station_id": "int64", "to_station_id": "int64"}
    locations_spec = {"station_id": "int64", "Latitude": "float64", "Longitude": "float64"}
    check_data_frame(paths, paths_spec)
    check_data_frame(locations, locations_spec)

    paths_with_start_locations = paths.merge(locations, left_on='from_station_id',
                                             right_on='station_id', copy=False).rename(
        columns={'Latitude': 'Start_Latitude', 'Longitude': 'Start_Longitude'}).drop(
        columns=["station_id"]
    )
    paths_with_start_and_stop_locations = paths_with_start_locations.merge(locations,
                                                      left_on='to_station_id',
                                                      right_on='station_id', copy=False).rename(
        columns={'Latitude': 'End_Latitude', 'Longitude': 'End_Longitude'}).drop(
        columns=["station_id"]
    )

    ret_val_spec = {
        "Trip Count": "int64", "from_station_id": "int64", "to_station_id": "int64",
        "Start_Latitude": "float64", "Start_Longitude": "float64", "End_Latitude": "float64",
        "End_Longitude": "float64"}
    check_data_frame(paths_with_start_and_stop_locations, ret_val_spec)

    return paths_with_start_and_stop_locations


def check_data_frame(data_frame, spec):
    for column_name in spec:
        if column_name not in data_frame:
            raise Exception("Column missing: {0}".format(column_name))
        elif data_frame[column_name].dtype != spec[column_name]:
            raise Exception("Data type incorrect for column {0}, expected {1}, got {2}".format(
                column_name, spec[column_name], data_frame[column_name].dtype))
    for data_frame_column in data_frame:
        if data_frame_column not in spec:
            raise Exception("Unexpected data frame column: {0}".format(data_frame_column))


def generate_heatmap():
    stations = get_station_list()
    trips = add_lat_and_lon_to_trips(get_and_format_trip_data("resources/Divvy_Trips_2018_06.csv"), stations)
    timeseries_heatmap_data = create_timeseries_data(trips)
    make_timeseries_map(timeseries_heatmap_data)

def create_html_map_with_path_data():
    trips = get_format_path_data()
    folium_map = create_folium_image_with_paths(trips)
    generate_html(folium_map)

def create_folium_image_with_paths(trips):
    min_lat, max_lat, max_lon, min_lon = find_max_and_min_lat_and_lon(trips)
    image_data = create_map_image_data(trips)
    map_overlay = make_map_image_overlay(image_data)
    delta_lat = get_aspect_ratio_and_return_delta_lat(map_overlay, max_lon, min_lon, min_lat)
    folium_map = make_folium_map(map_overlay, max_lat, delta_lat, min_lon, max_lon)
    return folium_map

def get_format_path_data():
    trips = get_trips()
    trips = identify_discrete_trips(trips)
    trips = filter_trips_by_hour(trips, 12)
    trips = count_trips(trips)
    trips = filter_trips_by_count(trips, 5)
    stations = get_and_format_station_data()
    trips = format_path_data(trips)
    trips = add_lat_and_lon_to_path_data_frame(trips, stations)
    return trips


def get_trips():
    stations = get_station_list()
    trips = add_lat_and_lon_to_trips(get_and_format_trip_data("resources/Divvy_Trips_2018_06.csv"), stations)
    return trips

def find_max_and_min_lat_and_lon(trips):
    min_lat = trips["Start_Latitude"].min()
    max_lat = trips["Start_Latitude"].max()
    max_lon = trips["Start_Longitude"].max()
    min_lon = trips["Start_Longitude"].min()
    return {min_lat, max_lat, max_lon, min_lon}

def identify_discrete_trips(trips):
    trips["path_id"] = [(id1, id2) for id1, id2 in zip(trips["from_station_id"],
                                                       trips["to_station_id"])]
    return trips

def filter_trips_by_hour(trips, hour):
    trips = trips[trips["hour"] == hour]
    return trips

def count_trips(trips):
    paths = trips.groupby("path_id").count()
    paths = paths.iloc[:, [1]]
    paths.columns = ['Trip Count']
    return paths

def filter_trips_by_count(paths, min_count):
    paths = paths[paths["Trip Count"] > min_count]
    return paths

def get_and_format_station_data():
    locations = get_station_list()
    locations = locations.loc[:, ['latitude', 'longitude']]
    locations.columns = ['Start_Latitude', 'Start_Longitude']
    return locations

def format_path_data(paths):
    paths["from_station_id"] = paths.index.map(lambda x: x[0])
    paths["to_station_id"] = paths.index.map(lambda x: x[1])
    paths = paths[paths["from_station_id"] != paths["to_station_id"]]
    return paths

def add_lat_and_lon_to_path_data_frame(paths, locations):
    paths = paths.join(locations, on="from_station_id")
    locations.columns = ["End Station Latitude", "End Station Longitude"]
    paths = paths.join(locations, on="to_station_id")
    paths.index = range(len(paths))
    return paths

def create_map_image_data(trips):
    min_lat, max_lat, max_lon, min_lon = find_max_and_min_lat_and_lon(trips)
    image_data = get_image_data(max_lat, max_lon, min_lon, trips)
    return image_data

def make_map_image_overlay(image_data):
    map_overlay = add_alpha(to_image(image_data * 10))
    return map_overlay

def get_aspect_ratio_and_return_delta_lat(map_overlay, max_lon, min_lon, min_lat):
    aspect_ratio = map_overlay.shape[1] / map_overlay.shape[0]
    delta_lat = (max_lon - min_lon) / aspect_ratio * np.cos(min_lat / 360 * 2 * np.pi)
    return delta_lat

def make_folium_map(map_overlay, max_lat, delta_lat, min_lon, max_lon):
    folium_map = folium.Map(location=[41.88, -87.62],
                             zoom_start=13,
                             tiles="CartoDB dark_matter",
                             width='50%')
    img = folium.raster_layers.ImageOverlay(map_overlay,
                                            bounds=[(max_lat - delta_lat, min_lon), (max_lat, max_lon)],
                                             opacity=1,
                                             name="Paths")

    img.add_to(folium_map)
    folium.LayerControl().add_to(folium_map)
    return folium_map

def generate_html(folium_map):
    folium_map.save('path_map2.html')

if __name__ == '__main__':
    create_html_map_with_path_data()