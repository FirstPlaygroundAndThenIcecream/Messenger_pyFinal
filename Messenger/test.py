import string
from itertools import product

# def get_value(numbers):
#     for i in numbers:
#         yield (i*2)
#
#
# x = [1, 2, 3, 4, 5]
# y = get_value(x)
# for i in range(0, len(x)):
#     print(next(y))
#
# my_num = (i*2 for i in x)
#
# for num in my_num:
#     print(num)
#
#
# # list store multiple types
# m = [1, 2.000, 'u']
#
# print(type(m[1]))


def test_brute_force():
    digits = string.digits
    print(digits[9])
    print(type(digits[0]))
    combination = (','.join(i) for i in product('123', repeat=4))
    print(type(combination))
    for each in combination:
            print(each)


test_brute_force()