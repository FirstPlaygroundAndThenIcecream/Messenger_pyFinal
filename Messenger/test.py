def get_value(numbers):
    for i in numbers:
        yield (i*2)


x = [1, 2, 3, 4, 5]
y = get_value(x)
for i in range(0, len(x)):
    print(next(y))

my_num = (i*2 for i in x)

for num in my_num:
    print(num)


# list store multiple types
m = [1, 2.000, 'u']

print(type(m[1]))

