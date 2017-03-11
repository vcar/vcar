from ...extensions import db

# -------------------------------- Status Model ------------------------------- #


class Status(db.Model):
    """ Status Model:
        The status of users and drivers.
    """
    __tablename__ = 'status'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    color = db.Column(db.String(255))

    def __init__(self, title, color="primary"):
        self.title = title
        self.color = color

    def __repr__(self):
        return self.title
