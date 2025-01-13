from flask import Flask
from app.models import db
from app.extensions import ma, limiter, cache
from app.blueprints.members import members_bp
from app.blueprints.books import books_bp
from app.blueprints.loans import loan_bp
from app.blueprints.items import items_bp
from app.blueprints.orders import orders_bp
from app.blueprints.ebooks import ebooks_bp


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    #Add extensions to app
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    #registering blueprints
    app.register_blueprint(members_bp, url_prefix='/members')
    app.register_blueprint(books_bp, url_prefix="/books")
    app.register_blueprint(loan_bp, url_prefix="/loans")
    app.register_blueprint(items_bp, url_prefix="/items")
    app.register_blueprint(orders_bp, url_prefix="/orders")
    app.register_blueprint(ebooks_bp, url_prefix="/ebooks")

    return app


