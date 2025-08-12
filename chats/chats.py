from flask_login import current_user

from .models import ChatUserLink, Chat, Message
from core.database import db
from core.sockets import socket
from users.models import User

def does_user_exist(user_id):
    user = User.query.get(user_id)
    return bool(user)

def does_chat_exist(user_id1:int, user_id2:int)->bool:
    common_chat = set()
    chats_user1 = get_chats(user_id1)
    chats_user2 = get_chats(user_id2)

    sum_two_chats = len(chats_user1) + len(chats_user2)

    for chat in chats_user1:
        common_chat.add(chat)
    for chat in chats_user2:
        common_chat.add(chat)

    if sum_two_chats > len(common_chat):
        return True
    else:
        return False

def get_chats(user_id:int):
    links = ChatUserLink.query.filter_by(user_id=user_id).all() #Get from the db the link chat-user, we will use this to get every link with the {user_id} and from here we can get the chats
    chats = Chat.query.filter(Chat.id.in_([link.chat_id for link in links])).all()
    return chats
def get_users(chat_id:int):
    links = ChatUserLink.query.filter_by(chat_id=chat_id).all() #Same thing here but we filter the link by the chat to get users, not by the user to get chats
    users = []
    for link in links:
        user = User.query.get(link.user_id)
        users.append(user)
    return users
def get_user_chats_links(user_id:int):
    links = ChatUserLink.query.filter_by(user_id=user_id).all()
    return links
def get_chat_user_link(user_id:int, chat_id:int):
    link = ChatUserLink.query.get((user_id, chat_id))
    return link

def get_chat_users_dict(user_id:int) -> dict: #This function use useful for the jinja2 code
    chat_users = dict()
    for chat in get_chats(user_id):
        chat_users[chat] = get_users(chat.id)

    return chat_users

def get_uid_user_dict(chat_id:int) -> dict: #This function use useful for the jinja2 code
    users = get_users(chat_id)
    uid_user_dict = dict()
    for user in users:
        uid_user_dict[user.id] = user

    return uid_user_dict

def create_chat(user_id1:int, user_id2:int):
    new_chat = Chat()
    db.session.add(new_chat)
    db.session.flush()

    users = User.query.filter(User.id.in_([user_id1, user_id2])).all()
    users_dict = {user.id: user for user in users}

    new_link = [None, None]
    new_link[0] = ChatUserLink(user_id=user_id1, chat_id=new_chat.id, name=users_dict[user_id2].nickname)
    new_link[1] = ChatUserLink(user_id=user_id2, chat_id=new_chat.id, name=users_dict[user_id1].nickname)

    db.session.add_all(new_link)

    db.session.commit()

def create_group(users_ids:list[int]):
    new_chat = Chat()
    db.session.add(new_chat)
    db.session.flush()

    users = User.query.filter(User.id.in_(users_ids)).all()

    for user in users:
        name = [nickname for nickname in user.nickname]
        name.remove(user.nickname)
        name = "".join(name)
        new_link = ChatUserLink(user_id=user.id, chat_id=new_chat.id, name=name)
        db.session.add(new_link)

    db.session.commit()

def is_user_in_chat(user_id:int, chat_id:int) -> bool:
    user = User.query.get(user_id)
    chat = Chat.query.get(chat_id)
    for link in chat.links:
        if link.user_id == user.id:
            return True

    return False

def send_message(chat_id:int, message:str):
    message_model = Message(chat_id=chat_id, author_id=current_user.id, message=message)
    db.session.add(message_model)
    db.session.commit()
    socket.emit('message', message_model.to_dict(), room=get_chat_room(chat_id))

def get_message(chat_id:int)->list[Message]:
    chat = Chat.query.get(chat_id)
    return chat.messages

def get_chat_room(chat_id:int) -> str:
    return f"chat:{chat_id}"
def get_useronline_room(user_id:int) -> str:
    return f"user_online:{str(user_id)}"