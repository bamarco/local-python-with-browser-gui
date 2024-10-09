#!/usr/bin/env python3
import os
import sys
import flask
import waitress
from flask import Flask, send_from_directory
from flask_cors import CORS
import backend

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError as error:
        # Path relative to the directory that this file is located in
        base_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(base_path, relative_path)

def flask_app(config):
    """
    In real world flask applicaitons, some configurations can interfere with the
    pattern suggested in the flask documentation (where a Flask app is defined
    at the top level). This pattern allows for more configuration capabilities,
    while losing the ability to use `flask run` during development.
    """
    app = Flask(__name__)
    CORS(app, resources={r'/*': {'origins': [f'http://127.0.0.1:{config.port}',
                                             f'http://localhost:{config.port}',
                                             f'https://127.0.0.1:{config.port}',
                                             f'https://localhost:{config.port}']}})

    @app.route("/")
    def hello():
        """
        We prepend the user interface with 'frontend' so other routes can be used
        for the api. An alternative approach would be to use a different port for
        the frontend and the api.
        """
        return '<a href="frontend/">Start Application</a>'

    @app.route('/ping', methods=['GET'])
    def ping_pong():
        return {'msg': backend.pong("ping")}

    #@app.route('/favicon.ico')
    #def favicon():
    #    return send_from_directory(os.path.join(resource_path("frontend"), "dist"), "favicon.ico")

    @app.route('/frontend/', defaults={'path':'index.html'})
    @app.route('/frontend/<path:path>', methods=['GET'])
    def index(path):
        """
        Deploys the vite based js frontend. We will need to `npm run build` in
        the 'frontend' directory every time we make changes.
        """
        frontend_dir = os.path.join(resource_path("frontend"), "dist")
        print(f"Deploying frontend from {frontend_dir}")
        return send_from_directory(frontend_dir, path)

    return app

def run_dev_server(config):
    """
    Run the server in development mode. We use this function because
    `flask run dev` is unavailable
    """
    app = flask_app(Config(5173))
    app.run(port=config.port, use_reloader=False, debug=True)

def run_prod_server(config):
    """
    Run the server in production mode.
    """
    app = flask_app(config)
    waitress.serve(app, port=config.port, url_scheme="http")


class Config:
    """
    Placeholder class for configuration. Will be replaced by system environment,
    config files, command line arguments, and the like.
    """
    def __init__(self, port=5000):
        self.port = port

if __name__ == '__main__':
    config = Config()
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        run_dev_server(config)
    else:
        run_prod_server(config)
