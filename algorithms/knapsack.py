# 0/1 Knapsack (DP optimal scheduler)
def knapsack(tasks, time_available):
    # tasks = [(name, time, value)]
    n = len(tasks)

    dp = [[0] * (time_available + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        name, t, val = tasks[i - 1]
        for cap in range(time_available + 1):
            if t > cap:
                dp[i][cap] = dp[i - 1][cap]
            else:
                dp[i][cap] = max(dp[i - 1][cap], dp[i - 1][cap - t] + val)

    # backtrack
    chosen = []
    cap = time_available

    for i in range(n, 0, -1):
        if dp[i][cap] != dp[i - 1][cap]:
            name, t, val = tasks[i - 1]
            chosen.append((name, t, val))
            cap -= t

    chosen.reverse()
    total_value = dp[n][time_available]
    total_time = sum(t for _, t, _ in chosen)

    return chosen, total_time, total_value
