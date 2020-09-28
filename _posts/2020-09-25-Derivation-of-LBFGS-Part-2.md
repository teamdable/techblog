---
layout: post
title:  "Derivation of LBFGS Part 2 - SR1 Method"
date:   2020-09-25 23:00:00 +0900
author: Taeho Oh
tags: [ 오태호, 머신러닝 ]
---

안녕하세요. 오태호입니다.

이 글에서는 Optimization 기법중에 하나인 LBFGS Method(Limited Memory Broyden–Fletcher–Goldfarb–Shanno Method)의 수식을 다음과 같이 4개의 Part에 걸쳐서 차근차근 유도하여 LBFGS Method의 구조를 조금 깊게 살펴보도록 하겠습니다.

* [Derivation of LBFGS Part 1 - Newton's Method](Derivation-of-LBFGS-Part-1)
* Derivation of LBFGS Part 2 - SR1 Method
* [Derivation of LBFGS Part 3 - BFGS Method](Derivation-of-LBFGS-Part-3)
* [Derivation of LBFGS Part 4 - LBFGS Method](Derivation-of-LBFGS-Part-4)

## Quasi Newton Method {#Quasi-Newton-Method}

[Newton's Method](Derivation-of-LBFGS-Part-1#Newtons-Method)를 사용하여 $f(\mathbf{x})$를 최소로 하는 $\mathbf{x}$를 찾는 식은 다음과 같습니다. 다음 식을 $\mathbf{x}_1$, $\mathbf{x}_2$, $\mathbf{x}_3$, $\cdots$ 와 같이 Iteration을 반복하면서 구하고자 하는 $\mathbf{x}$에 점점 가까운 값을 구합니다.

$$
\mathbf{x}_{k+1}=\mathbf{x}_k-t_k[\nabla^2 f(\mathbf{x}_k)]^{-1}\nabla f(\mathbf{x}_k)
$$

여기에서 $\mathbf{x}$의 차원이 높은 경우에는 $[\nabla^2 f(\mathbf{x}_k)]^{-1}$의 계산량이 매우 커서 계산이 매우 힘듭니다. 그래서 이런 경우를 극복하기 위해 $[\nabla^2 f(\mathbf{x}_k)]^{-1}$을 정확하게 계산하는 것이 아니라 근사해서 구한 다음에 사용하는 다양한 기법이 있는데 이런 기법들을 Quasi Newton Method라고 합니다.

$[\nabla^2 f(\mathbf{x}_k)]^{-1}$을 근사하기 위한 수식을 조금 더 간결하게 표기하기 위해 다음과 같이 몇가지 Vector와 Matrix를 정의합니다.

$$
\mathbf{s}_k=\mathbf{x}_{k+1}-\mathbf{x}_k \\
\mathbf{g}_k=\nabla f(\mathbf{x}_{k}) \\
\mathbf{y}_k=\mathbf{g}_{k+1}-\mathbf{g}_k \\
\mathbf{B}_k \approx \nabla^2 f(\mathbf{x}_k) \\
\mathbf{H}_k=\mathbf{B}_k^{-1}
$$

$[\nabla^2 f(\mathbf{x}_k)]^{-1}$를 근사해서 구하기 위해 일단 $\nabla^2 f(\mathbf{x}_k)$를 근사해서 $\mathbf{B}_k$를 구하고 이를 기반으로 $\mathbf{H}_k$를 구합니다. $\mathbf{B}_k$를 구하는 방법으로는 Iteration마다 조금씩 $\mathbf{B}_k$에 변화를 줘서 $\mathbf{B}_k$가 $\nabla^2 f(\mathbf{x}_k)$과 유사해 지도록 해서 구합니다.

## Secant Equation {#Secant-Equation}

$\mathbf{B}_{k+1}$를 $\nabla^2 f(\mathbf{x}_k)$에 근사시키기 위해 다음과 같은 식을 만족시키도록 합니다. 이 식은 Secant Equation이라고 합니다.

$$
\mathbf{B}_{k+1}\mathbf{s}_k=\mathbf{y}_k
$$

이 식을 직관적으로 살펴보면, $$\mathbf{x}_{k+1}$$과 $$\mathbf{x}_k$$의 차이를 $$\mathbf{B}_{k+1}$$에 곱해주면 $$\nabla f(\mathbf{x}_{k+1})$$과 $$\nabla f(\mathbf{x}_k)$$의 차이가 된다는 것을 의미합니다. $$\nabla^2 f(\mathbf{x}_k)$$의 정의를 생각해 보면 이것을 만족하는 $\mathbf{B}_{k+1}$는 $\nabla^2 f(\mathbf{x}_k)$에 가까울 것이라는 것을 추측할 수 있습니다.

## Sherman Morrison Woodbury Formula {#Sherman-Morrison-Woodbury-Formula}

$\mathbf{B}_k$를 구한 후에 $\mathbf{H}_k$를 구할 때 다음 식을 이용합니다. 이 식은 Sherman Morrison Woodbury Formula라고 합니다.

$$
(\mathbf{A}+\mathbf{UCV})^{-1}=\mathbf{A}^{-1}-\mathbf{A}^{-1}\mathbf{U}(\mathbf{C}^{-1}+\mathbf{V}\mathbf{A}^{-1}\mathbf{U})^{-1}\mathbf{V}\mathbf{A}^{-1}
$$

이 식은 다음과 같이 증명합니다.

$$
\begin{aligned}
&(\mathbf{A}+\mathbf{UCV})(\mathbf{A}^{-1}-\mathbf{A}^{-1}\mathbf{U}(\mathbf{C}^{-1}+\mathbf{V}\mathbf{A}^{-1}\mathbf{U})^{-1}\mathbf{V}\mathbf{A}^{-1}) \\
&=\mathbf{I}-\mathbf{U}(\mathbf{C}^{-1}+\mathbf{V}\mathbf{A}^{-1}\mathbf{U})^{-1}\mathbf{V}\mathbf{A}^{-1}+\mathbf{U}\mathbf{C}\mathbf{V}\mathbf{A}^{-1}-\mathbf{U}\mathbf{C}\mathbf{V}\mathbf{A}^{-1}\mathbf{U}(\mathbf{C}^{-1}+\mathbf{V}\mathbf{A}^{-1}\mathbf{U})^{-1}\mathbf{V}\mathbf{A}^{-1} \\
&=\mathbf{I}+\mathbf{U}\mathbf{C}\mathbf{V}\mathbf{A}^{-1}-[\mathbf{U}(\mathbf{C}^{-1}+\mathbf{V}\mathbf{A}^{-1}\mathbf{U})^{-1}\mathbf{V}\mathbf{A}^{-1}+\mathbf{U}\mathbf{C}\mathbf{V}\mathbf{A}^{-1}\mathbf{U}(\mathbf{C}^{-1}+\mathbf{V}\mathbf{A}^{-1}\mathbf{U})^{-1}\mathbf{V}\mathbf{A}^{-1})] \\
&=\mathbf{I}+\mathbf{U}\mathbf{C}\mathbf{V}\mathbf{A}^{-1}-(\mathbf{U}+\mathbf{U}\mathbf{C}\mathbf{V}\mathbf{A}^{-1}\mathbf{U})(\mathbf{C}^{-1}+\mathbf{V}\mathbf{A}^{-1}\mathbf{U})^{-1}\mathbf{V}\mathbf{A}^{-1} \\
&=\mathbf{I}+\mathbf{U}\mathbf{C}\mathbf{V}\mathbf{A}^{-1}-\mathbf{U}\mathbf{C}(\mathbf{C}^{-1}+\mathbf{V}\mathbf{A}^{-1}\mathbf{U})(\mathbf{C}^{-1}+\mathbf{V}\mathbf{A}^{-1}\mathbf{U})^{-1}\mathbf{V}\mathbf{A}^{-1} \\
&=\mathbf{I}+\mathbf{U}\mathbf{C}\mathbf{V}\mathbf{A}^{-1}-\mathbf{U}\mathbf{C}\mathbf{V}\mathbf{A}^{-1} \\
&=\mathbf{I}
\end{aligned}
$$

Sherman Morrison Woodbury Formula가 성립하기 위해서는 $\mathbf{A}^{-1}$와 $\mathbf{C}^{-1}$와 $(\mathbf{C}^{-1}+\mathbf{V}\mathbf{A}^{-1}\mathbf{U})^{-1}$가 존재해야 합니다.

이 글에서는 $\mathbf{A}$가 [Positive Definite Matrix](Proof-of-the-F-Test-for-Linear-Regression#Positive-Definite-Matrix)이고 $\mathbf{C}=\mathbf{I}$이고 $\mathbf{V}=\mathbf{U}^T$인 경우에 Sherman Morrison Woodbury Formula를 사용합니다. 이때 $\mathbf{A}^{-1}$와 $\mathbf{C}^{-1}$와 $(\mathbf{C}^{-1}+\mathbf{V}\mathbf{A}^{-1}\mathbf{U})^{-1}$가 존재한다는 것은 다음과 같이 확인합니다.

$\mathbf{A}$가 Positive Definite Matrix라면, $\mathbf{A}$의 Eigenvalue는 모두 Positive가 되어서, $\mathbf{A}$는 Full Rank Matrix가 되어 $\mathbf{A}^{-1}$이 존재합니다.

$\mathbf{C}=\mathbf{I}$라면 $\mathbf{C}^{-1}$가 당연히 존재합니다.

$\mathbf{A}$가 Positive Definite Matrix이기 때문에, $\mathbf{A}^{-1}$도 Positive Definite Matrix가 되며, $\mathbf{A}^{-1}$는 [Cholesky Decomposition](Proof-of-the-F-Test-for-Linear-Regression#Cholesky-Decomposition)에 의해 $\mathbf{L}\mathbf{L}^T$으로 표현할 수 있습니다.

$\mathbf{P}$를 아래와 같이 정의합니다.

$$
\mathbf{P}=\mathbf{C}^{-1}+\mathbf{V}\mathbf{A}^{-1}\mathbf{U}
$$

$\mathbf{P}\mathbf{x}=\mathbf{0}$을 만족하는 경우가 $\mathbf{x}=\mathbf{0}$이 유일한 경우라면 $\mathbf{P}^{-1}$이 존재합니다.

$\mathbf{P}\mathbf{x}=\mathbf{0}$을 만족하는 $\mathbf{x}\neq\mathbf{0}$인 $\mathbf{x}$가 존재한다면 $\mathbf{x}^T\mathbf{P}\mathbf{x}=\mathbf{0}$을 만족하는 $\mathbf{x}\neq\mathbf{0}$인 $\mathbf{x}$가 존재합니다.

$\mathbf{x}^T\mathbf{P}\mathbf{x}=\mathbf{0}$을 만족하는 $\mathbf{x}\neq\mathbf{0}$인 $\mathbf{x}$가 존재하지 않는다면 $\mathbf{P}\mathbf{x}=\mathbf{0}$을 만족하는 $\mathbf{x}\neq\mathbf{0}$인 $\mathbf{x}$가 존재하지 않습니다.

$\mathbf{x}^T\mathbf{P}\mathbf{x}=\mathbf{0}$을 만족하는 경우가 $\mathbf{x}=\mathbf{0}$이 유일한 경우라면 $\mathbf{P}\mathbf{x}=\mathbf{0}$을 만족하는 경우는 $\mathbf{x}=\mathbf{0}$이 유일한 경우입니다.

$\mathbf{x}^T\mathbf{P}\mathbf{x}=\mathbf{0}$을 만족하는 경우가 $\mathbf{x}=\mathbf{0}$이 유일한 경우라면 $\mathbf{P}^{-1}$이 존재합니다.

$$
\begin{aligned}
\mathbf{x}^T\mathbf{P}\mathbf{x}
&=\mathbf{x}^T(\mathbf{C}^{-1}+\mathbf{V}\mathbf{A}^{-1}\mathbf{U})\mathbf{x} \\
&=\mathbf{x}^T(\mathbf{I}^{-1}+\mathbf{U}^T\mathbf{A}^{-1}\mathbf{U})\mathbf{x} \\
&=\mathbf{x}^T(\mathbf{I}+\mathbf{U}^T\mathbf{L}\mathbf{L}^T\mathbf{U})\mathbf{x} \\
&=\mathbf{x}^T\mathbf{x}+(\mathbf{L}^T\mathbf{U}\mathbf{x})^T(\mathbf{L}^T\mathbf{U}\mathbf{x}) \\
&=\|\mathbf{x}\|^2+\|\mathbf{L}^T\mathbf{U}\mathbf{x}\|^2 \\
\end{aligned}
$$

$\mathbf{x}^T(\mathbf{C}^{-1}+\mathbf{V}\mathbf{A}^{-1}\mathbf{U})\mathbf{x}=\mathbf{0}$을 만족하는 경우는 $\mathbf{x}=\mathbf{0}$인 경우가 유일하므로 $(\mathbf{C}^{-1}+\mathbf{V}\mathbf{A}^{-1}\mathbf{U})^{-1}$이 존재합니다.

## SR1 Method {#SR1-Method}

$$\mathbf{x}_k$$, $$\mathbf{x}_{k+1}$$, $$\nabla f(\mathbf{x}_k)$$, $$\nabla f(\mathbf{x}_{k+1})$$를 구한 후에, $$\mathbf{s}_k$$와 $$\mathbf{y}_k$$를 구하고, [Secant Equation](#Secant-Equation)을 만족하는 $$\mathbf{B}_{k+1}$$를 구하는데 이것은 $$\mathbf{B}_k$$을 조금만 변형시켜서 구합니다. Secant Equation을 만족하는 $$\mathbf{B}_{k+1}$$는 여러가지가 존재하며 $$\mathbf{B}_k$$을 조금만 변형시키는 방법도 여러가지가 존재합니다. 여기서는 $$\mathbf{B}_{k+1}$$를 구하는 [Quasi Newton Method](#Quasi-Newton-Method)중에 하나인 SR1 Method(Symmetric Rank 1 Method)를 살펴보겠습니다.

SR1 Method는 다음과 같이 $\mathbf{B}_{k+1}$을 구할 때 $\mathbf{B}_k$을 다음과 같이 조금만 변형 시켜서 구합니다.

$$
\mathbf{B}_{k+1}=\mathbf{B}_k+a\mathbf{u}_k\mathbf{u}_k^T
$$

$a\mathbf{u}_k\mathbf{u}_k^T$은 Symmetric Matrix이고 Rank 1 Matrix입니다. $a\mathbf{u}_k\mathbf{u}_k^T$가 구체적으로 어떤 값을 가지는지 Secant Equation을 이용해서 계산해 보겠습니다.

$$
\mathbf{B}_{k+1}=\mathbf{B}_k+a\mathbf{u}_k\mathbf{u}_k^T \\
\mathbf{B}_{k+1}\mathbf{s}_k=\mathbf{y}_k \\
(\mathbf{B}_k+a\mathbf{u}_k\mathbf{u}_k^T)\mathbf{s}_k=\mathbf{y}_k \\
a\mathbf{u}_k\mathbf{u}_k^T\mathbf{s}_k=\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k \\
(a\mathbf{u}_k^T\mathbf{s}_k)\mathbf{u}_k=\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k \\
\mathbf{u}_k=\frac{\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k}{a\mathbf{u}_k^T\mathbf{s}_k} \\
\mathbf{s}_k^T(a\mathbf{u}_k^T\mathbf{s}_k)\mathbf{u}_k=\mathbf{s}_k^T(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k) \\
a(\mathbf{u}_k^T\mathbf{s}_k)(\mathbf{s}_k^T\mathbf{u}_k)=\mathbf{s}_k^T(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k) \\
a(\mathbf{u}_k^T\mathbf{s}_k)^2=\mathbf{s}_k^T(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)=(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)^T\mathbf{s}_k \\
\begin{aligned}
\mathbf{B}_{k+1}
&=\mathbf{B}_k+a\mathbf{u}_k\mathbf{u}_k^T \\
&=\mathbf{B}_k+a\frac{(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)}{a\mathbf{u}_k^T\mathbf{s}_k}\frac{(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)^T}{a\mathbf{u}_k^T\mathbf{s}_k} \\
&=\mathbf{B}_k+\frac{(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)^T}{a(\mathbf{u}_k^T\mathbf{s}_k)^2} \\
&=\mathbf{B}_k+\frac{(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)^T}{(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)^T\mathbf{s}_k}
\end{aligned}
$$

정리하면 다음과 같습니다.

$$
\mathbf{B}_{k+1}=\mathbf{B}_k+\frac{(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)^T}{(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)^T\mathbf{s}_k}
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
\mathbf{U}=\sqrt{a}\mathbf{u}_{k} \\
\mathbf{V}=\sqrt{a}\mathbf{u}_{k}^T \\
\begin{aligned}
\mathbf{H}_{k+1}
&=\mathbf{B}_{k+1}^{-1} \\
&=(\mathbf{B}_k+a\mathbf{u}_k\mathbf{u}_k^T)^{-1} \\
&=\mathbf{B}_k^{-1}-\frac{\mathbf{B}_k^{-1}\sqrt{a}\mathbf{u}_k\sqrt{a}\mathbf{u}_k^T\mathbf{B}_k^{-1}}{1+\sqrt{a}\mathbf{u}_k^T\mathbf{B}_k^{-1}\sqrt{a}\mathbf{u}_k} \\
&=\mathbf{H}_k-\frac{a\mathbf{H}_k\mathbf{u}_k\mathbf{u}_k^T\mathbf{H}_k}{1+a\mathbf{u}_k^T\mathbf{H}_k\mathbf{u}_k} \\
&=\mathbf{H}_k-\frac{a\mathbf{H}_k\frac{(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)}{a\mathbf{u}_k^T\mathbf{s}_k}\frac{(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)^T}{a\mathbf{u}_k^T\mathbf{s}_k}\mathbf{H}_k}{1+a\frac{(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)^T}{a\mathbf{u}_k^T\mathbf{s}_k}\mathbf{H}_k\frac{(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)}{a\mathbf{u}_k^T\mathbf{s}_k}} \\
&=\mathbf{H}_k-\frac{(\mathbf{H}_k\mathbf{y}_k-\mathbf{s}_k)(\mathbf{H}_k\mathbf{y}_k-\mathbf{s}_k)^T}{a(\mathbf{u}_k^T\mathbf{s}_k)^2+(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)^T(\mathbf{H}_k\mathbf{y}_k-\mathbf{s}_k)} \\
&=\mathbf{H}_k-\frac{(\mathbf{H}_k\mathbf{y}_k-\mathbf{s}_k)(\mathbf{H}_k\mathbf{y}_k-\mathbf{s}_k)^T}{(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)^T\mathbf{s}_k+(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)^T(\mathbf{H}_k\mathbf{y}_k-\mathbf{s}_k)} \\
&=\mathbf{H}_k-\frac{(\mathbf{H}_k\mathbf{y}_k-\mathbf{s}_k)(\mathbf{H}_k\mathbf{y}_k-\mathbf{s}_k)^T}{(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)^T\mathbf{s}_k+(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)^T\mathbf{H}_k\mathbf{y}_k-(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)^T\mathbf{s}_k} \\
&=\mathbf{H}_k-\frac{(\mathbf{H}_k\mathbf{y}_k-\mathbf{s}_k)(\mathbf{H}_k\mathbf{y}_k-\mathbf{s}_k)^T}{(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)^T\mathbf{H}_k\mathbf{y}_k} \\
&=\mathbf{H}_k-\frac{(\mathbf{H}_k\mathbf{y}_k-\mathbf{s}_k)(\mathbf{H}_k\mathbf{y}_k-\mathbf{s}_k)^T}{(\mathbf{H}_k\mathbf{y}_k-\mathbf{s}_k)^T\mathbf{y}_k} \\
&=\mathbf{H}_k+\frac{(\mathbf{s}_k-\mathbf{H}_k\mathbf{y}_k)(\mathbf{s}_k-\mathbf{H}_k\mathbf{y}_k)^T}{(\mathbf{s}_k-\mathbf{H}_k\mathbf{y}_k)^T\mathbf{y}_k} \\
\end{aligned}
$$

정리하면 다음과 같습니다.

$$
\mathbf{H}_{k+1}=\mathbf{H}_k+\frac{(\mathbf{s}_k-\mathbf{H}_k\mathbf{y}_k)(\mathbf{s}_k-\mathbf{H}_k\mathbf{y}_k)^T}{(\mathbf{s}_k-\mathbf{H}_k\mathbf{y}_k)^T\mathbf{y}_k}
$$

SR1 Method에는 몇 가지 단점이 있습니다.

$$(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)^T\mathbf{s}_k \approx 0$$이 되면 $$\mathbf{B}_{k+1}=\mathbf{B}_k+\frac{(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)^T}{(\mathbf{y}_k-\mathbf{B}_k\mathbf{s}_k)^T\mathbf{s}_k}$$에서 분모가 $0$이 되기 때문에 $$\mathbf{B}_{k+1}$$과 $$\mathbf{H}_{k+1}$$을 안정적으로 구할 수 없습니다.

그리고 Newton's Method에서 $f(\mathbf{x})$의 최소값을 구하기 위해서는 $\nabla^2 f(\mathbf{x}_k)$이 Positive Definite Matrix가 되어야 하기 때문에 Quasi Newton Method에서도 $\mathbf{B}_k$와 $\mathbf{H}_k$가 Positive Definite Matrix가 되어야 합니다. 하지만 SR1 Method에서는 $\mathbf{B}_k$와 $\mathbf{H}_k$가 Positive Definite Matrix임을 보장하지 않습니다.

## Conclusion {#Conclusion}

이 글에서는 LBFGS Method를 살펴보기 위한 과정으로 SR1 Method에 대해 살펴보았습니다.

SR1 Method는 $\mathbf{H}_{k+1}$을 안정적으로 구할 수 없는 문제가 있습니다.

[Derivation of LBFGS Part 3 - BFGS Method](Derivation-of-LBFGS-Part-3)에서는 안정적으로 $\mathbf{H}_{k+1}$을 구하는 방법을 알아보도록 하겠습니다.
