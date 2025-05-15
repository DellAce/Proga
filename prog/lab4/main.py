#!/usr/bin/python3

import ctypes 

# Загрузка библиотеки
test = ctypes.CDLL('./libtest.so')

##
# Работа с функциями
##

# Указываем, что функция возвращает int
test.func_ret_int.restype = ctypes.c_int
# Указываем, что функция принимает аргумент int
test.func_ret_int.argtypes = [ctypes.c_int, ]

# Указываем, что функция возвращает double
test.func_ret_double.restype = ctypes.c_double
# Указываем, что функция принимает аргумент double
test.func_ret_double.argtypes = [ctypes.c_double]

# Указываем, что функция возвращает char *
test.func_ret_str.restype = ctypes.c_char_p
# Указываем, что функция принимает аргумент char *
test.func_ret_str.argtypes = [ctypes.POINTER(ctypes.c_char), ]

# Указываем, что функция возвращает char
test.func_many_args.restype = ctypes.c_char
# Указываем, что функция принимает аргументы int, double. char, short
test.func_many_args.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_char, ctypes.c_short]

print('ret func_ret_int: ', test.func_ret_int(101))
print('ret func_ret_double: ', test.func_ret_double(12.123456789))

# Необходимо строку привести к массиву байтов, затем полученный массив байтов приводим к строке.
print('ret func_ret_str: ', test.func_ret_str('Hello!'.encode('utf-8')).decode("utf-8") )

print('ret func_many_args: ', test.func_many_args(15, 18.1617, 'X'.encode('utf-8'), 32000).decode("utf-8"))

print()

##
# Работа с переменными
##

# Указываем, что переменная типа int
a = ctypes.c_int.in_dll(test, "a")
print('ret a: ', a.value)

# Изменяем значение переменной.
a.value = 22
a = ctypes.c_int.in_dll(test, "a")
print('ret a: ', a.value)

# Указываем, что переменная типа double
b = ctypes.c_double.in_dll(test, "b")
print('ret b: ', b.value)

# Указываем, что переменная типа char
c = ctypes.c_char.in_dll(test, "c")
print('ret c: ', c.value.decode("utf-8"))

