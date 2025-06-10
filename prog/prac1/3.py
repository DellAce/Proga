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


def max_square_of_ones(matrix):
    if not matrix:
        return 0
    n = len(matrix)
    m = len(matrix[0])
    dp = [[0] * m for _ in range(n)]
    max_side = 0

    for i in range(n):
        for j in range(m):
            if matrix[i][j] == 1:
                if i == 0 or j == 0:
                    dp[i][j] = 1
                else:
                    dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
                max_side = max(max_side, dp[i][j])
    return max_side


mat = [[1, 0, 1, 0, 0], [0, 0, 1, 1, 1], [1, 1, 0, 1, 1]]
print(max_square_of_ones(mat))
