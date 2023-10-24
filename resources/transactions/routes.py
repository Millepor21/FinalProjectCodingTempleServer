from flask.views import MethodView
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from resources.employees.EmployeeModel import EmployeeModel
from resources.managers.ManagerModel import ManagerModel
from schemas import TransactionSchema
from . import bp
from .TransactionModel import TransactionModel

bp.route('/transaction')
class TransactionList(MethodView):
    
    @bp.response(200, TransactionSchema)
    def get(self):
        return TransactionModel.query.all()
    
    @jwt_required()
    @bp.arguments(TransactionSchema)
    @bp.response(200, TransactionSchema)
    def post(self, transaction_data):
        employee_id = get_jwt_identity()
        if employee_id in EmployeeModel.id:
            transaction = TransactionModel(**transaction_data, employee_id=employee_id)
            try:
                transaction.save()
                return transaction
            except IntegrityError:
                abort(400, message='Invalid Employee Id')
        abort(400, message='Only employees can create transactions')

bp.route('/transaction/<transaction_id>')
class Transaction(MethodView):
    
    @jwt_required()
    @bp.response(200, TransactionSchema)
    def get(self, transaction_id):
        t = TransactionModel.query.get(transaction_id)
        if t:
            return t
        abort(400, message='Invalid Transaction Id')

    @jwt_required()
    def delete(self, transaction_id):
        manager_id = get_jwt_identity()
        t = TransactionModel.query.get(transaction_id)
        if t and manager_id in ManagerModel.id:
            if t.employee_id in EmployeeModel.query.filter_by(manager_id=manager_id).all():
                t.delete()
                return {'message':'Transaction Deleted'}, 202
            abort(401, message='Manager does not manage the employee in charge of this transaction and thus cannot delete it')
        abort(400, message='Invalid transaction id or the account trying to delete this transaction is not a manager')
        