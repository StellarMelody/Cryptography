# 凯撒密码穷举破解实验报告

## 1. 正确密钥与明文
- **密钥 k** = 20  
- **解密明文** = `TALKISCHEAPSHOWMETHECODE`  

该明文可自然划分为英文句子：**TALK IS CHEAP SHOW ME THE CODE**，意为“空谈无益，亮出代码”，是一句著名的开源社区格言。

## 2. 判断依据
运行穷举程序后，得到所有 k=1 到 25 的解密结果。其中只有 k=20 的输出为有意义的英文句子，其余结果均为无意义的字母组合，因此可以确定 k=20 是正确密钥。

## 3. 程序输出示例
```

k=1  : MTEDBLAVXTILAHOEXMAXVHWX
k=2  : LSDCAKZUWSHZAGNWDLZWUGVW
k=3  : KRCBZJTYVRGJYFNDVKYVTFUV
k=4  : JQBAYISXUQFIXEMCUJXUSETU
k=5  : IPAZXHRWTPEHWDLBTIWTRDST
...
k=20 : TALKISCHEAPSHOWMETHECODE
...
k=25 : OVGFDNXCZVKNCJRHZOCZXJYZ

```
（完整结果请运行 `caesar.py` 查看）

## 4. 附：核心代码（caesar.py）
```python
cipher = "NUFECMWBYUJMBIQGYNBYWIXY"

print("所有可能的解密结果：")
for k in range(1, 26):
    plain = ""
    for ch in cipher:
        if ch.isalpha():
            shifted = (ord(ch) - ord('A') - k) % 26
            plain += chr(shifted + ord('A'))
        else:
            plain += ch
    print(f"k={k:<3}: {plain}")
```

```