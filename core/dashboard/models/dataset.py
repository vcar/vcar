import re
from datetime import datetime
from unicodedata import normalize

from ...extensions import db

# -------------------------------- Brand Model ------------------------------ #

def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    try:
        return unicode(delim.join(result))
    except:
        d = d = bytes(delim, 'utf-8')
        return str(d.join(result).decode("utf-8"))


class Dataset(db.Model):
    """ Dataset Model """
    __tablename__ = 'datasets'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    logo = db.Column(db.String(255), nullable=True)
    author = db.Column(db.String(255), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    lab = db.Column(db.String(255), nullable=True)
    template = db.Column(db.String(255), nullable=True)

    article = db.relationship("Article", uselist=False, back_populates="dataset")
    
    status = db.Column(db.SmallInteger, default=1)
    created = db.Column(db.DateTime(), default=datetime.utcnow())

    def __init__(self, name, **kwargs):
        self.name = name
        self.slug = kwargs.get('slug', slugify(name, '_'))
        self.template = kwargs.get('template', '')
        self.logo = kwargs.get('logo', DEFAULT_PHOTO)
        self.author = kwargs.get('author', '')
        self.website = kwargs.get('website', '')
        self.description = kwargs.get('description', '')
        self.lab = kwargs.get('lab', '')

    def __repr__(self):
        return self.name
