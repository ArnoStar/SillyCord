from flask import Blueprint, redirect, url_for

core = Blueprint('core', __name__)

@core.route('/')
def index():
    return redirect(url_for('auth.login'))