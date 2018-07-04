import logging.config
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail
from flask_httpauth import HTTPBasicAuth
from src.library.celery import CeleryWrapper
from src.config import Config, CeleryConfig

# initiate Celery
celery = CeleryWrapper(__name__,
                       backend=CeleryConfig.backend_url,
                       broker=CeleryConfig.broker_url,
                       include=['src.tasks'])
# set SQLAlchemy
db = SQLAlchemy()

# set Marshmallow
mm = Marshmallow()

# set Mail
mail = Mail()

# set Api
api = Api()

auth = HTTPBasicAuth()

def create_app(config_class=Config):
    """
        Create an application factory - a clean way to create app instances and avoid package/import errors
        See http://flask.pocoo.org/docs/0.12/patterns/appfactories/
    """

    #
    # create app and initiate app services
    #

    # initiate Flask
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

    # initiate init
    api.init_app(app)

    return app