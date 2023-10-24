from flask import Flask
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from Config import Config
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
jwt = JWTManager(app)

from resources.transactions import bp as transaction_bp
api.register_blueprint(transaction_bp)
from resources.employees import bp as employee_bp
api.register_blueprint(employee_bp)
from resources.managers import bp as manager_bp
api.register_blueprint(manager_bp)

# from resources.transactions import routes
# from resources.employees import routes
# from resources.managers import routes

from resources.transactions.TransactionModel import TransactionModel
from resources.employees.EmployeeModel import EmployeeModel
from resources.managers.ManagerModel import ManagerModel