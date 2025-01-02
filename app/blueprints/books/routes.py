from pydoc import pager
from flask import jsonify, request
from . import books_bp
from .schemas import book_schema, books_schema
from app.models import db
from app.models import Book
from sqlalchemy import select, delete
from marshmallow import ValidationError
from app.extensions import cache

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

#PAGINATION!
@books_bp.route("/", methods=['GET'])
# @cache.cached(timeout=60)
def get_books():
    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(Book)
        books = db.paginate(query, page=page, per_page=per_page)
        return books_schema.jsonify(books), 200
    except:
        query = select(Book)
        books = db.session.execute(query).scalars().all() 
        return books_schema.jsonify(books), 200  


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
    
#MOST POPULAR BOOKS
@books_bp.route("/popular", methods=['GET'])
def popular_books():
    query = select(Book)
    books = db.session.execute(query).scalars().all()

    books.sort(key= lambda book: len(book.loans), reverse=True)

    return books_schema.jsonify(books)

#QUERY PARAMETER ROUTE
@books_bp.route("/search", methods=['GET'])
def search_book():
    title = request.args.get("title")
    
    query = select(Book).where(Book.title.like(f'%{title}%')) # % - wildcard character meaning any number, of any character(s) can be hear
    books = db.session.execute(query).scalars().all()

    return books_schema.jsonify(books)
