from uuid import uuid4

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash

from ..constants import STRING_LEN, DEFAULT_AVATAR, USER, ADMIN, INACTIVE
from ..helpers import get_current_time
from ...extensions import db


# -------------------------------- User Model ------------------------------- #

class User(db.Model, UserMixin):
    """ User Model:
        the user can be a person or even a campany, he/it can manage drivers
        and vehicles.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(STRING_LEN))
    username = db.Column(db.String(STRING_LEN), nullable=False, unique=True)
    email = db.Column(db.String(STRING_LEN), nullable=False, unique=True)
    password = db.Column(db.String(STRING_LEN), nullable=False)
    avatar = db.Column(db.String(STRING_LEN), nullable=True, default=DEFAULT_AVATAR)
    role = db.Column(db.SmallInteger, default=USER)
    activation = db.Column(db.String(STRING_LEN))
    status = db.Column(db.SmallInteger, default=INACTIVE)
    last_login = db.Column(db.DateTime(), default=get_current_time())
    created = db.Column(db.DateTime(), default=get_current_time())

    def __init__(self, username, email, password, fullname=None, avatar=None, role=USER, status=INACTIVE):
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
        return self.role == ADMIN

    def get_id(self):
        return self.id

    def __repr__(self):
        return '{} ({})'.format(self.username, self.email)

    def get_role(self):
        return USER_ROLE[self.role]

    def get_status(self):
        return USER_STATUS[self.status]

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
