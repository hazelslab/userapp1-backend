from datetime import datetime

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from flask_socketio import SocketIO, emit
from pymongo import MongoClient

import bcrypt

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'test-key'  # Ändere dies zu einem sicheren geheimen Schlüssel
jwt = JWTManager(app)

# Konfigurieren von Flask-SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

client = MongoClient('mongodb+srv://userapp1user:userapp1user@cluster0.xxtjtei.mongodb.net/?retryWrites=true&w=majority')
db = client['userapp1']


@app.route('/')
def start():
    return 'Hello, World!'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    user = {
        'username': data['username'],
        'email': data['email'],
        'firstname': data['firstname'],
        'lastname': data['lastname'],
        'password': data['password']
    }

    db.users.insert_one(user)
    return jsonify({'message': 'Registrierung erfolgreich!'})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = db.users.find_one({'username': data['username']})

    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user['password'].encode('utf-8')):
        access_token = create_access_token(identity=user['username'])
        return jsonify({'access_token': access_token})
    else:
        return jsonify({'message': 'Ungültiger Benutzername oder Passwort'}), 401


@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    sender = data['sender']
    recipient = data['recipient']
    message = data['message']

    db.messages.insert_one({
        'sender': sender,
        'recipient': recipient,
        'message': message,
        'timestamp': datetime.utcnow()
    })

    return jsonify({'message': 'Nachricht gesendet'})


@app.route('/get_messages', methods=['POST'])
def get_messages():
    data = request.get_json()
    sender = data['sender']
    recipient = data['recipient']

    messages = list(db.messages.find({
        '$or': [
            {'sender': sender, 'recipient': recipient},
            {'sender': recipient, 'recipient': sender}
        ]
    }))

    for message in messages:
        message['_id'] = str(message['_id'])
        message['timestamp'] = message['timestamp'].strftime('%Y-%m-%d %H:%M:%S')

    return jsonify(messages)

if __name__ == '__main__':
    app.run(debug=True)
