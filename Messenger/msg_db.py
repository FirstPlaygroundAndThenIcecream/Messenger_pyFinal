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
    if not user_find is None:
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
    user = {
        "user_name": name,
        "password": password
    }
    return user



# ---------------print test----------------

# print(type(user_collection))
#
# print(type(user_collection.find_one({
#     "user_name": "hugo"
# })))
# x = check_name_duplicate("John")
#
# # user_collection.find_one({"user_name": "John"})
# print(user_collection.find_one({"user_name": "John"})['user_name'])
# print(x)


# result = check_name_duplicate("Ji")
# print(result)
#

result = verify_user("tintin", "tintin")
print(result)