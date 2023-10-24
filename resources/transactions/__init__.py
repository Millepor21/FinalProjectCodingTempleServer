from flask_smorest import Blueprint

bp = Blueprint('transactions',__name__)

from . import routes