from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from src.config import Config
from src.app import db
from src.models import FeedModel


# initiate app
app = Flask(__name__)

# set configs
app.config.from_object(Config)

db.init_app(app)

migrate = Migrate(app, db, directory=Config.MIGRATION_DIR_PATH)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()