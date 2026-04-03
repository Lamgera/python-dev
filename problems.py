# Блок 2

# 3.9. (уровень сложности: средний)

# Реализовать функцию-однострочник для RLE-сжатия. Пример работы:

# >>> rle_encode('ABBCCCDEF')
# [('A', 1), ('B', 2), ('C', 3), ('D', 1), ('E', 1), ('F', 1)]

from itertools import groupby

rle_encode = lambda data: [(char, len(list(group))) for char, group in groupby(data)]
print (rle_encode('AABBBCC'))