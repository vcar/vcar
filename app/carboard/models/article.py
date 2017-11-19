from datetime import datetime
from ...extensions import db

# -------------------------------- Brand Model ------------------------------ #


class Article(db.Model):
    """ Article Model """
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    authors = db.Column(db.String(255))
    abstract = db.Column(db.String(255), nullable=True)
    publication_date = db.Column(db.DateTime(), nullable=True)
    keywords = db.Column(db.String(255), nullable=True)
    reference = db.Column(db.String(255), nullable=True)
    link = db.Column(db.String(255), nullable=True)

    dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.id'), nullable=True)
    dataset = db.relationship('Dataset', back_populates="article")

    created = db.Column(db.DateTime(), default=datetime.utcnow())

    def __init__(self, name, authors, dataset_id=None, abstract=None, publication_date=None, keywords=None, reference=None, link=None):
        self.dataset_id = dataset_id
        self.name = name
        self.authors = authors
        self.abstract = abstract
        self.publication_date = publication_date
        self.keywords = keywords
        self.reference = reference
        self.link = link

    def __repr__(self):
        return self.name
