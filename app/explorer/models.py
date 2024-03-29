from datetime import datetime
from ..extensions import db

# -------------------------------- Chart Model ------------------------------ #


class Chart(db.Model):
    """ Chart Model """
    __tablename__ = 'charts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True)
    token = db.Column(db.String(255), unique=True)
    isValid = db.Column(db.SmallInteger, default=0)
    error = db.Column(db.String(255), nullable=True)
    query = db.Column(db.String(255), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')

    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'))
    driver = db.relationship('Driver')

    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    vehicle = db.relationship('Vehicle')

    status = db.Column(db.SmallInteger, default=1)
    deleted = db.Column(db.SmallInteger, default=0)
    updated = db.Column(db.DateTime(), default=datetime.utcnow())
    created = db.Column(db.DateTime(), default=datetime.utcnow())

    def __init__(self, name, user_id, driver_id, vehicle_id, query, **kwargs):
        self.name = name
        self.user_id = user_id
        self.driver_id = driver_id
        self.vehicle_id = vehicle_id
        self.query = query
        self.isValid = kwargs.get('isValid', True)
        self.error = kwargs.get('error', None)

    def __repr__(self):
        return self.name
