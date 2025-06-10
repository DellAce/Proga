def exist(board, word):
    n, m = len(board), len(board[0])

    def dfs(i, j, k):
        if k == len(word):
            return True
        if not (0 <= i < n and 0 <= j < m) or board[i][j] != word[k]:
            return False
        tmp, board[i][j] = board[i][j], "#"
        ok = any(
            dfs(i + di, j + dj, k + 1) for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1))
        )
        board[i][j] = tmp
        return ok

    return any(dfs(i, j, 0) for i in range(n) for j in range(m))


board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
word = "ABCCED"
print(exist(board, word))
