from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from typing import List

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


loan_book = db.Table(
    "loan_book",
    Base.metadata,
    db.Column("loan_id", db.ForeignKey("loans.id")),
    db.Column("book_id", db.ForeignKey("books.id"))
)

class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(150), unique=True, nullable=False)
    DOB: Mapped[date] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(db.String(100), nullable=False)

    loans: Mapped[List["Loan"]] = db.relationship(back_populates="member", cascade="all, delete") #When we delete a Memeber we remove the records of their loans
    orders: Mapped[List["Order"]] = db.relationship(back_populates="member", cascade="all, delete")

class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(primary_key=True)
    loan_date: Mapped[date]
    member_id: Mapped[int] = mapped_column(db.ForeignKey("members.id"), nullable=False)

    member: Mapped["Member"] = db.relationship(back_populates="loans")
    books: Mapped[List["Book"]] = db.relationship(secondary=loan_book, back_populates="loans")

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[str] = mapped_column(db.String(100), nullable=False)
    genre: Mapped[str] = mapped_column(db.String(50), nullable=False)
    desc: Mapped[str] = mapped_column(db.String(255), nullable=False)
    title: Mapped[str] = mapped_column(db.String(100), nullable=False)

    loans: Mapped[List["Loan"]] = db.relationship(secondary=loan_book, back_populates="books")

class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    price: Mapped[float] = mapped_column(db.Float(), nullable=False)

    order_items: Mapped[List["OrderItems"]] = db.relationship(back_populates = "item")

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_date: Mapped[date] = mapped_column(nullable=False)
    member_id: Mapped[int] = mapped_column(db.ForeignKey("members.id"), nullable=False)

    member: Mapped["Member"] = db.relationship(back_populates="orders")
    order_items: Mapped[List["OrderItems"]] = db.relationship(back_populates = "order")

class OrderItems(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(db.ForeignKey("orders.id"), nullable=False)
    item_id: Mapped[int] = mapped_column(db.ForeignKey("items.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)

    order: Mapped["Order"] = db.relationship(back_populates= "order_items")
    item: Mapped["Item"] = db.relationship(back_populates= "order_items")