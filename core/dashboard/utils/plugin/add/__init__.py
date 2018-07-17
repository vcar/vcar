import os
import sys
import re

from .src import templates_gen, views_gen, static_contain, info_gen, main_gen


class CreateNewPlugin:
  """docstring for NewPlugin"""
  base_path = "plugins"
  plugin_name = ""
  plugin_init = ""

  default_contents = {}

  def __init__(self, name, desc, author_name, author_mail, python_version, plugin_requirements, contributors_names=[], interfaces=[], license_type="BSD", version="1.0.0"):

    lowercase = lambda s: s[:1].lower() + s[1:] if s else ''
    name_list = list(filter(None, re.split(r"[, \-!?:]+", name)))
    name_list[0]=lowercase(name_list[0])
    self.plugin_name = '_'.join(name_list)
    self.plugin_init = """from os import getcwd\n"""\
          +"""from core.plugin import AppPlugin\n"""\
          + """from .src.views import """+self.plugin_name+"""\n\n"""\
          +"""__plugin__ = \""""+''.join(name_list).title()+"""\" \n\n"""\
          +"""__version__ = \""""+version+"""\" """+"""\n\n\n"""\
          +"""class """+''.join(name_list).title()+"""(AppPlugin):"""+"""\n"""\
          +"""    def setup(self):"""+"""\n"""\
          +"""        self.register_blueprint("""+self.plugin_name+""")\n"""

    if plugin_requirements=="":
      your_requirement = '''#Your dependencies here!  [pip freeze >  plugins/'''+name+'''/my_requirement.txt]'''
    else:
      your_requirement = plugin_requirements
    your_license = static_contain.copyright
    info_json = info_gen.info(self.plugin_name, author_name, desc, license_type, version, python_version)
    authors_fild = info_gen.authors(name, author_name, author_mail, contributors_names)
    doc_algo = '''## Hello world *DOC*'''
    config_param = ''''''
    readme_instr = ''''''

    main_contain = main_gen.set_main_algo(interfaces)
    views_contain = views_gen.views_template(self.plugin_name)
    template_index_contain = templates_gen.index_template(name, self.plugin_name, html_body='<p id="style_test">Body Contain!</p>')
    template_docs_contain = templates_gen.docs_template(name, self.plugin_name)
    default_contents = {
      "dirs" : [
        {
          "path" : "",
          "names": ["Docs", "workspace", "View"]
        },
        {
          "path" : "View",
          "names": ["static", "templates"]
        },
        {
          "path" : "View/templates",
          "names": [self.plugin_name]
        },
        {
          "path" : "View/static",
          "names": [self.plugin_name]
        }
      ],
      "packages" : [
        {
          "path" : "",
          "names": ["src"],
          "contains": ["from .views import "+self.plugin_name]
        },
        {
          "path" : "src",
          "names": ["algorithms"],
          "contains": ['''''']
        },
        {
          "path" : "src/algorithms",
          "names": ["helpers", "models", "preprocess"],
          "contains": ['''''', '''''', '''''']
        }
      ],
      "files" : [
        {
          "path" : "",
          "names": ["AUTHORS", "info.json", "LICENSE", "my_requirement.txt", "README.md"],
          "contains": [authors_fild, info_json, your_license, your_requirement, readme_instr]
        },
        {
          "path" : "Docs",
          "names": ["DOC.md"],
          "contains": [doc_algo]
        },
        {
          "path" : "src",
          "names": ["views.py"],
          "contains": [views_contain]
        },
        {
          "path" : "src/algorithms",
          "names": ["main.py", "config_param.py"],
          "contains": [main_contain, config_param]
        },
        {
          "path" : "View/templates/"+self.plugin_name,
          "names": ["index.html", "docs.html"],
          "contains": [template_index_contain, template_docs_contain]
        }
      ]
    }
    self.default_contents = default_contents



  def create(self, name, contents):
    root = os.path.join(self.base_path, name)
    if not os.path.exists(root):
      try:
        os.mkdir(root)
        self.new_file(root, "__init__.py", self.plugin_init)
        print ("root = {}".format(root))

        for directory in contents["dirs"]:
          for n in directory["names"]:
            self.new_dir( os.path.join(root, directory["path"]), n )

        for package in contents["packages"]:
          for n in range(len(package["names"])):
            self.new_package( os.path.join(root, package["path"]), package["names"][n], package["contains"][n] )

        for f in contents["files"]:
          for i in range(len(f["names"])):
            self.new_file( os.path.join(root, f["path"]), f["names"][i], f["contains"][i])

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

