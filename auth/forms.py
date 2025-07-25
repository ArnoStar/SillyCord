from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email

from users.models import USERNAME_MAX_LENGTH, USERNAME_MIN_LENGTH, PASSWORD_MAX_LENGTH, PASSWORD_MIN_LENGTH


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=USERNAME_MAX_LENGTH)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")

class SigninForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=USERNAME_MAX_LENGTH, min=USERNAME_MIN_LENGTH)])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=PASSWORD_MAX_LENGTH, min=PASSWORD_MIN_LENGTH)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")

class EmailConfirmForm(FlaskForm):
    key = StringField("Code", validators=[DataRequired()])
    submit = SubmitField("Confirm Email")