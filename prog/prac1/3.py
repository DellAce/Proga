"""
Дана матрица NxM, которая заполнена 0 или 1. Необходимо выполнить поиск квадрата 
с максимальной стороной, заполненного только 1. Вывести длину стороны найденного 
квадрата.
Пример входной матрицы имеет вид:

1 0 1 0 0
0 0 1 1 1
1 1 0 1 1   
Ответ: 2
"""
matrix = [[1, 0, 1, 0, 0],
         [0, 0, 1, 1, 1],
         [1, 1, 0, 1, 1]]
max = 0
