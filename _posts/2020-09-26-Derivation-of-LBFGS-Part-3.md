---
layout: post
title:  "Derivation of LBFGS - Part 3"
date:   2020-09-26 23:00:00 +0900
author: Taeho Oh
tags: [ 오태호, 머신러닝 ]
---

안녕하세요. 오태호입니다.

이 글은 [Derivation of LBFGS - Part 3](Derivation-of-LBFGS-Part-3)입니다. 이 글을 읽기 전에 [Derivation of LBFGS - Part 1](Derivation-of-LBFGS-Part-1), [Derivation of LBFGS - Part 2](Derivation-of-LBFGS-Part-2)를 먼저 읽으시길 바랍니다.

## BFGS Method {#BFGS-Method}

[Quasi-Newton-Method](Derivation-of-LBFGS-Part-2#Quasi-Newton-Method)중에 하나인 [SR1-Method](Derivation-of-LBFGS-Part-2#SR1-Method)는 $$\mathbf{H}_{k+1}$$을 안정적으로 구할 수 없는 문제가 있습니다. $$\mathbf{H}_{k+1}$$을 안정적으로 구하기 위해 SR1 Method를 조금 개량한 BFGS Method(Broyden Fletcher Goldfarb Shanno Method)를 알아보겠습니다.

SR1 Method에서는 Rank 1 Matrix를 사용해서 $$\mathbf{B}_{k+1}$$을 구했는데 BFGS Method에서는 다음과 같이 Rank 2 Matrix를 사용해서 $$\mathbf{B}_{k+1}$$을 구합니다.

$$
\mathbf{B}_{k+1}=\mathbf{B}_k+a\mathbf{u}_k\mathbf{u}_k^T+b\mathbf{v}_k\mathbf{v}_k^T
$$

$$\mathbf{u}_k=\mathbf{y}_k$$, $$\mathbf{v}_k=\mathbf{B}_k\mathbf{s}_k$$로 설정하고 $$a\mathbf{u}_k\mathbf{u}_k^T+b\mathbf{v}_k\mathbf{v}_k^T$$가 구체적으로 어떤 값을 가지는지 Secant Equation을 이용해서 계산해 보겠습니다. $$\mathbf{u}_k$$와 $$\mathbf{v}_k$$가 Linearly Independent한 것도 이용합니다.

$$
\mathbf{B}_{k+1}=\mathbf{B}_k+a\mathbf{u}_k\mathbf{u}_k^T+b\mathbf{v}_k\mathbf{v}_k^T \\
\mathbf{B}_{k+1}\mathbf{s}_k=\mathbf{y}_k \\
(\mathbf{B}_k+a\mathbf{u}_k\mathbf{u}_k^T+b\mathbf{v}_k\mathbf{v}_k^T)\mathbf{s}_k=\mathbf{y}_k \\
(a\mathbf{u}_k^T\mathbf{s}_k)\mathbf{u}_k+(b\mathbf{v}_k^T\mathbf{s}_k)\mathbf{v}_k=\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k \\
(a\mathbf{u}_k^T\mathbf{s}_k)\mathbf{u}_k=\mathbf{y}_k=\mathbf{u}_k \\
(b\mathbf{v}_k^T\mathbf{s}_k)\mathbf{v}_k=-\mathbf{B}_k\mathbf{s}_k=-\mathbf{v}_k \\
a=\frac{1}{\mathbf{u}_k^T\mathbf{s}_k}=\frac{1}{\mathbf{y}_k^T\mathbf{s}_k} \\
b=-\frac{1}{\mathbf{v}_k^T\mathbf{s}_k}=-\frac{1}{\mathbf{s}_k^T\mathbf{B}_k^T\mathbf{s}_k}=-\frac{1}{\mathbf{s}_k^T\mathbf{B}_k\mathbf{s}_k} \\
\begin{aligned}
\mathbf{B}_{k+1}
&=\mathbf{B}_k+\frac{1}{\mathbf{y}_k^T\mathbf{s}_k}\mathbf{y}_k\mathbf{y}_k^T-\frac{1}{\mathbf{s}_k^T\mathbf{B}_k\mathbf{s}_k}\mathbf{B}_k\mathbf{s}_k\mathbf{s}_k^T\mathbf{B}_k^T \\
&=\mathbf{B}_k-\frac{\mathbf{B}_k\mathbf{s}_k\mathbf{s}_k^T\mathbf{B}_k}{\mathbf{s}_k^T\mathbf{B}_k\mathbf{s}_k}+\frac{\mathbf{y}_k\mathbf{y}_k^T}{\mathbf{y}_k^T\mathbf{s}_k} \\
\end{aligned}
$$

정리하면 다음과 같습니다.

$$
\mathbf{B}_{k+1}=\mathbf{B}_k-\frac{\mathbf{B}_k\mathbf{s}_k\mathbf{s}_k^T\mathbf{B}_k}{\mathbf{s}_k^T\mathbf{B}_k\mathbf{s}_k}+\frac{\mathbf{y}_k\mathbf{y}_k^T}{\mathbf{y}_k^T\mathbf{s}_k}
$$

이제 여기서 구한 $$\mathbf{B}_{k+1}$$을 이용해서 $$\mathbf{H}_{k+1}$$를 구해야 합니다. $$\mathbf{B}_{k+1}$$을 이용해서 $$\mathbf{H}_{k+1}$$를 구하기 위해 [Sherman Morrison Woodbury Formula](#Sherman-Morrison-Woodbury-Formula)을 이용합니다.

Sherman Morrison Woodbury Formula는 다음과 같습니다.

$$
(\mathbf{A}+\mathbf{UCV})^{-1}=\mathbf{A}^{-1}-\mathbf{A}^{-1}\mathbf{U}(\mathbf{C}^{-1}+\mathbf{V}\mathbf{A}^{-1}\mathbf{U})^{-1}\mathbf{V}\mathbf{A}^{-1}
$$

$\mathbf{H}_{k+1}$은 다음과 같이 구합니다.

$$
\mathbf{A}=\mathbf{B}_{k} \\
\mathbf{C}=\mathbf{I} \\
\mathbf{U}=
\begin{bmatrix}
\mathbf{B}_k\mathbf{s}_k & \mathbf{y}_k
\end{bmatrix} \\
\mathbf{V}=
\begin{bmatrix}
-\frac{1}{\mathbf{s}_k^T\mathbf{B}_k\mathbf{s}_k} & 0 \\
0 & \frac{1}{\mathbf{y}_k^T\mathbf{s}_k}
\end{bmatrix}
\begin{bmatrix}
\mathbf{s}_k^T\mathbf{B}_k \\
\mathbf{y}_k^T
\end{bmatrix}
$$

$$
\begin{aligned}
\mathbf{H}_{k+1}
&=\mathbf{B}_{k+1}^{-1} \\
&=(\mathbf{B}_k+a\mathbf{u}_k\mathbf{u}_k^T+b\mathbf{v}_k\mathbf{v}_k^T)^{-1} \\
&=\left (\mathbf{B}_k-\frac{\mathbf{B}_k\mathbf{s}_k\mathbf{s}_k^T\mathbf{B}_k}{\mathbf{s}_k^T\mathbf{B}_k\mathbf{s}_k}+\frac{\mathbf{y}_k\mathbf{y}_k^T}{\mathbf{y}_k^T\mathbf{s}_k}\right )^{-1} \\
&=\left ( \mathbf{A} + \mathbf{UCV} \right )^{-1} \\
&=\left (
\mathbf{B}_k
+
\begin{bmatrix}
\mathbf{B}_k\mathbf{s}_k & \mathbf{y}_k
\end{bmatrix}
\begin{bmatrix}
-\frac{1}{\mathbf{s}_k^T\mathbf{B}_k\mathbf{s}_k} & 0 \\
0 & \frac{1}{\mathbf{y}_k^T\mathbf{s}_k}
\end{bmatrix}
\begin{bmatrix}
\mathbf{s}_k^T\mathbf{B}_k \\
\mathbf{y}_k^T
\end{bmatrix}
\right )^{-1} \\
&=\mathbf{B}_k^{-1}-\mathbf{B}_k^{-1}
\begin{bmatrix}
\mathbf{B}_k\mathbf{s}_k & \mathbf{y}_k
\end{bmatrix}
\left (
\mathbf{I}
+
\begin{bmatrix}
-\frac{1}{\mathbf{s}_k^T\mathbf{B}_k\mathbf{s}_k} & 0 \\
0 & \frac{1}{\mathbf{y}_k^T\mathbf{s}_k}
\end{bmatrix}
\begin{bmatrix}
\mathbf{s}_k^T\mathbf{B}_k \\
\mathbf{y}_k^T
\end{bmatrix}
\mathbf{B}_k^{-1}
\begin{bmatrix}
\mathbf{B}_k\mathbf{s}_k & \mathbf{y}_k
\end{bmatrix}
\right )^{-1}
\begin{bmatrix}
-\frac{1}{\mathbf{s}_k^T\mathbf{B}_k\mathbf{s}_k} & 0 \\
0 & \frac{1}{\mathbf{y}_k^T\mathbf{s}_k}
\end{bmatrix}
\begin{bmatrix}
\mathbf{s}_k^T\mathbf{B}_k \\
\mathbf{y}_k^T
\end{bmatrix}
\mathbf{B}_k^{-1} \\
&=\mathbf{H}_k-
\begin{bmatrix}
\mathbf{s}_k & \mathbf{H}_k\mathbf{y}_k
\end{bmatrix}
\left (
\begin{bmatrix}
-\frac{1}{\mathbf{s}_k^T\mathbf{B}_k\mathbf{s}_k} & 0 \\
0 & \frac{1}{\mathbf{y}_k^T\mathbf{s}_k}
\end{bmatrix}^{-1}
\left (
\mathbf{I}
+
\begin{bmatrix}
-\frac{1}{\mathbf{s}_k^T\mathbf{B}_k\mathbf{s}_k} & 0 \\
0 & \frac{1}{\mathbf{y}_k^T\mathbf{s}_k}
\end{bmatrix}
\begin{bmatrix}
\mathbf{s}_k^T\mathbf{B}_k \\
\mathbf{y}_k^T
\end{bmatrix}
\mathbf{H}_k
\begin{bmatrix}
\mathbf{B}_k\mathbf{s}_k & \mathbf{y}_k
\end{bmatrix}
\right )
\right )^{-1}
\begin{bmatrix}
\mathbf{s}_k^T \\
\mathbf{y}_k^T\mathbf{H}_k
\end{bmatrix} \\
&=\mathbf{H}_k-
\begin{bmatrix}
\mathbf{s}_k & \mathbf{H}_k\mathbf{y}_k
\end{bmatrix}
\left (
\begin{bmatrix}
-\mathbf{s}_k^T\mathbf{B}_k\mathbf{s}_k & 0 \\
0 & \mathbf{y}_k^T\mathbf{s}_k
\end{bmatrix}
+
\begin{bmatrix}
\mathbf{s}_k^T\mathbf{B}_k \\
\mathbf{y}_k^T
\end{bmatrix}
\mathbf{H}_k
\begin{bmatrix}
\mathbf{B}_k\mathbf{s}_k & \mathbf{y}_k
\end{bmatrix}
\right )^{-1}
\begin{bmatrix}
\mathbf{s}_k^T \\
\mathbf{y}_k^T\mathbf{H}_k
\end{bmatrix} \\
&=\mathbf{H}_k-
\begin{bmatrix}
\mathbf{s}_k & \mathbf{H}_k\mathbf{y}_k
\end{bmatrix}
\left (
\begin{bmatrix}
-\mathbf{s}_k^T\mathbf{B}_k\mathbf{s}_k & 0 \\
0 & \mathbf{y}_k^T\mathbf{s}_k
\end{bmatrix}
+
\begin{bmatrix}
\mathbf{s}_k^T\mathbf{B}_k\mathbf{s}_k & \mathbf{s}_k^T\mathbf{y}_k \\
\mathbf{y}_k^T\mathbf{s}_k & \mathbf{y}_k^T\mathbf{H}_k\mathbf{y}_k
\end{bmatrix}
\right )^{-1}
\begin{bmatrix}
\mathbf{s}_k^T \\
\mathbf{y}_k^T\mathbf{H}_k
\end{bmatrix} \\
&=\mathbf{H}_k-
\begin{bmatrix}
\mathbf{s}_k & \mathbf{H}_k\mathbf{y}_k
\end{bmatrix}
\begin{bmatrix}
0 & \mathbf{s}_k^T\mathbf{y}_k \\
\mathbf{y}_k^T\mathbf{s}_k & \mathbf{y}_k^T(\mathbf{s}_k+\mathbf{H}_k\mathbf{y}_k)
\end{bmatrix}^{-1}
\begin{bmatrix}
\mathbf{s}_k^T \\
\mathbf{y}_k^T\mathbf{H}_k
\end{bmatrix} \\
&=\mathbf{H}_k-
\begin{bmatrix}
\mathbf{s}_k & \mathbf{H}_k\mathbf{y}_k
\end{bmatrix}
\left (
\frac{1}{-\mathbf{s}_k^T\mathbf{y}_k\mathbf{y}_k^T\mathbf{s}_k}
\begin{bmatrix}
\mathbf{y}_k^T(\mathbf{s}_k+\mathbf{H}_k\mathbf{y}_k) & -\mathbf{s}_k^T\mathbf{y}_k \\
-\mathbf{y}_k^T\mathbf{s}_k & 0
\end{bmatrix}
\right )
\begin{bmatrix}
\mathbf{s}_k^T \\
\mathbf{y}_k^T\mathbf{H}_k
\end{bmatrix} \\
&=\mathbf{H}_k+
\frac{1}{\mathbf{s}_k^T\mathbf{y}_k\mathbf{y}_k^T\mathbf{s}_k}
\begin{bmatrix}
\mathbf{s}_k\mathbf{y}_k^T(\mathbf{s}_k+\mathbf{H}_k\mathbf{y}_k)-\mathbf{H}_k\mathbf{y}_k\mathbf{y}_k^T\mathbf{s}_k & -\mathbf{s}_k\mathbf{s}_k^T\mathbf{y}_k
\end{bmatrix}
\begin{bmatrix}
\mathbf{s}_k^T \\
\mathbf{y}_k^T\mathbf{H}_k
\end{bmatrix} \\
&=\mathbf{H}_k+
\frac{1}{(\mathbf{y}_k^T\mathbf{s}_k)^2}
(
\mathbf{s}_k\mathbf{y}_k^T(\mathbf{s}_k+\mathbf{H}_k\mathbf{y}_k)\mathbf{s}_k^T-\mathbf{H}_k\mathbf{y}_k\mathbf{y}_k^T\mathbf{s}_k\mathbf{s}_k^T-\mathbf{s}_k\mathbf{s}_k^T\mathbf{y}_k\mathbf{y}_k^T\mathbf{H}_k
) \\
&=\mathbf{H}_k+
\frac{\mathbf{s}_k\mathbf{s}_k^T}{\mathbf{y}_k^T\mathbf{s}_k}+
\frac{\mathbf{s}_k\mathbf{y}_k^T\mathbf{H}_k\mathbf{y}_k\mathbf{s}_k^T}{(\mathbf{y}_k^T\mathbf{s}_k)^2}-
\frac{\mathbf{H}_k\mathbf{y}_k\mathbf{s}_k^T}{\mathbf{y}_k^T\mathbf{s}_k}-
\frac{\mathbf{s}_k\mathbf{y}_k^T\mathbf{H}_k}{\mathbf{y}_k^T\mathbf{s}_k} \\
&=\left (
\mathbf{I}-
\frac{\mathbf{s}_k\mathbf{y}_k^T}{\mathbf{y}_k^T\mathbf{s}_k}
\right )
\mathbf{H}_k
\left (
\mathbf{I}-
\frac{\mathbf{y}_k\mathbf{s}_k^T}{\mathbf{y}_k^T\mathbf{s}_k}
\right )
+
\frac{\mathbf{s}_k\mathbf{s}_k^T}{\mathbf{y}_k^T\mathbf{s}_k} \\
\end{aligned}
$$

정리하면 다음과 같습니다.

$$
\mathbf{H}_{k+1}
=\left (
\mathbf{I}-
\frac{\mathbf{s}_k\mathbf{y}_k^T}{\mathbf{y}_k^T\mathbf{s}_k}
\right )
\mathbf{H}_k
\left (
\mathbf{I}-
\frac{\mathbf{y}_k\mathbf{s}_k^T}{\mathbf{y}_k^T\mathbf{s}_k}
\right )
+
\frac{\mathbf{s}_k\mathbf{s}_k^T}{\mathbf{y}_k^T\mathbf{s}_k}
$$

BFGS Method는 큰 단점이 하나 있습니다. Iteration마다 $\mathbf{H}_k$를 저장해야 하는데 이것은 $\mathbf{x}$이 고차원인 경우에 $\mathbf{H}_k$의 크기가 너무 커서 저장하기가 쉽지 않습니다.

## Conclusion {#Conclusion}

이 글에서는 LBFGS를 살펴보기 위한 과정으로 BFGS Method에 대해 살펴보았습니다.

BFGS Method에는 $\mathbf{x}$이 고차원인 경우에 $\mathbf{H}_k$를 저장하기가 쉽지 않은 문제가 있습니다.

다음 Part에서는 $\mathbf{H}_k$를 저장하지 않고 BFGS Method를 수행하는 방법을 알아보도록 하겠습니다.
