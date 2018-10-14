import folium
from source.get_trip_and_station_data import get_and_format_trip_data, get_station_list, add_lat_and_lon_to_trips

def create_heatmap_list(trips_df):
    '''
    :param trips: dataframe
    :return: list of lists of latitudes and longitudes
    '''

    heat_data = []
    for i, trip in trips_df.iterrows():
        lat_start = trip['Start_Latitude']
        lon_start = trip['Start_Longitude']
        lat_end = trip['End_Latitude']
        lon_end = trip['End_Longitude']
        lat_change = lat_start - lat_end
        lon_change = lon_start - lon_end
        heat_data += [[lat_start, lon_start],
                      [lat_start + lat_change / 2, lon_start + lon_change / 2],
                      [lat_end, lon_end]]
    return heat_data

def create_timeseries_data(trips_df):
    heat_df = trips_df.dropna(axis=0, subset=['Start_Latitude', 'Start_Longitude', 'End_Latitude', 'End_Longitude', 'hour'])

    heat_data1 = []
    for i in range(0, 24):
        heat_data2 = []
        heat_data1.append(heat_data2)

        for index, row in heat_df[heat_df['hour'] == i].iterrows():
            start_lat_lon = [row['Start_Latitude'], row['Start_Longitude']]
            end_lat_lon = [row['End_Latitude'], row['End_Longitude']]
            heat_data2.append(start_lat_lon)
            heat_data2.append(end_lat_lon)
    return heat_data1


def make_heatmap_html(heatmap_list):
    folium_map = folium.Map(location=[41.88, -87.62],
                    zoom_start = 13,)
    folium.plugins.HeatMap(heatmap_list, radius=7, min_opacity=0.25).add_to(folium_map)
    folium_map.save('heatmap.html')
    return folium_map

def make_timeseries_map_html(heatmap_data):
    folium_map = folium.Map(location=[41.88, -87.62],
                            zoom_start=13, )
    folium.plugins.HeatMapWithTime(heatmap_data, auto_play=True, max_opacity=8, radius=7, min_opacity=0.25).add_to(folium_map)
    folium_map.save('heatmap_with_time.html')
    return folium_map

def generate_timeseries_heatmap():
    stations = get_station_list()
    trips = add_lat_and_lon_to_trips(get_and_format_trip_data("resources/Divvy_Trips_2018_06.csv"), stations)
    timeseries_heatmap_data = create_timeseries_data(trips)
    make_timeseries_map_html(timeseries_heatmap_data)