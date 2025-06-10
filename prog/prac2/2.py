from math import isqrt


def sum_squares(n):
    res = []
    while n:
        k = isqrt(n)
        if k == 0:
            return -1
        res.append(k)
        n -= k * k
    return sorted(res) or -1
