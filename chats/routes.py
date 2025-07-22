from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from flask_socketio import join_room

from .chats import get_chat_users_dict, is_user_in_chat, send_message, get_users, get_uid_user_dict, \
    create_chat, get_chat_room, get_user_chats_links, get_chat_user_link
from core.sockets import socket
from .models import Chat

chats = Blueprint('chats', __name__, template_folder='templates', static_folder='static')

online_users = set() #In the future upgrade to Redis

@chats.route("/contacts", methods=['GET', 'POST'])
def contacts():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    user_chats_links = get_user_chats_links(current_user.id)

    return render_template('contacts.html', user_chats_links=user_chats_links)

@chats.route("/chats/<chat_id>")
def chat(chat_id):
    chat = Chat.query.get(chat_id)
    user_uid_dict = get_uid_user_dict(chat_id)
    chat_user_link = get_chat_user_link(current_user.id, chat_id)

    if is_user_in_chat(current_user.id, chat.id):
        return render_template("chat.html", chat=chat, uid_users_dict=user_uid_dict, chat_user_link=chat_user_link)
    else:
        return "You don't have access to this chat", 403

@socket.on('connect')
def connect():
    online_users.add(current_user.id)
@socket.on('disconnect')
def disconnect():
    online_users.discard(current_user.id)

@socket.on('message')
def message(data):
    chat_id = data['chat']
    message = data['message']
    if is_user_in_chat(current_user.id, chat_id):
        send_message(chat_id, message)
@socket.on('join_chat')
def join(chat_id:int):
    if is_user_in_chat(current_user.id, chat_id):
        join_room(get_chat_room(chat_id))