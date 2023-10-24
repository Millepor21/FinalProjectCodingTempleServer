from flask_smorest import Blueprint

bp = Blueprint('employees',__name__)

from . import routes, auth_routes