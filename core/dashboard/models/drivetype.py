from ...extensions import db

# -------------------------------- Status Model ------------------------------- #


class DriveType(db.Model):
    """ DriveType Model:
        The type of driving records.
    """
    __tablename__ = 'drivetypes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name
