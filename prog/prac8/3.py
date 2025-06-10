def find_chain(pairs):
    pairs.sort(key=lambda x: x[1])
    cur = -float("inf")
    cnt = 0
    for a, b in pairs:
        if a > cur:
            cnt += 1
            cur = b
    return cnt


pairs = [[1, 2], [2, 3], [3, 4]]
print(find_chain(pairs))
