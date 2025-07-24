from datetime import datetime, UTC

from flask_login import UserMixin

from core.database import db

MAX_TEMP_USER_LIFE_TIME = 15 #minutes

USERNAME_MAX_LENGTH = 20
USERNAME_MIN_LENGTH = 1
PASSWORD_MAX_LENGTH = 40
PASSWORD_MIN_LENGTH = 1
EMAIL_MAX_LENGTH = 128
PROFILE_PICTURE_NAME_MAX_LENGTH = 128
class User(db.Model, UserMixin):
    #Information useful for the good functioning of the app
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(USERNAME_MAX_LENGTH), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(EMAIL_MAX_LENGTH), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    date_joined = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))

    #Not used in the logic of the application, fully customizable by the user
    nickname = db.Column(db.String(USERNAME_MAX_LENGTH), unique=False, nullable=False)
    profile_picture = db.Column(db.String(PROFILE_PICTURE_NAME_MAX_LENGTH), nullable=True)
    description = db.Column(db.Text, nullable=False, default='')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'profile_picture': self.profile_picture,
            'description': self.description,
        }

class TemporaryUser(db.Model):
    session = db.Column(db.String(255), nullable=False, primary_key=True)
    username = db.Column(db.String(USERNAME_MAX_LENGTH), unique=True)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(EMAIL_MAX_LENGTH), unique=True, nullable=False)
    confirmation_key = db.Column(db.String(255), nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))