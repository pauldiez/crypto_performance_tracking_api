import logging.config
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail
from flask_httpauth import HTTPBasicAuth
from src.library.celery import CeleryWrapper
from src.config import Config, CeleryConfig

# setup our task manger
celery = CeleryWrapper(__name__,
                       backend=CeleryConfig.backend_url,
                       broker=CeleryConfig.broker_url,
                       include=['src.tasks'])

# set our database ORM object
db = SQLAlchemy()

# set our data validation object
mm = Marshmallow()  # used for validation

# set our email object
mail = Mail()

# set our api object that will help define our endpoints
api = Api()

# set our auth object that will be used to project our
# endpoints from the public
auth = HTTPBasicAuth()

def create_app(config_class=Config):
    """Setup our app configurations and initialize our libraries and services.
    """

    # initiate our framework use to create this app
    app = Flask(__name__)

    # set configs
    app.config.from_object(config_class)

    # set logging config
    logging.config.dictConfig(Config.logging_dict)

    # initiate database models (SQLAlchemy)
    db.init_app(app)

    # initiate data models (Marshmallow)
    mm.init_app(app)

    # initiate mail
    mail.init_app(app)

    # initiate celery
    celery.init_app(app)
    app.celery = celery

    # setup api routes
    import src.routes

    # initiate our app
    api.init_app(app)

    return app