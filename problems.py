# Блок 2

# 5.6. (уровень сложности: средний)

# Реализуйте простую систему проверки орфографии с помощью функции вычисления
# расстояния Левенштейна. Для работы потребуется словарь русских слов с указанием
# частот встречаемости.


DICT = {
    'по-моему': 100, 
    'я': 500, 
    'написал': 80, 
    'всё': 150, 
    'правильно': 90
}

def get_lev_dist(s1, s2):
    n, m = len(s1), len(s2)
    if n < m: 
        s1, s2 = s2, s1
    prev = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        curr = [i + 1]
        for j, c2 in enumerate(s2):
            curr.append(min(prev[j+1]+1, curr[j]+1, prev[j]+(c1!=c2)))
        prev = curr
    return prev[-1]

def spell_word(word, dictionary):
    if word in dictionary: 
        return word
    for dist in [1, 2]:
        candidates = [w for w in dictionary if get_lev_dist(word, w) == dist]
        if candidates:
            return max(candidates, key=lambda w: dictionary[w])
    
    return word

def spell(text):
    words = text.split()
    return " ".join(spell_word(w, DICT) for w in words)

print(spell('помоему я напесал усё правильна'))