import numpy as np

from source.make_station_map import *
from source.draw_paths import *
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


def generate_all_html_pages():
    stations = get_station_list()
    trips = add_lat_and_lon_to_trips(get_and_format_trip_data("resources/Divvy_Trips_2018_06.csv"), stations)
    stations = add_trip_counts_to_stations(stations, trips)
    station_map = put_stations_on_map(stations)

    #makes timeseries heatmap
    timeseries_heatmap_data = create_timeseries_data(trips)
    make_timeseries_map(timeseries_heatmap_data)

    #code below here makes map with path lines on it
    min_lat = trips["Start_Latitude"].min()
    max_lat = trips["Start_Latitude"].max()
    max_lon = trips["Start_Longitude"].max()
    min_lon = trips["Start_Longitude"].min()

    # make a list of locations (latitude longitude) for each station id
    locations = trips.groupby("from_station_id").mean()

    locations = locations.loc[:,["Start_Latitude", "Start_Longitude"]]

    trips["path_id"] = [(id1,id2) for id1,id2 in zip(trips["from_station_id"],
                                                         trips["to_station_id"])]

    paths = trips[trips["hour"]==9].groupby("path_id").count().iloc[:,[1]]

    paths.columns = ["Trip Count"]

    # select only paths with more than X trips
    paths = paths[paths["Trip Count"]>5]
    paths["from_station_id"] = paths.index.map(lambda x:x[0])
    paths["to_station_id"] = paths.index.map(lambda x:x[1])

    paths = paths[paths["from_station_id"]!=paths["to_station_id"]]
    # # join latitude/longitude into new table
    paths = paths.join(locations,on="from_station_id")

    locations.columns = ["End Station Latitude","End Station Longitude"]
    paths = paths.join(locations,on="to_station_id")

    paths.index = range(len(paths))

    image_data = get_image_data(max_lat, max_lon, min_lon, paths)

    folium_map = folium.Map(location=[41.88, -87.62],
                            zoom_start=13,
                            tiles="CartoDB dark_matter",
                            width='50%')

    # create the overlay
    map_overlay = add_alpha(to_image(image_data*10))

    # compute extent of image in lat/lon
    aspect_ratio = map_overlay.shape[1]/map_overlay.shape[0]
    delta_lat = (max_lon-min_lon)/aspect_ratio*np.cos(min_lat/360*2*np.pi)

    # add the image to the map
    img = folium.raster_layers.ImageOverlay(map_overlay,
                               bounds = [(max_lat-delta_lat,min_lon),(max_lat,max_lon)],
                               opacity = 1,
                               name = "Paths")

    img.add_to(folium_map)
    folium.LayerControl().add_to(folium_map)

    # show the map
    folium_map.save('path_map.html')

if __name__ == '__main__':
    generate_all_html_pages()
