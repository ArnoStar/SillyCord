from core.app import create_app
from core.sockets import socket

#import eventlet
#eventlet.monkey_patch() #Recommended when using flask-socketIO, do probably something useful?

app = create_app()

if __name__ == '__main__':
    socket.run(app)