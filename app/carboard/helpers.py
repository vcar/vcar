import os
import re
from unicodedata import normalize
from uuid import uuid4
from time import strftime
from datetime import datetime

from flask import request, url_for
from werkzeug import secure_filename

from config.config import DefaultConfig
from .constants import UPLOAD_DATASET_DIR, ALLOWED_DATASET_EXTENSIONS

# ------------------------------ View Helpers ------------------------------- #


def paginate(query, max_per_page=25):
    """ Helper to manage paginate configuration
        it take as argument a query and return a
        paginated query with given parametters
    """
    # obtain pagination arguments from the URL's query string
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get('per_page', max_per_page, type=int),
        max_per_page
    )
    # run the query with Flask-SQLAlchemy's pagination
    p = query.paginate(page, per_page)
    # build the pagination metadata to include in the response
    pages = {
        'page': page,
        'per_page': per_page,
        'total': p.total,
        'pages': p.pages
    }
    if p.has_prev:
        pages['prev_url'] = url_for(
            request.endpoint, page=p.prev_num, per_page=per_page)
    else:
        pages['prev_url'] = None
    if p.has_next:
        pages['next_url'] = url_for(
            request.endpoint, page=p.next_num, per_page=per_page)
    else:
        pages['next_url'] = None
    pages['first_url'] = url_for(
        request.endpoint, page=1, per_page=per_page)
    pages['last_url'] = url_for(
        request.endpoint, page=p.pages, per_page=per_page)
    # return a dictionary as a response
    return {'items': p.items, 'pages': pages}


def upload_file(file_data, upload_dir, oldFile=None):
    """ Upload Files """
    if file_data:
        file = secure_filename(str(uuid4()) + os.path.splitext(file_data.filename)[1].lower())
        path = os.path.join(upload_dir, strftime("%Y/%m"))
        # os.makedirs(path, exist_ok=True) Py 3.4+
        make_dir(path)
        file_data.save("/".join([path, file]))
        if oldFile is not None:
            pass
        return "/".join([strftime("%Y/%m"), file])
    return None

def upload_dsfile(input='file', dataset='_default'):
    """Upload a dataset file"""
    result = {'status': False, 'message': 'No input file'}
    if input not in request.files:
        return result
    file = request.files[input]
    if file.filename == '':
        return result
    if '.' not in file.filename:
        result['message'] = 'File without any extension'
        return result
    if file.filename.rsplit('.', 1)[1] not in ALLOWED_DATASET_EXTENSIONS:
        result['message'] = 'Extension not allowed'
        return result
    directory = "/".join([UPLOAD_DATASET_DIR, str(dataset)])
    make_dir(directory)
    file_path = "/".join([directory, secure_filename(str(uuid4()) + os.path.splitext(file.filename)[1].lower())])
    file.save(file_path)
    return {'status': True, 'message': file_path}













def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))


def choices(Model, placeholder=None, cond=1, orderField='name'):
    if cond:
        c = [(b.id, b) for b in Model.query.filter_by(status=cond).order_by(orderField).all()]
    else:
        c = [(b.id, b) for b in Model.query.order_by(orderField).all()]
    if placeholder is not None:
        c.insert(0, ('0', placeholder))
    else:
        c.insert(0, ('0', 'Select an option ...'))
    return c


def make_dir(dir_path):
    """ Make recursive directories """
    try:
        if not os.path.exists(dir_path) and not os.path.isdir(dir_path):
            os.makedirs(dir_path)
    except Exception as e:
        raise e


def redirect_back():
    """ Redirect back to last url """
    return request.args.get('next') or request.referrer or url_for('index')


def get_current_time():
    return datetime.utcnow()


def pretty_date(dt, default=None):
    """ Returns string representing "time since" e.g. 5 hours ago etc."""

    if default is None:
        default = 'just now'
    now = datetime.utcnow()
    diff = now - dt
    periods = (
        (diff.days / 365, 'year', 'years'),
        (diff.days / 30, 'month', 'months'),
        (diff.days / 7, 'week', 'weeks'),
        (diff.days, 'day', 'days'),
        (diff.seconds / 3600, 'hour', 'hours'),
        (diff.seconds / 60, 'minute', 'minutes'),
        (diff.seconds, 'second', 'seconds'),
    )
    for period, singular, plural in periods:
        if not period:
            continue
        if period == 1:
            return u'%d %s ago' % (period, singular)
        else:
            return u'%d %s ago' % (period, plural)
    return default


def allowed_extensions(filename):
    """ check if the file extension is allowed """
    return '.' in filename and filename.rsplit('.', 1)[1] in DefaultConfig.ALLOWED_AVATAR_EXTENSIONS


# ------------------------------- Form Helpers ------------------------------ #
