from source.get_trip_and_station_data import get_and_format_trip_data, get_station_list

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

def get_trips():
    stations = get_station_list()
    trips = add_lat_and_lon_to_trips(get_and_format_trip_data("resources/Divvy_Trips_2018_06.csv"), stations)
    return trips

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

def format_and_clean_path_data(paths):
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