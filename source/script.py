from make_station_map import *
from draw_paths import *
from make_heatmap import *
import numpy as np

stations = get_station_list()
trips = add_lat_and_lon_to_trips(get_and_format_trip_data("resources/Divvy_Trips_2018_06.csv"), stations)
stations = add_trip_counts_to_stations(stations, trips)
station_map = put_stations_on_map(stations)

# timeseries_heatmap_data = create_timeseries_data(trips)
# make_timeseries_map(timeseries_heatmap_data)

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