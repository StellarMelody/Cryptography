def caesar(text, k, decrypt=False):
    """凯撒加解密通用函数"""
    k = -k if decrypt else k
    res = []
    for c in text:
        if c.isupper():
            res.append(chr((ord(c) - ord('A') + k) % 26 + ord('A')))
        elif c.islower():
            res.append(chr((ord(c) - ord('a') + k) % 26 + ord('A')))
        else:
            res.append(c)
    return ''.join(res)

if __name__ == "__main__":
    cipher = "NUFECMWBYUJMBIQGYNBYMWIXY"
    
    print("密文:", cipher)
    print("=" * 50)
    print("穷举所有可能的密钥 k (1~25):\n")
    
    for k in range(1, 26):
        print(f"k={k:2d}: {caesar(cipher, k, decrypt=True)}")
    
    print("=" * 50)
    
    correct_k = 20
    plain = caesar(cipher, correct_k, decrypt=True)
    print(f"\n✅ 正确密钥与明文:")
    print(f"k={correct_k}: {plain}")
    
    # 验证
    verify = caesar(plain, correct_k)
    print(f"\n验证（加密回去）: {verify}")
    print(f"验证结果: {'✓ 正确' if verify == cipher else '✗ 错误'}")