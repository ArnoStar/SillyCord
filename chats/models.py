from datetime import datetime, UTC
from enum import unique

from core.database import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now(UTC))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    messages = db.relationship('Message', backref='chat', lazy=True)
    links = db.relationship('ChatUserLink', backref='chat', lazy=True)

class ChatUserLink(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False, nullable=False, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), unique=False, nullable=False, primary_key=True)