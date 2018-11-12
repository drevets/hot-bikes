from flask import Blueprint, render_template, request
from source.constants import station_list
from source.utility import get_hour_from_time_string
from source.make_route_map import find_intersecting_routes_and_save_map_html

bp = Blueprint('index', __name__)


@bp.route('/', methods=('GET', 'POST'))
def homepage():
    if request.method == 'GET':
        return render_template('homepage.html', stations=station_list)

    elif request.method == 'POST':
        gender = request.form['gender']
        start_station = request.form['start_station']
        end_station = request.form['end_station']
        hour = get_hour_from_time_string(request.form['time'])
        print('the type of time', type(hour))
        print('This is your preferred gender', gender)
        print('This is your start station', start_station)
        print('This is your end station', end_station)
        print('this is your time', hour)
        find_intersecting_routes_and_save_map_html(gender, hour, start_station, end_station)
        return render_template('intersecting_routes.html')