from datetime import datetime
from ...extensions import db

# -------------------------------- Driver Model ------------------------------- #


class Model(db.Model):
    """ Vehicle Models Model """
    __tablename__ = 'models'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))
    brand = db.relationship('Brand', backref='model')

    status = db.Column(db.SmallInteger, default=1)
    created = db.Column(db.DateTime(), default=datetime.utcnow())

    def __init__(self, name, brand_id):
        self.name = name
        self.brand_id = brand_id

    def __repr__(self):
        return self.name
