from pymongo import MongoClient

KEY = 4

client = MongoClient('mongodb://localhost:27017/')

msg_db = client.py_db

user_collection = msg_db['msg_user']


def add_user_to_db(name, password):
    user = make_user(name, password)
    user_collection.insert_one(user)


def verify_user(name, password):
    user_find = user_collection.find_one({'user_name': name})

    if user_find is None:
        return False
    else:
        user_find_password = decrypt_user_password(user_find['password'], KEY)
        print(user_find_password)
        if password == user_find_password:
            return True
        else:
            return False


def check_name_duplicate(name):
    result = user_collection.find_one({"user_name": name})
    if result is None:
        return False
    else:
        return True


def make_user(name, password):
    encrypt_password = encrypt_user_password(password, KEY)
    user = {
        "user_name": name,
        "password": encrypt_password
    }
    return user


def encrypt_user_password(password, key):
    new_psw = ""
    for each in password:
        after_modify = chr(ord(each) + key)
        new_psw += after_modify
    return new_psw


def decrypt_user_password(encrypt_psw, key):
    back_original = ""
    for each in encrypt_psw:
        decrypt_psw = chr(ord(each) - key)
        back_original += decrypt_psw
    return back_original

