from app.models import Loan
from app.extensions import ma
from marshmallow import fields

class LoanSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Loan
        include_fk = True

loan_schema = LoanSchema()
loans_schema = LoanSchema(many=True)

class AddBook(ma.Schema):
    book_id =   fields.Integer(required=True)
    class Meta:
        fields = ("book_id", )

add_book_schema = AddBook()
    