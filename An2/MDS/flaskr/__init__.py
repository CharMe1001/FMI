from flask import Flask
from flask import render_template
from flask_socketio import SocketIO, join_room, leave_room, emit
#import pymongo

def create_app():
    app = Flask(__name__)
    #client = pymongo.MongoClient(
    #    "mongodb+srv://CharacterMe:extraword12@cluster0.jwkwr.mongodb.net/?retryWrites=true&w=majority")
    #db = client.get_database('Test')
    #collection = db.get_collection('Flask')

    socketio = SocketIO(app)
    room = ""

    @socketio.on('joinRoom')
    def on_join_room(roomName):
        nonlocal room
        if room != "":
            leave_room(room)

        room = roomName
        join_room(roomName)

    @socketio.on('receive')
    def on_receive(msg):
        if room == "":
            return

        emit('receive', msg, room=room)

    @app.route("/")
    def main():
        #collection.insert_one({'name': 'John'})
        return render_template("index.html")

    return app
