import jinja2
import flask

from .carboard.constants import USER_ROLES

filters = flask.Blueprint('filters', __name__)

# ---------------------- -- -- -- -- -- -- -- -- -- -- ---------------------- #


@jinja2.contextfilter
@filters.app_template_filter()
def roles(context, value):
    """ Return the Role name from USER_ROLES list."""
    return USER_ROLES[value][1]
# ---------------------- -- -- -- -- -- -- -- -- -- -- ---------------------- #


@jinja2.contextfilter
@filters.app_template_filter()
def status(context, value):
    return 2
