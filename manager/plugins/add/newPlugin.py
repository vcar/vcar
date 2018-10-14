import os
import sys
from .struct import config_gen, services_gen, static_contain, info_gen, main_gen
import re
from flask_login import login_required, current_user

class CreateNewPlugin:
	"""docstring for NewPlugin"""
	base_path = "plugins/community"
	plugin_name = ""
	user_name = "unknown"
	py_version = "2"
	py_upgrade = ".7"
	install_requirements=True

	default_contents = {}

	@login_required
	def __init__(self, name, desc, author_name, author_mail, python_version,\
	 plugin_requirements, contributors_names=[], interfaces=[], license_type="BSD",\
	  version="1.0.0"):
		#print("\n===========================\nabs path :")
		#print(os.path.abspath("."))
		self.py_version = python_version[-1]
		lowercase = lambda s: s[:1].lower() + s[1:] if s else ''
		name_list = list(filter(None, re.split("[, \-!?:]+", name)))
		name_list[0]=lowercase(name_list[0])
		self.plugin_name = '_'.join(name_list)
		try:
			self.user_name = current_user.username
		except Exception as e:
			print(e)
		
		if plugin_requirements=="":
			self.install_requirements = False
			your_requirement = '''#Your dependencies here!  [pip freeze >  vcar/plugins/community/'''+self.user_name+'''/'''+self.plugin_name+'''/workspace/plugin_requirement.txt]'''
		else:
			your_requirement = plugin_requirements
		your_license = static_contain.copyright
		info_json = info_gen.info(self.plugin_name, author_name, desc, license_type, version, python_version)
		authors_fild = info_gen.authors(name, author_name, author_mail, contributors_names)
		doc_plugin = '''## How to start using this plugin? *DOC*'''
		config_param = config_gen.config_template(self.plugin_name, self.user_name)
		readme_instr = ''''''

		main_contain = main_gen.set_main_algo(interfaces)
		service_app_contain = services_gen.app_template(self.plugin_name, self.user_name)
		service_wsgi_contain = services_gen.wsgi_template()
		default_contents = {
			"dirs" : [
				{
					"path" : "",
					"names": ["workspace", "services"]
				},
				{
					"path" : "workspace",
					"names": ["config", "docs"]
				}
			], 
			"packages" : [
				{
					"path" : "workspace",
					"names": ["algorithms"],
					"contains": ['''''']
				}
				#,{
				#	"path" : "workspace/algorithms",
				#	"names": ["helpers", "models", "preprocess"],
				#	"contains": ['''''', '''''', '''''']
				#}
			],
			"files" : [
				{
					"path" : "workspace",
					"names": ["AUTHORS", "info.json", "LICENSE", "plugin_requirement.txt", "README.md"],
					"contains": [authors_fild, info_json, your_license, your_requirement, readme_instr] 
				},
				{
					"path" : "workspace/docs",
					"names": ["DOC.md"],
					"contains": [doc_plugin] 
				},
				{
					"path" : "workspace/config",
					"names": ["init.conf"],
					"contains": [config_param] 
				},
				{
					"path" : "workspace/algorithms",
					"names": ["main.py"],
					"contains": [main_contain] 
				},
				{
					"path" : "services",
					"names": ["app.py", "wsgi.py"],
					"contains": [service_app_contain, service_wsgi_contain] 
				}
			]
		}
		self.default_contents = default_contents
		
		

	def create(self, name, contents):
		user_plugins = os.path.join(self.base_path, self.user_name)
		if not os.path.exists(user_plugins):
			try:
				os.mkdir(user_plugins)
			except Exception as e:
				return str(e)
		
		root = os.path.join(user_plugins, name)
		if not os.path.exists(root):
			try:
				os.mkdir(root)

				for directory in contents["dirs"]:
					for n in directory["names"]:
						self.new_dir( os.path.join(root, directory["path"]), n )

				for package in contents["packages"]:
					for n in range(len(package["names"])):
						self.new_package( os.path.join(root, package["path"]), package["names"][n], package["contains"][n] )

				for f in contents["files"]:
					for i in range(len(f["names"])):
						self.new_file( os.path.join(root, f["path"]), f["names"][i], f["contains"][i])

				env_path = os.path.join(os.path.abspath("."), root, 'workspace/.env')
				print("env_path : "+env_path)
				cmd1 = 'sudo virtualenv --python=python'+str(self.py_version)+self.py_upgrade+' '+env_path
				cmd2 = 'sudo '+env_path+'/bin/pip install gunicorn werkzeug flask psutil requests Pillow flask-login'
				cmd3 = 'sudo '+env_path+'/bin/pip install -r '+os.path.join(root, 'workspace/plugin_requirement.txt')
				
				os.system(cmd1)
				os.system(cmd2)
				if self.install_requirements:
					os.system(cmd3)
				# Log files
				os.system("sudo mkdir -p /usr/local/var/log/vcar/"+self.plugin_name)

				return "True"
			except Exception as e:
				return str(e)
		else:
			return "False"

	def new_dir(self, path, name):
		dir_name = os.path.join(path, name)
		print ("directory : ",dir_name)
		if not os.path.exists(dir_name):
			os.mkdir(dir_name)

	def new_package(self, path, name, contain):
		package_name = os.path.join(path, name)
		print ("package : ",package_name)
		if not os.path.exists(package_name):
			os.mkdir(package_name)
			self.new_file(package_name, "__init__.py", contain)

	def new_file(self, path, name, contain):
		with open(os.path.join(path, name), "w") as file:
			file.write(contain)

	def run(self):
		state = self.create(self.plugin_name, self.default_contents)
		print ("\nCreation state : ",state)
		return state

