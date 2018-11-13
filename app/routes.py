from flask import Blueprint, render_template, request, redirect
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
        find_intersecting_routes_and_save_map_html(gender, hour, start_station, end_station)
        return redirect(location='/intersect')

@bp.route('/intersect', methods=('GET', 'POST'))
def intersect():
    if request.method == 'GET':
        return render_template('intersecting_routes.html')
    elif request.method == 'POST':
        return redirect('/')