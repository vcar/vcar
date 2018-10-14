import logging
from flask_login import login_required, current_user
from flask import request, current_app
from flask_restplus import Resource
#import flask_plugins
from multiprocessing.pool import ThreadPool
from subprocess import check_call
import os
import json

from ..serializers.add_plugin_serializer import plugin_get_schema, plugin_post_schema
from ...restplus import rest_api
from manager.plugins.add.newPlugin import CreateNewPlugin




log = logging.getLogger(__name__)

ns = rest_api.namespace('plugin/add', description='Operations related to add a new plugin')

@login_required
@ns.route('/')
class NewPlugin(Resource):

    @rest_api.marshal_list_with(plugin_get_schema)
    def get(self):
        """
        Returns list of all user's plugins.
        """
        def get_info(path_p, name):
            path = path_p+name+"/workspace/info.json"
            try:
                with open(path, 'r') as f:
                    plugin_info = json.load(f)
                    info = dict((k,plugin_info[k]) for k in ("identifier","name","author","license","description","version","python") if k in plugin_info)
                    return info
            except Exception:
                return {
                    "identifier":name,
                    "name": "",
                    "author": "",
                    "license": "",
                    "description": "",
                    "version": "",
                    "python":""
                    }

        try:            
            path_p = "plugins/community/"+current_user.username+"/"
            l_plugins = list(filter(lambda x: os.path.isdir(path_p+x) and not x.startswith('.'), os.listdir(path_p)))
            plugins_info = []
            for x in l_plugins:
                plugins_info.append(get_info(path_p, x))

        except Exception:
            plugins_info = None

        return plugins_info

    @rest_api.response(201, 'Plugin successfully created.')
    @rest_api.response(202, 'Plugin name already exist.')
    @rest_api.response(203, 'ERROR! Plugin has not been created!')
    @rest_api.expect(plugin_post_schema, validate=True)
    def post(self):
        """
        Creates a new plugin.
        """
        data = request.json
        
        try:
            usr_plugin_dir = os.path.join("plugins/community", current_user.username, data['plugin_name'])
            if os.path.exists(usr_plugin_dir):
                try:
                    pass
                except Exception as e:
                    print('ERROR! Plugin already exist! : {}'.format(str(e)))
                    return None, 202
            thread_function = CreateNewPlugin(data['plugin_name'], data['description'], data['author_name'], data['author_email'], data['python_version'], data['plugin_requirements'], data['contributor_names'], data['plugin_api_interfaces'], data['license_type'], data['plugin_version'])
            pool = ThreadPool(processes=1)
            async_result = pool.apply_async(thread_function.run, ())
            return_val = async_result.get()
            
            if return_val=="True":
                '''Plugin has been created successfully'''
                return None, 201
                
            elif return_val=="False":
                '''Plugin name already exist'''
                return None, 202
                
            else:
                '''ERROR !'''
                try:
                    pass
                except Exception as e:
                    print('ERROR! : {}'.format(str(e)))
                    raise

        except Exception as e:
            print('ERROR! Plugin has not been created! : {}'.format(str(e)))
            return None, 203

@login_required
@ns.route('/<string:identifier>')
@rest_api.response(404, 'Plugin name not found.')
class IdentPlugin(Resource):

    @rest_api.marshal_with(plugin_get_schema)
    def get(self, identifier):
        """
        Returns a Plugin with a list of infos.
        """
        try:
            # To do ...
            #plugins = flask_plugins.get_plugin_from_all(identifier)
            pass
        except Exception:
            plugins = None

        return {"To do"}


    @rest_api.response(204, 'Plugin successfully deleted.')
    @rest_api.response(205, 'ERROR! Plugin has not been deleted!')
    def delete(self, identifier):
        """
        Delete Plugin.
        """
        
        try:
            pass
            return None, 204
        except Exception:
            return None, 205
        
        
