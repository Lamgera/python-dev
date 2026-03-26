# Блок 2

# 5.4. (уровень сложности: средний)

# Реализованная функция вычисления расстояния Левенштейна дает только миниальное число операций.
# Было бы полезно узнать, какие именно операции произведены над исходной строкой.
# Реализуйте функцию lev_dist_ops.

def lev_dist_ops(s1, s2):
    n, m = len(s1), len(s2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1): dp[i][0] = i
    for j in range(m + 1): dp[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            dp[i][j] = min(dp[i-1][j] + 1,
                           dp[i][j-1] + 1,
                           dp[i-1][j-1] + cost)
    ops = []
    curr_i, curr_j = n, m
    while curr_i > 0 or curr_j > 0:
        dist = dp[curr_i][curr_j]
        if curr_i > 0 and curr_j > 0 and s1[curr_i-1] == s2[curr_j-1]:
            curr_i -= 1
            curr_j -= 1
            continue
            
        if curr_i > 0 and curr_j > 0 and dist == dp[curr_i-1][curr_j-1] + 1:
            ops.append('замена')
            curr_i -= 1
            curr_j -= 1
        elif curr_i > 0 and dist == dp[curr_i-1][curr_j] + 1:
            ops.append('удаление')
            curr_i -= 1
        elif curr_j > 0 and dist == dp[curr_j-1][curr_j] + 1:
            ops.append('вставка')
            curr_j -= 1
            
    return ops[::-1]

print(lev_dist_ops('столб', 'слон'))