from flask import Blueprint, render_template, request, url_for, flash, redirect, session
from flask_login import current_user

from users.models import TemporaryUser
from .forms import LoginForm, SigninForm, EmailConfirmForm
from .auth import login_app_user, why_app_user_invalid, signin_app_user, why_new_app_user_invalid, create_temporary_app_user

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chats.contacts'))

    form = LoginForm()
    if request.method == 'GET':
        return render_template("login.html", form=form)

    elif form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if login_app_user(username, password):
            return redirect(url_for('chats.contacts'))
        else:
            for error in why_app_user_invalid(username, password):
                flash(error)
            return render_template("login.html", form=form)

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('chats.contacts'))

    form = SigninForm()
    if request.method == 'GET':
        return render_template("signin.html", form=form)
    elif request.method == 'POST':
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        email = form.email.data
        if create_temporary_app_user(username, email, password, confirm_password):
            return redirect(url_for('auth.email_confirmation'))
        else:
            for error in why_new_app_user_invalid(username, email, password, confirm_password):
                flash(error)
            return render_template("signin.html", form=form)

@auth.route('/email-confirmation', methods=['GET', 'POST'])
def email_confirmation():
    if session.get('user_id', None) is None:
        return redirect(url_for('auth.signin'))
    temp_user = TemporaryUser.query.get(session.get('user_id'))
    if temp_user is None:
        return redirect(url_for('auth.signin'))
    form = EmailConfirmForm()
    if request.method == 'GET':
        return render_template('email_confirmation.html', form=form)
    elif request.method == 'POST':
        valid_key = temp_user.confirmation_key
        key = form.key.data

        if valid_key == key:
            signin_app_user()
            return redirect(url_for('chats.contacts'))
        else:
            flash("Wrong confirmation key.")
            return render_template('email_confirmation.html', form=form)