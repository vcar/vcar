from uuid import uuid4
from datetime import datetime
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
from ..constants import DEFAULT_AVATAR, ROLE_USER, ROLE_ADMIN
from ...extensions import db


# -------------------------------- User Model ------------------------------- #

class User(db.Model, UserMixin):
    """ User Model:
        the user can be a person or even a campany, he/it can manage drivers
        and vehicles.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255))
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255), nullable=True, default=DEFAULT_AVATAR)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    activation = db.Column(db.String(255))
    status = db.Column(db.SmallInteger, default=1)
    last_login = db.Column(db.DateTime(), default=datetime.utcnow())
    created = db.Column(db.DateTime(), default=datetime.utcnow())

    def __init__(self, username, email, password, fullname=None, avatar=None, role=ROLE_USER, status=1):
        self.fullname = fullname or username
        self.username = username
        self.email = email.lower()
        self.password = generate_password_hash(password)
        self.avatar = avatar
        self.role = role
        self.activation = str(uuid4())
        self.status = status

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_authenticated(self):
        return True

    def is_active(self):
        return self.status

    def is_anonymous(self):
        return False

    def is_admin(self):
        return self.role == ROLE_ADMIN

    def get_id(self):
        return self.id

    def __repr__(self):
        return '{} ({})'.format(self.username, self.email)

    def get_role(self):
        return self.role

    def get_status(self):
        return self.status

    @classmethod
    def check_username(cls, username):
        return cls.query.exists().where(User.username == username).scalar()

    @classmethod
    def authenticate(cls, login, password):
        user = cls.query.filter(
            db.or_(User.username == login, User.email == login)
        ).first()
        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False
        return user, authenticated

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter(User.id == id).first()
