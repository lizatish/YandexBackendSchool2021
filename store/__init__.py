from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from store.config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)

    from store.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app


app = create_app()
