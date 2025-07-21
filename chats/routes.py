from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from flask_socketio import join_room

from .chats import get_chats, get_chat_users_dict, is_user_in_chat, send_message, get_users, get_user_uid_dict
from core.sockets import socket
from .models import Chat

chats = Blueprint('chats', __name__, template_folder='templates', static_folder='static')

online_user = set() #In the future upgrade to Redis

@chats.route("/contacts", methods=['GET', 'POST'])
def contacts():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    chats_users = get_chat_users_dict(current_user.id)

    return render_template('contacts.html', chats=chats_users)

@chats.route("/chats/<chat_id>")
def chat(chat_id):
    chat = Chat.query.get(chat_id)
    user_uid_dict = get_user_uid_dict(chat_id)

    if chat.name != None: #If the name is None that's that the chat is not a group, it's a chat between 2 people
        chat_name = chat.name
    else:
        user_list = get_users(chat.id) #This code filter to get the nickname of the user that is NOT currently using the app
        user_list.remove(current_user)
        chat_name = user_list[0].nickname

    if is_user_in_chat(current_user.id, chat.id):
        return render_template("chat.html", chat=chat, users=user_uid_dict, chat_name=chat_name)
    else:
        return "You don't have access to this chat", 403

@socket.on('connect')
def connect():
    online_user.add(current_user.id)
@socket.on('disconnect')
def disconnect():
    online_user.discard(current_user.id)

@socket.on('message')
def message(data):
    chat_id = data['chat']
    message = data['message']
    if is_user_in_chat(current_user.id, chat_id):
        send_message(chat_id, message)
@socket.on('join')
def join(room:int):
    if is_user_in_chat(current_user.id, room):
        join_room(str(room))