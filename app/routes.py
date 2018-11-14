from flask import Blueprint, render_template, request, redirect, url_for
from source.constants import station_list
from source.utility import get_hour_from_time_string, sanitize_gender
from source.make_route_map import find_intersecting_routes_and_save_map_html

bp = Blueprint('index', __name__)


@bp.route('/', methods=('GET', 'POST'))
def homepage():
    if request.method == 'GET':
        return render_template('homepage.html', stations=station_list)

    elif request.method == 'POST':
        gender = sanitize_gender(request.form['gender'])
        start_station = request.form['start_station']
        end_station = request.form['end_station']
        hour = get_hour_from_time_string(request.form['time'])
        trip_data = find_intersecting_routes_and_save_map_html(gender, hour, start_station, end_station)
        return redirect(url_for('index.intersect',
                                gender=trip_data['gender'],
                                years=trip_data['age'],
                                date=trip_data['date'],
                                location=trip_data['location']))

@bp.route('/intersect', methods=('GET', 'POST'))
def intersect():
    if request.method == 'GET':
        gender = request.args['gender']
        years = request.args['years']
        date = request.args['date']
        location = request.args['location']
        return render_template('intersecting_routes.html',
                               gender=gender,
                               years=years,
                               date=date,
                               location=location)
    elif request.method == 'POST':
        return redirect('/')
