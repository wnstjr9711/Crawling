# # def myFun(**kwargs):
# #     print(type(kwargs), kwargs)
# #     for k, v in kwargs.items():
# #         print("{0}: {1}".format(k, v))
# #
# #
# # s = myFun(a = 1, b = 2)
# # print(s)
# #
# #
# # def h(a, b, c):
# #     print(a, b, c)
# #
# #
# # dargs = {'a':1, 'b':2, 'c':3}
# # h(*dargs)
# #
# #
# # int()
# # with open('asd.txt', 'w') as f:
# #     f.write('''<DoCa
# #     b
# #     c''')
# #
# #
# # class MyInteger:
# #     def __init__(self, i):
# #         self.i = i
# #
# #     def __str__(self):
# #         return str(self.i)
# #
# #     def __add__(self, other):
# #         return self.i + other
# #
# #     def __sub__(self, other):
# #         return self.i - other
# #
# #     def __mul__(self, other):
# #         return self.i * other
# #
# #
# # i = MyInteger(20)
# # print(i)
# # print(str(i))
# #
# # print()
# # i = i + 10
# # print(i)
# #
# # print()
# # i += 10
# # print(i)
# #
# # print()
# # i += 15
# # print(i)
# #
# # print()
# # i *= 10
# # print(i)
# class MyInteger2:
#     def __init__(self, i):
#         self.i = i
#
#     def __str__(self):
#         return str(self.i)
#
#     def __add__(self, other):
#         return MyInteger2(self.i + other)
#
#     def __sub__(self, other):
#         return MyInteger2(self.i - other)
#
#     def __mul__(self, other):
#         return MyInteger2(self.i * other)
#
#     __radd__ = __add__
#
# i = MyInteger2(20)
# print(i)
# print(str(i))
#
# print()
# i = i + 10
# print(i)
#
# print()
# i += 10
# print(i)
#
# print()
# i += 15
# print(i)
#
# print()
# i *= 10
# print(i)
#
#
#
#
# class MyString:
#     def __init__(self, str):
#         self.str = str
#
#     def __neg__(self):
#         t = list(self.str)
#         t.reverse()
#         return ''.join(t)
#
#     __invert__ = __neg__
#
#
# m = MyString("abcdef")
# print(-m)
# print(~m)
#
# class StringRepr:
#     def __repr__(self):
#         return 'StringRepr()'
#     def __str__(self):
#         return 'str called'
#
#
# s = StringRepr()
# q = eval(repr(s))
# print(q)


# 상속과 다형성
# class Super:
#     def __init__(self):
#         print('Super init called')
#
#     def perform(self):
#         print('Super')
#
#
# class Sub(Super):
#     def __init__(self):
#         print('sub init called')
#
#
# s = Sub()
# s.perform()
#
# class Person:
#     def __init__(self, name, phone=None):
#         self.name = name
#         self.phone = phone
#
#     def __str__(self):
#         return '<Person {0} {1}>'.format(self.name, self.phone)
#
#
# class Employee(Person):  # 괄호 안에 쓰여진 클래스는 슈퍼클래스를 의미한다.
#     def __init__(self, name, phone, position, salary):
#         # Person.__init__(self, name, phone) # Person클래스의 생성자 호출 --> Unbound Method Call
#         # super().__init__(name, phone)                 # --> Bound Method Call - 1
#         super(Employee, self).__init__(name, phone)  # --> Bound Method Call - 2
#
#         self.position = position
#         self.salary = salary
#
#
# e = Employee("LEE", "010-5000-1111", "대리", "3000")
# print(e)
# print()
