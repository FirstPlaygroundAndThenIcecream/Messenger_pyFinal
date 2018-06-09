from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')

msg_db = client.py_db

user_collection = msg_db['msg_user']


def add_user_to_db(name, password):
    user = {
        "user_name": name,
        "password": password
    }
    user_collection.insert_one(user)


print(type(user_collection))