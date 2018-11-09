from flask import Blueprint, render_template, request

bp = Blueprint('index', __name__)


@bp.route('/', methods=('GET', 'POST'))
def homepage():
    if request.method == 'GET':
        return render_template('homepage.html')

    elif request.method == 'POST':
        age = request.form['age']
        print('This is your age', age)
        return render_template('homepage.html')