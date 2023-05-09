import bcrypt
from flask_bcrypt import Bcrypt
from pymongo import MongoClient



client = MongoClient('mongodb+srv://userapp1user:userapp1user@cluster0.xxtjtei.mongodb.net/?retryWrites=true&w=majority')
db = client['userapp1']


user = {
    'username': 'test',
    'email': 'test',
    'firstname': 'test',
    'lastname': 'test',
    'password': 'test'
}

db.users.insert_one(user)