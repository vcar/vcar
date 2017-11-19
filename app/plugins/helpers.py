from os import path
from flask_misaka import markdown


def render_md(filepath, file):
    """
        Function takes as input a markdown file and generate
        a rendred html file as output
    """
    try:
        with open(path.join(str(filepath[0]), str(file))) as fd:
            mkdwn = fd.read()
            html = markdown(mkdwn)
    except Exception:
        html = None

    return html
