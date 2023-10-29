from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token

from schemas import AuthUserSchema, EmployeeSchema
from . import bp 
from .EmployeeModel import EmployeeModel

@bp.post('/register_employee')
@bp.arguments(EmployeeSchema)
@bp.response(201, EmployeeSchema)
def register(employee_data):
    employee = EmployeeModel()
    employee.from_dict(employee_data)
    if employee_data['username'] not in EmployeeModel.username:
        employee.save()
        return employee_data
    else:
        abort(400, message='Username Already Taken')

@bp.post('/login_employee')
@bp.arguments(AuthUserSchema)
def login(login_info):
    employee = EmployeeModel.query.filter_by(username=login_info['username']).first()
    if employee and employee.check_password(login_info['password']):
        access_token = create_access_token(identity=employee.id)
        return {'access_token':access_token}
    abort(400, message='Invalid Username or Password') 