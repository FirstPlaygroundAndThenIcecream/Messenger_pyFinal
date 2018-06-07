import User
import ModuleTest
import queue



user = User.User("Jane", id)
print(user.getUsername())

x = ModuleTest.addFunc(2, 3)

q = queue.Queue()

q.put("a")
q.put("b")
q.put("c")


print(q.get())
print(q.get())