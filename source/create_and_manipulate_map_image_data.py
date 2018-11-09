import numpy as np
import folium

from source.create_image_data import to_image, get_image_data, add_alpha


def find_max_and_min_lat_and_lon(trips):
    min_lat = trips["Start_Latitude"].min()
    max_lat = trips["Start_Latitude"].max()
    max_lon = trips["Start_Longitude"].max()
    min_lon = trips["Start_Longitude"].min()
    return {min_lat, max_lat, max_lon, min_lon}

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