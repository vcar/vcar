from flask_restplus import fields
from ...restplus import rest_api




list_licence_types = ['Proprietary', 'MIT', 'BSD', 'Apache', 'GPL Freedom 0', 'GPL Freedom 1', 'GPL Freedom 2', 'GPL Freedom 3', 'EULA', 'Workstation', 'Concurrent Use', 'Site', 'Perpetual', 'Non-Perpetual', 'License with Maintenance']


interface_input_arg = rest_api.model('Interface input arg', {
    'ArgName': fields.String(required=True, example='arg1', pattern='^[A-Za-z]+[A-Za-z0-9_]*$', min_length=1, max_length=100, readOnly=True, description='Input arg name'),
    'ArgType': fields.String(readOnly=True, example='float', enum=['bool','int', 'uint', 'float', 'complex', 'string', 'time', 'enum'], description='Input arg type'),

})

plugin_interface = rest_api.model('Plugin interface', {
    'InterfaceName': fields.String(required=True,  example='interface2', pattern='^[A-Za-z]+[A-Za-z0-9_]*$', min_length=1, max_length=100, readOnly=True, description='Interface name'),
    'InputArgs': fields.List(fields.Nested(interface_input_arg)),
    'OutputFormat': fields.String(readOnly=True, enum=['json'], example='json', description='Output interface format'),
    'DrawFormat':  fields.String(readOnly=True, enum=['Text', 'Bar-charts', 'Pie-charts','Line/Area-charts', 'Other'], example='Text', description='Draw interface format'),
})

plugin_get_schema = rest_api.model('Get plugin info', {
    'identifier': fields.String(attribute='identifier', example='test_plugin', pattern='[A-Za-z0-9_]+', min_length=5, max_length=100, readOnly=True, description='The unique identifier of a plugin post'),
    'plugin_name': fields.String(attribute='name', example='test plugin', required=True, pattern='[A-Z a-z 0-9]+', min_length=5, max_length=100, readOnly=True, description='The unique name of a plugin post'),
    'description': fields.String(required=True, example='This plugin is created from the Api', readOnly=True, description='Plugin description'),
    'author_name': fields.String(attribute='author', example='Team', required=True, description='Author name'),
    'plugin_version': fields.String(attribute='version', readOnly=True, default='1.0.0', example='1.0.0', description='Plugin version'),
    'python_version': fields.String(attribute='python', readOnly=True, enum=['py2','py3'], default='py2', example='py3', description='Python version'),
    'license_type': fields.String(attribute='license', readOnly=True, enum=list_licence_types, example='MIT', description='License type', default='BSD'),
})

plugin_post_schema = rest_api.inherit('Create a new plugin', plugin_get_schema, {
    'author_email': fields.String(readOnly=True, example='team@vcar.ai', description='Author e-mail'),
    'contributor_names': fields.List(fields.String, example=["Name 1", "Name 2"]),
    'plugin_requirements': fields.String(readOnly=True, example='requirement1==version\nrequirement2==version\nrequirement3', description='Plugin requirements'),
    'python_version': fields.String(attribute='python', readOnly=True, enum=['py2','py3'], default='py2', example='py3', description='Python version'),
    'plugin_api_interfaces': fields.List(fields.Nested(plugin_interface))
})
