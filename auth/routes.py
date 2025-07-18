from flask import Blueprint, render_template, request

from .forms import LoginForm, SigninForm
from .auth import login_app_user, why_app_user_invalid, signin_app_user, why_new_app_user_invalid

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template("login.html", form=form)

    elif form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if login_app_user(username, password):
            return 'You are logged in!'
        else:
            return why_app_user_invalid(username, password)[0]

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if request.method == 'GET':
        return render_template("signin.html", form=form)
    elif form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        if signin_app_user(username, password, confirm_password):
            return "You've created an account successfully!"
        else:
            return why_new_app_user_invalid(username, password,confirm_password)[0]