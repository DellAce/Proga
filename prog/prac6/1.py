def to_base7(num):
    if num == 0:
        return "0"
    sign = "-" if num < 0 else ""
    num = abs(num)
    digs = []
    while num:
        digs.append(str(num % 7))
        num //= 7
    return sign + "".join(digs[::-1])


num = 100
print(to_base7(num))
