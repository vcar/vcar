from datetime import datetime
from ...extensions import db

# -------------------------------- Record Model ------------------------------- #


class Record(db.Model):
    """ Record Model: """
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')

    drivetype_id = db.Column(db.Integer, db.ForeignKey('drivetypes.id'))
    drivetype = db.relationship('DriveType')

    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=True)
    driver = db.relationship('Driver')

    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=True)
    vehicle = db.relationship('Vehicle')

    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    status = db.relationship('Status')

    trace = db.Column(db.String(255))
    start = db.Column(db.DateTime(), nullable=True)
    end = db.Column(db.DateTime(), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    created = db.Column(db.DateTime(), default=datetime.utcnow())

    def __init__(self, user_id, drivetype_id, trace, **kwargs):
        self.vars = kwargs
        self.user_id = user_id
        self.drivetype_id = drivetype_id
        self.trace = trace
        self.name = kwargs.get('name', "Record")
        self.driver_id = kwargs.get('driver_id', None)
        self.vehicle_id = kwargs.get('vehicle_id', None)
        self.status_id = kwargs.get('status_id', 1)
        self.start = kwargs.get('start', None)
        self.end = kwargs.get('end', None)
        self.description = kwargs.get('description', None)

    def __repr__(self):
        return '{} {}'.format(self.name, self.id)
