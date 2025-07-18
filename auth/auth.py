from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from core.login_manager import login_manager
from core.database import db
from users.models import User, USERNAME_MAX_LENGTH, USERNAME_MIN_LENGTH, PASSWORD_MAX_LENGTH, PASSWORD_MIN_LENGTH

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


def is_new_app_user_valid(username, password, confirm_password) -> bool:
    user = User.query.filter_by(username=username).first()
    if user is not None or password != confirm_password:
        return False
    if len(username) > USERNAME_MAX_LENGTH or len(username) < USERNAME_MIN_LENGTH:
        return False
    if len(password) > PASSWORD_MAX_LENGTH or len(password) < PASSWORD_MIN_LENGTH:
        return False

    return True

def why_new_app_user_invalid(username, password, confirm_password) -> list[str]:
    errors = []
    user = User.query.filter_by(username=username).first()
    if user is not None:
        errors.append(f"User {username} already exists.")
    if password != confirm_password:
        errors.append(f"Passwords do not match.")
    if len(username) > USERNAME_MAX_LENGTH or len(username) < USERNAME_MIN_LENGTH:
        errors.append(f"Username should be between {USERNAME_MIN_LENGTH} and {USERNAME_MAX_LENGTH}.")
    if len(password) > PASSWORD_MAX_LENGTH or len(password) < PASSWORD_MIN_LENGTH:
        errors.append(f"Password should be between {PASSWORD_MIN_LENGTH} and {PASSWORD_MAX_LENGTH}.")

    return errors

def signin_app_user(username:str, password:str, confirm_password) -> bool:
    valid = is_new_app_user_valid(username, password, confirm_password)
    if valid:
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, nickname=username)
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(username=username).first()
        login_user(user)

    return valid