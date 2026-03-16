cipher = "NUFECMWBYUJMBIQGYNBYWIXY"
print("密文:", cipher)
print("穷举所有可能的密钥（k=1~25）：\n")

for k in range(1, 26):
    plain = ""
    for ch in cipher:
        p = (ord(ch) - ord('A') - k) % 26
        plain += chr(p + ord('A'))
    print(f"k={k:<2}: {plain}")