from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='client/build')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost:5432/hot_bikes'
    db.init_app(app)


    @app.route('/')
    def index():
        return send_from_directory('client/build', 'index.html')

    @app.route('/<path:path>')
    def serve(path):
        return send_from_directory('client/build', path)

#why isn't this working?
    @app.route('/api')
    def api():
        print('hello')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(use_reloader=True, port=5000, threaded=True)


