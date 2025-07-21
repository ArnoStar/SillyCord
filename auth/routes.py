from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import current_user

from .forms import LoginForm, SigninForm
from .auth import login_app_user, why_app_user_invalid, signin_app_user, why_new_app_user_invalid

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
    elif form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        if signin_app_user(username, password, confirm_password):
            return redirect(url_for('chats.contacts'))
        else:
            for error in why_new_app_user_invalid(username, password, confirm_password):
                flash(error)
            return render_template("signin.html", form=form)