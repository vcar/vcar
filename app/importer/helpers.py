import os
import re
from unicodedata import normalize
from uuid import uuid4
from time import strftime
from datetime import datetime

from flask import request, url_for, session, redirect, flash
from werkzeug import secure_filename

from config.config import DefaultConfig
from .constants import UPLOAD_TRACE_DIR, ALLOWED_TRACE_EXTENSIONS

# ------------------------------ View Helpers ------------------------------- #


def upload_file(file_data, upload_dir, oldFile=None):
    """ Upload Files """
    if file_data:
        file = secure_filename(
            str(uuid4()) + os.path.splitext(file_data.filename)[1].lower())
        path = os.path.join(upload_dir, strftime("%Y/%m"))
        # os.makedirs(path, exist_ok=True) Py 3.4+
        make_dir(path)
        file_data.save("/".join([path, file]))
        if oldFile is not None:
            pass
        return "/".join([strftime("%Y/%m"), file])
    return None


def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    if type(text) == str:
        text = text.decode()
    result = []
    _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))


def choices(Model, placeholder=None, cond=1, orderField='name'):
    if cond:
        c = [(b.id, b) for b in Model.query.filter_by(
            status=cond).order_by(orderField).all()]
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


def allowed_extensions(filename):
    """ check if the file extension is allowed """
    return '.' in filename and filename.rsplit('.', 1)[1] in DefaultConfig.ALLOWED_AVATAR_EXTENSIONS


def checkSteps(step):
    if step >= 1:
        if 'import' not in session or 'user' not in session['import'] or 'platform' not in session['import']:
            flash('Please choose a platform first.', 'success')
            return redirect(url_for('importer.platform'))
        elif step == 1:
            return True
    if step >= 2:
        if 'vehicle' not in session['import']:
            flash('Please choose a vehicle or select an anonymous one.', 'success')
            return redirect(url_for('importer.vehicle'))
        elif step == 2:
            return True
    if step >= 3:
        if 'driver' not in session['import']:
            flash('Please choose a driver or select an anonymous one.', 'success')
            return redirect(url_for('importer.driver'))
        elif step == 3:
            return True
    if step > 4:
        if 'files' not in session['import']:
            flash('Please upload some files before getting here', 'success')
            return redirect(url_for('importer.records'))
        elif step == 4:
            return True


def upload_trace(input='file', user_id=0):
    """Upload a trace file"""
    result = {'status': False, 'message': 'No input file'}
    if input not in request.files:
        return result
    file = request.files[input]
    if file.filename == '':
        return result
    if '.' not in file.filename:
        result['message'] = 'File without any extension'
        return result
    if file.filename.rsplit('.', 1)[1] not in ALLOWED_TRACE_EXTENSIONS:
        result['message'] = 'Extension not allowed'
        return result
    directory = "/".join([UPLOAD_TRACE_DIR, str(user_id)])
    directory = "/".join([directory, strftime("%Y/%m")])
    make_dir(directory)
    file_path = "/".join([directory, secure_filename(str(uuid4()) +
                                                     os.path.splitext(file.filename)[1].lower())])
    file.save(file_path)
    return {'status': True, 'message': file_path}

# ------------------------------- Form Helpers ------------------------------ #
