from flask import jsonify, request
from . import books_bp
from .schemas import book_schema, books_schema
from app.models import db
from app.models import Book
from sqlalchemy import select, delete
from marshmallow import ValidationError

@books_bp.route("/", methods=['POST'])
def create_book():
    try: 
        book_data = book_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_book = Book(author=book_data['author'], genre=book_data['genre'], desc=book_data['desc'], title=book_data['title'])
    
    db.session.add(new_book)
    db.session.commit()

    return book_schema.jsonify(new_book), 201


@books_bp.route("/", methods=['GET'])
def get_books():
    query = select(Book)
    result = db.session.execute(query).scalars().all()
    return books_schema.jsonify(result), 200


@books_bp.route("/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    query = select(Book).where(Book.id == book_id)
    book = db.session.execute(query).scalars().first()
    
    if book == None:
        return jsonify({"message": "invalid book id"})
    
    try: 
        book_data = book_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in book_data.items():
        setattr(book, field, value)

    db.session.commit()
    return book_schema.jsonify(book), 200

@books_bp.route("/<int:book_id>", methods=['DELETE'])
def delete_book(book_id):
    query = select(Book).where(Book.id == book_id)
    book = db.session.execute(query).scalars().first()

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": f"succesfully deleted user {book_id}"})
    