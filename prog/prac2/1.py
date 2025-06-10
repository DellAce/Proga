def tree_paths(levels):
    if not levels:
        return []
    paths = []

    def dfs(i, cur):
        if i >= len(levels) or levels[i] is None:
            return
        cur.append(levels[i])
        l, r = 2 * i + 1, 2 * i + 2
        if (l >= len(levels) or levels[l] is None) and (
            r >= len(levels) or levels[r] is None
        ):
            paths.append(cur.copy())
        else:
            dfs(l, cur)
            dfs(r, cur)
        cur.pop()

    dfs(0, [])
    return paths


data = [1, 2, 3, None, 4]
print(tree_paths(data))
