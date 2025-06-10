def word_break(s, dict_):
    n = len(s)
    dp = [True] + [False] * n
    for i in range(1, n + 1):
        dp[i] = any(dp[i - len(w)] and s[i - len(w) : i] == w for w in dict_)
    return dp[-1]


s = "applepenapple"
wordDict = ["apple", "pen"]
print(word_break(s, wordDict))
