from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, HiddenField
from wtforms.validators import (
    DataRequired, Regexp, ValidationError, Email, Length, EqualTo
)
from flask_wtf.file import FileAllowed, FileField
from .models.user import User
from .constants import (
    USERNAME_LEN_MIN, USERNAME_LEN_MAX, PASSWORD_LEN_MIN,
    FULLNAME_LEN_MIN, FULLNAME_LEN_MAX
)
# ------------------------ custom validation methods ------------------------ #


def name_exist(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User already exists !')


def email_exist(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('Email already exists !')


# ---------------------------- User form classes ---------------------------- #

class RegisterForm(Form):
    """ RegisterForm Form """
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=USERNAME_LEN_MIN, max=USERNAME_LEN_MAX),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username is not correct !")
            ),
            # name_exist
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            # email_exist
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=PASSWORD_LEN_MIN),
            EqualTo('password2', message='Password must much !')
        ]
    )
    password2 = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired()
        ]
    )
    avatar = FileField(
        'Avatar', validators=[
            FileAllowed(['jpg', 'png', 'gif'], 'Images only plz :) ')
        ]
    )


class LoginForm(Form):
    """Login Form"""
    # next = HiddenField()
    login = StringField(
        'Username or email',
        validators=[
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )
    remember = BooleanField('Remember me?')
    # submit = SubmitField('Sign in')


class RecoverPasswordForm(Form):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )


class ChangePasswordForm(Form):
    activation_key = HiddenField()
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=PASSWORD_LEN_MIN),
            EqualTo('password2', message='Password must much !')
        ]
    )
    password2 = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired()
        ]
    )


class ReauthForm(Form):
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=PASSWORD_LEN_MIN),
            EqualTo('password2', message='Password must much !')
        ]
    )


class ProfileForm(Form):
    fullname = StringField(
        'Full name',
        validators=[
            Length(min=FULLNAME_LEN_MIN, max=FULLNAME_LEN_MAX),
            Regexp(
                r'^[a-zA-Z0-9,._-]+$',
                message=("Full name is not correct !")
            ),
            name_exist
        ]
    )
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=USERNAME_LEN_MIN, max=USERNAME_LEN_MAX),
            Regexp(
                r'^[a-zA-A0-9_]+$',
                message=("Username is not correct !")
            ),
            name_exist
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exist
        ]
    )
    avatar = FileField(
        'Avatar', validators=[
            FileAllowed(['jpg', 'png', 'gif'], 'Images only plz :)')
        ]
    )
