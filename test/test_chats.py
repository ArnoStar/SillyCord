import pytest

from core.app import create_app
from core.database import db
from users.models import User
from chats.models import Chat, ChatUserLink

from chats.chats import create_chat, create_group

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


def test_create_group(app):
    users = []
    for i in range(3):
        users.append(User(username=f"test_login{i}", email=f"test@test.test{i}", password=f"test_password{i}",
                    nickname=f"test_nickname{i}"))
    db.session.add_all(users)
    db.session.commit()
    users_id = [user.id for user in users]

    create_group(users_id)



    assert len(Chat.query.all()) == 1
    assert len(ChatUserLink.query.all()) == 3
