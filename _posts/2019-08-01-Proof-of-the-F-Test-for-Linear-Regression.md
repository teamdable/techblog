---
layout: post
title:  "Proof of the F Test for Linear Regression"
date:   2019-08-01 23:00:00 +0900
author: Taeho Oh
tags: [ 오태호, 수학, 통계학 ]
---
안녕하세요. 오태호입니다.

Linear Regression에서 Predictor와 Response가 얼마나 관계가 있는지 조사하는 방법으로 F Test를 사용합니다. Linear Regression 관련 책을 살펴보면 F Test의 식의 유도과정이 생략되어 있는 경우가 많아서 이해가 쉽지 않은 경우가 많습니다. 그래서 이번 글에서는 Linear Regression의 F Test 식을 유도해 보도록 하겠습니다. Linear Regression의 다른 수식에서도 흔히 접할 수 있는 Degree of Freedom의 의미도 이해하기가 쉽지 않은데 이 글을 통해 조금이라도 이해에 도움이 되었으면 좋겠습니다.

증명과정중에 Matrix나 Vector는 굵은 글꼴로 표현하도록 하겠습니다. 그리고 Vector는 특별히 언급이 없으면 Column Vector를 의미합니다.

## Trace {#Trace}

* $n \times n$인 $\mathbf{A}$의 Trace는 아래와 같이 정의합니다.

  $$
  tr(\mathbf{A})=\sum_{i=1}^n a_{ii}
  $$

* $tr(\mathbf{AB})$는 아래와 같은 성질이 있습니다.

  $$
  \begin{aligned}
  tr(\mathbf{AB})
  &=(\mathbf{AB})_{11}+(\mathbf{AB})_{22}+\cdots+(\mathbf{AB})_{nn} \\
  &=a_{11}b_{11}+a_{12}b_{21}+\cdots+a_{1k}b_{k1} \\
  &+a_{21}b_{12}+a_{22}b_{22}+\cdots+a_{2k}b_{k2} \\
  &+\vdots \\
  &+a_{n1}b_{1n}+a_{n2}b_{2n}+\cdots+a_{nk}b_{kn} \\
  &=a_{11}b_{11}+a_{21}b_{12}+\cdots+a_{n1}b_{1n} \\
  &+a_{12}b_{21}+a_{22}b_{22}+\cdots+a_{n2}b_{2n} \\
  &+\vdots \\
  &+a_{1k}b_{k1}+a_{2k}b_{k2}+\cdots+a_{nk}b_{kn} \\
  &=(\mathbf{BA})_{11}+(\mathbf{BA})_{22}+\cdots+(\mathbf{BA})_{kk} \\
  &=tr(\mathbf{BA})
  \end{aligned}
  $$

* $\mathbf{A}$가 Eigen Decomposition을 통해 $\mathbf{Q\Lambda}\mathbf{Q}^{-1}$로 표현될 수 있다면 $tr(\mathbf{A})$를 아래와 같이 Eigenvalue의 합으로 구할 수 있습니다.

  $$
  \begin{aligned}
  tr(\mathbf{A})
  &=tr(\mathbf{Q\Lambda}\mathbf{Q}^{-1}) \\
  &=tr((\mathbf{Q\Lambda})\mathbf{Q}^{-1}) \\
  &=tr(\mathbf{Q}^{-1}(\mathbf{Q\Lambda})) \\
  &=tr(\mathbf{\Lambda}) \\
  &=\lambda_1 + \lambda_2 + \cdots + \lambda_n \\
  \end{aligned}
  $$

## Positive Definite Matrix {#Positive-Definite-Matrix}

* 임의의 Vector $\mathbf{x}$에 대해 아래와 같은 성질을 만족하는 Symmetric Matrix $\mathbf{A}$를 Positive Definite Matrix라고 정의합니다.

  $$
  \mathbf{x}^T\mathbf{A}\mathbf{x} \gt 0
  $$

* Positive Definite Matrix $\mathbf{A}$가 Eigen Decomposition을 통해 $\mathbf{Q\Lambda}\mathbf{Q}^{-1}$로 표현될 수 있다면 아래와 같이 $\mathbf{A}$의 모든 Eigenvalue가 $0$보다 크다는 것을 알 수 있습니다. 참고로 $\mathbf{A}$는 Symmetric Matrix이므로 $\mathbf{A}$의 Eigenvector로 이루어진 $\mathbf{Q}$는 Orthogonal Matrix이므로 $\mathbf{Q}^{-1}=\mathbf{Q}^T$가 성립합니다.

  $$
  \begin{aligned}
  \mathbf{x}^T\mathbf{A}\mathbf{x}
  &=\mathbf{x}^T\mathbf{Q}\mathbf{\Lambda}\mathbf{Q}^{-1}\mathbf{x} \\
  &=\mathbf{x}^T\mathbf{Q}\mathbf{\Lambda}\mathbf{Q}^T\mathbf{x} \\
  &=\mathbf{y}^T\mathbf{\Lambda}\mathbf{y} & \text{ } (\mathbf{y}=\mathbf{Q}^T\mathbf{x}) \\
  &=y_1^2\lambda_1+y_2^2\lambda_2+\cdots+y_n^2\lambda_n \gt 0
  \end{aligned}
  $$

  임의의 Vector $\mathbf{y}$에 대해 만족하기 위해서는 모든 Eigenvalue가 $0$보다 커야 합니다.

## LDLT Decomposition {#LDLT-Decomposition}

$\mathbf{A}$가 Symmetric일 때 LDU Decomposition의 결과에 $\mathbf{U}=\mathbf{L}^T$라는 사실을 이용한 Decomposition을 LDLT Decomposition이라고 정의합니다.

$$
\begin{aligned}
\mathbf{A}
&=\mathbf{LDU} \\
&=\mathbf{LD}\mathbf{L}^T \\
\end{aligned}
$$

## Cholesky Decomposition {#Cholesky-Decomposition}

$\mathbf{A}$가 Positive Definite일 때 모든 Eigenvalue가 $0$보다 큰 사실을 이용해서 LDLT Decomposition의 결과에서 $\mathbf{L}\mathbf{L}^T$로 Decomposition을 하는 것을 Cholesky Decomposition이라고 정의합니다.

$$
\begin{aligned}
\mathbf{A}
&=\mathbf{L}'\mathbf{D}\mathbf{L}'^T \\
&=\mathbf{L}'\mathbf{D}^{\frac{1}{2}}\mathbf{D}^{\frac{1}{2}}\mathbf{L}'^T \\
&=\mathbf{L}\mathbf{L}^T & \text{ } (\mathbf{L}=\mathbf{L}'\mathbf{D}^{\frac{1}{2}})
\end{aligned}
$$

## Idempotent Matrix {#Idempotent-Matrix}

* 아래와 같은 성질을 만족하는 $\mathbf{A}$를 Idempotent Matrix라고 정의합니다.

  $$
  \mathbf{A}^2=\mathbf{A}
  $$

* $\mathbf{A}$가 Idempotent Matrix이고 임의의 Eigenvalue를 $\lambda$라 하고 임의의 Eigenvector를 $\mathbf{x}$라고 할 때 $rank(\mathbf{A})$를 다음과 같이 구할 수 있습니다.

  $$
  \begin{aligned}
  \lambda\mathbf{x}
  &=\mathbf{Ax} \\
  &=\mathbf{A}^2\mathbf{x} \\
  &=\mathbf{A}(\mathbf{Ax}) \\
  &=\mathbf{A}(\lambda\mathbf{x}) \\
  &=\lambda(\mathbf{Ax}) \\
  &=\lambda(\lambda\mathbf{x}) \\
  &=\lambda^2\mathbf{x} \\
  \end{aligned} \\
  \lambda=\lambda^2 \\
  \lambda=0 \text{ or } 1 \\
  rank(\mathbf{A})=tr(\mathbf{A})
  $$

## Simultaneously Diagonalizable Matrix {#Simultaneously-Diagonalizable-Matrix}

Matirx $\mathbf{A}$, $\mathbf{B}$가 같은 Eigenvector로 Diagonalize가 가능하면 Simultaneously Diagonalizable라고 정의합니다.

* $\mathbf{A}$, $\mathbf{B}$가 Simultaneously Diagonalizable하면 $\mathbf{AB}=\mathbf{BA}$를 만족하는 것은 다음과 같이 증명할 수 있습니다.

  $$
  \mathbf{P}^{-1}\mathbf{A}\mathbf{P}=
  \begin{bmatrix}
  \lambda_1 & 0 & \cdots & 0 \\
  0 & \lambda_2 & \cdots & 0 \\
  \vdots & \vdots & \ddots & \vdots \\
  0 & 0 & \cdots & \lambda_n
  \end{bmatrix} \\
  \mathbf{P}^{-1}\mathbf{B}\mathbf{P}=
  \begin{bmatrix}
  \mu_1 & 0 & \cdots & 0 \\
  0 & \mu_2 & \cdots & 0 \\
  \vdots & \vdots & \ddots & \vdots \\
  0 & 0 & \cdots & \mu_n
  \end{bmatrix} \\
  \mathbf{P}^{-1}\mathbf{A}\mathbf{P}\mathbf{P}^{-1}\mathbf{B}\mathbf{P}
  =\mathbf{P}^{-1}\mathbf{A}\mathbf{B}\mathbf{P}
  =
  \begin{bmatrix}
  \lambda_1\mu_1 & 0 & \cdots & 0 \\
  0 & \lambda_2\mu_2 & \cdots & 0 \\
  \vdots & \vdots & \ddots & \vdots \\
  0 & 0 & \cdots & \lambda_n\mu_n
  \end{bmatrix} \\
  \mathbf{P}^{-1}\mathbf{B}\mathbf{P}\mathbf{P}^{-1}\mathbf{A}\mathbf{P}
  =\mathbf{P}^{-1}\mathbf{B}\mathbf{A}\mathbf{P}
  =
  \begin{bmatrix}
  \mu_1\lambda_1 & 0 & \cdots & 0 \\
  0 & \mu_2\lambda_2 & \cdots & 0 \\
  \vdots & \vdots & \ddots & \vdots \\
  0 & 0 & \cdots & \mu_n\lambda_n
  \end{bmatrix} \\
  \mathbf{P}^{-1}\mathbf{A}\mathbf{B}\mathbf{P}=\mathbf{P}^{-1}\mathbf{B}\mathbf{A}\mathbf{P} \\
  \mathbf{A}\mathbf{B}=\mathbf{B}\mathbf{A}
  $$

* $\mathbf{AB}=\mathbf{BA}$를 만족하고 $\mathbf{A}$의 모든 Eigenvalue가 서로 다를 때 $\mathbf{A}$의 Eigenvector는 $\mathbf{B}$의 Eigenvector라는 것을 다음과 같이 증명할 수 있습니다.

  $\mathbf{v}$가 $\mathbf{A}$의 Eigenvector이고 $\lambda$가 $\mathbf{A}$의 Eigenvalue일 때 다음과 같이 정리할 수 있습니다.

  $$
  \mathbf{Av}=\lambda\mathbf{v} \\
  \mathbf{ABv}=\mathbf{BAv}=\mathbf{B}\lambda\mathbf{v}=\lambda\mathbf{Bv} \\
  \mathbf{A}(\mathbf{Bv})=\lambda(\mathbf{Bv})
  $$

  $\mathbf{Bv}$도 $\mathbf{A}$의 Eigenvector가 됩니다. $\mathbf{A}$의 모든 Eigenvalue는 서로 다르기 때문에 $\mathbf{Bv}=\mu\mathbf{v}$로 표현이 가능해야만 합니다. 만약에 표현이 불가능하다면 한 Eigenvalue에 두 Eigenvector가 존재하게 되어서 $\mathbf{A}$의 모든 Eigenvalue는 서로 달라야 한다는 가정에 모순이 발생하기 때문입니다. 즉, $\mathbf{Bv}=\mu\mathbf{v}$이며 $\mathbf{v}$는 $\mathbf{B}$의 Eigenvector가 됩니다.

* $\mathbf{AB}=\mathbf{BA}$를 만족할 때 $\mathbf{A}$의 Eigenvector가 $\mathbf{B}$의 Eigenvector라는 것을 다음과 같이 증명할 수 있습니다.

  $$
  \mathbf{D}=\mathbf{P}^{-1}\mathbf{A}\mathbf{P}=
  \begin{bmatrix}
  \lambda_1\mathbf{I}_{m_1} & \mathbf{0} & \cdots & \mathbf{0} \\
  \mathbf{0} & \lambda_2\mathbf{I}_{m_2} & \cdots & \mathbf{0} \\
  \vdots & \vdots & \ddots & \vdots \\
  \mathbf{0} & \mathbf{0} & \cdots & \lambda_k\mathbf{I}_{m_k}
  \end{bmatrix} \\
  \mathbf{C}=\mathbf{P}^{-1}\mathbf{B}\mathbf{P}=
  \begin{bmatrix}
  \mathbf{C}_{11} & \mathbf{C}_{12} & \cdots & \mathbf{C}_{1k} \\
  \mathbf{C}_{21} & \mathbf{C}_{22} & \cdots & \mathbf{C}_{2k} \\
  \vdots & \vdots & \ddots & \vdots \\
  \mathbf{C}_{k1} & \mathbf{C}_{k2} & \cdots & \mathbf{C}_{kk}
  \end{bmatrix}
  $$

  $\mathbf{D}$는 $n \times n$의 Diagonal Matrix입니다. $$\mathbf{I}_{m_i}$$는 $m_i \times m_i$인 Identity Matrix입니다. $\sum_{j=1}^km_i=n$입니다. $i \ne j$일 때 $\lambda_i \ne \lambda_j$입니다. $\mathbf{C}_{ii}$는 $$\mathbf{I}_{m_i}$$와 동일한 크기의 Block Matrix입니다.

  $$
  \mathbf{DC}=
  \begin{bmatrix}
  \lambda_1\mathbf{C}_{11} & \lambda_1\mathbf{C}_{12} & \cdots & \lambda_1\mathbf{C}_{1k} \\
  \lambda_2\mathbf{C}_{21} & \lambda_2\mathbf{C}_{22} & \cdots & \lambda_2\mathbf{C}_{2k} \\
  \vdots & \vdots & \ddots & \vdots \\
  \lambda_k\mathbf{C}_{k1} & \lambda_k\mathbf{C}_{k2} & \cdots & \lambda_k\mathbf{C}_{kk}
  \end{bmatrix} \\
  \mathbf{CD}=
  \begin{bmatrix}
  \lambda_1\mathbf{C}_{11} & \lambda_2\mathbf{C}_{12} & \cdots & \lambda_k\mathbf{C}_{1k} \\
  \lambda_1\mathbf{C}_{21} & \lambda_2\mathbf{C}_{22} & \cdots & \lambda_k\mathbf{C}_{2k} \\
  \vdots & \vdots & \ddots & \vdots \\
  \lambda_1\mathbf{C}_{k1} & \lambda_2\mathbf{C}_{k2} & \cdots & \lambda_k\mathbf{C}_{kk}
  \end{bmatrix} \\
  \begin{aligned}
  \mathbf{CD}
  &=\mathbf{P}^{-1}\mathbf{B}\mathbf{P}\mathbf{P}^{-1}\mathbf{A}\mathbf{P} \\
  &=\mathbf{P}^{-1}\mathbf{B}\mathbf{A}\mathbf{P} \\
  &=\mathbf{P}^{-1}\mathbf{A}\mathbf{B}\mathbf{P} \\
  &=\mathbf{P}^{-1}\mathbf{A}\mathbf{P}\mathbf{P}^{-1}\mathbf{B}\mathbf{P} \\
  &=\mathbf{DC}
  \end{aligned}
  $$

  $\mathbf{CD}=\mathbf{DC}$이면서 $i \ne j$일 때 $\lambda_i \ne \lambda_j$이기 위해서는 $i \ne j$일 때 $\mathbf{C}_{ij}=\mathbf{0}$이 되어야 합니다. 정리하면 $\mathbf{C}$는 다음과 같이 됩니다.

  $$
  \mathbf{C}=\mathbf{P}^{-1}\mathbf{B}\mathbf{P}=
  \begin{bmatrix}
  \mathbf{C}_{11} & \mathbf{0} & \cdots & \mathbf{0} \\
  \mathbf{0} & \mathbf{C}_{22} & \cdots & \mathbf{0} \\
  \vdots & \vdots & \ddots & \vdots \\
  \mathbf{0} & \mathbf{0} & \cdots & \mathbf{C}_{kk}
  \end{bmatrix}
  $$

  Diagonal Matrix인 $\mathbf{E}_{ii}$를 다음과 같이 정의합니다.

  $$
  \mathbf{E}_{11}=\mathbf{Q}_{11}^{-1}\mathbf{C}_{11}\mathbf{Q}_{11} \\
  \mathbf{E}_{22}=\mathbf{Q}_{22}^{-1}\mathbf{C}_{22}\mathbf{Q}_{22} \\
  \vdots \\
  \mathbf{E}_{kk}=\mathbf{Q}_{kk}^{-1}\mathbf{C}_{kk}\mathbf{Q}_{kk}
  $$

  $\mathbf{R}$을 다음과 같이 정의합니다.

  $$
  \mathbf{R}=\mathbf{P}
  \begin{bmatrix}
  \mathbf{Q}_{11} & \mathbf{0} & \cdots & \mathbf{0} \\
  \mathbf{0} & \mathbf{Q}_{22} & \cdots & \mathbf{0} \\
  \vdots & \vdots & \ddots & \vdots \\
  \mathbf{0} & \mathbf{0} & \cdots & \mathbf{Q}_{kk}
  \end{bmatrix}
  $$

  $\mathbf{R}^{-1}\mathbf{A}\mathbf{R}$과 $\mathbf{R}^{-1}\mathbf{B}\mathbf{R}$을 다음과 같이 계산해 봅니다.

  $$
  \begin{aligned}
  \mathbf{R}^{-1}\mathbf{A}\mathbf{R}
  &=
  \begin{bmatrix}
  \mathbf{Q}_{11}^{-1} & \mathbf{0} & \cdots & \mathbf{0} \\
  \mathbf{0} & \mathbf{Q}_{22}^{-1} & \cdots & \mathbf{0} \\
  \vdots & \vdots & \ddots & \vdots \\
  \mathbf{0} & \mathbf{0} & \cdots & \mathbf{Q}_{kk}^{-1}
  \end{bmatrix}
  \mathbf{P}^{-1}\mathbf{A}\mathbf{P}
  \begin{bmatrix}
  \mathbf{Q}_{11} & \mathbf{0} & \cdots & \mathbf{0} \\
  \mathbf{0} & \mathbf{Q}_{22} & \cdots & \mathbf{0} \\
  \vdots & \vdots & \ddots & \vdots \\
  \mathbf{0} & \mathbf{0} & \cdots & \mathbf{Q}_{kk}
  \end{bmatrix} \\
  &=
  \begin{bmatrix}
  \lambda_1\mathbf{I}_{m_1} & \mathbf{0} & \cdots & \mathbf{0} \\
  \mathbf{0} & \lambda_2\mathbf{I}_{m_2} & \cdots & \mathbf{0} \\
  \vdots & \vdots & \ddots & \vdots \\
  \mathbf{0} & \mathbf{0} & \cdots & \lambda_k\mathbf{I}_{m_k}
  \end{bmatrix} \\
  \mathbf{R}^{-1}\mathbf{B}\mathbf{R}
  &=
  \begin{bmatrix}
  \mathbf{Q}_{11}^{-1} & \mathbf{0} & \cdots & \mathbf{0} \\
  \mathbf{0} & \mathbf{Q}_{22}^{-1} & \cdots & \mathbf{0} \\
  \vdots & \vdots & \ddots & \vdots \\
  \mathbf{0} & \mathbf{0} & \cdots & \mathbf{Q}_{kk}^{-1}
  \end{bmatrix}
  \mathbf{P}^{-1}\mathbf{B}\mathbf{P}
  \begin{bmatrix}
  \mathbf{Q}_{11} & \mathbf{0} & \cdots & \mathbf{0} \\
  \mathbf{0} & \mathbf{Q}_{22} & \cdots & \mathbf{0} \\
  \vdots & \vdots & \ddots & \vdots \\
  \mathbf{0} & \mathbf{0} & \cdots & \mathbf{Q}_{kk}
  \end{bmatrix} \\
  &=
  \begin{bmatrix}
  \mathbf{Q}_{11}^{-1}\mathbf{C}_{11}\mathbf{Q}_{11} & \mathbf{0} & \cdots & \mathbf{0} \\
  \mathbf{0} & \mathbf{Q}_{22}^{-1}\mathbf{C}_{22}\mathbf{Q}_{22} & \cdots & \mathbf{0} \\
  \vdots & \vdots & \ddots & \vdots \\
  \mathbf{0} & \mathbf{0} & \cdots & \mathbf{Q}_{kk}^{-1}\mathbf{C}_{kk}\mathbf{Q}_{kk}
  \end{bmatrix} \\
  &=
  \begin{bmatrix}
  \mathbf{E}_{11} & \mathbf{0} & \cdots & \mathbf{0} \\
  \mathbf{0} & \mathbf{E}_{22} & \cdots & \mathbf{0} \\
  \vdots & \vdots & \ddots & \vdots \\
  \mathbf{0} & \mathbf{0} & \cdots & \mathbf{E}_{kk}
  \end{bmatrix}
  \end{aligned}
  $$

  $\mathbf{R}^{-1}\mathbf{A}\mathbf{R}$과 $\mathbf{R}^{-1}\mathbf{B}\mathbf{R}$는 Diagonal Matrix이고, $\mathbf{R}$의 Column Vector는 $\mathbf{A}$의 Eigenvector이면서 $\mathbf{B}$의 Eigenvector입니다.

## Quadratic Form {#Quadratic-Form}

$\mathbf{A}$가 Symmetric할 때 $\mathbf{x}^T\mathbf{A}\mathbf{x}$ 형태의 식을 Quadratic Form이라고 정의합니다. 여기서는 이 Quadratic Form의 특징에 대해 설명합니다.

* $\mathbf{x} \sim N(\mathbf{0},\sigma^2\mathbf{I})$이고, $rank(\mathbf{A})=r$이고, $\mathbf{A}$가 Symmetric하고, $\mathbf{A}$가 Idempotent할 때, $\frac{\mathbf{x}^T\mathbf{A}\mathbf{x}}{\sigma^2} \sim \chi^2_r$인 것을 다음과 같이 증명합니다.

  $\mathbf{A}$가 Symmetric하기 때문에 $\mathbf{A}$를 Diagonalize할 수 있는 Orthogonal Matrix $\mathbf{Q}$가 존재합니다.

  $$
  \mathbf{Q}^T\mathbf{AQ}
  =
  \begin{bmatrix}
  \mathbf{\lambda}_1 & 0 & \cdots & 0 \\
  0 & \mathbf{\lambda}_2 & \cdots & 0 \\
  \vdots & \vdots & \ddots & \vdots \\
  0 & 0 & \cdots & \mathbf{\lambda}_n
  \end{bmatrix}
  =
  \begin{bmatrix}
  \mathbf{I}_r & \mathbf{0} \\
  \mathbf{0} & \mathbf{0} \\
  \end{bmatrix}
  $$

  $\mathbf{A}$가 Idempotent하기 때문에 $rank(\mathbf{A})=tr(\mathbf{A})=r$입니다. $\mathbf{v}=\mathbf{Q}^T\mathbf{x}$로 $\mathbf{v}$를 정의합니다.

  $$
  E(\mathbf{v})=\mathbf{Q}^TE(\mathbf{x})=\mathbf{0} \\
  Var(\mathbf{v})=\mathbf{Q}^TVar(\mathbf{x})\mathbf{Q}=\mathbf{Q}^T\sigma^2\mathbf{I}\mathbf{Q}=\sigma^2\mathbf{I} \\
  \mathbf{v} \sim N(\mathbf{0},\sigma^2\mathbf{I}) \\
  \frac{\mathbf{x}^T\mathbf{A}\mathbf{x}}{\sigma^2}
  =\frac{\mathbf{v}^T\mathbf{Q}^T\mathbf{A}\mathbf{Q}\mathbf{v}}{\sigma^2}
  =\frac{1}{\sigma^2}\mathbf{v}^T
  \begin{bmatrix}
  \mathbf{I}_r & \mathbf{0} \\
  \mathbf{0} & \mathbf{0}
  \end{bmatrix}
  \mathbf{v}
  \sim \chi_r^2
  $$

  $Var(\mathbf{v})=\mathbf{Q}^TVar(\mathbf{x})\mathbf{Q}$의 증명은 [Covariance Matrix](/techblog/Derivation-of-the-Multivariate-Normal-Distribution#Covariance-Matrix)을 참조합니다.

* $\mathbf{x} \sim N(\mathbf{0},\mathbf{\Sigma})$이고, $rank(\mathbf{A})=r$이고, $\mathbf{A}$가 Symmetric하고, $\mathbf{A\Sigma}$가 Idempotent할 때, $\mathbf{x}^T\mathbf{A}\mathbf{x} \sim \chi^2_r$인 것을 다음과 같이 증명합니다.

  $$
  \mathbf{A\Sigma A\Sigma}=\mathbf{A\Sigma} \\
  \mathbf{A\Sigma A\Sigma}\mathbf{\Sigma}^{-1}=\mathbf{A\Sigma}\mathbf{\Sigma}^{-1} \\
  \mathbf{A\Sigma A}=\mathbf{A} \\
  \begin{aligned}
  \mathbf{x}^T\mathbf{A}\mathbf{x}
  &=\mathbf{x}^T\mathbf{\Sigma}^{-\frac{1}{2}}\mathbf{\Sigma}^{\frac{1}{2}}\mathbf{A}\mathbf{\Sigma}^{\frac{1}{2}}\mathbf{\Sigma}^{-\frac{1}{2}}\mathbf{x} \\
  &=(\mathbf{\Sigma}^{-\frac{1}{2}}\mathbf{x})^T\mathbf{\Sigma}^{\frac{1}{2}}\mathbf{A}\mathbf{\Sigma}^{\frac{1}{2}}(\mathbf{\Sigma}^{-\frac{1}{2}}\mathbf{x})
  \end{aligned} \\
  \mathbf{v}=\mathbf{\Sigma}^{-\frac{1}{2}}\mathbf{x} \sim N(\mathbf{0},\mathbf{\Sigma}^{-\frac{1}{2}}\mathbf{\Sigma}(\mathbf{\Sigma}^{-\frac{1}{2}})^T)=N(\mathbf{0},\mathbf{I}) \\
  (\mathbf{\Sigma}^{\frac{1}{2}}\mathbf{A}\mathbf{\Sigma}^{\frac{1}{2}})^2=\mathbf{\Sigma}^{\frac{1}{2}}\mathbf{A}\mathbf{\Sigma}^{\frac{1}{2}}\mathbf{\Sigma}^{\frac{1}{2}}\mathbf{A}\mathbf{\Sigma}^{\frac{1}{2}}=\mathbf{\Sigma}^{\frac{1}{2}}(\mathbf{A\Sigma A})\mathbf{\Sigma}^{\frac{1}{2}}=\mathbf{\Sigma}^{\frac{1}{2}}\mathbf{A}\mathbf{\Sigma}^{\frac{1}{2}}
  $$

  $\mathbf{\Sigma}^{\frac{1}{2}}\mathbf{A}\mathbf{\Sigma}^{\frac{1}{2}}$는 Idempotent하다는 것을 알 수 있습니다. 그리고 $\mathbf{A}$는 정의에 의해 Symmetric이고 $\mathbf{\Sigma}$는 Covariance Matrix이기 때문에 Symmetric하여 $\mathbf{\Sigma}^{\frac{1}{2}}\mathbf{A}\mathbf{\Sigma}^{\frac{1}{2}}$도 Symmetric합니다. $rank(\mathbf{A})=r$이고 $rank(\mathbf{\Sigma})=n$이기 때문에 $rank(\mathbf{\Sigma}^{\frac{1}{2}}\mathbf{A}\mathbf{\Sigma}^{\frac{1}{2}})=r$이 됩니다. $\mathbf{B}=\mathbf{\Sigma}^{\frac{1}{2}}\mathbf{A}\mathbf{\Sigma}^{\frac{1}{2}}$와 같이 $\mathbf{B}$를 정의합니다. $\mathbf{B}$는 Symmetric하고, Idempotent하고, $rank(\mathbf{B})=r$이 됩니다.

  $$
  \mathbf{x}^T\mathbf{A}\mathbf{x}=\mathbf{v}^T\mathbf{B}\mathbf{v} \sim \chi_r^2
  $$

* $\mathbf{x} \sim N(\boldsymbol{\mu},\mathbf{\Sigma})$이고, $\mathbf{A}$가 $n \times n$ Matrix 이고, $rank(\mathbf{A})=r$이고, $\mathbf{A}$가 Symmetric하고, $\mathbf{B}$가 $n \times n$ Matrix 이고, $\mathbf{B}$가 Symmetric하고, $\mathbf{A \Sigma B}=\mathbf{0}$이면, $\mathbf{x}^T\mathbf{A}\mathbf{x}$와 $\mathbf{x}^T\mathbf{B}\mathbf{x}$는 Independent하다는 것을 다음과 같이 증명합니다.

  $\mathbf{\Sigma}$는 Covariance Matrix이므로 Positive Definite이 되고 [Cholesky Decomposition](#Cholesky-Decomposition)을 이용하여 $\mathbf{\Sigma}=\mathbf{T}\mathbf{T}^T$로 표현할 수 있습니다.

  $\mathbf{C}=\mathbf{T}^T\mathbf{AT}$로 정의하고 $\mathbf{K}=\mathbf{T}^T\mathbf{BT}$로 정의합니다. 참고로, $\mathbf{A}$와 $\mathbf{B}$가 Symmetric이므로 $\mathbf{C}$와 $\mathbf{K}$도 Symmetric합니다.

  $$
  \mathbf{0}=\mathbf{A\Sigma B}=\mathbf{AT}\mathbf{T}^T\mathbf{B}=\mathbf{T}^T\mathbf{AT}\mathbf{T}^T\mathbf{BT}=(\mathbf{T}^T\mathbf{AT})(\mathbf{T}^T\mathbf{BT})=\mathbf{CK} \\
  \mathbf{A}=(\mathbf{T}^T)^{-1}\mathbf{C}\mathbf{T}^{-1} \\
  \mathbf{B}=(\mathbf{T}^T)^{-1}\mathbf{K}\mathbf{T}^{-1} \\
  \mathbf{CK}=(\mathbf{CK})^T=\mathbf{K}^T\mathbf{C}^T=\mathbf{KC} \\
  \mathbf{CK}=\mathbf{KC}
  $$

  $\mathbf{CK}=\mathbf{KC}$이므로 $\mathbf{C}$와 $\mathbf{K}$는 [Simultaneously Diagonalizable Matrix](#Simultaneously-Diagonalizable-Matrix)이고, $\mathbf{C}$와 $\mathbf{K}$를 Diagonalize할 수 있는 $\mathbf{Q}$가 존재합니다.

  $$
  \mathbf{Q}^T\mathbf{C}\mathbf{Q}=
  \begin{bmatrix}
  d_1 & 0 & \cdots & \cdots & \cdots & \cdots & 0 \\
  0 & d_2 & \cdots & \cdots & \cdots & \cdots & 0 \\
  \vdots & \vdots & \ddots & \vdots & \vdots & \vdots & \vdots \\
  0 & 0 & \cdots & d_r & 0 & \cdots & 0 \\
  \vdots & \vdots & \vdots & 0 & 0 & \cdots & 0 \\
  \vdots & \vdots & \vdots & \vdots & \vdots & \ddots & \vdots \\
  0 & 0 & \cdots & 0 & 0 & \cdots & 0
  \end{bmatrix} \\
  \mathbf{Q}^T\mathbf{K}\mathbf{Q}=
  \begin{bmatrix}
  e_1 & 0 & \cdots & 0 \\
  0 & e_2 & \cdots & 0 \\
  \vdots & \vdots & \ddots & \vdots \\
  0 & 0 & \cdots & e_n
  \end{bmatrix} \\
  $$

  $\mathbf{CK}=\mathbf{0}$이고 $d_1$, $d_2$, $\cdots$, $d_r$은 $0$이 아니므로 $e_1$, $e_2$, $\cdots$, $e_r$은 $0$이 됩니다.

  $$
  \mathbf{Q}^T\mathbf{CQ}=
  \begin{bmatrix}
  \mathbf{D} & \mathbf{0} \\
  \mathbf{0} & \mathbf{0} \\
  \end{bmatrix} \\
  \mathbf{Q}^T\mathbf{KQ}=
  \begin{bmatrix}
  \mathbf{0} & \mathbf{0} \\
  \mathbf{0} & \mathbf{E} \\
  \end{bmatrix} \\
  $$

  $\mathbf{D}$는 $r \times r$인 Diagonal Matrix이고 $\mathbf{E}$는 $(n-r) \times (n-r)$인 Diagonal Matrix입니다.

  $\mathbf{v}=\mathbf{Q}^T\mathbf{T}^{-1}\mathbf{x}$로 $\mathbf{v}$를 정의합니다.

  $$
  E(\mathbf{v})=\mathbf{Q}^T\mathbf{T}^{-1}\boldsymbol{\mu} \\
  \begin{aligned}
  Var(\mathbf{v})
  &=(\mathbf{Q}^T\mathbf{T}^{-1})\mathbf{\Sigma}(\mathbf{Q}^T\mathbf{T}^{-1})^T \\
  &=\mathbf{Q}^T\mathbf{T}^{-1}\mathbf{\Sigma}(\mathbf{T}^{-1})^T\mathbf{Q} \\
  &=\mathbf{Q}^T\mathbf{T}^{-1}\mathbf{T}\mathbf{T}^T(\mathbf{T}^{-1})^T\mathbf{Q} \\
  &=\mathbf{I}
  \end{aligned} \\
  \mathbf{v} \sim N(\mathbf{Q}^T\mathbf{T}^{-1}\boldsymbol{\mu}, \mathbf{I})
  $$

  $\mathbf{v}$의 Covariance Matrix가 $\mathbf{I}$이므로 Random Variable $v_1$, $v_2$, $\cdots$, $v_n$은 Independent합니다.

  $$
  \mathbf{x}=\mathbf{TQv} \\
  \mathbf{x}^T=\mathbf{v}^T\mathbf{Q}^T\mathbf{T}^T \\
  \begin{aligned}
  \mathbf{x}^T\mathbf{Ax}
  &=\mathbf{v}^T\mathbf{Q}^T\mathbf{T}^T\mathbf{ATQv} \\
  &=\mathbf{v}^T\mathbf{Q}^T\mathbf{T}^T(\mathbf{T}^T)^{-1}\mathbf{C}\mathbf{T}^{-1}\mathbf{TQv} \\
  &=\mathbf{v}^T\mathbf{Q}^T\mathbf{C}\mathbf{Qv} \\
  \mathbf{x}^T\mathbf{Bx}
  &=\mathbf{v}^T\mathbf{Q}^T\mathbf{T}^T\mathbf{BTQv} \\
  &=\mathbf{v}^T\mathbf{Q}^T\mathbf{T}^T(\mathbf{T}^T)^{-1}\mathbf{K}\mathbf{T}^{-1}\mathbf{TQv} \\
  &=\mathbf{v}^T\mathbf{Q}^T\mathbf{K}\mathbf{Qv}
  \end{aligned}
  $$

  $\mathbf{Q}^T\mathbf{C}\mathbf{Q}$를 살펴보면 $\mathbf{x}^T\mathbf{Ax}$는 $\mathbf{v}$중에서 Random Variable $v_1$, $v_2$, $\cdots$, $v_r$에만 Depend하고, $\mathbf{Q}^T\mathbf{K}\mathbf{Q}$를 살펴보면 $\mathbf{x}^T\mathbf{Bx}$는 $\mathbf{v}$중에서 Random Variable $v_{r+1}$, $v_{r+2}$, $\cdots$, $v_n$에만 Depend하다는 사실을 알 수 있습니다. 그래서 $\mathbf{x}^T\mathbf{Ax}$와 $\mathbf{x}^T\mathbf{Bx}$는 Independent합니다.

## Non-central Chi-squared Distribution {#Non-central-Chi-squared-Distribution}

[Central Chi-squared Distribution](/techblog/Derivation-of-the-Probability-Distribution-Functions#Chi-squared)은 $X_i$가 iid이고, $X_i \sim N(0,1)$일 때, $\sum_{i=1}^r X_i^2 \sim \chi_r^2$와 같이 정의합니다.

Non-central Chi-squared Distribution은 $X_i$가 iid이고, $X_i \sim N(\mu_i,1)$이고, $\lambda=\sum_{i=1}^r\mu_i^2$일 때, $\sum_{i=1}^r X_i^2 \sim \chi_r^2(\lambda)$와 같이 정의합니다.

[Quadratic Form](#Quadratic-Form)을 참조해 보면 $\mathbf{x} \sim N(\mathbf{0},\sigma^2\mathbf{I})$이고, $rank(\mathbf{A})=r$이고, $\mathbf{A}$가 Symmetric하고, $\mathbf{A}$가 Idempotent할 때, $\frac{\mathbf{x}^T\mathbf{A}\mathbf{x}}{\sigma^2} \sim \chi^2_r$이 됩니다. 같은 조건에서 $\mathbf{x} \sim N(\boldsymbol{\mu},\sigma^2\mathbf{I})$인 경우를 살펴보면 $\frac{\mathbf{x}^T\mathbf{A}\mathbf{x}}{\sigma^2} \sim \chi^2_r(\frac{\boldsymbol{\mu}^T\mathbf{A}\boldsymbol{\mu}}{\sigma^2})$가 됩니다.

[Quadratic Form](#Quadratic-Form)을 참조해 보면 $\mathbf{x} \sim N(\mathbf{0},\mathbf{\Sigma})$이고, $rank(\mathbf{A})=r$이고, $\mathbf{A}$가 Symmetric하고, $\mathbf{A\Sigma}$가 Idempotent할 때, $\mathbf{x}^T\mathbf{A}\mathbf{x} \sim \chi^2_r$이 됩니다. 같은 조건에서 $\mathbf{x} \sim N(\boldsymbol{\mu},\mathbf{\Sigma})$인 경우를 살펴보면 $\mathbf{x}^T\mathbf{A}\mathbf{x} \sim \chi^2_r(\boldsymbol{\mu}^T\mathbf{A}\boldsymbol{\mu})$가 됩니다.

## Linear Regression {#Linear-Regression}

Linear Regression에서 사용할 Symbol들을 아래와 같이 정의합니다.

$$
\mathbf{y}=\mathbf{X}\boldsymbol{\beta}+\boldsymbol{\epsilon} \\
\boldsymbol{\epsilon} \sim N(\mathbf{0}, \sigma^2\mathbf{I}) \\
\hat{\mathbf{y}}=\mathbf{X}\boldsymbol{\beta} \\
\mathbf{y}=
\begin{bmatrix}
y_1 & y_2 & \cdots & y_n
\end{bmatrix}^T \\
\hat{\mathbf{y}}=
\begin{bmatrix}
\hat{y}_1 & \hat{y}_2 & \cdots & \hat{y}_n
\end{bmatrix}^T \\
\mathbf{X}=
\begin{bmatrix}
X_{11} & X_{12} & X_{13} & \cdots & X_{1p} \\
X_{21} & X_{22} & X_{23} & \cdots & X_{2p} \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
X_{n1} & X_{n2} & X_{n3} & \cdots & X_{np}
\end{bmatrix}
=
\begin{bmatrix}
1 & X_{12} & X_{13} & \cdots & X_{1p} \\
1 & X_{22} & X_{23} & \cdots & X_{2p} \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
1 & X_{n2} & X_{n3} & \cdots & X_{np}
\end{bmatrix} \\
\boldsymbol{\beta}=
\begin{bmatrix}
\beta_1 & \beta_2 & \cdots & \beta_p
\end{bmatrix}^T \\
\boldsymbol{\epsilon}=
\begin{bmatrix}
\epsilon_1 & \epsilon_2 & \cdots & \epsilon_n
\end{bmatrix}^T \\
\bar{y}=\frac{1}{n}\sum_{i=1}^ny_i \\
SSTO=\sum_{i=1}^n(y_i-\bar{y}) \\
SSE=\sum_{i=1}^n(y_i-\hat{y}_i) \\
SSR=\sum_{i=1}^n(\hat{y}_i-\bar{y}) \\
\mathbf{1}=
\begin{bmatrix}
1 & 1 & \cdots & 1
\end{bmatrix}^T \\
\mathbf{J}=
\begin{bmatrix}
1 & 1 & \cdots & 1 \\
1 & 1 & \cdots & 1 \\
\vdots & \vdots & \ddots & \vdots \\
1 & 1 & \cdots & 1
\end{bmatrix} \\
\mathbf{H}=\mathbf{X}(\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T \\
$$

Linear Regression에 대해 설명하도록 하겠습니다. 수집된 Input Data가 $\mathbf{X}$에 저장되어 있고, 수집된 Output Data는 $\mathbf{y}$에 저장되어 있습니다. $\mathbf{X}$ Matrix의 각각의 Row가 하나의 Input Data이고, $\mathbf{y}$ Vector의 각각의 Element가 하나의 Output Data입니다. 예를 들어, 세번째 Input Data는 $\begin{bmatrix}X_{31} & X_{32} & X_{33} & \cdots & X_{3p}\end{bmatrix}$이고, 세번째 Output Data는 $y_3$입니다. Data로 가지고 있지 않은 Input을 입력했을 때 적절한 Output을 출력하는 Function을 만들고 싶습니다. 즉, $\begin{bmatrix}X_{i1} & X_{i2} & X_{i3} & \cdots & X_{ip}\end{bmatrix}$을 입력하면 $y_i$을 출력하는 Function을 만들고 싶습니다. 그래서 일단 그 Function의 형태를 $\mathbf{y}=\mathbf{X}\boldsymbol{\beta}$로 구성하고 해당 조건을 성립시키는 $\boldsymbol{\beta}$를 찾는 것을 시도합니다. 하지만 이것은 거의 불가능한 목표입니다. $\mathbf{y}=\mathbf{X}\boldsymbol{\beta}$는 단순한 형태라서 가지고 있는 Data가 모두 만족하도록 만드는 것이 불가능한 것이 일반적이기 때문입니다. 그래서 이 Function이 Input Data로부터 추정하는 Output은 실제 Output Data와 어느정도 Error가 발생하는 것을 피할 수 없습니다. 이 Error를 $\boldsymbol{\epsilon}$으로 설정합니다. 예를 들어 네번째 Output Data는 $y_4$이고, Function이 네번째 Input Data는 로부터 추정한 Output Data는 $\hat{y}_4$이고, 네번째 Error는 $\epsilon_4=y_4-\hat{y}_4$가 됩니다.

$$
\begin{align}
\epsilon_4
&=y_4-\hat{y_4} \\
&=y_4-
\begin{bmatrix}
X_{41} & X_{42} & X_{43} & \cdots & X_{4p}
\end{bmatrix}
\begin{bmatrix}
\beta_1 & \beta_2 & \beta_3 & \cdots & \beta_p
\end{bmatrix}^T
\end{align}
$$

각각의 Error는(첫번째 Data에 대한 Error, 두번째 Data에 대한 Error, ...) iid하고 Independent해서 $Var(\boldsymbol{\epsilon})=\sigma^2\mathbf{I}$가 됩니다.

Linear Regression에서 $\beta_1$은 Input Data에 영향을 받지 않고 Output Data에 직접 영향을 주도록 설정하는 것이 일반적입니다. 그렇게 하기 위해서 $\mathbf{X}$의 첫번째 Column은 모두 1로 설정합니다. 그래서 $X_{i1}$은 모두 1로 설정합니다.

Error를 최소화시키는 $\boldsymbol{\beta}$를 구하기 위해서, 다음과 같이 $\mathbf{y}$를 $\mathbf{X}$의 Column Space에 Projection해서 이것을 $\hat{\mathbf{y}}$으로 정하고, $\boldsymbol{\beta}$를 $\mathbf{X}$로 변환했을 때 $\hat{\mathbf{y}}$이 나오는 $\boldsymbol{\beta}$를 구합니다. $\mathbf{X}$의 Column Space에 Projection해 주는 Matrix를 Projection Matrix라고 하고 $\mathbf{H}$로 표기합니다.

$$
\hat{\mathbf{y}}=\mathbf{H}\mathbf{y} \\
\hat{\mathbf{y}}=\mathbf{X}(\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y} \\
\hat{\mathbf{y}}=\mathbf{X}\boldsymbol{\beta} \\
\boldsymbol{\beta}=(\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}
$$

$SSTO=SSR+SSE$이라는 것은 다음과 같이 증명할 수 있습니다.

$$
\begin{align}
SSTO
&=\sum_{i=1}^n(y_i-\bar{y})^2 \\
&=\sum_{i=1}^n((\hat{y}_i-\bar{y})+(y_i-\hat{y}_i))^2 \\
&=\sum_{i=1}^n((\hat{y}_i-\bar{y})^2+(y_i-\hat{y}_i)^2+2(\hat{y}_i-\bar{y})(y_i-\hat{y}_i)) \\
&=\sum_{i=1}^n(\hat{y}_i-\bar{y})^2+\sum_{i=1}^n(y_i-\hat{y}_i)^2+2\sum_{i=1}^n\hat{y}_i(y_i-\hat{y}_i)-2\bar{y}\sum_{i=1}^n(y_i-\hat{y}_i) \\
&=\sum_{i=1}^n(\hat{y}_i-\bar{y})^2+\sum_{i=1}^n(y_i-\hat{y}_i)^2+2\sum_{i=1}^n\hat{y}_i\epsilon_i-2\bar{y}\sum_{i=1}^n\epsilon_i \\
&=SSR+SSE+0+0 \\
&=SSR+SSE
\end{align}
$$

## Linear Regression in Quadratic Form {#Linear-Regression-in-Quadratic-Form}

$SSTO$를 Quadratic Form으로 표현하면 다음과 같습니다.

$$
\begin{aligned}
SSTO
&=\sum_{i=1}^n(y_i-\bar{y})^2 \\
&=\sum_{i=1}^n(y_i^2-2y_i\bar{y}+\bar{y}^2) \\
&=\sum_{i=1}^n(y_i^2-2y_i(\frac{1}{n}\sum_{j=1}^ny_j)+(\frac{1}{n}\sum_{j=1}^ny_j)^2) \\
&=\sum_{i=1}^ny_i^2-2(\sum_{i=1}^ny_i)(\frac{1}{n}\sum_{j=1}^ny_j)+n(\frac{1}{n}\sum_{j=1}^ny_j)^2 \\
&=\sum_{i=1}^ny_i^2-\frac{2}{n}(\sum_{i=1}^ny_i)^2+\frac{1}{n}(\sum_{i=1}^ny_i)^2 \\
&=\sum_{i=1}^ny_i^2-\frac{1}{n}(\sum_{i=1}^ny_i)^2 \\
&=\sum_{i=1}^ny_i^2-\frac{1}{n}(y_1\sum_{i=1}^ny_i+y_2\sum_{i=1}^ny_i+\cdots+y_n\sum_{i=1}^ny_i) \\
&=\sum_{i=1}^ny_i^2-\frac{1}{n}\begin{bmatrix}\sum_{i=1}^ny_i & \sum_{i=1}^ny_i & \cdots & \sum_{i=1}^ny_i\end{bmatrix}\mathbf{y} \\
&=\sum_{i=1}^ny_i^2-\frac{1}{n}\mathbf{y}^T\mathbf{J}\mathbf{y} \\
&=\mathbf{y}^T\mathbf{y}-\frac{1}{n}\mathbf{y}^T\mathbf{J}\mathbf{y} \\
&=\mathbf{y}^T(\mathbf{I}-\frac{1}{n}\mathbf{J})\mathbf{y} \\
\end{aligned}
$$

$SSE$를 Quadratic Form으로 표현하면 다음과 같습니다. $\mathbf{H}$가 Symmetric하면서 Idempotent한 것을 이용합니다.

$$
\begin{aligned}
SSE
&=\sum_{i=1}^n(y_i-\hat{y})^2 \\
&=(\mathbf{y}-\hat{\mathbf{y}})^T(\mathbf{y}-\hat{\mathbf{y}}) \\
&=\mathbf{y}^T\mathbf{y}-\mathbf{y}^T\hat{\mathbf{y}}-\hat{\mathbf{y}}^T\mathbf{y}+\hat{\mathbf{y}}^T\hat{\mathbf{y}} \\
&=\mathbf{y}^T\mathbf{y}-2\hat{\mathbf{y}}^T\mathbf{y}+\hat{\mathbf{y}}^T\hat{\mathbf{y}} \\
&=\mathbf{y}^T\mathbf{y}-2(\mathbf{H}\mathbf{y})^T\mathbf{y}+(\mathbf{H}\mathbf{y})^T\mathbf{H}\mathbf{y} \\
&=\mathbf{y}^T\mathbf{y}-2\mathbf{y}^T\mathbf{H}^T\mathbf{y}+\mathbf{y}^T\mathbf{H}^T\mathbf{H}\mathbf{y} \\
&=\mathbf{y}^T\mathbf{y}-2\mathbf{y}^T\mathbf{H}\mathbf{y}+\mathbf{y}^T\mathbf{H}\mathbf{H}\mathbf{y} \\
&=\mathbf{y}^T\mathbf{y}-2\mathbf{y}^T\mathbf{H}\mathbf{y}+\mathbf{y}^T\mathbf{H}^2\mathbf{y} \\
&=\mathbf{y}^T\mathbf{y}-2\mathbf{y}^T\mathbf{H}\mathbf{y}+\mathbf{y}^T\mathbf{H}\mathbf{y} \\
&=\mathbf{y}^T\mathbf{y}-\mathbf{y}^T\mathbf{H}\mathbf{y} \\
&=\mathbf{y}^T(\mathbf{I}-\mathbf{H})\mathbf{y} \\
\end{aligned}
$$

$SSR$을 Quadratic Form으로 표현하면 다음과 같습니다.

$$
\begin{aligned}
SSR
&=SSTO-SSE \\
&=\mathbf{y}^T(\mathbf{I}-\frac{1}{n}\mathbf{J})\mathbf{y}-\mathbf{y}^T(\mathbf{I}-\mathbf{H})\mathbf{y} \\
&=\mathbf{y}^T(\mathbf{H}-\frac{1}{n}\mathbf{J})\mathbf{y} \\
\end{aligned}
$$

$\mathbf{I}$, $\frac{1}{n}\mathbf{J}$, $\mathbf{H}$는 모두 Symmetric합니다. 그래서 $\mathbf{I}-\frac{1}{n}\mathbf{J}$, $\mathbf{I}-\mathbf{H}$, $\mathbf{H}-\frac{1}{n}\mathbf{J}$도 모두 Symmetric합니다.

$\mathbf{I}$, $\mathbf{H}$는 모두 Idempotent합니다.

$\frac{1}{n}\mathbf{J}$가 Idempotent한 것은 다음과 같이 확인할 수 있습니다.

$$
\begin{aligned}
(\frac{1}{n}\mathbf{J})^2
&=
\frac{1}{n^2}
\begin{bmatrix}
1 & 1 & \cdots & 1 \\
1 & 1 & \cdots & 1 \\
\vdots & \vdots & \ddots & \vdots \\
1 & 1 & \cdots & 1
\end{bmatrix}
\begin{bmatrix}
1 & 1 & \cdots & 1 \\
1 & 1 & \cdots & 1 \\
\vdots & \vdots & \ddots & \vdots \\
1 & 1 & \cdots & 1
\end{bmatrix} \\
&=
\frac{1}{n^2}
\begin{bmatrix}
n & n & \cdots & n \\
n & n & \cdots & n \\
\vdots & \vdots & \ddots & \vdots \\
n & n & \cdots & n
\end{bmatrix} \\
&=
\frac{1}{n}
\begin{bmatrix}
1 & 1 & \cdots & 1 \\
1 & 1 & \cdots & 1 \\
\vdots & \vdots & \ddots & \vdots \\
1 & 1 & \cdots & 1
\end{bmatrix} \\
&=\frac{1}{n}\mathbf{J}
\end{aligned}
$$

$\mathbf{I}-\frac{1}{n}\mathbf{J}$가 Idempotent한 것은 다음과 같이 확인해 볼 수 있습니다.

$$
\begin{aligned}
(\mathbf{I}-\frac{1}{n}\mathbf{J})^2
&=\mathbf{I}^2-\frac{2}{n}\mathbf{J}\mathbf{I}+(\frac{1}{n}\mathbf{J})^2 \\
&=\mathbf{I}-\frac{2}{n}\mathbf{J}+\frac{1}{n}\mathbf{J} \\
&=\mathbf{I}-\frac{1}{n}\mathbf{J} \\
\end{aligned}
$$

$\mathbf{I}-\mathbf{H}$가 Idempotent한 것은 다음과 같이 확인해 볼 수 있습니다.

$$
\begin{aligned}
(\mathbf{I}-\mathbf{H})^2
&=\mathbf{I}^2-2\mathbf{H}\mathbf{I}+\mathbf{H}^2 \\
&=\mathbf{I}-2\mathbf{H}+\mathbf{H} \\
&=\mathbf{I}-\mathbf{H}
\end{aligned}
$$

$\mathbf{1}$의 Column Space로 Projection하는 Projection Matrix를 구해보면 다음과 같습니다.

$$
\begin{aligned}
\mathbf{1}(\mathbf{1}^T\mathbf{1})^{-1}\mathbf{1}^T
&=\mathbf{1}(n)^{-1}\mathbf{1}^T \\
&=\frac{1}{n}\mathbf{J}
\end{aligned}
$$

$\mathbf{H}$는 $\mathbf{X}$의 Column Space로 Projection하는 Projection Matrix이고, $\frac{1}{n}\mathbf{J}$는 $\mathbf{1}$의 Column Space로 Projection하는 Projection Matrix입니다. 그리고 $X_{i1}$가 모두 $1$로 설정되어 있기 때문에 $\mathbf{X}$의 Column Space는 $\mathbf{1}$의 Column Space를 포함합니다. 그래서 $\mathbf{X}$의 Column Space로 Projection하고 $\mathbf{1}$의 Column Space로 Projection한 결과, $\mathbf{1}$의 Column Space로 Projection하고 $\mathbf{X}$의 Column Space로 Projection한 결과, $\mathbf{1}$의 Column Space로 Projection한 결과는 모두 동일합니다. 정리하면 다음이 성립합니다.

$$
\frac{1}{n}\mathbf{H}\mathbf{J}=\frac{1}{n}\mathbf{J}\mathbf{H}=\frac{1}{n}\mathbf{J}
$$

이 특징을 이용하여 $\mathbf{H}-\frac{1}{n}\mathbf{J}$이 Idempotent한 것은 다음과 같이 확인해 볼 수 있습니다.

$$
\begin{aligned}
(\mathbf{H}-\frac{1}{n}\mathbf{J})^2
&=\mathbf{H}^2-\frac{1}{n}\mathbf{HJ}-\frac{1}{n}\mathbf{JH}+(\frac{1}{n}\mathbf{J})^2 \\
&=\mathbf{H}-\frac{1}{n}\mathbf{J}-\frac{1}{n}\mathbf{J}+\frac{1}{n}\mathbf{J} \\
&=\mathbf{H}-\frac{1}{n}\mathbf{J} \\
\end{aligned}
$$

$\mathbf{I}-\frac{1}{n}\mathbf{J}$, $\mathbf{I}-\mathbf{H}$, $\mathbf{H}-\frac{1}{n}\mathbf{J}$이 모두 Symmetric하고 Idempotent한 것을 확인했습니다. 이번에는 각각의 Rank를 구해 보도록 하겠습니다. [Idempotent Matrix](#Idempotent-Matrix)를 이용합니다. $\mathbf{X}$는 $n \times p$ Matrix이므로 $rank(\mathbf{H})=p$이 되는 것도 이용합니다.

$$
\begin{aligned}
rank(\mathbf{I}-\frac{1}{n}\mathbf{J})
&=tr(\mathbf{I}-\frac{1}{n}\mathbf{J}) \\
&=tr(\mathbf{I})-tr(\frac{1}{n}\mathbf{J}) \\
&=n-\frac{1}{n}n \\
&=n-1
\end{aligned} \\
\begin{aligned}
rank(\mathbf{I}-\mathbf{H})
&=tr(\mathbf{I}-\mathbf{H}) \\
&=tr(\mathbf{I})-tr(\mathbf{H}) \\
&=n-p
\end{aligned} \\
\begin{aligned}
rank(\mathbf{H}-\frac{1}{n}\mathbf{J})
&=tr(\mathbf{H}-\frac{1}{n}\mathbf{J}) \\
&=tr(\mathbf{H})-tr(\frac{1}{n}\mathbf{J}) \\
&=p-1
\end{aligned} \\
$$

여기서 얻은 결과들을 정리해 보면 다음과 같습니다.

$$
SSTO=\mathbf{y}^T(\mathbf{I}-\frac{1}{n}\mathbf{J})\mathbf{y} \\
SSR=\mathbf{y}^T(\mathbf{H}-\frac{1}{n}\mathbf{J})\mathbf{y} \\
SSE=\mathbf{y}^T(\mathbf{I}-\mathbf{H})\mathbf{y} \\
SSTO=SSR+SSE \\
\mathbf{y}^T(\mathbf{I}-\frac{1}{n}\mathbf{J})\mathbf{y}=\mathbf{y}^T(\mathbf{H}-\frac{1}{n}\mathbf{J})\mathbf{y}+\mathbf{y}^T(\mathbf{I}-\mathbf{H})\mathbf{y} \\
\mathbf{I} \text{ is symmetric and idempotent.} \\
\frac{1}{n}\mathbf{J} \text{ is symmetric and idempotent.} \\
\mathbf{H} \text{ is symmetric and idempotent.} \\
\mathbf{I}-\frac{1}{n}\mathbf{J} \text{ is symmetric and idempotent.} \\
\mathbf{I}-\mathbf{H} \text{ is symmetric and idempotent.} \\
\mathbf{H}-\frac{1}{n}\mathbf{J} \text{ is symmetric and idempotent.} \\
rank(\mathbf{I})=n \\
rank(\frac{1}{n}\mathbf{J})=1 \\
rank(\mathbf{H})=p \\
rank(\mathbf{I}-\frac{1}{n}\mathbf{J})=n-1 \\
rank(\mathbf{I}-\mathbf{H})=n-p \\
rank(\mathbf{H}-\frac{1}{n}\mathbf{J})=p-1 \\
$$

## F Test for Linear Regression

[Linear Regression](#Linear-Regression)을 살펴보면 다음이 성립함을 알 수 있습니다.

$$
\mathbf{y} \sim N(\mathbf{X}\boldsymbol{\beta},\sigma^2\mathbf{I})
$$

[Quadratic Form](#Quadratic-Form)과 [Linear Regression in Quadratic Form](#Linear-Regression-in-Quadratic-Form)을 살펴보면 다음이 만족하기 때문에 $SSE$와 $SSR$이 Independent하다는 것을 알 수 있습니다.

$$
\begin{aligned}
(\mathbf{I}-\mathbf{H})(\sigma^2\mathbf{I})(\mathbf{H}-\frac{1}{n}\mathbf{J})
&=\sigma^2(\mathbf{H}-\frac{1}{n}\mathbf{J}-\mathbf{H}^2+\frac{1}{n}\mathbf{H}\mathbf{J}) \\
&=\sigma^2(\mathbf{H}-\frac{1}{n}\mathbf{J}-\mathbf{H}+\frac{1}{n}\mathbf{J}) \\
&=0
\end{aligned}
$$

$\mathbf{v}=\frac{\mathbf{y}}{\sigma}$로 $\mathbf{v}$를 정의하면, $\mathbf{v} \sim N(\frac{\mathbf{X}\boldsymbol{\beta}}{\sigma}, \mathbf{I})$이 됩니다. [Non-central Chi-squared Distribution](#Non-central-Chi-squared-Distribution)을 살펴보면 $\mathbf{I}-\mathbf{H}$가 Symmetric하고 $(\mathbf{I}-\mathbf{H})\mathbf{I}$가 Idempotent하기 때문에 다음이 성립한다는 것을 알 수 있습니다. $rank(\mathbf{I}-\mathbf{H})=n-p$는 [Linear Regression in Quadratic Form](#Linear-Regression-in-Quadratic-Form)를 참조합니다.

$$
\frac{SSE}{\sigma^2}
=(\frac{\mathbf{y}}{\sigma})^T(\mathbf{I}-\mathbf{H})(\frac{\mathbf{y}}{\sigma})
\sim \chi_{n-p}^2((\frac{\mathbf{X}\boldsymbol{\beta}}{\sigma})^T(\mathbf{I}-\mathbf{H})(\frac{\mathbf{X}\boldsymbol{\beta}}{\sigma}))
$$

마찬가지 방법으로 $\mathbf{H}-\frac{1}{n}\mathbf{J}$가 Symmetric하고 $(\mathbf{H}-\frac{1}{n}\mathbf{J})\mathbf{I}$가 Idempotent하기 때문에 다음이 성립한다는 것을 알 수 있습니다. $rank(\mathbf{H}-\frac{1}{n}\mathbf{J})=p-1$는 [Linear Regression in Quadratic Form](#Linear-Regression-in-Quadratic-Form)를 참조합니다.

$$
\frac{SSR}{\sigma^2}
=(\frac{\mathbf{y}}{\sigma})^T(\mathbf{H}-\frac{1}{n}\mathbf{J})(\frac{\mathbf{y}}{\sigma})
\sim \chi_{p-1}^2((\frac{\mathbf{X}\boldsymbol{\beta}}{\sigma})^T(\mathbf{H}-\frac{1}{n}\mathbf{J})(\frac{\mathbf{X}\boldsymbol{\beta}}{\sigma}))
$$

$\boldsymbol{\beta}=\mathbf{0}$로 Null Hypothesis를 설정하면 다음과 같이 됩니다.

$$
\frac{SSE}{\sigma^2}=\chi_{n-p}^2 \\
\frac{SSR}{\sigma^2}=\chi_{p-1}^2
$$

SSR과 SSE는 Independent하므로 F Statistic을 다음과 같이 계산할 수 있습니다. F Distribution에 대해서는 [Derivation of the Probability Distribution Functions](/techblog/Derivation-of-the-Probability-Distribution-Functions#F)을 참조합니다.

$$
F=\frac{\frac{\frac{SSR}{\sigma^2}}{p-1}}{\frac{\frac{SSE}{\sigma^2}}{n-p}}=\frac{\frac{SSR}{p-1}}{\frac{SSE}{n-p}}=\frac{\frac{SSTO-SSE}{p-1}}{\frac{SSE}{n-p}} \sim F(p-1,n-p)
$$

$n$은 가지고 있는 Data의 수($\mathbf{y}$ Vector의 Element 수, $\mathbf{X}$ Matrix의 Row의 수), $p$는 찾아야 하는 Parameter의 수($\boldsymbol{\beta}$ Vector의 Element 수, $\mathbf{X}$ Matrix의 Column의 수)입니다. $\boldsymbol{\beta}=\mathbf{0}$이라는 뜻은 Input과 Output이 관계가 없다는 뜻입니다. F Statistic으로 얻게 되는 결과는 $F(p-1,n-p)$를 따릅니다. 이것의 의미는 Input과 Output이 관계가 없다고 가정했을 때 현재 가지고 있는 Input Data와 Output Data의 조합을 우연히 얻게 될 확률이며, 이것은 만약에 여기서 계산된 Input Data와 Output Data의 조합을 우연히 얻게 될 확률이 충분히 낮다면(예를 들어 5%이하) Null Hypothesis를 기각해서 Input과 Output이 관계가 있다는 것을 의미하고, 이 확률이 높다면 Null Hypothesis를 기각하는 것이 불가능하여 Input과 Output이 관계가 있다고 있다고 확신하기 힘들다는 것을 의미합니다.
