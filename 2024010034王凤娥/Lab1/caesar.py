# caesar.py
# 穷举法破解凯撒密码
ciphertext = "NUFECMWBYUJMBIQGYNBYWIXY"  # 题目给出的密文

def caesar_decrypt(ciphertext, k):
    """
    凯撒密码解密函数
    :param ciphertext: 密文（大写英文字母）
    :param k: 密钥（偏移量，1~25）
    :return: 解密后的明文
    """
    plaintext = ""
    for c in ciphertext:
        if c.isalpha() and c.isupper():  # 只处理大写字母
            # 将字母转换为 0-25 的数字，解密后再转回字母
            original_pos = ord(c) - ord('A')
            new_pos = (original_pos - k) % 26
            plaintext += chr(new_pos + ord('A'))
        else:
            plaintext += c  # 非字母字符保持不变
    return plaintext

# 穷举所有可能的密钥 k（1~25），并输出结果
print("===== 所有密钥解密结果 =====")
for k in range(1, 26):
    plain = caesar_decrypt(ciphertext, k)
    print(f"k={k:2d} : {plain}")