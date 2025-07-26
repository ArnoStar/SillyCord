from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length

from users.models import USERNAME_MAX_LENGTH, USERNAME_MIN_LENGTH

class ProfilePictureForm(FlaskForm):
    profile_picture = FileField('Profile Picture', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')
class NicknameForm(FlaskForm):
    nickname = StringField('Nickname', validators=[DataRequired(), Length(min=USERNAME_MIN_LENGTH, max=USERNAME_MAX_LENGTH)])
    submit = SubmitField('Submit')
class DescriptionForm(FlaskForm):
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=0, max=400)]) #change max and min value in the future
    submit = SubmitField('Submit')