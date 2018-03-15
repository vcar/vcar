from datetime import datetime
from ...extensions import db

# -------------------------------- Vehicle Model ------------------------------- #


class Vehicle(db.Model):
    """ Vehicle Model: """
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)

    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))
    brand = db.relationship('Brand')

    model_id = db.Column(db.Integer, db.ForeignKey('models.id'), nullable=True)
    model = db.relationship('Model')

    image = db.Column(db.String(255), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('vehicles', lazy='dynamic'))

    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=True)
    driver = db.relationship('Driver')

    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    status = db.relationship('Status')

    created = db.Column(db.DateTime(), default=datetime.utcnow())

    def __init__(self, brand_id, user_id, **kwargs):
        self.vars = kwargs
        self.brand_id = brand_id
        self.user_id = user_id
        self.model_id = kwargs.get('model_id', None)
        self.driver_id = kwargs.get('driver_id', None)
        self.status_id = kwargs.get('status_id', 1)
        self.image = kwargs.get('image')

    def __repr__(self):
        return '{} ({})'.format(self.brand, self.model)
