from flask import jsonify, request
from . import loan_bp
from .schemas import loan_schema, loans_schema, return_loan_schema, edit_loan_schema
from app.models import db, Book, Loan
from sqlalchemy import select, delete
from marshmallow import ValidationError


@loan_bp.route("/", methods=["POST"])
def create_loan():
    try:
        loan_data = loan_schema.load(request.json)
        print(loan_data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_loan = Loan(loan_date=loan_data['loan_date'], member_id=loan_data["member_id"])

    for book_id in loan_data["book_ids"]:
        query = select(Book).where(Book.id==book_id)
        book = db.session.execute(query).scalar()
        if book:
            new_loan.books.append(book)
        else:
            return jsonify({"message": "invalid book id"}), 400
        
    db.session.add(new_loan)
    db.session.commit()

    
    return return_loan_schema.jsonify(new_loan), 201


@loan_bp.route("/", methods=['GET'])
def get_loans():
    query = select(Loan)
    result = db.session.execute(query).scalars().all()
    return loans_schema.jsonify(result), 200


@loan_bp.route("/<int:loan_id>", methods=['DELETE'])
def delete_loan(loan_id):
    query = select(Loan).where(Loan.id == loan_id)
    loan = db.session.execute(query).scalars().first()

    db.session.delete(loan)
    db.session.commit()
    return jsonify({"message": f"succesfully deleted loan {loan_id}"}), 200


@loan_bp.route("/<int:loan_id>", methods=['PUT'])
def edit_loan(loan_id):
    try:
        loan_edits = edit_loan_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Loan).where(Loan.id == loan_id)
    loan = db.session.execute(query).scalars().first()

    for book_id in loan_edits['add_book_ids']:
        query = select(Book).where(Book.id ==book_id)
        book = db.session.execute(query).scalars().first()

        if book and book not in loan.books:
            loan.books.append(book)
        
    for book_id in loan_edits['remove_book_ids']:
        query = select(Book).where(Book.id ==book_id)
        book = db.session.execute(query).scalars().first()

        if book and book in loan.books:
            loan.books.remove(book)

    db.session.commit()
    return return_loan_schema.jsonify(loan)



    

