from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token

from schemas import AuthUserSchema, ManagerSchema
from . import bp 
from .ManagerModel import ManagerModel

@bp.post('/register')
@bp.arguments(ManagerSchema)
@bp.response(201, ManagerSchema)
def register(manager_data):
    manager = ManagerModel()
    manager.from_dict(manager_data)
    try:
        manager.save()
        return manager_data
    except IntegrityError:
        abort(400, message='Username Already Taken')

@bp.post('/login')
@bp.arguments(AuthUserSchema)
def login(login_info):
    manager = ManagerModel.query.filter_by(username=login_info['username']).first()
    if manager and manager.check_password(login_info['password']):
        access_token = create_access_token(identity=manager.id)
        return {'access_token':access_token}
    abort(400, message='Invalid Username or Password')