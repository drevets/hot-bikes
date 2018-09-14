from functions import get_and_format_trip_data, get_station_list, add_trip_counts_to_stations, put_stations_on_map, add_lat_and_lon_to_trips

trips = get_and_format_trip_data("resources/Divvy_Trips_2018_06.csv")
stations = get_station_list()
stations = add_trip_counts_to_stations(stations, trips)
map = put_stations_on_map(stations)



