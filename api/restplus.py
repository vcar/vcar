import logging
import traceback

from flask_restplus import Api
from core.config.config import DefaultConfig as settings
from sqlalchemy.orm.exc import NoResultFound

log = logging.getLogger(__name__)

rest_api = Api(version='1.0', title='vCar API',
          description='A simple test of a Flask RestPlus powered API')


@rest_api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.DEBUG:
        return {'message': message}, 500


@rest_api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404
