from flask import Blueprint

loan_bp = Blueprint('loan_bp', __name__)

from . import routes