def solve(eq):
    L, R = eq.split("=")

    def parse(s):
        c = a = 0
        num = ""
        sign = 1
        for ch in s + "+":
            if ch in "+-":
                if num:
                    a += sign * int(num)
                    num = ""
                sign = 1 if ch == "+" else -1
            elif ch == "x":
                c += sign * (int(num) if num else 1)
                num = ""
            else:
                num += ch
        return c, a

    c1, a1 = parse(L)
    c2, a2 = parse(R)
    c, a = c1 - c2, a2 - a1
    return (
        "бесконечное множество решений"
        if c == 0 and a == 0
        else "нет решений" if c == 0 else f"x={a//c}"
    )


eq = "x+5-3+x=6+x-2"
print(solve(eq))
