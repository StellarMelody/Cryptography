cipher = "NUFECMWBYUJMBIQGYNBYWIXY"

print("密钥 | 解密结果")
print("-----+---------------------------")
for key in range(1, 26):
    plain = []
    for c in cipher:
        if c.isalpha():
            shifted = ord(c) - key
            if shifted < ord('A'):
                shifted += 26
            plain.append(chr(shifted))
        else:
            plain.append(c)
    plaintext = ''.join(plain)
    print(f"{key:2d}   | {plaintext}")