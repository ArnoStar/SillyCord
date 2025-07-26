from dotenv import load_dotenv
import os

from flask import Flask

from .database import db
from .routes import core
from .login_manager import login_manager
from .mail import mail
from .sockets import socket
from auth.routes import auth
from chats.routes import chats
from profile.routes import profile

def create_app():
    load_dotenv()

    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config["UPLOAD_FOLDER"] = "static/uploads"
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    db.init_app(app)
    with app.app_context():
        db.create_all()

    login_manager.init_app(app)


    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

    mail.init_app(app)

    socket.init_app(app)

    app.register_blueprint(core)
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(chats, url_prefix="/chats")
    app.register_blueprint(profile, url_prefix="/profile")

    return app