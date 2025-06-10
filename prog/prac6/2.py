def count_combos(amount, coins):
    dp = [1] + [0] * amount
    for c in coins:
        for v in range(c, amount + 1):
            dp[v] += dp[v - c]
    return dp[amount]


amount = 5
coins = [1, 2, 5]
print(count_combos(amount, coins))
