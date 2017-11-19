import jinja2
import flask

from .carboard.constants import ROLES, MIMETYPE

filters = flask.Blueprint('filters', __name__)

# ---------------------- -- -- -- -- -- -- -- -- -- -- ---------------------- #


@jinja2.contextfilter
@filters.app_template_filter()
def roles(context, value):
    """ Return the Role name from ROLES list."""
    return ROLES[value][1]
# ---------------------- -- -- -- -- -- -- -- -- -- -- ---------------------- #


@jinja2.contextfilter
@filters.app_template_filter()
def mimetypes(context, value):
    """ Return the Format name from MIMETYPE list."""
    return MIMETYPE[value][1]
# ---------------------- -- -- -- -- -- -- -- -- -- -- ---------------------- #


@jinja2.contextfilter
@filters.app_template_filter()
def status(context, value):
    return 2
