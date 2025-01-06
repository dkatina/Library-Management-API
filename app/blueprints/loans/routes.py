from flask import request, jsonify
from app.blueprints.loans import loans_bp
from app.blueprints.loans.schemas import loan_schema, loans_schema, add_book_schema
from marshmallow import ValidationError
from app.models import Loan, db, Book
from sqlalchemy import select, delete

@loans_bp.route("/", methods=["POST"])
def create_loan():
    try:
        loan_data = loan_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_loan = Loan(loan_date=loan_data['loan_date'], member_id=loan_data['member_id'])
    
    db.session.add(new_loan)
    db.session.commit()
    return jsonify({"status": "Successfully create New Loan", "loan": loan_schema.dump(new_loan)}), 201

@loans_bp.route("/", methods=['GET'])
def get_loans():
    query = select(Loan)
    loans = db.session.execute(query).scalars().all()

    return loans_schema.jsonify(loans)

@loans_bp.route("/add_book/<int:loan_id>", methods=['PUT'])
def add_book(loan_id):
    try:
        book_data = add_book_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    book = db.session.get(Book, book_data['book_id'])
    loan = db.session.get(Loan, loan_id)

    if book and loan:
        loan.books.append(book)

        db.session.commit()
        return jsonify({"message": "book added successfully"})
    else:
        return jsonify({"message": "Invalid book id or loan id"})

    

