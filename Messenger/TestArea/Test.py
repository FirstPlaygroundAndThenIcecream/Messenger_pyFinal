
from TestArea import ModuleTest
import queue

import User



user = User.User("lei", "128.0.0.1")

user_1 = User.User("joe", "127.0.0.1")

users = []

users.append(user)
users.append(users)

print(user.get_name())

user.set_visible(False)

print(user.is_visible())

print('this' + str(len(users)))