from ..constants import STRING_LEN, ACTIVE
from ..helpers import get_current_time
from ...extensions import db

# -------------------------------- Driver Model ------------------------------- #


class Model(db.Model):
    """ Vehicle Models Model """
    __tablename__ = 'models'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(STRING_LEN))

    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))
    brand = db.relationship('Brand', backref='model')

    status = db.Column(db.SmallInteger, default=ACTIVE)
    created = db.Column(db.DateTime(), default=get_current_time())

    def __init__(self, name, brand_id):
        self.name = name
        self.brand_id = brand_id

    def __repr__(self):
        return self.name
