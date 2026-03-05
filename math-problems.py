#Блок 1 - Математические задачи


# 3.8. (уровень сложности: средний)
# Четыре умножения из предыдущей задачи – не предел.
# Советский ученый Анатолий Алексеевич Карацуба в 1960 г. предложил формулу
# (а для общего случая – рекурсивный алгоритм), требующую лишь трех умножений.
# Выведите эту формулу с подсказками от преподавателя и реализуйте функцию mul16k(x, y).

def mul_bits(x, y, bites):
    x &= (2 ** bites - 1)
    y &= (2 ** bites - 1)
    return x * y

def mul16k(x, y):
    x_hi = x >> 8
    x_lo = x & 0xFF
    
    y_hi = y >> 8
    y_lo = y & 0xFF

    A = mul_bits(x_hi, y_hi, 8)
    B = mul_bits(x_lo, y_lo, 8)
    
    sum_x = x_hi + x_lo
    sum_y = y_hi + y_lo
    C = mul_bits(sum_x, sum_y, 9)
    
    middle = C - A - B
    result = (A << 16) + (middle << 8) + B
    
    return result


def run_tests():
    print("Запуск тестов для mul16k (Карацуба)...")
    assert mul16k(10, 20) == 200, "Ошибка в простом тесте"
    assert mul16k(255, 255) == 65025, "Ошибка на границе 8 бит"
    assert mul16k(256, 256) == 65536, "Ошибка 256 * 256"

    max_val = (1 << 16) - 1
    assert mul16k(max_val, max_val) == max_val * max_val, "Ошибка на макс. значениях"

    val_a = 0x1234
    val_b = 0x5678
    expected = val_a * val_b
    res = mul16k(val_a, val_b)
    assert res == expected, f"Ошибка: {val_a} * {val_b} = {res}, ожидалось {expected}"

    val_c = 0x01FF
    assert mul16k(val_c, val_c) == val_c * val_c, "Ошибка при переполнении суммы половин"

    print("Все тесты для mul16k пройдены успешно!")

run_tests()
