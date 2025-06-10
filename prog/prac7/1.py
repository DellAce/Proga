from itertools import combinations


def valid_square(p1, p2, p3, p4):
    d = sorted(
        (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
        for a, b in combinations([p1, p2, p3, p4], 2)
    )
    return d[0] > 0 and d[0] == d[1] == d[2] == d[3] and d[4] == d[5] == 2 * d[0]


p1 = [0, 0]
p2 = [1, 1]
p3 = [1, 0]
p4 = [0, 1]
print(valid_square(p1, p2, p3, p4))
