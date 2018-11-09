from flask import Flask, render_template
from . import routes

def create_app():
    app = Flask(__name__)

    app.register_blueprint(routes.bp)

    return app
