from matplotlib.colors import LinearSegmentedColormap, hsv_to_rgb, rgb_to_hsv
import scipy.ndimage.filters
from PIL import Image, ImageDraw
import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')

def get_kernel(kernel_size, blur=1 / 20, halo=.001):
    """
    Create an (n*2+1)x(n*2+1) numpy array.
    Output can be used as the kernel for convolution.
    """
    x, y = np.mgrid[0:kernel_size * 2 + 1, 0:kernel_size * 2 + 1]
    center = kernel_size + 1
    r = np.sqrt((x - center) ** 2 + (y - center) ** 2)

    kernel = np.exp(-r / kernel_size / blur) + (1 - r / r[center, 0]).clip(0) * halo
    return kernel


def add_lines(image_array, xys, width=1, weights=None):
    """
    Add a set of lines (xys) to an existing image_array
    width: width of lines
    weights: [], optional list of multipliers for lines.
    """

    for i, xy in enumerate(xys):

        image = Image.new("L", (image_array.shape[1], image_array.shape[0]))
        ImageDraw.Draw(image).line(xy, 200, width=width)

        new_image_array = np.asarray(image, dtype=np.uint8).astype(float)

        if weights is not None:
            new_image_array *= weights[i]

        image_array += new_image_array

    new_image_array = scipy.ndimage.filters.convolve(image_array, get_kernel(width * 4))
    return new_image_array


def to_image(array, hue=.62):
    """converts an array of floats to an array of RGB values using a colormap"""

    image_data = np.log(array + 1)

    saturation_values = [[0, 0], [1, .68], [.78, .87], [0, 1]]
    colors = [hsv_to_rgb([hue, x, y]) for x, y in saturation_values]
    cmap = LinearSegmentedColormap.from_list("my_colormap", colors)

    out = cmap(image_data / image_data.max())

    out = (out * 255).astype(np.uint8)
    return out

def latlon_to_pixel(lat, lon, image_shape, max_lat, max_lon, min_lon):
    delta_x = image_shape[1] / (max_lon - min_lon)

    delta_y = delta_x / np.cos(lat / 360 * np.pi * 2)
    pixel_y = (max_lat - lat) * delta_y
    pixel_x = (lon - min_lon) * delta_x
    return (pixel_y, pixel_x)


def row_to_pixel(row, image_shape, max_lat, max_lon, min_lon):
    """
    convert a row (1 trip) to pixel coordinates
    of start and end point
    """
    start_y, start_x = latlon_to_pixel(row["Start_Latitude"],
                                       row["Start_Longitude"], image_shape, max_lat, max_lon, min_lon)
    end_y, end_x = latlon_to_pixel(row["End Station Latitude"],
                                   row["End Station Longitude"], image_shape, max_lat, max_lon, min_lon)
    xy = (start_x, start_y, end_x, end_y)
    return xy


def get_image_data(max_lat, max_lon, min_lon, paths, min_count=0, max_count=None):
    # generate empty pixel array
    image_data = np.zeros((900 * 2, 400 * 2))

    # generate pixel coordinates of starting points and end points
    if max_count is None:
        max_count = paths["Trip Count"].max() + 1

    selector = (paths["Trip Count"] >= min_count) & (paths["Trip Count"] < max_count)
    xys = [row_to_pixel(row, image_data.shape, max_lat, max_lon, min_lon) for i, row in paths[selector].iterrows()]
    # draw the lines
    image_data = add_lines(image_data, xys, weights=paths["Trip Count"], width=1)
    return image_data


def add_alpha(image_data):
    """
    Uses the Value in HSV as an alpha channel.
    This creates an image that blends nicely with a black background.
    """

    # get hsv image
    hsv = rgb_to_hsv(image_data[:, :, :3].astype(float) / 255)

    # create new image and set alpha channel
    new_image_data = np.zeros(image_data.shape)
    new_image_data[:, :, 3] = hsv[:, :, 2]

    # set value of hsv image to either 0 or 1.
    hsv[:, :, 2] = np.where(hsv[:, :, 2] > 0, 1, 0)

    # combine alpha and new rgb
    new_image_data[:, :, :3] = hsv_to_rgb(hsv)
    return new_image_data
