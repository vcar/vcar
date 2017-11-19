import os
from time import strftime
from datetime import datetime

from flask import request, url_for
from werkzeug import secure_filename

from config.config import DefaultConfig
from .constants import UPLOAD_TRACE_DIR, ALLOWED_TRACE_EXTENSIONS, TRANSFORM

# ------------------------------ View Helpers ------------------------------- #


def upload_trace(input='file', user_id=0):
    """Upload a trace file"""
    result = {'status': False, 'message': 'No input file'}
    if input not in request.files:
        return result
    file = request.files[input]
    if file.filename == '':
        return result
    if '.' not in file.filename:
        result['message'] = 'extension not allowed'
        return result
    if file.filename.rsplit('.', 1)[1] not in ALLOWED_TRACE_EXTENSIONS:
        result['message'] = 'extension not allowed'
        return result
    directory = "/".join([UPLOAD_TRACE_DIR, str(user_id)])
    directory = "/".join([directory, strftime("%Y/%m")])
    make_dir(directory)
    file_path = "/".join([directory, secure_filename(file.filename)])
    file.save(file_path)
    return {'status': True, 'message': file_path}


def correct_value(value):
    try:
        return int(value)
    except:
        for k, v in TRANSFORM.items():
            if value == v:
                return k
        return -99999


def correct_time(timestamp):
    try:
        timestamp = str(timestamp)
        t = timestamp.split('.')
        return '{}{}'.format(t[0], t[1][:3].ljust(3, '0'))
    except:
        return timestamp.split('.')[0]


def debug(obj):
    print("\n------------------ Start DEBUG ------------------")
    for a, v in obj.__dict__.iteritems():
        print("\t [{}] = {}".format(a, v))
    print("------------------- END DEBUG -------------------\n")


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

# ------------------------------- Form Helpers ------------------------------ #
