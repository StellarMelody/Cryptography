# 密码学习题集 - 公钥加密、RSA 与 ElGamal
## 第 1 题
回顾对称加密：可以加密一条 32 位消息，并得到一条 32 位密文（例如使用一次性密码本，或基于 nonce 的加密系统）。

公钥加密系统是否也能做到这一点？
- 可以，RSA-OAEP 系统可以产生 32 位密文。
- 可以，当加密短明文时，可以把公钥加密算法的输出截断为与明文相同的长度。
- 可以做到，这取决于系统的具体细节。
- ✅ 不可以，密文很短的公钥加密系统永远不可能是安全的。

## 第 2 题
设 $(\operatorname{Gen}, E, D)$ 是一个语义安全的公钥加密系统。算法 $E$ 能否是确定性的？
- 可以，有些公钥加密方案是确定性的。
- 不可以，但选择密文安全的加密可以是确定性的。
- 可以，RSA 加密是确定性的。
- ✅ 不可以，语义安全的公钥加密必须是随机化的。

## 第 3 题
设 $(\operatorname{Gen}, E, D)$ 是一个选择密文安全的公钥加密系统，消息空间为 $\{0,1\}^{128}$。以下哪些系统也是选择密文安全的？

1. $(\operatorname{Gen}, E', D')$，其中
$$ E'(pk, m) = E(pk, m \oplus 1^{128}) $$
$$ D'(sk, c) = D(sk, c) \oplus 1^{128} $$
✅ CCA 安全

2. $(\operatorname{Gen}, E', D')$，其中
$$ E'(pk, m) = (E(pk, m), 0^{128}) $$
$$ D'(sk, (c_1, c_2)) = D(sk, c_1) $$
✅ CCA 安全

3. $(\operatorname{Gen}, E', D')$，其中
$$ E'(pk, m) = (E(pk, m), E(pk, m)) $$
$$ D'(sk, (c_1, c_2)) = D(sk, c_1) $$
❌ 非 CCA 安全

4. $(\operatorname{Gen}, E', D')$，其中
$$ E'(pk, m) = (E(pk, m), E(pk, m)) $$
$$ D'(sk, (c_1, c_2)) =
\begin{cases}
D(sk, c_1) & \text{若 } D(sk, c_1) = D(sk, c_2) \\
\bot & \text{否则}
\end{cases} $$
✅ CCA 安全

## 第 4 题
回顾 RSA 公钥由 RSA 模数 $N$ 和指数 $e$ 组成。Alice 使用 $(N,3)$，$d_a = 3^{-1}\bmod\varphi(N)$。哪一项是 $\varphi(N)$ 的整数倍？
- $d_a - 1$
- $3d_a$
- $d_a + 1$
- ✅ $3d_a - 1$

## 第 5 题
$y$ 满足
$$
\begin{cases}
y \equiv 1 \pmod p \\
y \equiv -1 \pmod q
\end{cases}
\quad \text{或} \quad
\begin{cases}
y \equiv -1 \pmod p \\
y \equiv 1 \pmod q
\end{cases}
$$
Alice 应如何利用 $y$ 分解 $N$？
- ✅ 计算 $\gcd(N, y-1)$
- 计算 $\gcd(N, 2y-1)$
- 计算 $\gcd(N, y)$

## 第 6 题
$N=pqr$，$p,q,r$ 为不同素数，$\varphi(N)$ 是多少？
- ✅ $\varphi(N) = (p-1)(q-1)(r-1)$
- $\varphi(N) = (p-1)(q-1)$
- $\varphi(N) = (p-1)(q-1)r$
- $\varphi(N) = (p-1)(q-1)(r+1)$

## 第 7 题
$a r_1 + b r_2 = 1$，$s_1 = s^{r_1},\ s_2 = s^{r_2}$，如何计算 $s$？
- $s = s_1^a / s_2^b \in \mathbb{Z}_N$
- ✅ $s = s_1^a \cdot s_2^b \in \mathbb{Z}_N$

## 第 8 题
$(c_0,c_1)=E(m_0)$，$(c_2,c_3)=E(m_1)$，构造 $m_0\cdot m_1$ 的密文：
- $(c_0/c_2,\ c_1/c_3)$ 是 $m_0\cdot m_1$ 的加密。
- $(c_0/c_3,\ c_1/c_2)$ 是 $m_0\cdot m_1$ 的加密。
- ✅ $(c_0 c_2,\ c_1 c_3)$ 是 $m_0\cdot m_1$ 的加密。
- $(c_0 c_3,\ c_1 c_2)$ 是 $m_0\cdot m_1$ 的加密。

## 第 9 题
私钥拆分 $a=a_1+a_2$，密文 $(u,c)$，两方解密流程：
- ✅ 参与方 1 返回 $u_1 \leftarrow u^{a_1}$，参与方 2 返回 $u_2 \leftarrow u^{a_2}$，然后计算 $v \leftarrow u_1 \cdot u_2$。
- 参与方 1 返回 $u_1 \leftarrow u^{a_1^2}$，参与方 2 返回 $u_2 \leftarrow u^{a_2^2}$，然后计算 $v \leftarrow u_1 \cdot u_2$。
- 参与方 1 返回 $u_1 \leftarrow u^{a_1}$，参与方 2 返回 $u_2 \leftarrow u^{a_2}$，然后计算 $v \leftarrow u_1 / u_2$。

## 第 10 题
Alice 测试 $a=b$ 的方式：
- ✅ Alice 通过检查 $B_2 / B_1^x = 1$ 来测试 $a=b$ 是否成立。

## 第 11 题
$N=pqr$ 三同等大小不同素数，Wiener 攻击 $d$ 的界：
- 对某个常数 $c$，有 $d < N^{1/2}/c$
- 对某个常数 $c$，有 $d < N^{2/3}/c$
- ✅ 对某个常数 $c$，有 $d < N^{1/6}/c$
- 对某个常数 $c$，有 $d < N^{1/5}/c$

## 第 12 题
$H$ 输出最高比特恒为 0，Hash-DH 假设是否成立？
- 是的，对于这样的 $H$，Hash-DH 总是成立。
- ✅ 不，这种情况下 Hash-DH 很容易被破解。
- 是的，对于某些群 $G$ 成立。
- ，