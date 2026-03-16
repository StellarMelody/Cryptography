def caesar_decrypt(ciphertext, k):
    """
    凯撒解密函数
    :param ciphertext: 密文字符串（大写字母）
    :param k: 密钥（移动位数）
    :return: 解密后的明文
    """
    plaintext = ""
    for c in ciphertext:
        if c.isalpha():
            original_pos = ord(c) - ord('A')
            new_pos = (original_pos - k) % 26
            plaintext += chr(new_pos + ord('A'))
        else:
            plaintext += c
    return plaintext
cipher = "NUFECMWBYUJMBIQGYNBYWIXY"
print("穷举破解凯撒密码结果：")
for k in range(1, 26):
    result = caesar_decrypt(cipher, k)
    print(f"k={k:<2d} : {result}")
