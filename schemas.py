from marshmallow import Schema, fields

class ManagerSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)

class EmployeeSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)

class TransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    amount = fields.Str(required=True)
    date = fields.Str()
    customer_name = fields.Str(required=True)
    employee_id = fields.Int()

class EmployeeTransactionsSchema(Schema):
    transactions = fields.List(fields.Nested(TransactionSchema), dump_only=True)

class ManagerEmployeesSchema(Schema):
    employees = fields.List(fields.Nested(EmployeeSchema), dump_only=True)

class AuthUserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class UpdateUserSchema(Schema):
  username = fields.Str(required=True)
  password = fields.Str(required = True, load_only = True)
  new_username = fields.Str()
  new_password = fields.Str()
  first_name = fields.Str()
  last_name = fields.Str()