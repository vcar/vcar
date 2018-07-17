def title_template(title, plugin_name):
	return """{% block title %}
    """+title+""" | """+plugin_name+""" | {{ super() }}
{% endblock %}"""


def header_template(header, blue_app, plugin_name, active_location):
	return """{% block content_header %}
    <section class="content-header">
        <h1>
            """+header+"""
        </h1>
        <ol class="breadcrumb">
            <li><a href="{{ url_for('carboard.index') }}"><i class="fa fa-dashboard"></i>Home</a></li>
            <li><a href="{{ url_for('"""+blue_app+""".index') }}">"""+plugin_name+"""</a></li>
            <li class="active">"""+active_location+"""</li>
        </ol>
    </section>

    <style>
    	."""+blue_app+""" #style_test {color:red;}
    </style>

{% endblock content_header %}"""


def index_template( plugin_name, blue_app, html_body="<p>Your Body Content !!</p>"):
	return """
{% extends "layout.html" %}
"""+title_template("Overview", plugin_name)+"""

"""+header_template("Overview", blue_app, plugin_name, "Overview")+"""

{% block content %}
	<div class="row">
        <div class="col-md-12">
            <div class="box">

                <div class="box-header with-border">
                    <h3 class="box-title">Overview</h3>
                </div>

                <div class="box-body markdown">
                	<div class=\""""+blue_app+"""\">
                    	{{ html |safe }}
                		"""+html_body+"""
                	</div>
				</div>
			</div>
		</div>
	</div>
	
{% endblock %}
"""


def docs_template(plugin_name, blue_app):
	return """
{% extends "layout.html" %}
"""+title_template("Documentation", plugin_name)+"""

"""+header_template("Documentation", blue_app, plugin_name, "Documentation")+"""

{% block content %}
    <div class="row">
        <div class="col-md-12">
            <div class="box">

                <div class="box-header with-border">
                    <h3 class="box-title">Documentation</h3>
                </div>

                <div class="box-body markdown">
                	<div class=\""""+blue_app+"""\">

	                    {% if html %}

	                        {{ html }}
	                    
	                    {% else %}
	                    
	                        Add a <code>DOC.md</code> file in the root folder of your plugin if you want to have documentation shows here. <br>
	                    
	                        <code>DOC.md</code> should containe <i>markdown/html</i> syntax

	                        <br><br>
	                    {% endif %}

                    </div>

                </div>
            </div>
        </div>
    </div>

    {% if not html %}
        <div class="callout callout-vcar">
            <h4>What is markdown ?</h4>
            <p>
                Markdown is a way to style text on the web. You control the display of the document; formatting words as bold or italic, adding images, and creating lists are just a few of the things we can do with Markdown. Mostly, Markdown is just regular text with a few non-alphabetic characters thrown in, like <code>#</code> or <code>*</code>.
            </p>
        </div>

        <div class="callout callout-vcar markdown">
            <h4>Syntax guide</h4>
            <p>
                {{ "
### Headers
    # This is an <h1> tag
    ## This is an <h2> tag
    ###### This is an <h6> tag
### Emphasis
    *This text will be italic*
    _This will also be italic_
    **This text will be bold**
    __This will also be bold__
    _You **can** combine them_
### Lists
#### Unordered
    * Item 1
    * Item 2
      * Item 2a
      * Item 2b
#### Ordered
    1. Item 1
    1. Item 2
    1. Item 3
       1. Item 3a
       1. Item 3b
### Images
    ![GitHub Logo](/images/logo.png)
    Format: ![Alt Text](url)
### Links
    http://github.com - automatic!
    [GitHub](http://github.com)
### Blockquotes
    As Kanye West said:
    > We're living the future so
    > the present is our ==past==.
### Inline code
    I think you should use an
    `<addr>` element here instead.
### Tables
    First Header | Second Header
    ------------ | -------------
    Content from cell 1 | Content from cell 2
    Content in the first column | Content in the second column
                " | markdown }}
            </p>
        </div>
    {% endif %}

{% endblock %}

"""