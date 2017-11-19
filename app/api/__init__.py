from flask import Blueprint

"""
    This package should represent the vCar API main package
"""

api = Blueprint('api', __name__, url_prefix='/api')
