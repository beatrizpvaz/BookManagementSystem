from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import LoginForm, RegistrationForm
from . import auth
from ..models import User
from .. import db

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    """
    Handles requests to the /login route
    Logs an user in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():
        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        user = User.query.filter_by(username = form.username.data).first()
        # if user and check_password_hash(user.user_password, form.password.data):
        if user and user.user_password == form.password.data:
            login_user(user)
            return redirect(url_for('home.homepage'))
        else:
            flash('Invalid username or password.')
    # load login template
    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    """
    Handles requests to the /register route
    Registers a new user in through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        newUser = User(
            username = form.username.data,
            email = form.email.data,
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            user_password = form.password.data
        )

        db.session.add(newUser)
        db.session.commit()
        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/logout')
def logout():
    """
    Handles requests to the /logout route
    Logs an user out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))