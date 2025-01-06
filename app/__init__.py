from flask import Flask
from app.models import db
from app.extensions import ma
from app.blueprints.members import members_bp
from app.blueprints.books import books_bp


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    #Add extensions to app
    db.init_app(app)
    ma.init_app(app)

    #registering blueprints
    app.register_blueprint(members_bp, url_prefix='/members')
    app.register_blueprint(books_bp, url_prefix="/books")


    return app


