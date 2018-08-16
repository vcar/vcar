def info(name, author_name, desc, license_type, version, python_version):
    return """{
    "identifier": \""""+name+"""\",
    "name": \""""+' '.join(name.split("_"))+"""\",
    "author": \""""+author_name+"""\",
    "license": \""""+license_type+"""\",
    "description": \""""+desc+"""\",
    "version": \""""+version+"""\",
    "python":\""""+python_version+"""\",
    "options": {
        "favorite": true,
        "treeview": true,
        "menu": [
            {
                "name": "Overview",
                "action": \""""+name+""".index\",
                "iclass": "fa fa-flask"
            },
            {
                "name": "Documentation",
                "action": \""""+name+""".docs\",
                "iclass": "fa fa-book"
            }
        ]
    }
}"""

def authors(plugin_name, author_name, author_mail, contributors_names=[]):
    cont_names = ""
    for cont_name in contributors_names:
        cont_names = cont_names+"* "+cont_name+"\n"
    return plugin_name+""" plugin is written and maintained by the """+author_name+"""


# vCar Team

* """+author_name+""" <"""+author_mail+""">
* Looking for more people :)


# Contributors

"""+cont_names+"""
* Feel free to join :)
"""