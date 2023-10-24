from flask.views import MethodView
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas import EmployeeSchema, AuthUserSchema, UpdateUserSchema, EmployeeTransactionsSchema
from . import bp
from .EmployeeModel import EmployeeModel

@bp.route('/employee')
class EmployeeList(MethodView):
    
    @bp.response(200, EmployeeSchema(many=True))
    def get(self):
        employees = EmployeeModel.query.all()
        return employees
    
    @jwt_required()
    @bp.arguments(AuthUserSchema)
    def delete(self, employee_data):
        employee_id = get_jwt_identity()
        employee = EmployeeModel.query.get(employee_id)
        if employee and employee.username == employee_data['username'] and employee.check_password(employee_data['password']):
            employee.delete()
            return {'message':f'{employee_data["username"]} deleted'}
        abort(400, message='Username or Password Invalid')

    @jwt_required()
    @bp.arguments(UpdateUserSchema)
    @bp.response(202, EmployeeSchema)
    def put(self, employee_data):
        employee_id = get_jwt_identity()
        employee = EmployeeModel.query.get(employee_id)
        if employee and employee.check_password(employee_data['password']) and employee.username == employee_data['username']:
            try:
                employee.from_dict(employee_data)
                employee.save()
                return employee
            except IntegrityError:
                abort(400, message='Username Already Taken')
        abort(400, message='Invalid Permissions to Edit This Employee')

@bp.route('/employees/<employee_id>')
class Employee(MethodView):
    
    @bp.response(200, EmployeeTransactionsSchema)
    def get(self, employee_id):
        employee = EmployeeModel.query.get_or_404(employee_id, description='Employee Not Found')
        return employee