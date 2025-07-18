from flask_login import UserMixin

from core.database import db

USERNAME_MAX_LENGTH = 20
USERNAME_MIN_LENGTH = 1
PASSWORD_MAX_LENGTH = 40
PASSWORD_MIN_LENGTH = 1
PROFILE_PICTURE_NAME_MAX_LENGTH = 128
class User(db.Model, UserMixin):
    #Information useful for the good functioning of the app
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(USERNAME_MAX_LENGTH), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    #Not used in the logic of the application, fully customizable by the user
    nickname = db.Column(db.String(USERNAME_MAX_LENGTH), unique=False, nullable=False)
    profile_picture = db.Column(db.String(PROFILE_PICTURE_NAME_MAX_LENGTH), nullable=True)
    description = db.Column(db.Text, nullable=False, default='')