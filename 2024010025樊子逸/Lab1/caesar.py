# 凯撒密码穷举破解
cipher = "NUFECMWBYUJMBIQGYNBYWIXY"

print("所有可能的解密结果：")
for k in range(1, 26):
    plain = ""
    for ch in cipher:
        if ch.isalpha():
            # 将大写字母转换为0-25的数字，减去k（解密），再取模26
            shifted = (ord(ch) - ord('A') - k) % 26
            plain += chr(shifted + ord('A'))
        else:
            plain += ch  # 保留非字母字符（本例中没有）
    # 按要求的格式输出：k=数字左对齐占3位，然后冒号和结果
    print(f"k={k:<3}: {plain}")