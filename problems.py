# Блок 2

# 5.5. (уровень сложности: средний)

# С использованием функции расстояния Левенштейна можно получить последовательность 
# команд редактирования, которые превращают исходную последовательность в результат. 
# Это может помочь компактно хранить данные – для измененной версии файла мы храним 
# только команды, которые производят эти изменения. В этой задаче необходимо 
# сгенерировать код на Питоне, который из исходного списка создает список-результат 
# с помощью минимального числа операций вставки, замены и удаления.

import random, string

def lev_dist_gen(s1, s2):
    n, m = len(s1), len(s2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1): dp[i][0] = i
    for j in range(m + 1): dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + cost)

    commands = []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and s1[i-1] == s2[j-1]:
            i -= 1; j -= 1
            continue
        
        if i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + 1:
            commands.append(f"x[{i-1}] = y[{j-1}]")
            i -= 1; j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j] + 1:
            commands.append(f"del x[{i-1}]")
            i -= 1
        elif j > 0 and dp[i][j] == dp[i][j-1] + 1:
            commands.append(f"x.insert({i}, y[{j-1}])")
            j -= 1
            
    return commands

def test_lev_gen():
  for _ in range(5):
      s1 = list(''.join(random.choices(string.ascii_lowercase, k=5)))
      s2 = list(''.join(random.choices(string.ascii_lowercase, k=5)))
      print(f"Первое случайное слово: {''.join(s1)}, Второе случайное слово: {''.join(s2)}")
      x, y = list(s1), list(s2)
      cmds = lev_dist_gen(s1, s2)

      for cmd in cmds:
        exec(cmd)
      assert x == y, f"Ошибка: {''.join(s1)} -> {''.join(s2)}, получили {''.join(x)}"

  return "Тесты пройдены!"

print(test_lev_gen())