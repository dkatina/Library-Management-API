from flask import Flask
from app.models import db
from app.extensions import ma, limiter, cache
from app.blueprints.members import members_bp
from app.blueprints.books import books_bp
from app.blueprints.loans import loan_bp
from app.blueprints.items import items_bp
from app.blueprints.orders import orders_bp
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs' #This will be the endpoint we visit to view our docs
API_URL = "/static/swagger.yaml" #Goes to swagger file and grabs the host url

swagger_bp = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Library API"})


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
    app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL )

    return app


