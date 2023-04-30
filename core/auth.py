from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from .models import db, User
from .forms import LoginForm, RegistrationForm, UpdateUserForm, CommentForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # check if the user exists and the password is correct
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.login'))

        # log in the user
        login_user(user)

        flash('You have been logged in', 'success')
        return redirect(url_for('main.index'))

    return render_template('login.html', form=form)


@auth_bp.route('/logout')
def logout():
    # log out the user
    logout_user()

    flash('You have been logged out', 'success')
    return redirect(url_for('main.index'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # check if the username or email already exists in the database
        if User.does_user_exist(form.username.data):
            flash('Username already exists', 'danger')
            return redirect(url_for('auth.register'))

        if User.does_email_exist(form.email.data):
            flash('Email address already registered', 'danger')
            return redirect(url_for('auth.register'))

        # create a new user object and add it to the database
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        # log in the user
        login_user(user)

        flash('Your account has been created', 'success')
        return redirect(url_for('main.index'))

    return render_template('register.html', form=form)


@auth_bp.route('/update', methods=['GET', 'POST'])
@login_required
def update_user():
    form = UpdateUserForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect', 'danger')
            return redirect(url_for('auth.update_user'))

        if User.does_user_exist(form.username.data) and form.username.data != current_user.username:
            flash('Username already exists', 'danger')
            return redirect(url_for('auth.update_user'))

        if User.does_email_exist(form.email.data) and form.email.data != current_user.email:
            flash('Email address already registered', 'danger')
            return redirect(url_for('auth.update_user'))

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.set_password(form.new_password.data)
        db.session.commit()

        flash('Your account has been updated', 'success')
        return redirect(url_for('main.index'))

    return render_template('update_user.html', form=form)


@auth_bp.route('/delete', methods=['GET', 'POST'])
@login_required
def delete_user():
    user = User.query.get(current_user.id)
    logout_user()
    db.session.delete(user)
    db.session.commit()

    flash('Your account has been deleted', 'success')
    return redirect(url_for('main.index'))