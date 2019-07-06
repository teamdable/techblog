---
layout: post
title:  "Derivation of the Multivariate Normal Distribution"
date:   2019-06-28 23:00:00 +0900
author: Taeho Oh
tags: [ 오태호, 수학, 통계학, 확률분포 ]
---
안녕하세요. 오태호입니다.

이번 글에서는 Multivariate Normal Distribution의 Probability Distribution Function을 유도해 보도록 하겠습니다. 교과서에 식만 나와 있고 유도과정이 나와 있지 않은 경우가 많아서 유도과정을 정리해 보았습니다.

증명과정중에 Matrix나 Vector는 굵은 글꼴로 표현하도록 하겠습니다. 그리고 Vector는 특별히 언급이 없으면 Column Vector를 의미합니다.

## Covariance Matrix {#Covariance-Matrix}

$\mathbf{X}$는 Random Variable $X_1$, $X_2$, $\cdots$, $X_n$으로 이루어진 Vector일 때 Covariance Matrix는 아래와 같이 정의됩니다.

$$
\begin{aligned}
\mathbf{C_X}
&=
\begin{bmatrix}
Var(X_1) & Cov(X_1, X_2) & \cdots & Cov(X_1, X_n) \\
Cov(X_2, X_1) & Var(X_2) & \cdots & Cov(X_2, X_n) \\
\vdots & \vdots & \ddots &  \vdots \\
Cov(X_n, X_1) & Cov(X_n, X_2) & \cdots & Var(X_n) \\
\end{bmatrix} \\
&=E((\mathbf{X}-E(\mathbf{X}))(\mathbf{X}-E(\mathbf{X}))^T)
\end{aligned}
$$

$\mathbf{A}$는 $n \times n$인 Matrix이고 $\mathbf{b}$는 크기가 $n$인 Vector일 때 $\mathbf{Y}=\mathbf{A}\mathbf{X}+\mathbf{b}$의 Covariance Matrix를 $\mathbf{C_X}$를 이용해서 아래와 같이 구할 수 있습니다.

$$
\begin{aligned}
\mathbf{C_Y}
&=E((\mathbf{Y}-E(\mathbf{Y}))(\mathbf{Y}-E(\mathbf{Y}))^T) \\
&=E((\mathbf{A}\mathbf{X}+\mathbf{b}-E(\mathbf{A}\mathbf{X}+\mathbf{b}))(\mathbf{A}\mathbf{X}+\mathbf{b}-E(\mathbf{A}\mathbf{X}+\mathbf{b}))^T) \\
&=E((\mathbf{A}\mathbf{X}-E(\mathbf{A}\mathbf{X}))(\mathbf{A}\mathbf{X}-E(\mathbf{A}\mathbf{X}))^T) \\
&=E(\mathbf{A}(\mathbf{X}-E(\mathbf{X}))(\mathbf{X}-E(\mathbf{X}))^T\mathbf{A}^T) \\
&=\mathbf{A}E((\mathbf{X}-E(\mathbf{X}))(\mathbf{X}-E(\mathbf{X}))^T)\mathbf{A}^T \\
&=\mathbf{A}\mathbf{C_X}\mathbf{A}^T
\end{aligned}
$$

## Method of Transformations {#Method-of-Transformations}

$\mathbf{Y}=G(\mathbf{X})$, $\mathbf{X}=G^{-1}(\mathbf{Y})=H(\mathbf{Y})$ 일 때 Probability Density Function $f_{\mathbf{Y}}(\mathbf{y})$는 다음과 같습니다. 

$$
\mathbf{X}=
\begin{bmatrix}
X_1 \\
X_2 \\
\vdots \\
X_n
\end{bmatrix}
=
\begin{bmatrix}
H_1(\mathbf{Y}) \\
H_2(\mathbf{Y}) \\
\vdots \\
H_n(\mathbf{Y})
\end{bmatrix} \\
J=\det
\begin{bmatrix}
\frac{\partial H_1}{\partial y_1} & \frac{\partial H_1}{\partial y_2} & \cdots & \frac{\partial H_1}{\partial y_n} \\
\frac{\partial H_2}{\partial y_1} & \frac{\partial H_2}{\partial y_2} & \cdots & \frac{\partial H_2}{\partial y_n} \\
\vdots & \vdots & \ddots & \vdots \\
\frac{\partial H_n}{\partial y_1} & \frac{\partial H_n}{\partial y_2} & \cdots & \frac{\partial H_n}{\partial y_n} \\
\end{bmatrix} \\
f_{\mathbf{Y}}(\mathbf{y})=f_{\mathbf{X}}(H(\mathbf{y}))\left | J \right |
$$

이 방법을 이용하여 $\mathbf{Y}=\mathbf{A}\mathbf{X}+\mathbf{b}$일 때 Probability Density Function $f_{\mathbf{Y}}(\mathbf{y})$는 다음과 같이 구합니다.

$$
\mathbf{Y}=\mathbf{A}\mathbf{X}+\mathbf{b}=G(\mathbf{X}) \\
\mathbf{X}=\mathbf{A}^{-1}(\mathbf{Y}-\mathbf{b})=H(\mathbf{Y}) \\
J=\det(\mathbf{A}^{-1})=\frac{1}{\det(\mathbf{A})} \\
f_{\mathbf{Y}}(\mathbf{y})=f_{\mathbf{X}}(H(\mathbf{y}))\left | J \right |=f_{\mathbf{X}}(\mathbf{A}^{-1}(\mathbf{y}-\mathbf{b}))\left | \frac{1}{\det(\mathbf{A})} \right |
$$

## Standard Normal Distribution {#Standard-Normal-Distribution}

$Z_i \sim N(0,1)$일 때 [Normal Distribution](/techblog/Derivation-of-the-Probability-Distribution-Functions#Normal)을 참조해 보면 Probability Density Function $f_{Z_i}(z_i)$는 다음과 같습니다.

$f_{Z_i}(z_i)=\frac{1}{\sqrt{2\pi}}\exp\left (-\frac{1}{2}z_i^2\right )$

$Z_i \sim N(0,1)$가 iid이고 $\mathbf{Z}= \begin{bmatrix} Z_1 & Z_2 & \cdots & Z_n \end{bmatrix}^T$라고 할 때 $f_{\mathbf{Z}}(\mathbf{z})$는 다음과 같습니다.

$$
\begin{aligned}
f_{\mathbf{Z}}(\mathbf{z})
&=\prod_{i=1}^{n}f_{Z_i}(z_i) \\
&=\frac{1}{(2\pi)^{\frac{n}{2}}}\exp\left (-\frac{1}{2}\sum_{i=1}^n z_i^2\right ) \\
&=\frac{1}{(2\pi)^{\frac{n}{2}}}\exp\left (-\frac{1}{2}\mathbf{z}^T\mathbf{z}\right ) \\
\end{aligned}
$$

## Multivariate Normal Distribution {#Multivariate-Normal-Distribution}

$\mathbf{Z} \sim (\mathbf{0}, \mathbf{I})$, $\mathbf{X} = \mathbf{A}\mathbf{Z}+\mathbf{m}$일때 $f_{\mathbf{X}}(\mathbf{x})$는 다음과 같이 구합니다.

$$
E(\mathbf{X})=\mathbf{m} \\
\mathbf{C_X}=\mathbf{A}\mathbf{C_Z}\mathbf{A}^T=\mathbf{A}\mathbf{A}^T \\
\det(\mathbf{C_X})=\det(\mathbf{A}\mathbf{A}^T)=\det(\mathbf{A})\det(\mathbf{A}^T)=(\det(\mathbf{A}))^2 \\
\sqrt{\det(\mathbf{C_X})}=\left | \det(\mathbf{A}) \right | \\
\begin{aligned}
f_{\mathbf{X}}(\mathbf{x})
&=f_{\mathbf{Z}}(H(\mathbf{x}))\left | J \right | \\
&=f_{\mathbf{Z}}(\mathbf{A}^{-1}(\mathbf{x}-\mathbf{m}))\left | \frac{1}{\det(\mathbf{A})} \right | \\
&=\frac{1}{(2\pi)^{\frac{n}{2}}}\left | \frac{1}{\det(\mathbf{A})} \right | \exp\left (-\frac{1}{2}(\mathbf{A}^{-1}(\mathbf{x}-\mathbf{m}))^T(\mathbf{A}^{-1}(\mathbf{x}-\mathbf{m}))\right ) \\
&=\frac{1}{(2\pi)^{\frac{n}{2}}\sqrt{\det(\mathbf{C_X})}}\exp\left (-\frac{1}{2}(\mathbf{x}-\mathbf{m})^T(\mathbf{A}\mathbf{A}^T)^{-1}(\mathbf{x}-\mathbf{m})\right ) \\
&=\frac{1}{(2\pi)^{\frac{n}{2}}\sqrt{\det(\mathbf{C_X})}}\exp\left (-\frac{1}{2}(\mathbf{x}-\mathbf{m})^T\mathbf{C_X}^{-1}(\mathbf{x}-\mathbf{m})\right ) \\
\end{aligned}
$$

우리는 보통 $\mathbf{X}$를 Data의 형태로 가지고 있고 $\mathbf{A}$를 가지고 있지 않은데 $f_{\mathbf{X}}(\mathbf{x})$를 살펴보면 $\mathbf{A}$가 필요없고 $\mathbf{C_X}$만 가지고 있으면 됩니다. $\mathbf{X}$의 Data를 통해 $\mathbf{C_X}$를 쉽게 계산할 수 있습니다. 하지만 $\mathbf{X}$의 차원이 늘어나면 $\mathbf{C_X}^{-1}$의 계산이 점점 어려워집니다.

## Bivariate Normal Distribution {#Bivariate-Normal-Distribution}

$X \sim N(\mu_X, \sigma_X)$, $Y \sim N(\mu_Y, \sigma_Y)$, $\rho=\frac{Cov(X,Y)}{\sigma_X\sigma_Y}$ 일 때 $f_{XY}(x,y)$는 다음과 같이 구합니다. Multivariate Normal Distribution의 특수 Case이기 때문에 Multivariate Normal Distribution을 사용하면 어렵지 않게 구할 수 있습니다.

$$
n=2 \\
\mathbf{X}=
\begin{bmatrix}
X \\
Y
\end{bmatrix} \\
\mathbf{x}=
\begin{bmatrix}
x \\
y
\end{bmatrix} \\
\mathbf{m}=
\begin{bmatrix}
\mu_X \\
\mu_Y
\end{bmatrix} \\
\mathbf{C_X}=
\begin{bmatrix}
Var(X) & Cov(X,Y) \\
Cov(Y,X) & Var(Y)
\end{bmatrix}
=
\begin{bmatrix}
\sigma_X^2 & \rho\sigma_X\sigma_Y \\
\rho\sigma_X\sigma_Y & \sigma_Y^2
\end{bmatrix} \\
\det(\mathbf{C_X})=\sigma_X^2\sigma_Y^2(1-\rho^2) \\
\mathbf{C_X}^{-1}=\frac{1}{\sigma_X^2\sigma_Y^2(1-\rho^2)}
\begin{bmatrix}
\sigma_Y^2 & -\rho\sigma_X\sigma_Y \\
-\rho\sigma_X\sigma_Y & \sigma_X^2
\end{bmatrix} \\
\begin{aligned}
f_{XY}(x,y)
&=f_{\mathbf{X}}(\mathbf{x}) \\
&=\frac{1}{(2\pi)^{\frac{n}{2}}\sqrt{\det(\mathbf{C_X})}}\exp\left (-\frac{1}{2}(\mathbf{x}-\mathbf{m})^T\mathbf{C_X}^{-1}(\mathbf{x}-\mathbf{m})\right ) \\
&=\frac{1}{2\pi\sigma_X\sigma_Y\sqrt{1-\rho^2}}\exp\left (-\frac{1}{2}\frac{1}{\sigma_X^2\sigma_Y^2(1-\rho^2)}
\begin{bmatrix}
x-\mu_X \\
y-\mu_Y
\end{bmatrix}^T
\begin{bmatrix}
\sigma_Y^2 & -\rho\sigma_X\sigma_Y \\
-\rho\sigma_X\sigma_Y & \sigma_X^2
\end{bmatrix}
\begin{bmatrix}
x-\mu_X \\
y-\mu_Y
\end{bmatrix}
\right ) \\
&=\frac{1}{2\pi\sigma_X\sigma_Y\sqrt{1-\rho^2}}\exp\left (-\frac{1}{2(1-\rho^2)}( (\frac{x-\mu_X}{\sigma_X})^2 + (\frac{y-\mu_Y}{\sigma_Y})^2 - 2\rho\frac{(x-\mu_X)(y-\mu_Y)}{\sigma_X\sigma_Y})\right )
\end{aligned}
$$



