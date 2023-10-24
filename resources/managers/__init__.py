from flask_smorest import Blueprint

bp = Blueprint('managers',__name__)

from . import routes, auth_routes