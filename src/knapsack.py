def knapsack(parcels, capacity):
    """0/1 Knapsack DP. Weight = parcel.weight, Value = parcel.priority."""
    n = len(parcels)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        p = parcels[i - 1]
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]
            if p.weight <= w:
                cand = dp[i - 1][w - p.weight] + p.priority
                if cand > dp[i][w]:
                    dp[i][w] = cand

    selected, w = [], capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(parcels[i - 1])
            w -= parcels[i - 1].weight
    selected.reverse()
    return selected, dp