# 凯撒密码穷举破译程序
# 功能：枚举1~25的密钥，解密密文并按指定格式输出

def caesar_decrypt(ciphertext, key):
    """
    凯撒密码解密函数
    :param ciphertext: 待解密的密文字符串（大写）
    :param key: 解密密钥（1~25）
    :return: 解密后的明文字符串
    """
    plaintext = []
    for char in ciphertext:
        # 仅处理大写字母（本题密文无其他字符）
        if 'A' <= char <= 'Z':
            # 字母向前移动key位（加密是向后移，解密反向）
            # 模26保证字母在A-Z范围内循环
            new_char_code = (ord(char) - ord('A') - key) % 26
            new_char = chr(new_char_code + ord('A'))
            plaintext.append(new_char)
        else:
            plaintext.append(char)
    return ''.join(plaintext)

# 实验给定的密文
cipher_text = "NUFECMWBYUJMBIQGYNBYWIXY"

# 枚举1~25的密钥，输出所有解密结果
print("凯撒密码穷举解密结果：")
print("-" * 40)
for k in range(1, 26):
    decrypted_text = caesar_decrypt(cipher_text, k)
    print(f"k={k:2d}  : {decrypted_text}")