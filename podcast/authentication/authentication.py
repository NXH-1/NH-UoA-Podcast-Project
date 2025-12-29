from flask import Blueprint, render_template, redirect, url_for, session, flash, g, request

import time
import random

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import podcast.authentication.services as services
import podcast.adapters.repository as repo

from password_validator import PasswordValidator

from functools import wraps

authentication_blueprint = Blueprint('authentication_bp', __name__,
                                     template_folder='templates',
                                     url_prefix='/authentication')


# generate unique for user id
def generate_unique_id():
    timestamp = int(time.time() * 256)
    random_number = random.randint(1000, 9999)
    return int(f"{timestamp}{random_number}")


@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register(counter=0):
    counter = request.args.get('counter', -1, type=int)
    form = RegistrationForm()

    if form.validate_on_submit():
        try:
            unique_id = generate_unique_id()
            # find y always in low case
            services.add_user(user_id=unique_id, username=form.user_name.data, password=form.password.data,
                               repo=repo.repo_instance)

            flash('Registration successful, please login.', 'success')
            return redirect(url_for('authentication_bp.login'))
        except services.NameNotUniqueException:
            flash('Your username is already taken', 'danger')
    return render_template('credentials.html',
                           title='Register',
                           form=form,
                           counter=counter)


@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login(counter=0):
    counter = request.args.get('counter', -1, type=int)
    form = LoginForm()

    if form.validate_on_submit():
        try:
            # find y always in low case
            user = services.get_user(form.user_name.data, repo.repo_instance)

            services.authenticate_user(form.user_name.data, form.password.data, repo.repo_instance)

            session['user_id'] = user['user_id']
            session['user_name'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('home_bp.home'))
        except services.AuthenticationException:
            flash("Password does not match Username", 'danger')
        except services.UnknownUserException:
            flash('Username not recognised', 'danger')
    return render_template('credentials.html', title='Login', form=form, counter=counter)


# possibly redirect to home or make it so the login page has same layout so they can access other stuff without needing
# to login
@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    flash('Logout successful.', 'success')
    return redirect(url_for('home_bp.home'))


# On hold (don't need it this phase)
# @authentication_blueprint.route('/subscriptions')
# def subscriptions():
#     username = session.get('user_name')
#     if username:
#         subscriptions = get_user_subscriptions(username)
#         return render_template('subscriptions.html', subscriptions=subscriptions)
#     else:
#         flash('Please log in first.', 'warning')
#         return redirect(url_for('authentication_bp.login'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_name' not in session:
            return redirect(url_for('authentication_bp.login'))
        return view(**kwargs)

    return wrapped_view


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Password must be at least 8 characters, have upper case letter,\
            a lower case letter and a digit'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    user_name = StringField('User name',
                            [DataRequired(message='Your user name is required'),
                             Length(min=3, message='The username must be at least 3 characters long.')])
    password = PasswordField('Password',
                             [DataRequired(message='Your password is required'),
                              PasswordValid()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    user_name = StringField('User name', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Login')
