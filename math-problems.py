#Блок 1 - Математические задачи

#3.3. (уровень сложности: средний)
# Умножение на 15. Используйте 3 сложения и 2 вычитания.

def mul_by_15(x):
    """
    1. x + x = 2x
    2. 2x + 2x = 4x
    3. 4x + 4x = 8x
    4. x - 8x = -7x 
    5. 8x - (-7x) = 15x 
    """
    
    val_2x = x + x
    val_4x = val_2x + val_2x
    val_8x = val_4x + val_4x
    diff = x - val_8x
    result = val_8x - diff
    
    return result

print (mul_by_15(2))