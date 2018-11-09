from flask import Blueprint, render_template, request

bp = Blueprint('index', __name__)


@bp.route('/', methods=('GET', 'POST'))
def homepage():
    if request.method == 'GET':
        return render_template('homepage.html')

    elif request.method == 'POST':
        from source.make_route_map import route_random_trip_on_folium_map # why is the function being called here?
        route_random_trip_on_folium_map()
        age = request.form['age']
        print('This is your age', age)
        return render_template('homepage.html')