---
layout: post
title:  "Derivation of LBFGS Part 3 - BFGS Method"
date:   2020-09-26 23:00:00 +0900
author: Taeho Oh
tags: [ 오태호, 머신러닝 ]
---

안녕하세요. 오태호입니다.

이 글에서는 Optimization 기법중에 하나인 LBFGS Method(Limited Memory Broyden–Fletcher–Goldfarb–Shanno Method)의 수식을 다음과 같이 4개의 Part에 걸쳐서 차근차근 유도하여 LBFGS Method의 구조를 조금 깊게 살펴보도록 하겠습니다.

* [Derivation of LBFGS Part 1 - Newton's Method](Derivation-of-LBFGS-Part-1)
* [Derivation of LBFGS Part 2 - SR1 Method](Derivation-of-LBFGS-Part-2)
* Derivation of LBFGS Part 3 - BFGS Method
* [Derivation of LBFGS Part 4 - LBFGS Method](Derivation-of-LBFGS-Part-4)

## BFGS Method {#BFGS-Method}

[Quasi Newton Method](Derivation-of-LBFGS-Part-2#Quasi-Newton-Method)중에 하나인 [SR1 Method](Derivation-of-LBFGS-Part-2#SR1-Method)는 $$\mathbf{H}_{k+1}$$을 안정적으로 구할 수 없는 문제가 있습니다. $$\mathbf{H}_{k+1}$$을 안정적으로 구하기 위해 SR1 Method를 조금 개량한 BFGS Method(Broyden Fletcher Goldfarb Shanno Method)를 알아보겠습니다.

SR1 Method에서는 Rank 1 Matrix ($a\mathbf{u}_k\mathbf{u}_k^T$)를 사용해서 $$\mathbf{B}_{k+1}$$을 구했는데 BFGS Method에서는 다음과 같이 Rank 2 Matrix ($a\mathbf{u}_k\mathbf{u}_k^T+b\mathbf{v}_k\mathbf{v}_k^T$)를 사용해서 $$\mathbf{B}_{k+1}$$을 구합니다.

$$
\mathbf{B}_{k+1}=\mathbf{B}_k+a\mathbf{u}_k\mathbf{u}_k^T+b\mathbf{v}_k\mathbf{v}_k^T
$$

$$\mathbf{u}_k=\mathbf{y}_k$$, $$\mathbf{v}_k=\mathbf{B}_k\mathbf{s}_k$$로 설정하고 $$a\mathbf{u}_k\mathbf{u}_k^T+b\mathbf{v}_k\mathbf{v}_k^T$$가 구체적으로 어떤 값을 가지는지 Secant Equation을 이용해서 계산해 보겠습니다.

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

SR1 Method에 있던 문제가 어떻게 개선되었는지 살펴보겠습니다.

SR1 Method에서는 $$\mathbf{B}_k$$와 $$\mathbf{H}_k$$가 [Positive Definite Matrix](Proof-of-the-F-Test-for-Linear-Regression#Positive-Definite-Matrix)라는 것이 보장되지 않았습니다.

BFGS Method에서 $$\mathbf{H}_k$$가 Positive Definite Matrix라는 것은 다음과 같이 확인합니다.

우선 $$\mathbf{H}_0$$을 적당한 Positive Definite Matrix로(예를 들어 $\mathbf{I}$로) 설정합니다.

만약에 $$\mathbf{H}_k$$가 Positive Definite Matrix라면 $$\mathbf{H}_{k+1}$$이 Positive Definite Matrix가 되는지 다음과 같이 확인합니다.

$$
\begin{aligned}
\mathbf{w}^T\mathbf{H}_{k+1}\mathbf{w}
&=\mathbf{w}^T\left (
\mathbf{I}-
\frac{\mathbf{s}_k\mathbf{y}_k^T}{\mathbf{y}_k^T\mathbf{s}_k}
\right )
\mathbf{H}_k
\left (
\mathbf{I}-
\frac{\mathbf{y}_k\mathbf{s}_k^T}{\mathbf{y}_k^T\mathbf{s}_k}
\right )\mathbf{w}
+
\mathbf{w}^T\frac{\mathbf{s}_k\mathbf{s}_k^T}{\mathbf{y}_k^T\mathbf{s}_k}\mathbf{w} \\
&=\left [ \left (
\mathbf{I}-
\frac{\mathbf{y}_k\mathbf{s}_k^T}{\mathbf{y}_k^T\mathbf{s}_k}
\right )\mathbf{w} \right ]^T
\mathbf{H}_k
\left [ \left (
\mathbf{I}-
\frac{\mathbf{y}_k\mathbf{s}_k^T}{\mathbf{y}_k^T\mathbf{s}_k}
\right )\mathbf{w} \right ]
+
\frac{\| \mathbf{s}_k^T\mathbf{w} \|^2}{\mathbf{y}_k^T\mathbf{s}_k} \\
\end{aligned}
$$

$$\mathbf{H}_k$$가 Positive Definite Matrix이므로 모든 $\mathbf{w}$에 대해 다음이 성립합니다.

$$
\left [ \left (
\mathbf{I}-
\frac{\mathbf{y}_k\mathbf{s}_k^T}{\mathbf{y}_k^T\mathbf{s}_k}
\right )\mathbf{w} \right ]^T
\mathbf{H}_k
\left [ \left (
\mathbf{I}-
\frac{\mathbf{y}_k\mathbf{s}_k^T}{\mathbf{y}_k^T\mathbf{s}_k}
\right )\mathbf{w} \right ] \gt 0
$$

만약에 $$\mathbf{y}_k^T\mathbf{s}_k \gt 0$$이 성립한다면 $$\frac{\| \mathbf{s}_k^T\mathbf{w} \|^2}{\mathbf{y}_k^T\mathbf{s}_k} \gt 0$$이 성립하면서 $$\mathbf{H}_{k+1}$$은 Positive Definite Matrix가 됩니다.

[Wolfe Conditions](Derivation-of-LBFGS-Part-1#Wolfe-Conditions)의 Curvature Condition이 성립하면 $$\mathbf{y}_k^T\mathbf{s}_k \gt 0$$가 성립함을 다음과 같이 확인합니다.

$$
t_k \gt 0 \\
0 \lt c_2 \lt 1 \\
\mathbf{g}_k^T \mathbf{p}_k \lt 0 \\
\mathbf{x}_{k+1}=\mathbf{x}_k+t_k\mathbf{p}_k \\
\mathbf{p}_k^T \nabla f(\mathbf{x}_k+t_k\mathbf{p}_k) \ge c_2 \mathbf{p}_k^T \nabla f(\mathbf{x}_k) \\
\mathbf{p}_k^T \nabla f(\mathbf{x}_{k+1}) \ge c_2 \mathbf{p}_k^T \nabla f(\mathbf{x}_k) \\
\mathbf{p}_k^T \mathbf{g}_{k+1} \ge c_2 \mathbf{p}_k^T \mathbf{g}_k \\
t_k\mathbf{p}_k^T \mathbf{g}_{k+1} \ge t_k c_2 \mathbf{p}_k^T \mathbf{g}_k \\
\mathbf{g}_{k+1}^T (t_k\mathbf{p}_k) \ge c_2 \mathbf{g}_k^T (t_k\mathbf{p}_k) \\
\mathbf{g}_{k+1}^T (\mathbf{x}_{k+1}-\mathbf{x}_k) \ge c_2 \mathbf{g}_k^T (\mathbf{x}_{k+1}-\mathbf{x}_k) \\
\mathbf{g}_{k+1}^T \mathbf{s}_k \ge c_2 \mathbf{g}_k^T \mathbf{s}_k \\
\mathbf{g}_{k+1}^T \mathbf{s}_k - \mathbf{g}_k^T \mathbf{s}_k \ge c_2 \mathbf{g}_k^T \mathbf{s}_k - \mathbf{g}_k^T \mathbf{s}_k \\
(\mathbf{g}_{k+1}^T - \mathbf{g}_k^T) \mathbf{s}_k \ge (c_2 - 1) \mathbf{g}_k^T \mathbf{s}_k \\
\begin{aligned}
\mathbf{y}_k^T \mathbf{s}_k \ge (c_2 - 1) \mathbf{g}_k^T \mathbf{s}_k
&=(c_2 - 1) \mathbf{g}_k^T ( \mathbf{x}_{k+1} - \mathbf{x}_k ) \\
&=(c_2 - 1) \mathbf{g}_k^T (t_k \mathbf{p}_k) \\
&=t_k (c_2 - 1) \mathbf{g}_k^T \mathbf{p}_k \gt 0 \\
\end{aligned} \\
\mathbf{y}_k^T \mathbf{s}_k \gt 0
$$

BFGS Method에서는, Wolfe Conditions의 Curvature Condition을 따라 Step Size $t_k$를 결정하고, Initial Inverse Hessian $$\mathbf{H}_0$$이 Positive Definite Matrix이면, Inverse Hessian $$\mathbf{H}_k$$는 모든 $$k$$에 대해 Positive Definite Matrix가 됩니다. 자연스럽게 Hessian $$\mathbf{B}_k$$도 모든 $$k$$에 대해 Positive Definite Matrix가 됩니다.

SR1 Method에서는, $$\mathbf{B}_{k+1}$$의 계산과정에서 $$(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)^T\mathbf{s}_k \approx 0$$이 되면, 분모가 $$0$$이 될 수가 있어서, $$\mathbf{B}_{k+1}$$과 $$\mathbf{H}_{k+1}$$을 안정적으로 구할 수 없었습니다.

BFGS Method에서는, Wolfe Conditions의 Curvature Condition을 따라 Step Size $$t_k$$를 결정하면, $$\mathbf{y}_k^T \mathbf{s}_k \gt 0$$가 보장되어, 계산과정에서 분모가 $$0$$이 되지 않아서 안정적으로 $$\mathbf{B}_{k+1}$$과 $$\mathbf{H}_{k+1}$$을 구할 수 있습니다.

하지만 BFGS Method에는 큰 단점이 하나 있습니다. Iteration마다 $\mathbf{H}_k$를 저장해야 하는데 이것은 $\mathbf{x}$이 $n$차원 Vector인 경우에 $\mathbf{H}_k$가 $n \times n$의 Matrix가 되기 때문에 $n$이 매우 큰 경우에 $\mathbf{H}_k$를 저장하기가 쉽지 않습니다.

## Conclusion {#Conclusion}

이 글에서는 LBFGS Method를 살펴보기 위한 과정으로 BFGS Method에 대해 살펴보았습니다.

BFGS Method에는 $\mathbf{x}$이 고차원인 Vector인 경우에 $\mathbf{H}_k$를 저장하기가 쉽지 않은 문제가 있습니다.

[Derivation of LBFGS Part 4 - LBFGS Method](Derivation-of-LBFGS-Part-4)에서는 $\mathbf{H}_k$를 저장하지 않고 BFGS Method를 수행하는 방법을 알아보도록 하겠습니다.
