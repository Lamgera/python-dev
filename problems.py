# Блок 2

# 4.3. (уровень сложности: средний)

# Вы получили зашифрованное сообщение и теперь предстоит его расшифровать:
# Известно, что для зашифрования использовался алгоритм TEA. Известен также ключ зашифрования/расшифрования:
# k = [0, 4, 5, 1]
# Имеется и функция на C/C++ для расшифровки данных (v – слова данных, k – ключ)

import struct

def decrypt(v, k):
    v0, v1 = v
    k0, k1, k2, k3 = k
    sum_val = 0xC6EF3720
    delta = 0x9E3779B9
    mask = 0xFFFFFFFF
    
    for _ in range(32):
        v1 = (v1 - (((v0 << 4) + k2) ^ (v0 + sum_val) ^ ((v0 >> 5) + k3))) & mask
        v0 = (v0 - (((v1 << 4) + k0) ^ (v1 + sum_val) ^ ((v1 >> 5) + k1))) & mask
        sum_val = (sum_val - delta) & mask
        
    return v0, v1

hex_data = """
E3238557 6204A1F8 E6537611 174E5747
5D954DA8 8C2DFE97 2911CB4C 2CB7C66B
E7F185A0 C7E3FA40 42419867 374044DF
2519F07D 5A0C24D4 F4A960C5 31159418
F2768EC7 AEAF14CF 071B2C95 C9F22699
FFB06F41 2AC90051 A53F035D 830601A7
EB475702 183BAA6F 12626744 9B75A72F
8DBFBFEC 73C1A46E FFB06F41 2AC90051
97C5E4E9 B1C26A21 DD4A3463 6B71162F
8C075668 7975D565 6D95A700 7272E637
"""
k = [0, 4, 5, 1]
words = [int(x, 16) for x in hex_data.split()]
result_bytes = bytearray()
for i in range(0, len(words), 2):
    v = (words[i], words[i+1])
    v0, v1 = decrypt(v, k)
    result_bytes.extend(struct.pack(">II", v0, v1))

print("расшифровкак:")
print(result_bytes.decode('utf-8', errors='ignore'))