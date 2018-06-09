from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')

msg_db = client.py_db

user_collection = msg_db['msg_user']


def add_user_to_db(name, password):
    user = make_user(name, password)
    user_collection.insert_one(user)


def verify_user(name, password):
    user = make_user(name, password)
    user_find = user_collection.find_one(user)
    return user_find


def make_user(name, password):
    user = {
        "user_name": name,
        "password": password
    }
    return user



# ---------------print test----------------

print(type(user_collection))

print(type(user_collection.find_one({
    "user_name": "hugo"
})))