from datetime import datetime, UTC

from core.database import db
from users.models import User

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'message' : self.message,
            'date' : self.date.isoformat(),
            'author' : User.query.get(self.author_id).to_dict(),
            'chat' : Chat.query.get(self.chat_id).to_dict()}

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    messages = db.relationship('Message', backref='chat', lazy=True)
    links = db.relationship('ChatUserLink', backref='chat', lazy=True)

    def to_dict(self):
        return {'id': self.id}

class ChatUserLink(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False, nullable=False, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), unique=False, nullable=False, primary_key=True)

    name = db.Column(db.Text, unique=False, nullable=False)