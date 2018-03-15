from flask import (
    render_template, request, flash, redirect, url_for
)
from flask_login import (
    login_user, logout_user, login_required, current_user
)

from .. import dashboard
from ..models.user import User
from ..forms.user import UserForm, LoginForm, RegisterForm
from ..helpers.helpers import paginate, upload_file
from ..constants.constants import PER_PAGE, USER_LOGO_DIR
from ...extensions import db


# --------------------- /dashboard/user/ : List of users ------------------ #

@dashboard.route('/user/')
@login_required
def indexUser():
    users = User.query.paginate(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', PER_PAGE, type=int),
    )
    return render_template('dashboard/user/index.html', users=users)

# ----------------------- /dashboard/user/id : Show user ------------------- #


@dashboard.route('/user/<int:id>', methods=['GET'])
@login_required
def showUser(id):
    user = User.query.get_or_404(id)
    return render_template('dashboard/user/show.html', user=user)

# ---------------------- /dashboard/user/new : Add user -------------------- #


@dashboard.route('/user/new', methods=['GET', 'POST'])
@login_required
def newUser():
    """ Add new user """

    form = UserForm()

    if form.validate_on_submit():
        avatar = upload_file(form.avatar.data, USER_LOGO_DIR)
        user = User(
            fullname=form.fullname.data,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            role=form.role.data,
            avatar=avatar
        )
        db.session.add(user)
        db.session.commit()
        flash('User {}, added successfully.'.format(form.username.data), 'success')
        return redirect(url_for('dashboard.indexUser'))

    return render_template('dashboard/user/new.html', form=form)

# -------------------- /dashboard/user/id/edit : Edit user ----------------- #


@dashboard.route('/user/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editUser(id):
    """ Edit existing user """
    user = User.query.get_or_404(id)
    oldAvatar = user.avatar
    form = UserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        user.set_password(form.password.data)
        avatar = upload_file(form.avatar.data, USER_LOGO_DIR)
        if avatar is None:
            user.avatar = oldAvatar
        else:
            user.avatar = avatar
        db.session.commit()
        flash('User {}, updated successfully.'.format(form.username.data), 'success')
        return redirect(url_for('dashboard.showUser', id=id))

    return render_template('dashboard/user/edit.html', form=form, id=id)

# ------------------ /dashboard/user/id/delete : Delete user --------------- #


@dashboard.route('/user/<int:id>/toggle', methods=['GET'])
@login_required
def toggleUser(id):
    user = User.query.get_or_404(id)
    # getattr(user, 'status', 0)
    status = user.status if user.status is not None else 0
    user.status = 1 - status
    db.session.commit()
    msg = 'activated' if user.status is 1 else 'deactivated'
    flash('User {}, {} successfully.'.format(user.username, msg), 'success')
    return redirect(url_for('dashboard.indexUser'))

# ------------------ /dashboard/user/id/delete : Delete user --------------- #


@dashboard.route('/user/<int:id>/delete', methods=['GET'])
@login_required
def deleteUser(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User {}, deleted successfully.'.format(user.username), 'success')
    return redirect(url_for('dashboard.indexUser'))

# ----------------------- /dashboard/login : User login page --------------------- #


@dashboard.route('/login', methods=['GET', 'POST'])
def login():
    """ User login method """
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    form = LoginForm()
    if form.validate_on_submit():
        # request.form.get('login', 'default')
        user, authenticated = User.authenticate(
            form.login.data, form.password.data
        )
        if user and authenticated:
            remember = form.remember.data == 'y'
            if login_user(user, remember=remember):
                flash("Wellcome back " + user.fullname, 'success')
                next = request.args.get('next')
                # if not next_is_valid(next):
                #     return abort(400)
                return redirect(next or url_for('dashboard.index'))
        else:
            flash('Sorry, invalid login', 'error')

    return render_template('dashboard/user/login.html', form=form)

# ----------------------- /dashboard/logout : User logout page ------------------- #


@dashboard.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'success')
    return redirect(url_for('frontend.index'))

# ----------------------- /dashboard/register : User register page --------------- #


@dashboard.route('/register', methods=['GET', 'POST'])
def register():
    """ User Sigup method """
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    form = RegisterForm()

    if form.validate_on_submit():
        avatar = upload_file(form.avatar.data, USER_LOGO_DIR)
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
            return redirect(url_for('dashboard.index'))

    return render_template('dashboard/user/register.html', form=form)

# ----------------------- /dashboard/profile : User profile page ----------------- #


@dashboard.route('/profile')
def profile():
    return render_template('dashboard/user/profile.html', user=current_user)

# ---------------------- /dashboard/profile : Public user profile page ----------- #


@dashboard.route('/<int:user_id>/profile')
def public_profile(user_id):
    user = User.get_by_id(user_id)
    return render_template('dashboard/user/profile.html', user=user)


# /\/\/\/\/\\/\/\/\/\\/\/\/\/\\/\/\/\/\\/\/\/\/\\/\/\/\/\\/\/\/\/\\/\/\\/\/\/ #
#                                                                             #
#            ================== Admin Blueprint =====================         #
#                                                                             #
# /\/\/\/\/\\/\/\/\/\\/\/\/\/\\/\/\/\/\\/\/\/\/\\/\/\/\/\\/\/\/\/\\/\//\/\/\/ #

# admin = Blueprint('admin', __name__, url_prefix='/admin')


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
# @admin.route('/dashboard/<int:user_id>', methods=['GET', 'POST'])
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
