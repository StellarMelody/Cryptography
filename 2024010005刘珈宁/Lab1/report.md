# Lab1：穷举法破译凯撒密码 实验报告

## 一、实验目的
 
### 通过凯撒解密函数对给定密文进行暴力破解，找到正确密钥并还原出有意义的明文。
 
## 二、实验过程
 
- 解密函数：使用提供的  caesar_decrypt  函数，它会对密文中的大写字母进行反向位移 k 位，非大写字母保持不变。
- 密文： ciphertext = "NUFECMWBYUJMBIQGYNBYWIXY" 
- 暴力破解：遍历 k=1 到 k=25，逐一解密并输出结果。

## 三、实验结果分析

1. 全密钥解密输出（部分）
```
k=1: MTEDBLVAXTILAHPFXMAXVHWX 
k=2: LSDCAKUZWSHKZGOEWLZWUGVW 
k=3: KRCBZJTYVRGJYFNDVKYVTFUV 
k=4: JQBAYISXUQFIXEMCUJXUSETU 
k=5: IPAZXHRWTPEHWDLBTIWTRDST 
k=6: HOZYWGQVSODGVCKASHVSQCRS 
k=7: GNYXVFPURNCFUBJZRGURPBQR 
k=8: FMXWUEOTQMBETAIYQFTQOAPQ 
k=9: ELWVTDNSPLADSZHXPESPNZOP 
k=10: DKVUSCMROKZCRYGWODROMYNO 
k=11: CJUTRBLQNJYBQXFVNCQNLXMN 
k=12: BITSQAKPMIXAPWEUMBPMKWLM 
k=13: AHSRPZJOLHWZOVDTLAOLJVKL 
k=14: ZGRQOYINKGVYNUCSKZNKIUJK 
k=15: YFQPNXHMJFUXMTBRJYMJHTIJ 
k=16: XEPOMWGLIETWLSAQIXLIGSHI 
k=17: WDONLVFKHDSVKRZPHWKHFRGH 
k=18: VCNMKUEJGCRUJQYOGVJGEQFG 
k=19: UBMLJTDIFBQTIPXNFUIFDPEF 
k=20: TALKISCHEAPSHOWMETHECODE 
k=21: SZKJHRBGDZORGNVLDSGDBNCD 
K=22: RYJIGQAFCYNQFMUKCRFCAMBC 
K=23: QXIHFPZEBXMPELTJBQEBZLAB 
k=24: PWHGEOYDAWLODKSIAPDAYKZA 
k=25: OVGFDNXCZVKNCJRHZOCZXJYZ
 ```
2. 正确的密钥  k 
```
 k=20 
 ```
3. 解密后的明文
 ```
密文： NUFECMWBYUJMBIQGYNBYWIXY 
解密后明文：TALKISCHEAPSHOWMETHECODE
断句后：TALK IS CHEAP SHOW ME THE CODE
译为:空谈无益，亮出代码。
 ```
4. 判断正确明文的方法
 ```
通过穷举法遍历  k=1  到  k=25 ，逐一解密密文。
只有当  k=20  时，解密结果是有意义的英文句子，符合日常语言逻辑；其他密钥对应的解密结果均为无意义的字母组合，因此判断  k=20  对应的结果为正确明文。
 ```
 ## 四、实验源代码
 ```python
凯撒解密函数：cipher是密文，k是密钥
def caesar_decrypt(cipher, k):
    plaintext = ""
    for char in cipher:
        # 仅处理大写字母
        if char.isupper():
            # 计算解密后的字母（反向移动k位）
            shifted = ord(char) - k
            if shifted < ord('A'):
                shifted += 26  # 循环到字母表末尾
            plaintext += chr(shifted)
        else:
            plaintext += char
    return plaintext

# 密文
ciphertext = "NUFECMWBYUJMBIQGYNBYWIXY"

# 穷举所有密钥k=1到25
for k in range(1, 26):
    result = caesar_decrypt(ciphertext, k)
    print(f"k={k:2d} : {result}")
```
## 五、实验总结
 
### 本次凯撒密码解密实验，我收获了三点核心内容：
 ```
1. 掌握了凯撒密码的原理与Python实现方法，学会用 ord() 、 chr() 处理字符转换。
2. 理解了暴力破解的思路，通过遍历密钥筛选有意义的明文。
3. 锻炼了从大量信息中筛选有效内容的能力，也体会到编程细节的重要性。
```