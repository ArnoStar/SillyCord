from flask import Flask

from .database import db
from .routes import core
from .login_manager import login_manager
from auth.routes import auth

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config["SECRET_KEY"] = "<KEY>"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///SillyCord.db"
    db.init_app(app)
    with app.app_context():
        db.create_all()

    login_manager.init_app(app)

    app.register_blueprint(core)
    app.register_blueprint(auth, url_prefix="/auth")

    return app