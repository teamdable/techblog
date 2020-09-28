---
layout: post
title:  "Derivation of LBFGS Part 4 - LBFGS Method"
date:   2020-09-27 23:00:00 +0900
author: Taeho Oh
tags: [ 오태호, 머신러닝 ]
---

안녕하세요. 오태호입니다.

이 글에서는 Optimization 기법중에 하나인 LBFGS Method(Limited Memory Broyden–Fletcher–Goldfarb–Shanno Method)의 수식을 다음과 같이 4개의 Part에 걸쳐서 차근차근 유도하여 LBFGS Method의 구조를 조금 깊게 살펴보도록 하겠습니다.

* [Derivation of LBFGS Part 1 - Newton's Method](Derivation-of-LBFGS-Part-1)
* [Derivation of LBFGS Part 2 - SR1 Method](Derivation-of-LBFGS-Part-2)
* [Derivation of LBFGS Part 3 - BFGS Method](Derivation-of-LBFGS-Part-3)
* Derivation of LBFGS Part 4 - LBFGS Method

## LBFGS Method {#LBFGS-Method}

[Quasi Newton Method](Derivation-of-LBFGS-Part-2#Quasi-Newton-Method)중에 하나인 [BFGS Method](Derivation-of-LBFGS-Part-3#BFGS-Method)는 $$\mathbf{H}_k$$의 크기가 너무 커서 저장이 쉽지 않은 문제가 있습니다. 여기서는 $$\mathbf{H}_k$$를 저장하지 않고 BFGS Method를 사용하는 LBFGS Method(Limited Memory Broyden Fletcher Goldfarb Shanno Method)를 살펴보겠습니다.

앞에서 정의했던 각종 수식을 다시 정리하면 다음과 같습니다.

$$
\mathbf{x}=
\begin{bmatrix}
x_1 \\
x_2 \\
\vdots \\
x_n
\end{bmatrix} \\
\nabla f(\mathbf{x})=
\begin{bmatrix}
\frac{\partial}{\partial x_1}f(\mathbf{x}) \\
\frac{\partial}{\partial x_2}f(\mathbf{x}) \\
\vdots \\
\frac{\partial}{\partial x_n}f(\mathbf{x}) \\
\end{bmatrix} \\
\nabla^2 f(\mathbf{x})=
\begin{bmatrix}
\frac{\partial^2}{\partial x_1^2}f(\mathbf{x}) & \frac{\partial^2}{\partial x_1 \partial x_2}f(\mathbf{x}) & \cdots & \frac{\partial^2}{\partial x_1 \partial x_n}f(\mathbf{x}) \\
\frac{\partial^2}{\partial x_2 x_1}f(\mathbf{x}) & \frac{\partial^2}{\partial x_2^2}f(\mathbf{x}) & \cdots & \frac{\partial^2}{\partial x_2 \partial x_n}f(\mathbf{x}) \\
\vdots & \vdots & \ddots & \vdots \\
\frac{\partial^2}{\partial x_n x_1}f(\mathbf{x}) & \frac{\partial^2}{\partial x_n x_2}f(\mathbf{x}) & \cdots & \frac{\partial^2}{\partial x_n^2}f(\mathbf{x}) \\
\end{bmatrix} \\
\mathbf{s}_k=\mathbf{x}_{k+1}-\mathbf{x}_k \\
\mathbf{g}_k=\nabla f(\mathbf{x}_{k}) \\
\mathbf{y}_k=\mathbf{g}_{k+1}-\mathbf{g}_k \\
\mathbf{B}_k \approx \nabla^2 f(\mathbf{x}_k) \\
\mathbf{H}_k=\mathbf{B}_k^{-1}
$$

Quasi Newton Method를 다시 살펴보면 다음과 같습니다.

$$
\begin{aligned}
\mathbf{x}_{k+1}=\mathbf{x}_k-t_k\mathbf{H}_k\mathbf{g}_k
\end{aligned}
$$

BFGS Method를 다시 살펴보면 다음과 같습니다.

$$
\begin{aligned}
\mathbf{B}_{k+1}
&=\mathbf{B}_k+a\mathbf{u}_k\mathbf{u}_k^T+b\mathbf{v}_k\mathbf{v}_k^T \\
&=\mathbf{B}_k-\frac{\mathbf{B}_k\mathbf{s}_k\mathbf{s}_k^T\mathbf{B}_k}{\mathbf{s}_k^T\mathbf{B}_k\mathbf{s}_k}+\frac{\mathbf{y}_k\mathbf{y}_k^T}{\mathbf{y}_k^T\mathbf{s}_k}
\end{aligned} \\
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

BFGS Method를 설명할 때 $$\mathbf{H}_k$$를 구하는 방법을 알아보았습니다. 그런데 Quasi Newton Method를 자세히 살펴보면 결국 필요한 것은 $$\mathbf{H}_k$$가 아니라 $$\mathbf{H}_k\mathbf{g}_k$$입니다. $$\mathbf{x}$$가 $$n$$차원 Vector일 때 $$\mathbf{H}_k$$를 저장하기 위해서는 $$n^2$$ Element의 Memory가 필요하지만 $$\mathbf{H}_k\mathbf{g}_k$$는 $$n$$ Element의 Memory만이 필요합니다. 그리고 $$\mathbf{H}_k$$는 Iteration마다 $$n$$차원 Vector 2개를($$\mathbf{u}_k$$와 $$\mathbf{v}_k$$를) 사용해서 Update를 하기 때문에 $$\mathbf{H}_k$$의 변화정보를 $$n \times 2$$ Element의 저장공간에 저장할 수 있습니다. 이런 특징을 보면 $$\mathbf{H}_k$$의 $$n^2$$ Element의 저장공간보다 훨씬 적은 저장공간을 사용하면서 BFGS Method를 사용할 수 있는 방법이 있을 것으로 상상할 수 있습니다. 이런 특징을 활용한 방법이 LBFGS Method입니다.

BFGS Method를 좀 더 간결하게 표현하기 위해 $$\rho_k$$를 다음과 같이 정의합니다.

$$
\rho_k=\frac{1}{\mathbf{y}_k^T\mathbf{s}_k}
$$

$$\rho_k$$를 이용해서 BFGS Method를 다음과 같이 간결하게 표현합니다.

$$
\mathbf{H}_{k+1}
=\left (
\mathbf{I}-
\rho_k\mathbf{s}_k\mathbf{y}_k^T
\right )
\mathbf{H}_k
\left (
\mathbf{I}-
\rho_k\mathbf{y}_k\mathbf{s}_k^T
\right )
+
\rho_k\mathbf{s}_k\mathbf{s}_k^T
$$

$$\mathbf{H}_k$$는 다음과 같습니다.

$$
\mathbf{H}_k
=\left (
\mathbf{I}-
\rho_{k-1}\mathbf{s}_{k-1}\mathbf{y}_{k-1}^T
\right )
\mathbf{H}_{k-1}
\left (
\mathbf{I}-
\rho_{k-1}\mathbf{y}_{k-1}\mathbf{s}_{k-1}^T
\right )
+
\rho_{k-1}\mathbf{s}_{k-1}\mathbf{s}_{k-1}^T
$$

BFGS는 $$\mathbf{H}_k$$를 구하려고 노력하지만, LBFGS Method는 $$\mathbf{H}_k$$대신에 다음과 같이 $$\mathbf{H}_k\mathbf{g}_k$$를 구하려고 노력합니다.

$$
\mathbf{H}_k\mathbf{g}_k
=\left (
\mathbf{I}-
\rho_{k-1}\mathbf{s}_{k-1}\mathbf{y}_{k-1}^T
\right )
\mathbf{H}_{k-1}
\left (
\mathbf{I}-
\rho_{k-1}\mathbf{y}_{k-1}\mathbf{s}_{k-1}^T
\right )\mathbf{g}_k
+
\rho_{k-1}\mathbf{s}_{k-1}\mathbf{s}_{k-1}^T\mathbf{g}_k
$$

이 식을 살펴보면 $$\mathbf{H}_k\mathbf{g}_k$$를 최대한 정확하게 구하기 위해서는 이전 Iteration인 $$\mathbf{H}_{k-1}$$을 최대한 정확하게 구해야 합니다. 그리고 $$\mathbf{H}_{k-1}$$을 최대한 정확하게 구하기 위해서는 $$\mathbf{H}_{k-2}$$을 최대한 정확하게 구해야 합니다. 하지만 그렇다고 해도 $$\mathbf{H}_{k-1000}$$ 같이 상당히 이전 Iteration 정보가 중요하지는 않습니다. 그래서 LBFGS Method에서는 적당히 이전 Iteration 정보까지만을 사용해서 $$\mathbf{H}_k\mathbf{g}_k$$를 구하려고 노력합니다. 얼마나 이전 Iteration 정보를 사용하는가를 History Size라고 합니다. History Size가 클수록 Memory를 많이 사용하게 되고 계산결과가 더 정확해집니다.

History Size가 $2$인 경우의 $$\mathbf{H}_k\mathbf{g}_k$$를 계산해서 규칙성을 찾아보겠습니다.

$$
\begin{aligned}

\mathbf{H}_k\mathbf{g}_k
&=(\mathbf{I}-\rho_{k-1}\mathbf{s}_{k-1}\mathbf{y}_{k-1}^T)\mathbf{H}_{k-1}(\mathbf{I}-\rho_{k-1}\mathbf{y}_{k-1}\mathbf{s}_{k-1}^T)\mathbf{g}_k+\rho_{k-1}\mathbf{s}_{k-1}\mathbf{s}_{k-1}^T\mathbf{g}_k \\
&=(\mathbf{I}-\rho_{k-1}\mathbf{s}_{k-1}\mathbf{y}_{k-1}^T)((\mathbf{I}-\rho_{k-2}\mathbf{s}_{k-2}\mathbf{y}_{k-2}^T)\mathbf{H}_{k-2}(\mathbf{I}-\rho_{k-2}\mathbf{y}_{k-2}\mathbf{s}_{k-2}^T)+\rho_{k-2}\mathbf{s}_{k-2}\mathbf{s}_{k-2}^T)(\mathbf{I}-\rho_{k-1}\mathbf{y}_{k-1}\mathbf{s}_{k-1}^T)\mathbf{g}_k+\rho_{k-1}\mathbf{s}_{k-1}\mathbf{s}_{k-1}^T\mathbf{g}_k \\
\end{aligned} \\

\mathbf{q}_k=\mathbf{g}_k \\
\alpha_{k-1}=\rho_{k-1}\mathbf{s}_{k-1}^T\mathbf{q}_k \\
\mathbf{q}_{k-1}=\mathbf{q}_k-\alpha_{k-1}\mathbf{y}_{k-1} \\

\mathbf{H}_k\mathbf{g}_k
=(\mathbf{I}-\rho_{k-1}\mathbf{s}_{k-1}\mathbf{y}_{k-1}^T)((\mathbf{I}-\rho_{k-2}\mathbf{s}_{k-2}\mathbf{y}_{k-2}^T)\mathbf{H}_{k-2}(\mathbf{I}-\rho_{k-2}\mathbf{y}_{k-2}\mathbf{s}_{k-2}^T)+\rho_{k-2}\mathbf{s}_{k-2}\mathbf{s}_{k-2}^T)\mathbf{q}_{k-1}+\alpha_{k-1}\mathbf{s}_{k-1} \\

\alpha_{k-2}=\rho_{k-2}\mathbf{s}_{k-2}^T\mathbf{q}_{k-1} \\
\mathbf{q}_{k-2}=\mathbf{q}_{k-1}-\alpha_{k-2}\mathbf{y}_{k-2} \\

\mathbf{H}_k\mathbf{g}_k
=(\mathbf{I}-\rho_{k-1}\mathbf{s}_{k-1}\mathbf{y}_{k-1}^T)((\mathbf{I}-\rho_{k-2}\mathbf{s}_{k-2}\mathbf{y}_{k-2}^T)\mathbf{H}_{k-2}\mathbf{q}_{k-2}+\alpha_{k-2}\mathbf{s}_{k-2})+\alpha_{k-1}\mathbf{s}_{k-1} \\

\mathbf{r}_{k-2}=\mathbf{H}_{k-2}\mathbf{q}_{k-2} \\
\beta_{k-2}=\rho_{k-2}\mathbf{y}_{k-2}^T\mathbf{r}_{k-2} \\

\mathbf{H}_k\mathbf{g}_k
=(\mathbf{I}-\rho_{k-1}\mathbf{s}_{k-1}\mathbf{y}_{k-1}^T)(\mathbf{r}_{k-2}-\beta_{k-2}\mathbf{s}_{k-2}+\alpha_{k-2}\mathbf{s}_{k-2})+\alpha_{k-1}\mathbf{s}_{k-1} \\

\mathbf{r}_{k-1}=\mathbf{r}_{k-2}+(\alpha_{k-2}-\beta_{k-2})\mathbf{s}_{k-2} \\
\beta_{k-1}=\rho_{k-1}\mathbf{y}_{k-1}^T\mathbf{r}_{k-1} \\

\mathbf{H}_k\mathbf{g}_k
=\mathbf{r}_{k-1}-\beta_{k-1}\mathbf{s}_{k-1}+\alpha_{k-1}\mathbf{s}_{k-1} \\

\mathbf{r}_{k}=\mathbf{r}_{k-1}+(\alpha_{k-1}-\beta_{k-1})\mathbf{s}_{k-1} \\

\begin{aligned}
\mathbf{H}_k\mathbf{g}_k
&=\mathbf{r}_k \\
&=\mathbf{r}_{k-1}+(\alpha_{k-1}-\beta_{k-1})\mathbf{s}_{k-1} \\
&=\mathbf{r}_{k-2}+(\alpha_{k-2}-\beta_{k-2})\mathbf{s}_{k-2}+(\alpha_{k-1}-\beta_{k-1})\mathbf{s}_{k-1} \\
&=\mathbf{H}_{k-2}\mathbf{q}_{k-2}+(\alpha_{k-2}-\beta_{k-2})\mathbf{s}_{k-2}+(\alpha_{k-1}-\beta_{k-1})\mathbf{s}_{k-1} \\
\end{aligned}
$$

여기서 $$\mathbf{H}_{k-2}$$에는 적당한 Matrix를 넣어줍니다. History Size가 큰 경우에는 $$\mathbf{I}$$를 넣어도 큰 문제가 없지만 LBFGS Method에서는 보통 Heuristic으로 $$\frac{\mathbf{s}_{k-1}^T\mathbf{y}_{k-1}}{\mathbf{y}_{k-1}^T\mathbf{y}_{k-1}}\mathbf{I}$$를 많이 사용합니다. 보통 이런 Heuristic을 사용하는 이유는 [Initial Inverse Hessian](#Initial-Inverse-Hessian)를 참조하기 바랍니다.

위에서 알아본 History Size 2의 $$\mathbf{H}_k\mathbf{g}_k$$의 계산과정을 일반화하여 History Size가 $$m$$일 때 계산과정을 정리하면 다음과 같습니다.

* $$\mathbf{q}_k \leftarrow \mathbf{g}_k$$
* For $$i=k-1,k-2,\cdots,k-m$$
  * $$\alpha_i \leftarrow \rho_i\mathbf{s}_i^T\mathbf{q}_{i+1}$$
  * $$\mathbf{q}_i \leftarrow \mathbf{q}_{i+1} - \alpha_i\mathbf{y}_i$$
* $$\gamma_k \leftarrow \frac{\mathbf{s}_{k-1}^T\mathbf{y}_{k-1}}{\mathbf{y}_{k-1}^T\mathbf{y}_{k-1}}\mathbf{I}$$
* $$\mathbf{H}_{k-m} \leftarrow \gamma_k\mathbf{I}$$
* $$\mathbf{r}_{k-m} \leftarrow \mathbf{H}_{k-m}\mathbf{q}_{k-m}$$
* For $$i=k-m,k-m+1,\cdots,k-1$$
  * $$\beta_i \leftarrow \rho_i\mathbf{y}_i^T\mathbf{r}_i$$
  * $$\mathbf{r}_{i+1} \leftarrow \mathbf{r}_i+(\alpha_i-\beta_i)\mathbf{s}_i$$
* $$\mathbf{H}_k\mathbf{g}_k \leftarrow \mathbf{r}_k$$

그런데 여기서 자세히 살펴보면 $$\mathbf{q}_i$$와 $$\mathbf{r}_i$$는 굳이 Index별로 여러 개를 저장할 필요가 없습니다. 그래서 아래와 같이 더 간단하게 정리할 수 있습니다.

* $$\mathbf{q} \leftarrow \mathbf{g}_k$$
* For $$i=k-1,k-2,\cdots,k-m$$
  * $$\alpha_i \leftarrow \rho_i\mathbf{s}_i^T\mathbf{q}$$
  * $$\mathbf{q} \leftarrow \mathbf{q} - \alpha_i\mathbf{y}_i$$
* $$\gamma_k \leftarrow \frac{\mathbf{s}_{k-1}^T\mathbf{y}_{k-1}}{\mathbf{y}_{k-1}^T\mathbf{y}_{k-1}}\mathbf{I}$$
* $$\mathbf{H}_{k-m} \leftarrow \gamma_k\mathbf{I}$$
* $$\mathbf{r} \leftarrow \mathbf{H}_{k-m}\mathbf{q}$$
* For $$i=k-m,k-m+1,\cdots,k-1$$
  * $$\beta_i \leftarrow \rho_i\mathbf{y}_i^T\mathbf{r}$$
  * $$\mathbf{r} \leftarrow \mathbf{r}+(\alpha_i-\beta_i)\mathbf{s}_i$$
* $$\mathbf{H}_k\mathbf{g}_k \leftarrow \mathbf{r}$$

LBFGS Method는 이와 같이 $$\mathbf{H}_k\mathbf{g}_k$$를 직접 계산하고 다음의 Iteration을 수행하는 것을 반복하여 $$f(\mathbf{x})$$를 최소화시키는 $$\mathbf{x}$$를 구하는 방법입니다. 이때, $$t_k$$는 [Wolfe Conditions](Derivation-of-LBFGS-Part-1#Wolfe-Conditions)를 사용해서 구한 적절한 값을 사용합니다.

$$
\mathbf{x}_{k+1}=\mathbf{x}_k-t_k\mathbf{H}_k\mathbf{g}_k
$$

BFGS Method는 $$\mathbf{H}_k$$를 계산하고 이것을 이용해 $$\mathbf{H}_k\mathbf{g}_k$$을 계산하기 때문에 Memory 사용량이 매우 높지만 LBFGS Method는 $$\mathbf{H}_k\mathbf{g}_k$$를 직접 계산하여 Memory 사용량을 BFGS Method에 비해 크게 낮출 수 있습니다.

## Initial Inverse Hessian {#Initial-Inverse-Hessian}

[LBFGS Method](#LBFGS-Method)을 살펴보면 Initial Inverse Hessian $$\mathbf{H}_{k-m}$$가 필요합니다. History Size가 큰 경우에는 $$\mathbf{I}$$를 사용해도 무방하지만 조금 더 개선된 Heuristic으로 다음과 같이 $$\mathbf{H}_{k-m}$$를 구해서 사용하는 경우가 많습니다. $$\mathbf{G}_{k-1}$$을 Hessian의 근사치라고 정의합니다.

$$
\mathbf{G}_{k-1}\mathbf{s}_{k-1}=\mathbf{y}_{k-1} \\
\mathbf{z}_{k-1}=\sqrt{\mathbf{G}_{k-1}}\mathbf{s}_{k-1} \\
\mathbf{y}_{k-1}=\mathbf{G}_{k-1}\mathbf{s}_{k-1}=\sqrt{\mathbf{G}_{k-1}}\mathbf{z}_{k-1} \\
\mathbf{s}_{k-1}=\frac{1}{\sqrt{\mathbf{G}_{k-1}}}\mathbf{z}_{k-1} \\
\begin{aligned}
\frac{\mathbf{s}_{k-1}^T\mathbf{y}_{k-1}}{\mathbf{y}_{k-1}^T\mathbf{y}_{k-1}}\mathbf{I}
&=\frac{(\frac{1}{\sqrt{\mathbf{G}_{k-1}}}\mathbf{z}_{k-1})^T(\sqrt{\mathbf{G}_{k-1}}\mathbf{z}_{k-1})}{(\sqrt{\mathbf{G}_{k-1}}\mathbf{z}_{k-1})^T(\sqrt{\mathbf{G}_{k-1}}\mathbf{z}_{k-1})}\mathbf{I} \\
&=\frac{\mathbf{z}_{k-1}^T\mathbf{z}_{k-1}}{\mathbf{z}_{k-1}^T\mathbf{G}_{k-1}\mathbf{z}_{k-1}}\mathbf{I}
\end{aligned}
$$

자세히 살펴보면 $$\frac{\mathbf{z}_{k-1}^T\mathbf{G}_{k-1}\mathbf{z}_{k-1}}{\mathbf{z}_{k-1}^T\mathbf{z}_{k-1}}\mathbf{I}$$의 Eigenvalue는 Hessian의 Eigenvalue와 유사하기 때문에 $$\frac{\mathbf{z}_{k-1}^T\mathbf{z}_{k-1}}{\mathbf{z}_{k-1}^T\mathbf{G}_{k-1}\mathbf{z}_{k-1}}\mathbf{I}$$의 Eigenvalue는 Inverse Hessian의 Eigenvalue와 유사하게 됩니다. 즉, $$\frac{\mathbf{s}_{k-1}^T\mathbf{y}_{k-1}}{\mathbf{y}_{k-1}^T\mathbf{y}_{k-1}}\mathbf{I}$$의 Eigenvalue는 Inverse Hessian의 Eigenvalue와 유사하게 되므로 $$\frac{\mathbf{s}_{k-1}^T\mathbf{y}_{k-1}}{\mathbf{y}_{k-1}^T\mathbf{y}_{k-1}}\mathbf{I}$$을 Initial Inverse Hessian으로 사용합니다.

## Conclusion {#Conclusion}

LBFGS Method를 처음부터 차근차근 유도해 보았습니다. 이 글이 LBFGS Method를 이해하는데 유용한 자료로 사용되기를 희망합니다.
