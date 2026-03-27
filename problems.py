# Блок 2

# 5.7. (уровень сложности: высокий)

# Доработайте систему проверки орфографии с помощью модифицированной функции
# расстояния Левенштейна, в которой учитываются:
# Замены сходных по написанию английских букв на русские.
# Перестановки пар соседних символов.


def improved_lev_dist(s1, s2):
    SIMILAR = {'a':'а', 'e':'е', 'o':'о', 'p':'р', 'c':'с', 'x':'х', 'y':'у'}
    d = {}
    n, m = len(s1), len(s2)
    for i in range(-1, n + 1): d[i, -1] = i + 1
    for j in range(-1, m + 1): d[-1, j] = j + 1
    for i in range(n):
        for j in range(m):
            if s1[i] == s2[j] or SIMILAR.get(s1[i]) == s2[j] or SIMILAR.get(s2[j]) == s1[i]:
                cost = 0
            else:
                cost = 1
            
            d[i, j] = min(
                d[i-1, j] + 1,
                d[i, j-1] + 1,
                d[i-1, j-1] + cost
            )
            if i > 0 and j > 0 and s1[i] == s2[j-1] and s1[i-1] == s2[j]:
                d[i, j] = min(d[i, j], d[i-2, j-2] + 1)

    return d[n-1, m-1]

def test_improved_speller():
    test_cases = [
        ("мама", "папа", 2, "Две замены (м->п, м->п)"),
        ("привет", "првиет", 1, "Транспозиция соседних символов (ив->ви)"),
        ("cлово", "слово", 0, "Визуальная схожесть (англ.'c' vs рус.'с')")
    ]

    for s1, s2, expected, description in test_cases:
        result = improved_lev_dist(s1, s2)
        status = "Пройден" if result == expected else "ПРОВАЛЕН"
        print(f"[{status}] {description}")
        print(f"   {s1} vs {s2} | Ожидалось: {expected}, Получено: {result}")
        print("-" * 50)

test_improved_speller()