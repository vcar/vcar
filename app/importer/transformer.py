from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# import main
from config.config import DefaultConfig
from config.database import DatabaseConfig
from ..extensions import db
from ..carboard.models.platform import Platform
from ..carboard.models.signal import Signal
from ..carboard.models.extrasignal import Extrasignal
from .helpers import slugify
from .constants import ACTIVE
# -------------------- Transformer Class : Version 0.1 ---------------------- #


class Transformer:

    def __init__(self, **kwargs):
        self.registerDB()

    def registerDB(self):
        self.app = Flask(__name__)
        self.app.config.from_object(DefaultConfig)
        self.app.config.from_object(DatabaseConfig)
        db = SQLAlchemy(self.app)

    def setPlatformById(self, platform_id):
        with self.app.app_context():
            self.platform = Platform.query.filter_by(id=platform_id, status=ACTIVE).first()
        self.signals = self.getAvailable()
        return self

    def setPlatformBySlug(self, platform_slug):
        with self.app.app_context():
            self.platform = Platform.query.filter_by(slug=platform_slug, status=ACTIVE).first()
        self.signals = self.getAvailable()
        return self
    
    def getAvailable(self):
        extra = self.platform.signals
        signals = {}
        for x in extra:
            if x.status == 1 and x.signal.status == 1:
                signals[str(x.name)] = {
                    'main': x.signal.name,
                    'class': x.signal.signalclass.name
                }
        return signals
    
    def getInfo(self, name, ignore=True):
        x = {}
        if name in self.signals:
            x['name'] = self.signals[name]['main']
            x['class'] = self.signals[name]['class']
        elif ignore == False:
            x['name'] = name
            x['class'] = 'unknown'
        else:
            x = None
        return x

    def getMain(self, extra, ignore=None):
        extra = slugify(extra)
        extrasignal = None
        with self.app.app_context():
            extrasignal = Extrasignal.query.filter_by(name=extra, platform_id=self.platform.id).first()
        ignore = self.ignore if ignore is None else ignore

        if extrasignal is not None:
            main = extrasignal.signal
            if main.status == ACTIVE and extrasignal.status == ACTIVE:
                return {
                    'name': main.name,
                    'main': True,
                    'class': main.signalclass.name,
                    'error': None
                }
            elif not ignore:
                return {
                    'name': main.name,
                    'main': True,
                    'class': main.signalclass.name,
                    'error': 'Signal `{}` is disabled but added to database anyway ! '.format(extra)
                }
            else:
                return {
                    'name': None,
                    'main': None,
                    'class': None,
                    'error': 'Signal `{}` is not currently supported'.format(extra)
                }
        else:
            if not ignore:
                msg = extrasignal
                return {
                    'name': extra,
                    'main': False,
                    'class': 'unknown',
                    'error': 'Signal `{}` is not currently supported but added to database anyway !'.format(extra)
                }
            else:
                return {
                    'name': None,
                    'main': None,
                    'class': None,
                    'error': 'Signal `{}` is not currently supported'.format(extra)
                }

    def getCorrectValue(self, value):
        return value;

    def __str__(self):
        str = ""
        for k, v in self.vars.items():
            str = str + "{} : {} | ".format(k, v)
        return str

    def showVars(self):
        print(self.vars)

    def setVar(self, k, v):
        self.vars[k] = v

    def getVar(self, k):
        return self.vars.get(k, None)
