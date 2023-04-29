from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from .models import db, User
from .forms import LoginForm, RegistrationForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # check if the user exists and the password is correct
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.login'))

        if not user.check_password(form.password.data):
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
