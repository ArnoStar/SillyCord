from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user

from .forms import ProfilePictureForm, NicknameForm, DescriptionForm
from users.models import User
from .profile import change_profile_picture, change_nickname, change_description

profile = Blueprint('profile', __name__, template_folder='templates')

@profile.route('/<int:user_id>')
def profile_page(user_id):
    user = User.query.get(user_id)
    return render_template("profile.html", user=user)

@profile.route('editor/<int:user_id>', methods=['GET', 'POST'])
def editor(user_id):
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    if not current_user.id == user_id:
        return "403, not authorized", 403

    profile_picture_form = ProfilePictureForm()
    nickname_form = NicknameForm()
    description_form = DescriptionForm()
    user = User.query.get(user_id)

    if profile_picture_form.validate_on_submit():
        file = profile_picture_form.profile_picture.data
        change_profile_picture(user, file)
    if nickname_form.validate_on_submit():
        change_nickname(user, nickname_form.nickname.data)
    if description_form.validate_on_submit():
        change_description(user, description_form.description.data)
    return render_template("profile_editor.html", user=user,
                            profile_picture_form=profile_picture_form,
                            nickname_form=nickname_form,
                            description_form=description_form)
