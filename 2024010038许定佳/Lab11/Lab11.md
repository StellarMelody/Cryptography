# Lab11：数字签名 —— 验证消息的真实性与完整性

## 实验简介

### 从哈希函数到数字签名

在前面的实验中，你已经学习了：

- **对称加密**（Lab1-Lab4）：使用相同的密钥进行加密和解密，适合大量数据的快速加密
- **非对称加密**（Lab5-Lab8）：使用公钥加密、私钥解密，解决了密钥分发问题
- **哈希函数**（Lab9）：将任意长度的数据映射为固定长度的摘要，具有单向性和抗碰撞性
- **公钥密码学应用**（Lab10）：RSA、ElGamal 等公钥加密系统的原理和实现

这些都是密码学的基础工具。但它们单独使用时，都有各自的局限：

- **对称加密**能保证机密性，但无法证明发送者身份
- **非对称密码学**可以用私钥生成签名来证明身份，但直接对大文件使用非对称运算效率太低
- **哈希函数**能检测数据是否被篡改，但无法证明哈希值本身是谁计算的

**数字签名**就是将这些工具组合起来，解决一个核心问题：**如何在不安全的网络中，让接收者确信一条消息确实来自声称的发送者，且内容未被篡改？**

### 数字签名解决的问题

想象以下场景：

**场景一：软件发布**
你从网上下载了一个软件安装包。网站上提供了文件的 SHA-256 哈希值。你下载后计算哈希，发现和网站上的一致。但问题来了：**网站本身可能被黑客入侵，哈希值也被替换了**。你如何确认这个哈希值确实是软件开发者发布的，而不是攻击者伪造的？

**场景二：电子邮件**
你收到一封"来自老板"的邮件，要求立即转账。邮件地址看起来很像老板的邮箱。但你如何确认这封邮件真的是老板发的，而不是钓鱼邮件？

**场景三：代码提交**
开源项目中，有人提交了一个 Pull Request。代码看起来没问题，但你如何确认这个提交真的来自声称的开发者，而不是有人冒用了他的 GitHub 账号？

这些场景的共同点是：**你需要验证消息的来源和完整性**。数字签名提供了这种能力。

### 数字签名的三大保证

数字签名技术提供了三个关键保证：

1. **身份认证（Authentication）**
   - 证明消息确实来自持有私钥的发送者
   - 就像手写签名证明文件是你本人签署的

2. **完整性保护（Integrity）**
   - 确保消息在传输过程中未被篡改
   - 任何微小的修改都会导致签名验证失败

3. **不可否认性（Non-repudiation）**
   - 发送者无法否认自己发送过该消息
   - 因为只有他持有生成签名所需的私钥

### Lab11 的目标

本次实验将带你深入理解数字签名的工作原理，并通过实际操作掌握"先加密、再对密文签名、验证后解密"的完整流程。

完成本实验后，你应该能够：

1. **理解数字签名的数学原理**：为什么"先哈希后签名"是必要的？哈希函数在签名中扮演什么角色？
2. **掌握加密后签名的完整流程**：从密钥生成、消息加密、密文哈希、密文签名到签名验证和解密的每一步操作
3. **理解签名的安全性**：为什么签名能防止篡改？为什么签名能证明身份？什么情况下签名会失效？
4. **理解 RSA 加密与数字签名的异同**：通过同一个消息文件串联加密、签名、验证和解密，区分"保密性"与"身份认证/完整性保护"
5. **理解签名在实际系统中的应用**：软件签名、代码签名、数字证书等场景

> **说明**：本实验使用 OpenSSL 工具，推荐在 Linux 或 macOS 环境下完成。Windows 用户可以使用 WSL 或 Git Bash。

---

## 数字签名的核心原理

在动手之前，先把数字签名的关键概念理解透彻。

### 数字签名 vs 手写签名

手写签名的特点：

- **固定不变**：同一个人的签名基本一致
- **难以伪造**：每个人的笔迹特征独特
- **绑定文件**：签名直接写在文件上，和文件内容物理绑定

但手写签名有个致命问题：**可以复制**。如果你在一份合同上签了名，别人可以扫描这个签名，粘贴到另一份你从未见过的合同上。

数字签名解决了这个问题：

- **签名和消息绑定**：签名是针对特定消息内容计算出来的，无法"复制粘贴"到其他消息上
- **不可伪造**：只有持有私钥的人才能生成有效签名
- **可验证**：任何人都可以用公钥验证签名的有效性

### 数字签名的基本流程

数字签名最基本的对象是"一段数据"。这段数据可以是明文消息，也可以是密文、软件安装包、代码提交或证书内容。本实验为了同时理解加密和签名，会先把明文加密成密文，再对密文进行哈希和签名。

#### 签名生成（发送方）

```text
待签名数据（本实验中是密文）
   ↓
计算哈希值（SHA-256）
   ↓
用签名私钥对哈希值签名
   ↓
得到数字签名
   ↓
发送：待签名数据 + 签名
```

#### 签名验证（接收方）

```text
收到：待签名数据 + 签名
   ↓
路径1：计算接收到的数据的哈希值 → 哈希值A
   ↓
路径2：用签名公钥验证签名 → 哈希值B
   ↓
比较哈希值A 和 哈希值B
   ↓
相同？ → 验证通过 ✓
不同？ → 验证失败 ✗（数据被篡改或签名伪造）
```

本实验中的完整顺序是：

```text
明文 message.txt
   ↓
用加密公钥加密 → encrypted_message.bin
   ↓
计算密文哈希
   ↓
用签名私钥对密文哈希签名 → signature.bin
   ↓
接收方先验证密文签名
   ↓
验证通过后，用加密私钥解密密文
```

### 为什么要先计算哈希值？

你可能会问：既然 RSA 签名本质上也是用私钥做数学运算，为什么不直接对整个消息或密文进行 RSA 运算作为签名？

原因有三个：

**1. 效率问题**

RSA 等非对称加密算法的运算速度远低于对称加密。对一个 1GB 的文件进行 RSA 运算是不现实的。

而哈希函数的计算速度很快，无论文件多大，都能快速生成固定长度的哈希值（例如 SHA-256 输出 256 位）。然后只需要对这 256 位进行 RSA 签名即可。

| 操作对象 | 大小 | RSA 签名耗时 |
| :------- | :--- | :---------- |
| 直接对 1GB 文件签名 | 1GB | 不可行 |
| 先计算 SHA-256，对哈希值签名 | 256 位（32 字节） | 毫秒级 |

**2. 输入长度问题**

RSA 一次只能处理不超过模数长度的数据块，签名标准也不是为直接处理任意长度文件设计的。先计算哈希值，可以把任意大小的文件压缩成固定长度摘要，再对摘要进行签名。

**3. 标准化问题**

哈希值是固定长度的，这使得签名算法的接口统一、简洁。无论消息是 1KB 还是 1GB，签名的输入都是固定的哈希值。

### RSA 签名的数学原理

回顾 RSA 加密的基本原理：

- **密钥生成**：选择两个大素数 $p$ 和 $q$，计算 $N = p \times q$，选择公钥指数 $e$ 和私钥指数 $d$，满足 $e \times d \equiv 1 \pmod{\varphi(N)}$
- **加密**：密文 $c = m^e \bmod N$
- **解密**：明文 $m = c^d \bmod N$

RSA 签名利用了 RSA 的**可逆性**：

- **签名**：签名 $\sigma = H(m)^d \bmod N$（用私钥 $d$）
- **验证**：计算 $\sigma^e \bmod N$，应该等于 $H(m)$（用公钥 $e$）

关键点：

1. **只有持有私钥 $d$ 的人才能计算 $\sigma = H(m)^d \bmod N$**
2. **任何人都可以用公钥 $e$ 验证：$\sigma^e \bmod N = H(m)$**
3. **如果消息被篡改**，$H(m)$ 改变，$\sigma^e \bmod N$ 就不会等于新的 $H(m')$，验证失败

### 为什么签名能防止篡改？

假设攻击者想要篡改消息：

**场景：修改消息内容**

1. Alice 发送消息 $m_1$："转账 100 元" + 签名 $\sigma_1 = H(m_1)^d \bmod N$
2. 攻击者截获后，想改成 $m_2$："转账 10000 元"
3. 攻击者把消息改为 $m_2$，但签名 $\sigma_1$ 还是原来的
4. Bob 收到后验证：$\sigma_1^e \bmod N = H(m_1)$，但现在消息是 $m_2$，$H(m_2) \ne H(m_1)$
5. 验证失败！Bob 发现消息被篡改

**场景：伪造签名**

1. 攻击者想为消息 $m_2$ 生成签名 $\sigma_2 = H(m_2)^d \bmod N$
2. 但攻击者没有私钥 $d$，无法计算 $H(m_2)^d \bmod N$
3. 攻击者试图暴力破解私钥 $d$？对于 2048 位 RSA，这需要数十亿年
4. 攻击者无法伪造签名

本实验中，签名对象不是明文消息，而是 `encrypted_message.bin`。把上面例子里的"消息"替换成"密文"，验证逻辑完全相同：密文一旦被篡改，签名验证就会失败。

### 哈希函数在签名中的关键作用

哈希函数必须满足三个性质，才能保证签名的安全：

**1. 抗原像性（Preimage Resistance）**

给定哈希值 $h$，找到满足 $H(m) = h$ 的消息 $m$ 在计算上不可行。

- **对签名的意义**：攻击者即使知道签名 $\sigma = H(m)^d \bmod N$，也无法反推出原始消息 $m$

**2. 抗第二原像性（Second Preimage Resistance）**

给定消息 $m_1$，找到另一个消息 $m_2 \ne m_1$ 使得 $H(m_1) = H(m_2)$ 在计算上不可行。

- **对签名的意义**：攻击者无法找到另一个消息 $m_2$，使得它的哈希值和原消息 $m_1$ 相同，从而重用签名

**3. 抗碰撞性（Collision Resistance）**

找到任意两个不同的消息 $m_1 \ne m_2$ 使得 $H(m_1) = H(m_2)$ 在计算上不可行。

- **对签名的意义**：攻击者无法事先准备两个内容不同但哈希值相同的消息，然后用其中一个签名，替换为另一个

### 为什么 SHA-1 不再安全？

SHA-1 曾经被广泛用于文件校验和数字签名，但它已经不再适合安全场景。2017 年，Google 和 CWI Amsterdam 公开了 SHA-1 碰撞攻击：攻击者可以构造两个内容不同、但 SHA-1 哈希值相同的文件。

这对数字签名非常危险。假设攻击者准备了两个文件：

1. 文件 A：看起来正常、愿意让别人签名的内容
2. 文件 B：攻击者真正想替换进去的恶意内容

如果两个文件的 SHA-1 哈希值相同，那么对文件 A 的签名也可能被拿去验证文件 B。也就是说，签名者以为自己签的是 A，验证者却可能看到 B 也能通过验证。

因此，现代数字签名不应使用 SHA-1。本实验使用 SHA-256。

### 常见的数字签名算法

| 算法 | 基础 | 签名长度 | 特点 |
| :--- | :--- | :------ | :--- |
| **RSA 签名** | RSA 公钥系统 | 与密钥长度相同（2048 位密钥 → 256 字节签名） | 最广泛使用，签名和验证速度适中 |
| **ECDSA** | 椭圆曲线密码学 | 较短（256 位曲线 → 64 字节签名） | 签名更短，验证较快，广泛用于区块链 |
| **EdDSA** | Edwards 曲线 | 64 字节（Ed25519） | 签名速度快，安全性高，抗侧信道攻击 |
| **DSA** | 离散对数 | 40-64 字节 | 已过时，不推荐使用 |

本实验主要使用 **RSA 签名**，因为它最容易理解，也最广泛使用。

---

## 实验环境准备

### 检查 OpenSSL 版本

OpenSSL 是一个强大的密码学工具库，提供了完整的数字签名功能。

检查你的系统是否已安装 OpenSSL：

```bash
openssl version
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `openssl` | OpenSSL 命令行工具 |
| `version` | 显示当前安装的 OpenSSL 版本 |

期望输出类似：

```
OpenSSL 3.0.2 15 Mar 2022 (Library: OpenSSL 3.0.2 15 Mar 2022)
```

或者：

```
OpenSSL 1.1.1s  1 Nov 2022
```

如果提示 `command not found`，需要安装 OpenSSL：

**Ubuntu/Debian**：
```bash
sudo apt update
sudo apt install openssl
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `sudo apt update` | 更新软件包索引 |
| `sudo apt install openssl` | 安装 OpenSSL 命令行工具 |

**macOS**（通常已预装）：
```bash
brew install openssl
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `brew install openssl` | 使用 Homebrew 安装 OpenSSL |

**Windows**（使用 Git Bash 或 WSL）：
Git Bash 通常已包含 OpenSSL。如果没有，可以通过 WSL 安装 Ubuntu 后再安装 OpenSSL。

### 创建实验目录

建议创建一个专门的目录来存放本次实验的所有文件：

```bash
mkdir -p ~/cryptography-lab11
cd ~/cryptography-lab11
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `mkdir -p` | 创建目录，`-p` 参数表示如果父目录不存在则一并创建 |
| `~/cryptography-lab11` | 在用户主目录下创建 `cryptography-lab11` 目录 |
| `cd` | 切换到该目录 |

### 清理残留文件（可选）

如果你之前做过本实验或中途出错需要重来，可以清理所有生成的文件：

```bash
rm -f signature_private_key.pem signature_public_key.pem encryption_private_key.pem encryption_public_key.pem message.txt signature.bin encrypted_message.bin tampered_encrypted_message.bin decrypted_message.txt
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `rm -f` | 强制删除文件，即使文件不存在也不报错 |
| `signature_private_key.pem` / `signature_public_key.pem` | 签名密钥文件 |
| `encryption_private_key.pem` / `encryption_public_key.pem` | 加密密钥文件 |
| 其他文件名 | 本实验过程中生成的消息、签名、密文和解密结果 |

---

## 任务一：生成签名密钥对和加密密钥对

本实验需要两对 RSA 密钥：

| 密钥对 | 私钥用途 | 公钥用途 |
| :----- | :------- | :------- |
| 签名密钥对 | 生成数字签名 | 验证数字签名 |
| 加密密钥对 | 解密密文 | 加密明文 |

实际系统中通常会区分签名密钥和加密密钥。本实验也采用这种方式，避免把同一对密钥混用于不同安全目标。

### 第一步：生成签名私钥

执行命令：

```bash
openssl genrsa -out signature_private_key.pem 2048
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `openssl` | OpenSSL 命令行工具 |
| `genrsa` | 生成 RSA 密钥对 |
| `-out signature_private_key.pem` | 输出文件名为 `signature_private_key.pem` |
| `2048` | 密钥长度为 2048 位 |

OpenSSL 版本不同，输出可能不同。有些版本没有任何输出，有些版本会显示类似下面的生成过程：

```
Generating RSA private key, 2048 bit long modulus (2 primes)
....................+++++
.............................+++++
e is 65537 (0x010001)
```

输出说明：

| 部分 | 含义 |
| :--- | :--- |
| `2048 bit long modulus` | 模数 N 的长度是 2048 位 |
| `+++++` | 生成过程中的进度指示 |
| `e is 65537` | 公钥指数 e 的值是 65537（常用值） |

生成的 `signature_private_key.pem` 文件包含了完整的 RSA 私钥信息，包括：
- 模数 N
- 公钥指数 e
- 私钥指数 d
- 素数 p 和 q
- 以及一些优化计算用的参数

### 第二步：查看私钥内容

执行命令：

```bash
openssl rsa -in signature_private_key.pem -text -noout
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `rsa` | RSA 密钥管理命令 |
| `-in signature_private_key.pem` | 输入文件 |
| `-text` | 以文本格式显示密钥详细信息 |
| `-noout` | 不输出编码后的密钥（只显示文本信息） |

期望输出（部分）：

```
Private-Key: (2048 bit, 2 primes)
modulus:
    00:c4:7e:3b:a1:2f:5d:8c:9e:f1:23:45:67:89:ab:
    cd:ef:01:23:45:67:89:ab:cd:ef:...（很长的十六进制数）
publicExponent: 65537 (0x10001)
privateExponent:
    00:8f:23:45:67:89:ab:cd:ef:01:23:45:67:89:ab:
    cd:ef:...（很长的十六进制数）
prime1:
    00:f1:23:45:67:89:ab:cd:ef:...（素数 p）
prime2:
    00:e9:87:65:43:21:ab:cd:ef:...（素数 q）
exponent1:
    00:d3:45:67:89:ab:cd:ef:...
exponent2:
    00:c7:65:43:21:fe:dc:ba:...
coefficient:
    00:b9:87:65:43:21:ab:cd:...
```

输出说明：

| 字段 | 含义 |
| :--- | :--- |
| `modulus` | RSA 模数 $N = p \times q$ |
| `publicExponent` | 公钥指数 $e$，通常是 65537 |
| `privateExponent` | 私钥指数 $d$，满足 $e \times d \equiv 1 \pmod{\varphi(N)}$ |
| `prime1` / `prime2` | 两个大素数 $p$ 和 $q$ |
| `exponent1` / `exponent2` | 用于中国剩余定理优化的参数 |
| `coefficient` | 用于中国剩余定理的系数 |

**重要提示**：私钥文件包含了所有敏感信息，**绝对不能泄露**！如果私钥泄露，任何人都可以伪造你的签名。

### 第三步：从签名私钥中提取签名公钥

签名公钥是可以公开分享的，用于验证签名。执行命令：

```bash
openssl rsa -in signature_private_key.pem -pubout -out signature_public_key.pem
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `-in signature_private_key.pem` | 从私钥文件读取 |
| `-pubout` | 输出公钥 |
| `-out signature_public_key.pem` | 输出到 `signature_public_key.pem` 文件 |

期望输出：

```
writing RSA key
```

### 第四步：查看公钥内容

执行命令：

```bash
openssl rsa -pubin -in signature_public_key.pem -text -noout
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `-pubin` | 输入的是公钥文件（不是私钥） |
| `-in signature_public_key.pem` | 输入文件 |
| `-text` | 以文本格式显示 |
| `-noout` | 不输出编码后的密钥 |

期望输出：

```
Public-Key: (2048 bit)
Modulus:
    00:c4:7e:3b:a1:2f:5d:8c:9e:f1:23:45:67:89:ab:
    cd:ef:01:23:45:67:89:ab:cd:ef:...（和私钥中的 modulus 相同）
Exponent: 65537 (0x10001)
```

输出说明：

公钥只包含两个信息：
- **Modulus（模数 N）**：和私钥中的模数相同
- **Exponent（公钥指数 e）**：通常是 65537

公钥可以安全地公开，不会泄露私钥信息。

### 第五步：比较签名密钥文件大小

执行命令：

```bash
ls -lh signature_private_key.pem signature_public_key.pem
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `ls -lh` | 以易读格式显示文件大小和权限 |
| `signature_private_key.pem` | 签名私钥文件 |
| `signature_public_key.pem` | 签名公钥文件 |

期望输出类似：

```
-rw------- 1 user user 1.7K Jun 22 10:30 signature_private_key.pem
-rw-r--r-- 1 user user  451 Jun 22 10:31 signature_public_key.pem
```

观察：
- 私钥文件大约 1.7KB（包含 N, e, d, p, q 等完整信息）
- 公钥文件大约 451 字节（只包含 N 和 e）
- 私钥文件的权限是 `600`（只有所有者可读写），公钥是 `644`（所有人可读）

### 第六步：生成加密专用 RSA 密钥对

生成加密专用私钥：

```bash
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out encryption_private_key.pem
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `genpkey` | 生成通用公钥算法密钥 |
| `-algorithm RSA` | 指定生成 RSA 密钥 |
| `-pkeyopt rsa_keygen_bits:2048` | 设置密钥长度为 2048 位 |
| `-out encryption_private_key.pem` | 输出加密专用私钥文件 |

从加密专用私钥中提取加密公钥：

```bash
openssl rsa -in encryption_private_key.pem -pubout -out encryption_public_key.pem
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `rsa` | RSA 密钥管理命令 |
| `-in encryption_private_key.pem` | 输入加密私钥文件 |
| `-pubout` | 从私钥中导出公钥 |
| `-out encryption_public_key.pem` | 输出加密公钥文件 |

查看文件大小：

```bash
ls -lh encryption_private_key.pem encryption_public_key.pem
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `ls -lh` | 以易读格式显示文件大小和权限 |
| `encryption_private_key.pem` | 加密私钥文件 |
| `encryption_public_key.pem` | 加密公钥文件 |

这对密钥只用于后续的 RSA 加密和解密，不用于数字签名。

### 任务一小结

完成这一步后，你应该有：
- ✅ `signature_private_key.pem` - RSA 签名私钥（保密）
- ✅ `signature_public_key.pem` - RSA 签名公钥（可公开）
- ✅ `encryption_private_key.pem` - RSA 加密私钥（保密）
- ✅ `encryption_public_key.pem` - RSA 加密公钥（可公开）

**截图要求**：
请对"生成签名密钥和加密密钥"的完整过程截图，截图应包含：
1. `openssl genrsa` 命令，以及随后能看到 `signature_private_key.pem` 已生成的结果
2. `openssl rsa -pubout` 命令提取公钥
3. `openssl rsa -pubin -text -noout` 显示公钥详情
4. 生成加密专用密钥对并查看文件大小

截图：

![生成密钥对](keygen.png)

---

## 任务二：创建消息并使用 RSA 加密文件

现在我们先模拟发送方保护消息内容：创建明文文件，然后用接收方的加密公钥把它加密成密文。

注意：RSA 只能直接加密较短的数据。本实验的 `message.txt` 很短，可以直接用 RSA-OAEP 加密；真实系统通常使用混合加密。

### 第一步：创建测试消息

创建一个测试文件 `message.txt`：

```bash
echo "这是一条重要消息，需要签名保护。发送者：张三，学号：2024010001" > message.txt
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `echo "..."` | 输出引号中的测试消息 |
| `>` | 将输出写入文件，会覆盖同名旧文件 |
| `message.txt` | 保存原始明文消息的文件 |

> **提示**：建议在消息中包含你自己的姓名和学号，便于解密后确认消息内容来自你的实验。

查看文件内容：

```bash
cat message.txt
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `cat` | 显示文件内容 |
| `message.txt` | 要查看的原始明文文件 |

期望输出：

```
这是一条重要消息，需要签名保护。发送者：张三，学号：2024010001
```

### 第二步：使用加密公钥加密消息

使用加密公钥 `encryption_public_key.pem` 加密 `message.txt`：

```bash
openssl pkeyutl -encrypt -pubin -inkey encryption_public_key.pem -in message.txt -out encrypted_message.bin -pkeyopt rsa_padding_mode:oaep
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `pkeyutl -encrypt` | 使用公钥算法执行加密操作 |
| `-pubin -inkey encryption_public_key.pem` | 输入的是加密公钥文件 |
| `-in message.txt` | 要加密的原始消息 |
| `-out encrypted_message.bin` | 输出密文文件 |
| `-pkeyopt rsa_padding_mode:oaep` | 使用 OAEP 填充，避免裸 RSA 加密 |

### 第三步：查看密文文件

查看密文文件大小：

```bash
ls -lh encrypted_message.bin
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `ls -lh` | 以易读格式显示文件大小和权限 |
| `encrypted_message.bin` | 要查看的密文文件 |

对于 2048 位 RSA 密钥，密文长度通常是 256 字节，因为 RSA 运算结果的长度等于模数 $N$ 的长度。

尝试直接查看密文：

```bash
xxd encrypted_message.bin | head -2
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `xxd encrypted_message.bin` | 以十六进制形式显示密文文件 |
| `head -2` | 只显示前 2 行输出 |
| `|` | 将前一个命令的输出传给后一个命令 |

期望输出类似：

```
00000000: 8f23 4567 89ab cdef 0123 4567 89ab cdef  .#Eg.....#Eg....
00000010: fedc ba98 7654 3210 0123 4567 89ab cdef  .....T2..#Eg....
```

你会看到一段不可读的二进制数据。密文的作用是隐藏消息内容，不能直接看出原始消息。

### 任务二小结

完成这一步后，你应该有：
- ✅ `message.txt` - 原始消息
- ✅ `encrypted_message.bin` - 加密后的密文

**截图要求**：
请对以下操作截图：
1. 创建并查看 `message.txt`
2. 使用 `encryption_public_key.pem` 加密消息
3. 查看 `encrypted_message.bin` 的大小和十六进制内容

截图：

![RSA加密](encrypt.png)

---

## 任务三：对密文计算哈希并生成数字签名

发送方现在已经有了密文 `encrypted_message.bin`。接下来不要签名明文，而是对密文计算哈希并生成签名。这样接收方可以先验证密文是否来自发送方、是否被篡改，再决定是否解密。

### 第一步：计算密文的哈希值

使用 SHA-256 计算密文哈希：

```bash
openssl dgst -sha256 encrypted_message.bin
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `dgst` | 摘要（digest）计算命令 |
| `-sha256` | 使用 SHA-256 哈希算法 |
| `encrypted_message.bin` | 输入文件是密文 |

期望输出类似：

```
SHA256(encrypted_message.bin)= a7f4c92e8b1234567890abcdef1234567890abcdef1234567890abcdef123456
```

> 不同 OpenSSL 版本可能显示为 `SHA2-256(encrypted_message.bin)= ...`，含义相同。

**重要观察**：
- 哈希值绑定的是密文内容，而不是明文内容
- 只要密文改动 1 个字节，哈希值就会完全不同

### 第二步：使用签名私钥对密文签名

使用签名私钥 `signature_private_key.pem` 对 `encrypted_message.bin` 生成签名：

```bash
openssl dgst -sha256 -sign signature_private_key.pem -out signature.bin encrypted_message.bin
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `dgst -sha256` | 先计算 SHA-256 哈希值 |
| `-sign signature_private_key.pem` | 使用签名私钥对哈希值签名 |
| `-out signature.bin` | 签名输出到 `signature.bin` 文件 |
| `encrypted_message.bin` | 要签名的密文文件 |

这个命令执行了什么？

1. 读取 `encrypted_message.bin` 的内容
2. 计算 SHA-256 哈希值
3. 用签名私钥对哈希值进行 RSA 签名：$\sigma = H(\text{encrypted\_message})^d \bmod N$
4. 将签名写入 `signature.bin`

### 第三步：查看签名文件

```bash
ls -lh signature.bin
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `ls -lh` | 以易读格式显示文件大小和权限 |
| `signature.bin` | 要查看的数字签名文件 |

期望输出：

```
-rw-r--r-- 1 user user 256 Jun 22 10:35 signature.bin
```

观察：
- 签名文件大小是 **256 字节**
- 签名长度由签名 RSA 密钥长度决定
- 签名不是密文，也不能用于恢复明文

### 任务三小结

完成这一步后，你应该有：
- ✅ `encrypted_message.bin` - 要发送的密文
- ✅ `signature.bin` - 对密文生成的数字签名

**截图要求**：
请对以下操作截图：
1. 计算密文的 SHA-256 哈希值（`openssl dgst -sha256 encrypted_message.bin`）
2. 生成密文签名（`openssl dgst -sha256 -sign ... encrypted_message.bin`）
3. 查看签名文件大小（`ls -lh signature.bin`）

截图：

![计算密文哈希值](hash.png)

![生成密文签名](sign.png)

---

## 任务四：验证密文签名并解密

接收方收到的是 `encrypted_message.bin` 和 `signature.bin`。正确处理顺序是：**先验证签名，再解密密文**。如果签名验证失败，不应继续解密或信任该密文。

### 第一步：验证密文签名

使用签名公钥 `signature_public_key.pem` 验证 `encrypted_message.bin` 的签名：

```bash
openssl dgst -sha256 -verify signature_public_key.pem -signature signature.bin encrypted_message.bin
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `dgst -sha256` | 使用 SHA-256 哈希算法 |
| `-verify signature_public_key.pem` | 使用签名公钥验证签名 |
| `-signature signature.bin` | 输入签名文件 |
| `encrypted_message.bin` | 被验证的是密文文件 |

期望输出：

```
Verified OK
```

这证明：
- 密文确实由对应签名私钥签名
- 密文内容在传输过程中没有被篡改

截图：

![验证密文签名成功](verify_ok.png)

### 第二步：测试密文被篡改后的验证结果

先复制一份密文：

```bash
cp encrypted_message.bin tampered_encrypted_message.bin
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `cp encrypted_message.bin tampered_encrypted_message.bin` | 复制一份密文用于篡改测试 |

再向复制出的密文末尾追加 1 个字节：

```bash
printf 'x' >> tampered_encrypted_message.bin
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `printf 'x'` | 输出一个字符 `x` |
| `>> tampered_encrypted_message.bin` | 将字符追加到篡改后的密文文件末尾 |

用原签名验证被篡改的密文：

```bash
openssl dgst -sha256 -verify signature_public_key.pem -signature signature.bin tampered_encrypted_message.bin
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `dgst -sha256` | 对被验证文件计算 SHA-256 哈希 |
| `-verify signature_public_key.pem` | 使用签名公钥验证签名 |
| `-signature signature.bin` | 使用原始密文对应的签名 |
| `tampered_encrypted_message.bin` | 被篡改后的密文文件 |

期望输出：

```
Verification failure
```

这证明：签名绑定的是密文内容。密文只要发生变化，验证就会失败。

截图：

![验证密文签名失败](verify_fail.png)

### 第三步：验证通过后解密密文

使用加密私钥 `encryption_private_key.pem` 解密原始密文：

```bash
openssl pkeyutl -decrypt -inkey encryption_private_key.pem -in encrypted_message.bin -out decrypted_message.txt -pkeyopt rsa_padding_mode:oaep
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `pkeyutl -decrypt` | 使用公钥算法执行解密操作 |
| `-inkey encryption_private_key.pem` | 使用加密私钥解密 |
| `-in encrypted_message.bin` | 输入原始密文文件 |
| `-out decrypted_message.txt` | 输出解密后的明文文件 |
| `-pkeyopt rsa_padding_mode:oaep` | 使用与加密时一致的 OAEP 填充模式 |

查看解密结果：

```bash
cat decrypted_message.txt
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `cat` | 显示文件内容 |
| `decrypted_message.txt` | 解密后得到的明文文件 |

比较原始明文和解密结果是否一致：

```bash
cmp message.txt decrypted_message.txt && echo "解密结果一致"
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `cmp message.txt decrypted_message.txt` | 比较原始明文和解密结果是否完全一致 |
| `&&` | 前一个命令成功时才执行后一个命令 |
| `echo "解密结果一致"` | 两个文件一致时输出提示 |

期望输出：

```
解密结果一致
```

### 第四步：观察完整流程中的文件

```bash
ls -lh message.txt encrypted_message.bin signature.bin decrypted_message.txt
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `ls -lh` | 以易读格式显示文件大小和权限 |
| `message.txt` | 原始明文文件 |
| `encrypted_message.bin` | RSA 加密后的密文 |
| `signature.bin` | 对密文生成的数字签名 |
| `decrypted_message.txt` | 解密后得到的明文 |

观察：

| 文件 | 含义 | 作用 |
| :--- | :--- | :--- |
| `message.txt` | 原始明文 | 发送前的消息 |
| `encrypted_message.bin` | 密文 | 保护消息内容 |
| `signature.bin` | 密文签名 | 证明密文来源并检测篡改 |
| `decrypted_message.txt` | 解密后的明文 | 接收方恢复出的消息 |

### 任务四小结

完成这一步后，你应该理解：
- ✅ 发送方流程：加密明文 -> 计算密文哈希 -> 对密文签名
- ✅ 接收方流程：验证密文签名 -> 解密密文
- ✅ 验证签名解决来源和完整性问题
- ✅ 解密解决内容保密问题

截图：

![解密密文](decrypt.png)

---

## 实验报告要求

### 截图要求

实验截图须清晰，终端文字可读，文件格式必须为 PNG。截图文件需与本 `Lab11.md` 放在同一目录下，并保证它们能在上方对应任务位置正常显示。只需提交以下 7 张实验截图：

| 截图内容 | 文件名 |
| :------- | :----- |
| 生成签名密钥对和加密密钥对 | `keygen.png` |
| 创建消息并使用 RSA 加密 | `encrypt.png` |
| 计算密文哈希值 | `hash.png` |
| 生成密文数字签名并查看签名文件大小 | `sign.png` |
| 验证签名成功 | `verify_ok.png` |
| 篡改密文后验证失败 | `verify_fail.png` |
| 验证通过后解密密文 | `decrypt.png` |

截图的正确放置位置：

1. `keygen.png`：放在任务一末尾，能看到生成签名密钥对和加密密钥对的过程。
2. `encrypt.png`：放在任务二末尾，能看到创建 `message.txt`、加密生成 `encrypted_message.bin`、查看密文的过程。
3. `hash.png`：放在任务三末尾，能看到 `openssl dgst -sha256 encrypted_message.bin` 的输出。
4. `sign.png`：放在任务三末尾，能看到生成密文签名和查看 `signature.bin` 文件大小。
5. `verify_ok.png`：放在任务四末尾，能看到密文签名验证成功的 `Verified OK`。
6. `verify_fail.png`：放在任务四末尾，能看到密文被篡改后的 `Verification failure`。
7. `decrypt.png`：放在任务四末尾，能看到验证通过后解密密文，并比较解密结果和原始明文一致。

除 `Lab11.md` 和上述截图外，其他实验过程中生成的文件都不需要提交。

---

## 实验结果填写

> 根据你的实验结果填写下表。若某项在截图中看不清，可写"截图中未见"，但不得留空。

### A. 密钥信息

| 项目 | 你的结果 |
| :--- | :------- |
| 签名 RSA 密钥长度（位） | 2048 位|
| 签名私钥 `signature_private_key.pem` 文件大小（字节） | 1976 字节|
| 签名公钥 `signature_public_key.pem` 文件大小（字节） |460 字节 |
| 签名公钥指数 e 的值 | 65537（十六进制 0x10001）|
| 签名公钥模数 N 的前 16 位十六进制 | 00c421c1f198720c|
| 加密私钥 `encryption_private_key.pem` 文件大小（字节） |1976 字节 |
| 加密公钥 `encryption_public_key.pem` 文件大小（字节） | 460 字节|

---

### B. 加密与密文哈希

| 项目 | 你的结果 |
| :--- | :------- |
| 原始消息内容（你写入的文字） | 这是一条重要消息，需要签名保护。发送者：马雨敏，学号：2024010012|
| 密文文件 encrypted_message.bin 大小（字节） |256 字节 |
| 密文 SHA-256 哈希值（完整的 64 位十六进制） | d41ac8f0606edef10af3c803e892104b885c93dd5c588db12997d7e39140fd8e|
| 密文 SHA-256 哈希值长度（十六进制字符数） |64 个字符 |

---

### C. 密文签名与验证

| 项目 | 你的结果 |
| :--- | :------- |
| 签名文件 signature.bin 大小（字节） |256 字节 |
| 原始密文的签名验证结果 | Verified OK（验证成功）|
| 篡改密文后的签名验证结果 |Verification failure（验证失败，bad signature） |

---

### D. 解密与流程理解

| 项目 | 你的结果 |
| :--- | :------- |
| 解密后的文件是否与原文件一致 |是，解密结果一致 |
| 加密操作使用的密钥文件 |encryption_public_key.pem（加密公钥） |
| 解密操作使用的密钥文件 | encryption_private_key.pem（加密私钥）|
| 签名操作使用的密钥文件 | signature_private_key.pem（签名私钥）|
| 验证签名操作使用的密钥文件 |signature_public_key.pem（签名公钥） |
| 接收方应先验证签名还是先解密 |先验证签名，再解密（防止收到篡改、恶意密文，避免无效解密运算） |

---

## 思考题

请根据实验过程和你的理解，回答以下问题。

### 1. 数字签名的三大保证

数字签名提供了哪三个关键保证？请分别解释它们的含义，并结合本次实验说明这三个保证是如何实现的。

> 答：三大特性：完整性、身份认证（真实性）、不可否认性
完整性
含义：确保消息在传输过程中没有被篡改、增删、修改。
实验体现：篡改encrypted_message.bin后，签名校验输出Verification failure；原始密文校验返回Verified OK，证明一旦文件改动，签名验证失败，检测出篡改。
身份认证（真实性）
含义：确认消息发送方身份，证明签名确实由对应私钥持有者生成，不是第三方伪造。
实验体现：只有持有signature_private_key.pem签名私钥才能生成合法签名；接收方使用配套公钥signature_public_key.pem验证，确认密文签名由对应发送方产生。
不可否认性
含义：发送方事后无法否认自己发送过该消息、生成过该签名。
实验体现：私钥仅发送方独有，签名由私钥唯一生成；第三方可通过公钥核验归属，发送方无法抵赖发送行为。

---

### 2. 为什么要"先哈希后签名"？

在本实验中，为什么要先计算密文的哈希值，而不是直接对整个密文进行 RSA 签名？请至少列举三个原因。

> 答：RSA 明文长度受限
2048 位 RSA 最多只能加密 / 签名小于 256 字节的数据；若密文很长，无法直接整体签名。SHA256 固定输出 32 字节哈希值，长度固定适配 RSA 签名长度限制。
提升运算效率
对几百 KB/MB 级大文件直接做 RSA 大数运算速度极慢；哈希运算速度极快，先压缩为固定短哈希再签名，大幅减少非对称运算开销。
规避 RSA 结构性安全漏洞
直接对原文 RSA 签名存在构造攻击风险；哈希打乱原文结构，消除可利用的数学规律，提升签名安全性。

---

### 3. 签名长度与密钥长度的关系

观察你生成的签名文件 `signature.bin` 的大小。为什么 2048 位的 RSA 密钥生成的签名长度是 256 字节？如果使用 4096 位的 RSA 密钥，签名长度会是多少？

> 答：原因：RSA 签名结果长度 = 密钥模长 ÷ 8（字节）
2048 bit ÷ 8 = 256 字节，因此signature.bin大小为 256 字节。
4096 位 RSA 签名长度：
4096 ÷ 8 = 512 字节


---

### 4. 哈希函数的安全性要求

哈希函数必须满足哪三个性质才能保证数字签名的安全？请分别解释这三个性质，并说明如果哈希函数不满足某个性质，会导致什么安全问题。

提示：抗原像性、抗第二原像性、抗碰撞性

> 答：抗原像（单向性）
定义：已知哈希结果，无法反向推算出原始输入。
风险：若不满足，攻击者拿到哈希值可还原原文，签名失去保护意义。
抗第二原像（弱抗碰撞）
定义：给定原文 M 及哈希 H (M)，找不到另一个不同 M'，使得 H (M')=H (M)。
风险：攻击者可构造替换文件，替换后签名依然验证通过，篡改无法被发现。
强抗碰撞
定义：无法找到两组完全不同输入 M1、M2，满足 H (M1)=H (M2)。
风险：攻击者预先构造两条内容不同但哈希相同的文件，先用正常文件签名，后续替换为恶意文件，验证依然合法。

---

### 5. SHA-1 的安全问题

为什么 SHA-1 哈希算法不再被推荐用于数字签名？2017 年 Google 发现的 SHA-1 碰撞攻击对数字签名有什么影响？请举例说明攻击者如何利用这个漏洞。

> 答：
淘汰原因：SHA-1 已被攻破，存在碰撞攻击，不再满足强抗碰撞特性，无法保障签名防篡改能力，密码学界与各大浏览器、标准组织逐步禁用 SHA-1 签名方案。
2017 Google 碰撞攻击影响：
攻击者可构造两份内容不同、SHA-1 哈希完全一致的文件。
攻击举例：
攻击者制作一份正常合同 A、一份恶意转账合同 B，二者 SHA-1 哈希相同；诱导用户对合同 A 签名，随后将签名绑定到合同 B，验证时哈希匹配、签名合法，实现合同伪造诈骗。

---

### 6. 公钥与私钥的角色

本实验使用了签名密钥对和加密密钥对。请分别说明：

- 签名私钥、签名公钥分别用于什么操作？
- 加密私钥、加密公钥分别用于什么操作？
- 如果攻击者获得了公钥，他能做什么？不能做什么？

> 答：签名密钥对
签名私钥signature_private_key.pem：发送方使用，对密文哈希生成数字签名
签名公钥signature_public_key.pem：接收方使用，验证签名合法性
加密密钥对
加密公钥encryption_public_key.pem：发送方加密明文message.txt，生成密文
加密私钥encryption_private_key.pem：接收方解密密文，还原原始消息
攻击者拿到公钥的权限
 可以：验证签名、加密消息、查询公钥模数指数等公开参数
不能：解密已加密数据、伪造合法签名、推导对应私钥

---

### 7. 签名与加密的区别

结合本实验"加密 -> 哈希 -> 签名 -> 验证 -> 解密"的流程，说明数字签名和消息加密有什么本质区别。它们分别解决什么问题？为什么不能简单地用加密代替签名？

> 答：本质区别与作用
消息加密（本实验 RSA 加密）
目标：保密性，防止第三方窃听读取内容；使用对方公钥加密，只有对方私钥可解密。
数字签名
目标：完整性、身份认证、不可否认，防止篡改、伪造、抵赖；使用自身私钥签名，所有人可用公钥核验。
为什么不能用加密代替签名
加密是双向隐私保护，任何人拿到私钥都可解密，无法证明发送者身份，不具备不可否认性；
加密只能防窃听，无法检测文件是否被中途篡改；
加密操作流向与签名相反：加密用对方公钥，签名用自身私钥，逻辑无法互相替代；
结合本流程：先加密保隐私，再签名防篡改 + 验身份，二者各司其职。


---

### 8. 签名的不可否认性

什么是"不可否认性"（Non-repudiation）？为什么数字签名能提供不可否认性，而消息认证码（MAC）不能？

提示：MAC 使用对称密钥，签名使用非对称密钥

> 答：不可否认性定义
消息发送完成后，发送方无法事后否认自己发送、签署过该消息。
数字签名具备、MAC 不具备的原因
数字签名（非对称密钥）：签名由发送方唯一私有私钥生成，公钥全网公开用于核验；第三方仲裁机构可核验签名归属，发送方无法抵赖。
MAC 消息认证码（对称密钥）：收发双方共用同一个密钥，双方都能生成 / 篡改 MAC 值；无法判定到底是发送方还是接收方篡改、伪造，无法作为抵赖举证依据。

---

### 9. 实际应用场景

请列举三个数字签名在现实世界中的应用场景（例如软件发布、电子邮件、代码签名等），并说明在这些场景中数字签名解决了什么问题。

> 答：软件安装包代码签名
场景：Windows/macOS 安装包、开源程序发布
作用：防止安装包被植入病毒木马篡改，校验程序来源为官方开发者，规避中间人投毒。
电子合同 / 电子签章
场景：线上劳动合同、商务购销电子协议
作用：确认签署人真实身份，合同不可篡改，具备法律层面不可否认效力，满足电子合规要求。
电子邮件 S/MIME 签名
场景：企业涉密邮件、对公商务邮件
作用：确认发件人身份，防止钓鱼仿冒邮箱，防止邮件传输中途内容被篡改。


---

### 10. 时间戳与签名

假设你今天对一份文件进行了签名。一年后，你声称这份文件是昨天才签名的。接收者如何验证签名的时间？数字签名本身能否证明签名的时间？如何解决这个问题？

提示：考虑可信时间戳服务（TSA）

> 答：数字签名本身无法证明签名时间，签名生成时不会自动嵌入可信时间信息，用户可事后重签倒填时间。
接收方核验方案：
发送方生成签名后，将签名 + 文件哈希提交可信时间戳服务机构 TSA；TSA 使用自身私钥，绑定权威标准时间生成时间戳签名，附加在原签名外。
验证逻辑：
接收方同时校验原文件签名有效性 + TSA 时间戳合法性，即可确认签名确切生成时间，杜绝倒签、后签篡改时间的作弊行为。

---

### 11. 密钥长度的选择

为什么本实验使用 2048 位的 RSA 密钥？1024 位是否足够安全？4096 位是否有必要？请查阅资料，说明不同密钥长度的安全性和性能权衡。

> 答：本实验选用 2048 位 RSA 原因：
安全性与性能均衡，是目前通用最低安全基线，可抵御现有常规暴力分解、量子前置攻击，运算速度适中，教学实验、商用场景通用性最强。
1024 位 RSA：不再足够安全
大数分解算法性能提升，1024 位模数可被针对性破解，NIST 等安全机构已明确淘汰，禁止用于长期敏感数据。
4096 位 RSA：安全性更高，但存在取舍
优势：抗破解能力更强，适配长期高密级保密场景
劣势：加解密、签名验证运算速度大幅变慢，CPU 开销高，资源消耗大；普通日常场景过度冗余，没必要强制使用。

---

### 12. 签名链

假设 Alice 对一份文件签名，然后 Bob 对"Alice 的签名"进行签名，形成"签名的签名"。这种做法有意义吗？在什么场景下可能需要多重签名？

> 答：有特定业务意义，不是冗余操作
原理：Alice 对文件签名，Bob 再对 Alice 的签名二次签名，形成嵌套签名链
适用场景
多级审批流程
例如财务付款审批：经办人 Alice 签字申请→部门主管 Bob 复核二次签名，两级签名全部有效才允许付款，实现逐级权责管控。
证书层级信任体系（CA 层级）
根 CA 签发中级 CA 证书，中级 CA 再签发用户证书，多层签名构建信任链，逐级核验合法性。
多方存证确权
知识产权、公证存证场景，多方依次对前序签名背书，每一方都留存签署凭证，界定各方责任。

---

## 实验扩展阅读

### 1. RSA-PSS vs PKCS#1 v1.5

OpenSSL 默认使用 PKCS#1 v1.5 填充方案。更安全的方案是 RSA-PSS（概率签名方案）。

使用 RSA-PSS 签名：

```bash
openssl dgst -sha256 -sigopt rsa_padding_mode:pss -sign signature_private_key.pem -out signature_pss.bin encrypted_message.bin
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `dgst -sha256` | 对密文计算 SHA-256 哈希 |
| `-sigopt rsa_padding_mode:pss` | 指定使用 RSA-PSS 填充模式 |
| `-sign signature_private_key.pem` | 使用签名私钥生成签名 |
| `-out signature_pss.bin` | 输出 RSA-PSS 签名文件 |
| `encrypted_message.bin` | 被签名的密文文件 |

验证：

```bash
openssl dgst -sha256 -sigopt rsa_padding_mode:pss -verify signature_public_key.pem -signature signature_pss.bin encrypted_message.bin
```

命令说明：

| 部分 | 含义 |
| :--- | :--- |
| `dgst -sha256` | 对密文重新计算 SHA-256 哈希 |
| `-sigopt rsa_padding_mode:pss` | 指定验证时也使用 RSA-PSS 填充模式 |
| `-verify signature_public_key.pem` | 使用签名公钥验证签名 |
| `-signature signature_pss.bin` | 输入 RSA-PSS 签名文件 |
| `encrypted_message.bin` | 被验证的密文文件 |

**区别**：
- PKCS#1 v1.5 是确定性的（同一消息每次签名结果相同）
- RSA-PSS 是概率性的（每次签名结果不同，因为包含随机盐值）
- RSA-PSS 有更强的安全性证明

---

### 2. 盲签名（Blind Signature）

盲签名允许签名者在不知道消息内容的情况下对消息签名。应用场景：
- 数字货币（防止追踪）
- 电子投票（保护隐私）
- 匿名认证

**原理**：
1. 请求者对消息进行"盲化"（乘以一个随机因子）
2. 签名者对盲化后的消息签名
3. 请求者"去盲"，得到原始消息的签名

OpenSSL 不直接支持盲签名，需要使用专门的密码学库。

---

### 3. 聚合签名（Aggregate Signature）

多个签名可以聚合成一个签名，减少存储和传输开销。应用场景：
- 区块链（多个交易的签名聚合）
- 证书链（多个证书的签名聚合）

**优势**：
- n 个签名聚合后的大小接近单个签名的大小
- 验证效率提高

**算法**：BLS 签名（基于配对的密码学）

---

### 4. 门限签名（Threshold Signature）

门限签名要求 n 个参与者中的 t 个人共同参与才能生成有效签名。应用场景：
- 多重签名钱包（例如 2-of-3 签名）
- 企业财务审批（需要多人授权）

**原理**：
- 私钥被分成 n 份，分别持有
- 任意 t 份私钥碎片可以联合生成签名
- 少于 t 份无法生成有效签名

---

## 常见问题与故障排除

### Q1: `openssl genrsa` 很慢怎么办？

**原因**：生成大素数需要时间，尤其是 4096 位密钥。

**解决**：
- 2048 位密钥通常在几秒内完成
- 如果超过 30 秒，检查系统熵池：`cat /proc/sys/kernel/random/entropy_avail`
- 可以安装 `haveged` 或 `rng-tools` 增加熵源

---

### Q2: 验证签名时提示 "unable to load Public Key"

**原因**：公钥文件格式不正确或文件路径错误。

**解决**：
- 检查文件是否存在：`ls -lh signature_public_key.pem`
- 检查文件内容：`cat signature_public_key.pem`，应该以 `-----BEGIN PUBLIC KEY-----` 开头
- 确保使用 `-pubin` 参数（如果验证时需要）

---

### Q3: 签名后文件变成了文本而不是二进制

**原因**：可能使用了 `-hex` 参数或重定向了输出。

**解决**：
- 确保使用 `-out signature.bin` 而不是 `> signature.txt`
- 检查文件类型：`file signature.bin`，应该显示 "data" 而不是 "ASCII text"

---

### Q4: 篡改密文后签名仍然验证成功

**原因**：可能没有保存修改或使用了错误的文件。

**解决**：
- 确认密文文件已修改：`xxd tampered_encrypted_message.bin | head -2`
- 确保验证时使用的是篡改后的 `tampered_encrypted_message.bin`
- 重新计算哈希值确认：`openssl dgst -sha256 tampered_encrypted_message.bin`

---

### Q5: Windows 上 OpenSSL 命令不可用

**原因**：Windows 没有预装 OpenSSL。

**解决**：
- 使用 Git Bash（通常包含 OpenSSL）
- 安装 WSL（Windows Subsystem for Linux）后在 Ubuntu 中操作
- 或者从 https://slproweb.com/products/Win32OpenSSL.html 下载安装

