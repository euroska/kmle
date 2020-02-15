import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uuid import FlaskUUID

from .config import CONFIG_BY_NAME

db = SQLAlchemy()  # pylint: disable=invalid-name
uuid = FlaskUUID()  # pylint: disable=invalid-name


def create_app(config_name=os.getenv('DOCAPI_ENV', 'dev')):
    app = Flask(__name__)
    app.config.from_object(CONFIG_BY_NAME[config_name])
    db.init_app(app)
    uuid.init_app(app)

    @app.after_request
    def add_header(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    return app
