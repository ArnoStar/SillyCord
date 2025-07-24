from secrets import token_hex
from datetime import datetime, timedelta, UTC

from flask import session
from flask_login import login_user, logout_user
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash

from core.login_manager import login_manager
from core.database import db
from core.mail import mail
from users.models import User, TemporaryUser, USERNAME_MAX_LENGTH, USERNAME_MIN_LENGTH, PASSWORD_MAX_LENGTH, \
    PASSWORD_MIN_LENGTH, MAX_TEMP_USER_LIFE_TIME


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def is_app_user_valid(username:str, password:str) -> bool:
    user = User.query.filter_by(username=username).first()
    if user is None or not check_password_hash(user.password, password):
        return False

    return True

def why_app_user_invalid(username:str, password:str) -> list[str]:
    errors = []
    user = User.query.filter_by(username=username).first()
    if user is None:
        errors.append(f"User {username} does not exist")
    elif not check_password_hash(user.password, password):
        errors.append(f"Password is incorrect")

    return errors

def login_app_user(username:str, password:str) -> bool:
    valid = is_app_user_valid(username, password)
    if valid:
        user = User.query.filter_by(username=username).first()
        login_user(user)
    return valid


def is_new_app_user_valid(username:str, email:str, password:str, confirm_password:str) -> bool:
    user = User.query.filter(or_(User.username==username,
                                 User.email== email)).first()
    temp_user = TemporaryUser.query.filter(or_(TemporaryUser.username==username,
                                 TemporaryUser.email== email)).first()

    if user is not None or temp_user is not None or password != confirm_password:
        return False
    if len(username) > USERNAME_MAX_LENGTH or len(username) < USERNAME_MIN_LENGTH:
        return False
    if len(password) > PASSWORD_MAX_LENGTH or len(password) < PASSWORD_MIN_LENGTH:
        return False
    if not '@' in email:
        return False

    return True

def why_new_app_user_invalid(username:str, email:str, password:str, confirm_password:str) -> list[str]:
    errors = []
    user = User.query.filter(or_(User.username == username,
                                 User.email == email)).first()
    temp_user = TemporaryUser.query.filter(or_(TemporaryUser.username == username,
                                               TemporaryUser.email == email)).first()
    if user is not None or temp_user is not None:
        errors.append(f"User {username} already exists or the email {email} is already taken.")
    if password != confirm_password:
        errors.append(f"Passwords do not match.")
    if len(username) > USERNAME_MAX_LENGTH or len(username) < USERNAME_MIN_LENGTH:
        errors.append(f"Username should be between {USERNAME_MIN_LENGTH} and {USERNAME_MAX_LENGTH}.")
    if len(password) > PASSWORD_MAX_LENGTH or len(password) < PASSWORD_MIN_LENGTH:
        errors.append(f"Password should be between {PASSWORD_MIN_LENGTH} and {PASSWORD_MAX_LENGTH}.")
    if not '@' in email:
        errors.append(f"Invalid email address.")

    return errors

def signin_app_user():
    temp_user = TemporaryUser.query.get(session['user_id'])

    new_user = User(username=temp_user.username, email=temp_user.email, password=temp_user.password, nickname=temp_user.username)
    db.session.add(new_user)
    db.session.delete(temp_user)
    db.session.commit()
    user = User.query.filter_by(username=temp_user.username).first()
    login_user(user)

def create_temporary_app_user(username:str, email:str, password:str, confirm_password:str) -> bool:
    delete_old_temporary_app_user()

    valid = is_new_app_user_valid(username, email, password, confirm_password)
    if valid:
        session['user_id'] = token_hex(16)
        hashed_password = generate_password_hash(password)
        confirmation_key = token_hex(16)
        new_temporary_user = TemporaryUser(session=session['user_id'], username=username, email=email, password=hashed_password, confirmation_key=confirmation_key)
        db.session.add(new_temporary_user)
        db.session.commit()

        mail.send_message(subject='Your confirmation code.',
                          recipients=[email],
                          body=f'You confirmation code is {confirmation_key}')

    return valid

def delete_old_temporary_app_user():
    max_life_time = datetime.now(UTC) - timedelta(minutes=MAX_TEMP_USER_LIFE_TIME)
    TemporaryUser.query.filter(TemporaryUser.date_joined < max_life_time).delete()
    db.session.commit()