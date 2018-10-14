from flask_restplus import fields
from ...restplus import rest_api

sys_stat_get_schema = rest_api.model('Get currents System Status', {
    'rss': fields.Integer(attribute='rss', required=True, readOnly=True, description='RAM usage(Bytes)'),
    'usedCPU': fields.Float(attribute='usedCPU', required=True, readOnly=True, description='CPU usage(%)'),
})

Current_sys_stat_get_schema = rest_api.model('Get currents Process Status', {
    
    'name': fields.String(attribute='name', required=True, readOnly=True, description='Process name'),
    'status': fields.String(attribute='status', required=True, readOnly=True, description='Process status'),
    'userName': fields.String(attribute='userName', required=True, readOnly=True, description='User name'),
    'rss': fields.Integer(attribute='rss', required=True, readOnly=True, description='RAM : Resident Set Size(Bytes)'),
    'usedCPU': fields.Float(attribute='usedCPU', required=True, readOnly=True, description='CPU usage(%)'),
    'numThreads': fields.Integer(attribute='numThreads', required=True, readOnly=True, description='Number Threads'),
})

waitCurrentProcess_post_schema = rest_api.model('Wait for process to terminate', {
    'pid': fields.Integer(attribute='pid', pattern='[0-9]+', min_length=1, max_length=20, required=True, readOnly=True, description='RAM usage(Bytes)'),
    'timeout': fields.Integer(attribute='timeout', pattern='[0-9]+', min_length=1, max_length=20, required=True, readOnly=True, description='time to wait in seconds'),
})