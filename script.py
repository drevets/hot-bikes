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



def generate_heatmap():
    stations = get_station_list()
    trips = add_lat_and_lon_to_trips(get_and_format_trip_data("resources/Divvy_Trips_2018_06.csv"), stations)
    timeseries_heatmap_data = create_timeseries_data(trips)
    make_timeseries_map(timeseries_heatmap_data)

def get_trips():
    stations = get_station_list()
    trips = add_lat_and_lon_to_trips(get_and_format_trip_data("resources/Divvy_Trips_2018_06.csv"), stations)
    return trips

def find_max_and_min_lat_and_lon():
    trips = get_trips()
    min_lat = trips["Start_Latitude"].min()
    max_lat = trips["Start_Latitude"].max()
    max_lon = trips["Start_Longitude"].max()
    min_lon = trips["Start_Longitude"].min()
    return {min_lat, max_lat, max_lon, min_lon}

#should also use the function that Max defined above

#so what are the parts that happen here...
    #get the locations and create just a list of stations with the lat and long
    #create new column with a tuple representing starting and ending stations
    #take a subset of the data by narrowing it down by hour
    #group it and count it and then drop the other columns, remaining with just a count of the paths and the path
    #rename that column to trip count
    #narrow it down to only five or less trips (might be better if not hard-coded)
    #then separate out those tuples again into their own columns (do we still need the station id??)
    #do two joins, to get the latitude and longitude back
    #questions: where is there duplicate work, work that doesn't quite make sense
    #figure out how to add Max's code back into it...and then write unit tests


def make_trip_map():
    trips = get_trips()
    print(trips.head(5))

    #so we're condensing the data down a little bit here to just have the from station ids and their lats and longs
    locations = trips.groupby("from_station_id").mean()
    print(locations.head(5))

    #so I don't think I need to do this...I think I can just use the station data and then drop columns
    locations = locations.loc[:, ["Start_Latitude", "Start_Longitude"]]
    print(locations.head(5))

    #and then here, we're creating a new column in trips with a tuple of from and to station ids
    trips["path_id"] = [(id1, id2) for id1, id2 in zip(trips["from_station_id"],
                                                       trips["to_station_id"])]

    print(trips['path_id'][5])
    print(trips.head(5))

    #selecting the hour, counting number of duplicate trips, and then filtering it down to one column
    paths2 = trips[trips["hour"] == 9].groupby("path_id").count().iloc[:, [1]]
    print(paths2.head(5))

    #renaming the one column
    paths.columns = ["Trip Count"]

    # select only paths with more than X trips
    paths = paths[paths["Trip Count"] > 5]

    #separate out the tuple that is now the index into their own discrete columns
    paths["from_station_id"] = paths.index.map(lambda x: x[0])
    paths["to_station_id"] = paths.index.map(lambda x: x[1])

    #remove any paths that have the same start and stop stations
    paths = paths[paths["from_station_id"] != paths["to_station_id"]]
    # # join latitude/longitude into new table for the from station id
    paths = paths.join(locations, on="from_station_id")

    #renaming the columns and then doing another join
    locations.columns = ["End Station Latitude", "End Station Longitude"]
    paths = paths.join(locations, on="to_station_id")

    print(paths.head(4))

    #re-indexing
    paths.index = range(len(paths))

    print(paths.head(4))

    min_lat, max_lat, max_lon, min_lon = find_max_and_min_lat_and_lon()

    image_data = get_image_data(max_lat, max_lon, min_lon, paths)

    folium_map = folium.Map(location=[41.88, -87.62],
                            zoom_start=13,
                            tiles="CartoDB dark_matter",
                            width='50%')

    # create the overlay
    map_overlay = add_alpha(to_image(image_data * 10))

    # compute extent of image in lat/lon
    aspect_ratio = map_overlay.shape[1] / map_overlay.shape[0]
    delta_lat = (max_lon - min_lon) / aspect_ratio * np.cos(min_lat / 360 * 2 * np.pi)

    # add the image to the map
    img = folium.raster_layers.ImageOverlay(map_overlay,
                                            bounds=[(max_lat - delta_lat, min_lon), (max_lat, max_lon)],
                                            opacity=1,
                                            name="Paths")

    img.add_to(folium_map)
    folium.LayerControl().add_to(folium_map)

    # show the map
    folium_map.save('path_map.html')


def generate_all_html_pages():
    stations = get_station_list()
    trips = add_lat_and_lon_to_trips(get_and_format_trip_data("resources/Divvy_Trips_2018_06.csv"), stations)
    stations = add_trip_counts_to_stations(stations, trips)
    station_map = put_stations_on_map(stations) #I'm pretty sure this isn't doing anything right here, not anything important at least

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
    make_trip_map()