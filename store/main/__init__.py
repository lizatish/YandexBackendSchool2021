from flask import Blueprint

bp = Blueprint('main', __name__)

from store.main import routes, models
