from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Length

from users.models import USERNAME_MAX_LENGTH, USERNAME_MIN_LENGTH

class FindUserForm(FlaskForm):
    username = StringField(label='Username of your friend (not the nickname):', validators=[DataRequired(), Length(min=USERNAME_MIN_LENGTH, max=USERNAME_MAX_LENGTH)])
    submit = SubmitField(label='Submit')