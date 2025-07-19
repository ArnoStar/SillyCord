from .models import ChatUserLink, Chat
from core.database import db
from users.models import User

def get_chats(user_id:int):
    links = ChatUserLink.query.filter_by(user_id=user_id).all() #Get from the db the link chat-user, we will use this to get every link with the {user_id} and from here we can get the chats
    chats = []
    for link in links:
        chat = Chat.query.get(link.chat_id)
        chats.append(chat)
    return chats
def get_users(chat_id:int):
    links = ChatUserLink.query.filter_by(chat_id=chat_id).all() #Same thing here but we filter the link by the chat to get users, not by the user to get chats
    users = []
    for link in links:
        user = User.query.get(link.user_id)
        users.append(user)
    return users

def get_chat_users_dict(user_id:int) -> dict: #This function use useful for the jinja2 code
    chat_users = dict()
    for chat in get_chats(user_id):
        chat_users[chat] = get_users(chat.id)

    return chat_users

def create_chat(users_ids:list[int]):
    default_name = ''

    new_chat = Chat(name=default_name)
    db.session.add(new_chat)
    db.session.flush()

    for user_id in users_ids:
        user = User.query.get(user_id)
        #default_name += user.nickname+" "

        new_link = ChatUserLink(user_id=user_id, chat_id=new_chat.id)
        db.session.add(new_link)

    #new_chat.name = default_name

    db.session.commit()