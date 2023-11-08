from flask.views import MethodView
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas import ManagerSchema, AuthUserSchema, UpdateUserSchema, ManagerEmployeesSchema
from . import bp
from .ManagerModel import ManagerModel

@bp.route('/manager')
class ManagerList(MethodView):
    
    @bp.response(200, ManagerSchema(many=True))
    def get(self):
        return ManagerModel.query.all()
    
    @jwt_required()
    @bp.arguments(AuthUserSchema)
    def delete(self, manager_data):
        manager_id = get_jwt_identity()
        manager = ManagerModel.query.get(manager_id)
        if manager and manager.username == manager_data['username'] and manager.check_password(manager_data['password']):
            manager.delete()
            return {'message':f'{manager_data["username"]} deleted'}
        abort(400, message='Username or Password Invalid')

    @jwt_required()
    @bp.arguments(UpdateUserSchema)
    @bp.response(202, ManagerSchema)
    def put(self, manager_data):
        manager_id = get_jwt_identity()
        manager = ManagerModel.query.get(manager_id)
        if manager and manager.check_password(manager_data['password']) and manager.username == manager_data['username']:
            try:
                manager.from_dict(manager_data)
                manager.save()
                return manager
            except IntegrityError:
                abort(400, message='Username Already Taken')
        abort(400, message='Invalid Permissions to Edit This manager')

@bp.route('/manager/<manager_id>')
class Manager(MethodView):
    
    @bp.response(200, ManagerEmployeesSchema)
    def get(self, manager_id):
        manager = ManagerModel.query.get_or_404(manager_id, description='Manager Not Found')
        return manager
    
@bp.route('/manager/account')
class ManagerAccount(MethodView):
    
    @jwt_required()
    @bp.response(200, ManagerEmployeesSchema)
    def get(self):
        manager_id = get_jwt_identity()
        if manager_id in ManagerModel.id:
            manager = ManagerModel.query.get(manager_id, description='Manager Not Found')
            return manager
        else:
            abort(400, message="Not a manager")