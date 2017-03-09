from flask import Blueprint

vizboard = Blueprint('vizboard', __name__, url_prefix='/vizboard')

from .explorer.views import *
