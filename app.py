from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from config import config

# Initialize extensions
db = SQLAlchemy()
cache = Cache()
migrate = Migrate()

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions with app
    db.init_app(app)
    cache.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints and routes
    from API import routes as main_routes
    app.register_blueprint(main_routes.bp)

    return app
