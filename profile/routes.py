from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

from .forms import ProfilePictureForm, NicknameForm, DescriptionForm
from users.models import User

profile = Blueprint('profile', __name__, template_folder='templates')

@profile.route('/<int:user_id>')
def profile_page(user_id):
    user = User.query.get(user_id)
    return render_template("profile.html", user=user)
@profile.route('editor/<int:user_id>')
def editor(user_id):
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    if current_user.id == user_id:
        user = User.query.get(user_id)
        profile_picture_form = ProfilePictureForm()
        nickname_form = NicknameForm()
        description_form = DescriptionForm()
        return render_template("profile_editor.html", user=user,
                               profile_picture_form=profile_picture_form,
                               nickname_form=nickname_form,
                               description_form=description_form)
    else:
        return "403, not authorized", 403