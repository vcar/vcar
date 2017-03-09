from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, HiddenField, SelectField
from wtforms.validators import (
    DataRequired, Regexp, ValidationError, Email, Length, EqualTo
)
from flask_wtf.file import FileAllowed, FileField
from ..models.user import User
from ..constants import USER_ROLES

# ------------------------ custom validation methods ------------------------ #


def name_exist(form, field):
    if User.query.filter_by(username=field.data).exists():
        raise ValidationError('User already exists !')


def email_exist(form, field):
    if User.query.filter_by(email=field.data).exists():
        raise ValidationError('Email already exists !')


# ---------------------------- User form classes ---------------------------- #

class UserForm(Form):
    """ User add/edit Form """
    fullname = StringField(
        'Full name',
        validators=[
            Length(min=3, max=50),
            Regexp(
                r'^[a-zA-Z0-9 ,._-]+$',
                message=("Full name is not correct !")
            )
        ]
    )
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=3, max=50),
            Regexp(
                r'^[a-zA-A0-9_]+$',
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
            Length(min=4),
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
            FileAllowed(['jpg', 'png', 'gif'], 'Images only plz :)')
        ]
    )
    role = SelectField(
        'Role',
        coerce=int,
        choices=USER_ROLES,
        validators=[
            DataRequired(),
        ]
    )


class RegisterForm(Form):
    """ RegisterForm Form """
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=3, max=50),
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
            Length(min=4),
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
            Length(min=4),
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
            Length(min=4),
            EqualTo('password2', message='Password must much !')
        ]
    )


class ProfileForm(Form):
    fullname = StringField(
        'Full name',
        validators=[
            Length(min=3, max=50),
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
            Length(min=3, max=50),
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
