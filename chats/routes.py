from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

from .chats import get_chats, create_chat, get_chat_users_dict
from core.sockets import socket
from .models import ChatUserLink

chats = Blueprint('chats', __name__, template_folder='templates', static_folder='static')

online_user = set() #In the future upgrade to Redis

@chats.route("/contacts", methods=['GET', 'POST'])
def contacts():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    chats_users = get_chat_users_dict(current_user.id)

    return render_template('contacts.html', chats=chats_users)

@socket.on('connect')
def connect():
    get_chats(current_user.id)
    online_user.add(current_user.id)
@socket.on('disconnect')
def disconnect():
    online_user.discard(current_user.id)