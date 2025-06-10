def multiply(a, b):
    if a == "0" or b == "0":
        return "0"
    res = [0] * (len(a) + len(b))
    for i, x in enumerate(reversed(a)):
        for j, y in enumerate(reversed(b)):
            res[i + j] += int(x) * int(y)
            res[i + j + 1] += res[i + j] // 10
            res[i + j] %= 10
    while res[-1] == 0:
        res.pop()
    return "".join(map(str, res[::-1]))


num1 = "2"
num2 = "3"
print(multiply(num1, num2))
