
from TestArea import ModuleTest
import queue





x = ModuleTest.addFunc(2, 3)

q = queue.Queue()

q.put("a")
q.put("b")
q.put("c")


print(q.get())
print(q.get())

print('this is \ntest'[9:])

print(len('you are log in as:\n'))

users = ['pabjek', 'huhkuwud', 'hugo']

s=''
for user in users[0:2]:
    s += user + " "

s = 'LIST ' + s
print(s)