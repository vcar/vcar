import os
import sys

##Virtualenv Settings
activate_this = '/home/karim/OpenXC/Dashboard/Flask/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

##Replace the standard out
sys.stdout = sys.stderr

##Add this file path to sys.path in order to import settings
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..'))

##Add this file path to sys.path in order to import app
sys.path.append('/home/karim/OpenXC/Dashboard/Flask/vcar/')

##Create appilcation for our app
from vcar.run import app as application
