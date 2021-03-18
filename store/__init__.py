
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_babel import Babel
from config import Config

db = SQLAlchemy()
migrate = Migrate()
babel = Babel()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    babel.init_app(app)
    # from store.errors import bp as errors_bp
    # store.register_blueprint(errors_bp)


    return app

app = create_app()

from store import routes, models