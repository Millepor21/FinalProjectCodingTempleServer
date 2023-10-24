from datetime import datetime
from app import db

class TransactionModel(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key = True)
    amount = db.Column(db.String, nullable = False)
    date = db.Column(db.String, default = datetime.utcnow)
    customer_name = db.Column(db.String, nullable = False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable = False)

    def __repr__(self):
        return f'<Amount: {self.amount}\nDate: {self.date}\nCustomer: {self.customer_name}\nEmployee: {self.employee_id}>'
    
    def from_dict(self, dict):
        for k,v in dict.items():
            setattr(self, k, v)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()