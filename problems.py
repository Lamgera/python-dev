# Блок 2

# 5.2. (уровень сложности: средний)

# Задача состоит в том, чтобы корректно декодировать и откорректировать следующее текстовое сообщение. 
# Известно, что каждое значение в исходной последовательности является 8-битным.

def decode_byte(encoded_int):
    
    bin_str = bin(encoded_int)[2:]
    bin_str = bin_str.zfill(24)
    decoded_bits = []
    
    for i in range(0, 24, 3):
        triplet = bin_str[i:i+3]
        if triplet.count('1') >= 2:
            decoded_bits.append('1')
        else:
            decoded_bits.append('0')
    
    return int("".join(decoded_bits), 2)

encoded_data = [
    815608, 2064837, 2093080, 2063879, 196608, 2067983, 
    10457031, 1830912, 2067455, 2093116, 1044928, 2064407, 
    6262776, 2027968, 4423680, 2068231, 2068474, 1999352, 
    1019903, 2093113, 2068439, 2064455, 1831360, 1936903, 
    2067967, 2068456
]

decoded_bytes = [decode_byte(val) for val in encoded_data]

message = bytes(decoded_bytes).decode('utf-8')

print(f"БАЙТЫ:\n {decoded_bytes}")
print(f"СООБЩЕНИЕ:\n {message}")