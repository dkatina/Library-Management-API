from flask import Blueprint

ebooks_bp = Blueprint('ebooks_bp', __name__)

from . import routes