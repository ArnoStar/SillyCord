from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user
from flask_socketio import join_room

from .chats import is_user_in_chat, send_message, get_uid_user_dict, \
    get_chat_room, get_user_chats_links, get_chat_user_link, does_chat_exist, create_chat, does_user_exist
from .models import Chat
from .forms import FindUserForm
from core.sockets import socket
from users.models import User

chats = Blueprint('chats', __name__, template_folder='templates', static_folder='static')

online_users = set() #In the future upgrade to Redis

@chats.route("/contacts", methods=['GET', 'POST'])
def contacts():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    user_chats_links = get_user_chats_links(current_user.id)

    return render_template('contacts.html', user_chats_links=user_chats_links)

@chats.route("/find", methods=['GET', 'POST'])
def find():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    form = FindUserForm()

    if request.method == "GET":
        return render_template('find_user.html', form=form)
    if request.method == "POST":
        user = User.query.filter_by(username=form.username.data).first()

        if user is None:
            flash('Invalid username.')
            return render_template('find_user.html', form=form)
        if does_chat_exist(current_user.id, user.id):
            flash("You already have this person in your contacts.", "error")
            return render_template('find_user.html', form=form)

        create_chat(current_user.id, user.id)
        return redirect(url_for('chats.contacts'))


@chats.route("/chats/<chat_id>")
def chat(chat_id):
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

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