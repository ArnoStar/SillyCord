# SillyCord
## A discord-like app based on flask

This is a simple messaging app, with basic features like: auth (username, password, email),
email confirmation, profiles, profile editing, realtime messaging.

## Run the project

You'll need python and git installed on your PC (I know this is really unexpected).\
If you want you can create a python virtual environment.
1. First clone the GitHub repository with this command.\
``git clone https://github.com/ArnoStar/SillyCord.git`` \
After that enter the SillyCord dir\
``cd SillyCord``
2. After that you'll need all the requirements, install them with this command\
``pip install -r requirements.txt``
3. Before running the project you need to set up some environment variables,
if you don't know how just create a .env file and set variables like this:
````
DEBUG=0 #Set to 0 if you want the debug set to false, 1 if true
SECRET_KEY=writeARandomSecretString
DATABASE_URL=sqlite:///SillyCord.db #Unless you know what you're doing you should this like it is

MAIL_SERVER=smtp.gmail.com #I recomand you to use the stmp gmail server
MAIL_USERNAME=yourMail@gmail.com
MAIL_PASSWORD=**** **** **** **** #This password is NOT the password of your gmail account you'll need to find the password for app
MAIL_DEFAULT_SENDER=yourMail@gmail.com #This should be the same email as upward
````
4. Now the setup is finished, you just need to run the project with this command:\
``py run.py``
