from flask import (
    Blueprint, render_template, request, flash, redirect, url_for
)
from flask_login import (
    login_user, logout_user, login_required, current_user
)

from ..extensions import db
# from ..decorators import admin_required
from .models.user import User
from .forms import LoginForm, RegisterForm
from .helpers import upload_avatar


user = Blueprint('user', __name__, url_prefix='/user')


# ----------------------- /user/index : User home page ---------------------- #

@user.route('/')
@login_required
def index():
    return render_template('user/index.html', user=current_user)

# ----------------------- /user/login : User login page --------------------- #


@user.route('/login', methods=['GET', 'POST'])
def login():
    """ User login method """
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))

    form = LoginForm()
    if form.validate_on_submit():
        # request.form.get('login', 'default')
        user, authenticated = User.authenticate(
            form.login.data, form.password.data
        )
        if user and authenticated:
            remember = form.remember.data == 'y'
            if login_user(user, remember=remember):
                flash("Logged in successfully", 'success')
                next = request.args.get('next')
                # if not next_is_valid(next):
                #     return abort(400)
                return redirect(next or url_for('user.index'))
        else:
            flash('Sorry, invalid login', 'error')

    return render_template('user/login.html', form=form)

# ----------------------- /user/logout : User logout page ------------------- #


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'success')
    return redirect(url_for('frontend.index'))

# ----------------------- /user/register : User register page --------------- #


@user.route('/register', methods=['GET', 'POST'])
def register():
    """ User Sigup method """
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))

    form = RegisterForm()

    if form.validate_on_submit():
        avatar = upload_avatar(form)
        user = User(
            username=form.username.data,
            email=form.email.data,
            avatar=avatar,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        flash('Yay, you successfully registered !', 'success')
        if login_user(user):
            return redirect(url_for('user.index'))

    return render_template('user/register.html', form=form)

# ----------------------- /user/profile : User profile page ----------------- #


@user.route('/profile')
def profile():
    return render_template('user/profile.html', user=current_user)

# ---------------------- /user/profile : Public user profile page ----------- #


@user.route('/<int:user_id>/profile')
def public_profile(user_id):
    user = User.get_by_id(user_id)
    return render_template('user/profile.html', user=user)


# /\/\/\/\/\\/\/\/\/\\/\/\/\/\\/\/\/\/\\/\/\/\/\\/\/\/\/\\/\/\/\/\\/\/\\/\/\/ #
#                                                                             #
#            ================== Admin Blueprint =====================         #
#                                                                             #
# /\/\/\/\/\\/\/\/\/\\/\/\/\/\\/\/\/\/\\/\/\/\/\\/\/\/\/\\/\/\/\/\\/\//\/\/\/ #

admin = Blueprint('admin', __name__, url_prefix='/admin')


# ----------------------  /admin/index : Admin home page -------------------- #


# @admin.route('/')
# @login_required
# @admin_required
# def index():
#     users = User.query.all()
#     return render_template('admin/index.html', users=users, active='index')
#
#
# @admin.route('/users')
# @login_required
# @admin_required
# def users():
#     users = User.query.all()
#     return render_template('admin/users.html', users=users, active='users')
#
#
# @admin.route('/user/<int:user_id>', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def user(user_id):
#     user = User.query.filter_by(id=user_id).first_or_404()
#     form = UserForm(obj=user, next=request.args.get('next'))
#     if form.validate_on_submit():
#         form.populate_obj(user)
#         db.session.add(user)
#         db.session.commit()
#         flash('User updated.', 'success')
#     return render_template('admin/user.html', user=user, form=form)
