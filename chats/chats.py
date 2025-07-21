from flask import jsonify
from flask_login import current_user

from .models import ChatUserLink, Chat, Message
from core.database import db
from core.sockets import socket
from users.models import User

def get_chats(user_id:int):
    links = ChatUserLink.query.filter_by(user_id=user_id).all() #Get from the db the link chat-user, we will use this to get every link with the {user_id} and from here we can get the chats
    chats = []
    for link in links:
        chat = Chat.query.get(link.chat_id)
        chats.append(chat)
    return chats
def get_users(chat_id:int):
    links = ChatUserLink.query.filter_by(chat_id=chat_id).all() #Same thing here but we filter the link by the chat to get users, not by the user to get chats
    users = []
    for link in links:
        user = User.query.get(link.user_id)
        users.append(user)
    return users

def get_chat_users_dict(user_id:int) -> dict: #This function use useful for the jinja2 code
    chat_users = dict()
    for chat in get_chats(user_id):
        chat_users[chat] = get_users(chat.id)

    return chat_users

def get_user_uid_dict(chat_id:int) -> dict: #This function use useful for the jinja2 code
    users = get_users(chat_id)
    user_uid_dict = dict()
    for user in users:
        user_uid_dict[user.id] = user

    return user_uid_dict

def create_chat(user_id1:int, user_id2:int):
    new_chat = Chat()
    db.session.add(new_chat)
    db.session.flush()

    new_link1 = ChatUserLink(user_id=user_id1, chat_id=new_chat.id)
    new_link2 = ChatUserLink(user_id=user_id2, chat_id=new_chat.id)

    db.session.add(new_link1)
    db.session.add(new_link2)

    db.session.commit()

def create_group(users_ids:list[int]):
    default_name = ''

    new_chat = Chat(name=default_name)
    db.session.add(new_chat)
    db.session.flush()

    for user_id in users_ids:
        user = User.query.get(user_id)
        default_name += user.nickname+" "

        new_link = ChatUserLink(user_id=user_id, chat_id=new_chat.id)
        db.session.add(new_link)

    new_chat.name = default_name

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
    socket.emit('message', message_model.to_dict(), room=str(chat_id))

def get_message(chat_id:int)->list[Message]:
    chat = Chat.query.get(chat_id)
    return chat.messages
