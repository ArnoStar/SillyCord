import pytest
from datetime import datetime, timedelta, UTC
from werkzeug.security import generate_password_hash
from flask_login import current_user
from flask import session

from core.app import create_app
from core.database import db
from users.models import User, TemporaryUser, USERNAME_MAX_LENGTH, PASSWORD_MAX_LENGTH, MAX_TEMP_USER_LIFE_TIME

#This is the part of the project that we want to test
from auth.auth import is_app_user_valid, login_app_user, is_new_app_user_valid, signin_app_user, create_temporary_app_user,\
    delete_old_temporary_app_user

@pytest.fixture
def app():
    app = create_app()

    app.config.update({
        'TESTING':True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

def test_is_app_user_valid(app):
    assert is_app_user_valid("test_login", "test_password") == False

    new_user = User(username="test_login", email="test@test.test", password=generate_password_hash("test_password"),
                    nickname="test_nickname")
    db.session.add(new_user)
    db.session.commit()

    assert is_app_user_valid("test_wrong_login", "test_wrong_password") == False
    assert is_app_user_valid("test_login", "test_wrong_password") == False
    assert is_app_user_valid("test_wrong_login", "test_password") == False
    assert is_app_user_valid("test_login", "test_password") == True

def test_login_app_user(app):
    assert login_app_user("test_login", "test_password") == False

    new_user = User(username="test_login", email="test@test.test", password=generate_password_hash("test_password"),
                    nickname="test_nickname")
    db.session.add(new_user)
    db.session.commit()

    with app.test_request_context():
        assert login_app_user("test_wrong_login", "test_password") == False
        assert login_app_user("test_login", "test_wrong_password") == False
        assert login_app_user("test_login", "test_password") == True

        assert current_user == new_user

def test_is_new_app_user_valid(app):

    assert is_new_app_user_valid("test_login", "test@test.test", "test_password",
                                 "test_password") == True
    assert is_new_app_user_valid("test_login", "test@test.test", "test_password",
                                 "test_another_password") == False
    assert is_new_app_user_valid("test_login", "test_email", "test_password", "test_password") == False
    assert is_new_app_user_valid("test_login_to_long"+" "*USERNAME_MAX_LENGTH,
                                 "test@test.test", "test_password",
                                 "test_password") == False
    assert is_new_app_user_valid("test_login", "test@test.test", "test_password_to_long"+" "*PASSWORD_MAX_LENGTH,
                                 "test_password") == False

def test_signin_app_user(app):
    with app.test_request_context():
        session['user_id'] = "test_id"

        new_temp_user = TemporaryUser(username="test_login", email="test@test.test", password=generate_password_hash("test_password"),
                        session="test_id", confirmation_key="test_key")
        db.session.add(new_temp_user)
        db.session.commit()

        signin_app_user()

        assert TemporaryUser.query.get("test_id") == None
        assert User.query.filter_by(username="test_login") != None

def test_create_temporary_app_user(app):
    with app.test_request_context():
        assert create_temporary_app_user("test_login", "test@test.test", "test_password",
                                 "test_password") == True
        assert TemporaryUser.query.get(session['user_id']) != None

def test_delete_old_temporary_app_user(app):

    delete_old_temporary_app_user()

    max_life_time = datetime.now(UTC) - timedelta(minutes=MAX_TEMP_USER_LIFE_TIME)

    assert TemporaryUser.query.filter(TemporaryUser.date_joined < max_life_time).all() == []