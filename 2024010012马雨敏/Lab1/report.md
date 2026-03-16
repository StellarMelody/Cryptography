# Lab1：穷举法破译凯撒密码 实验报告

## 一、实验目的
1. 理解凯撒密码的加密与解密原理。
2. 掌握穷举法（暴力破解）在密码分析中的应用。
3. 实现对给定凯撒密文的全密钥范围解密，并识别出有意义的明文。


## 二、实验过程：
1. 初始化密文：定义需要解密的密文字符串。
2. 遍历密钥：使用 for 循环遍历 k=1 到 k=25 的所有可能密钥。
3. 逐字符解密：
- 对密文中的每个大写字母，用 ord() 获取其ASCII码，减去密钥 k 得到解密后的ASCII码。
- 如果结果小于 ord('A') ，则加26实现字母循环（如A向前移1位变为Z）。
- 用 chr() 将解密后的ASCII码转回字符，拼接成明文。
- 非大写字母直接保留。
4. 输出结果：打印每个密钥对应的解密结果


## 三、核心代码实现
### 题目给的密文
ciphertext = "NUFECMWBYUJMBIQGYNBYWIXY"

### 穷举1到25的密钥
```python
for k in range(1, 26):
    plaintext = ""
    for char in ciphertext:
        if char.isupper():
            shifted = ord(char) - k
            if shifted < ord('A'):
                shifted += 26
            plaintext += chr(shifted)
        else:
            plaintext += char
    print(f"k={k:2d} : {plaintext}")
```

## 四、实验结果与分析
1. 全密钥解密输出
```
k= 1 : MTEDBLVAXTILAHPFXMAXVHWX
k= 2 : LSDCAKUZWSHKZGOEWLZWUGVW
k= 3 : KRCBZJTYVRGJYFNDVKYVTFUV
k= 4 : JQBAYISXUQFIXEMCUJXUSETU
k= 5 : IPAZXHRWTPEHWDLBTIWTRDST
k= 6 : HOZYWGQVSODGVCKASHVSQCRS
k= 7 : GNYXVFPURNCFUBJZRGURPBQR
k= 8 : FMXWUEOTQMBETAIYQFTQOAPQ
k= 9 : ELWVTDNSPLADSZHXPESPNZOP
k=10 : DKVUSCMROKZCRYGWODROMYNO
k=11 : CJUTRBLQNJYBQXFVNCQNLXMN
k=12 : BITSQAKPMIXAPWEUMBPMKWLM
k=13 : AHSRPZJOLHWZOVDTLAOLJVKL
k=14 : ZGRQOYINKGVYNUCSKZNKIUJK
k=15 : YFQPNXHMJFUXMTBRJYMJHTIJ
k=16 : XEPOMWGLIETWLSAQIXLIGSHI
k=17 : WDONLVFKHDSVKRZPHWKHFRGH
k=18 : VCNMKUEJGCRUJQYOGVJGEQFG
k=19 : UBMLJTDIFBQTIPXNFUIFDPEF
k=20 : TALKISCHEAPSHOWMETHECODE
k=21 : SZKJHRBGDZORGNVLDSGDBNCD
k=22 : RYJIGQAFCYNQFMUKCRFCAMBC
k=23 : QXIHFPZEBXMPELTJBQEBZLAB
k=24 : PWHGEOYDAWLODKSIAPDAYKZA
k=25 : OVGFDNXCZVKNCJRHZOCZXJYZ
```
2. 正确结果说明
- 正确的密钥 k=20
  解密后明文：TALKISCHEAPSHOWMETHECODE
  断句后：TALK IS CHEAP SHOW ME THE CODE（空谈无益，亮出代码。）

- 判断依据：
1. 凯撒密码解密后，只有 k=20 对应的结果包含可识别的英文单词（如 TALK），符合自然语言特征。
2. 其他密钥对应的解密结果均为无意义的字母组合，不具备可读性，因此可排除。

## 五、实验总结
本次凯撒密码解密实验，我通过暴力破解法遍历密钥，掌握了凯撒密码的移位解密逻辑，熟悉了 ord() 和 chr() 函数的字符转换用法，同时学会了从大量无意义结果中筛选有效明文的方法，也体会到编程细节对结果准确性的影响。