import os
from werkzeug.utils import secure_filename
from time import time
from PIL import Image
from flask import current_app

from core.database import db
from users.models import User, DEFAULT_PROFILE_PICTURE

def change_profile_picture(user:User, image):
    image_name = secure_filename(str(time())+image.filename) #Time is an easy way to make the file name unique
    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_name)

    #Making the image a square, and resizing it. This is used only on time, this is why I didn't make a function for this
    image = Image.open(image)
    width, height = image.size
    min_side = min(width, height)
    left = (width - min_side)//2
    top = (height - min_side)//2
    right = width - left
    bottom = height - top
    image = image.crop((left, top, right, bottom))

    image.save(image_path)
    old_file_name = user.profile_picture
    if old_file_name != DEFAULT_PROFILE_PICTURE:
        old_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], old_file_name)
        os.remove(old_file_path) #Delete the old profile_picture
    user.profile_picture = image_name
    db.session.commit()
def change_nickname(user:User, nickname):
    user.nickname = nickname
    db.session.commit()
def change_description(user:User, description):
    user.description = description
    db.session.commit()