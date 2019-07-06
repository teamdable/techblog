---
layout: post
title:  "Independent and Uncorrelated"
date:   2019-07-05 23:00:00 +0900
author: Taeho Oh
tags: [ 오태호, 수학, 통계학 ]
---
안녕하세요. 오태호입니다.

이번 글에서는 Independent와 Uncorrelated에 관해서 설명해 드리도록 하겠습니다. Independent와 Uncorrelated는 다른 개념인데 같다고 착각하는 사람도 많아서 어떤 차이가 있고 어떤 관계가 있는지 살펴보도록 하겠습니다.

## Independent {#Independent}
Random Variable $X$와 $Y$가 Independent하다는 것은 다음과 같이 정의합니다.

$$
P(X,Y)=P(X)P(Y)
$$

$X$와 $Y$의 joint pdf를 $f_{XY}(x,y)$라고 하고 $X$와 $Y$의 각각의 pdf를 $f_X(x)$, $f_Y(y)$라고 한다면 $X$와 $Y$가 Independent일 때 다음과 같은 성질을 가집니다.

$$
f_{XY}(x,y)=f_X(x)f_Y(y)
$$

## Uncorrelated {#Uncorrelated}
Random Variable $X$와 $Y$가 Uncorrelated하다는 것은 다음과 같이 정의합니다.

$$
E(XY)=E(X)E(Y)
$$

Random Variable $X$와 $Y$의 Covariance는 아래와 같이 정의합니다.

$$
\begin{aligned}
Cov(X,Y)
&=E((X-E(X))(Y-E(Y))) \\
&=E(XY-E(Y)X-E(X)Y+E(X)E(Y)) \\
&=E(XY)-E(X)E(Y)
\end{aligned}
$$

Random Variable $X$와 $Y$가 Uncorrelated하면 Covariance는 아래와 같이 $0$이 됩니다.

$$
\begin{aligned}
Cov(X,Y)
&=E(XY)-E(X)E(Y) \\
&=E(X)E(Y)-E(X)E(Y) \\
&=0
\end{aligned}
$$

## Independent and Uncorrelated {#Independent-and-Uncorrelated}
Random Variable $X$와 $Y$가 Independent일 때, $X$와 $Y$는 Uncorrelated하다는 것은 다음과 같이 증명합니다.

$X$와 $Y$의 pdf를 각각 $f_X(x)$, $f_Y(y)$라고 하면 $E(X)$, $E(Y)$, $E(XY)$는 다음과 같이 구할 수 있습니다.

$$
E(X)=\int_{-\infty}^\infty xf_X(x)dx \\
E(Y)=\int_{-\infty}^\infty yf_Y(y)dy \\
E(XY)=\int_{-\infty}^\infty \int_{-\infty}^\infty xyf_{XY}(x,y)dxdy \\
$$

$X$와 $Y$가 Independent하면 $f_{XY}(x,y)=f_X(x)f_Y(y)$이므로 아래와 같이 정리할 수 있습니다.

$$
\begin{aligned}
E(XY)
&=\int_{-\infty}^\infty \int_{-\infty}^\infty xyf_{XY}(x,y)dxdy \\
&=\int_{-\infty}^\infty \int_{-\infty}^\infty xyf_X(x)f_Y(y)dxdy \\
&=\int_{-\infty}^\infty xf_X(x)dx\int_{-\infty}^\infty yf_Y(y)dy \\
&=E(X)E(Y)
\end{aligned}
$$

즉, Random Variable $X$와 $Y$가 Independent하면 $X$와 $Y$는 Uncorrelated합니다.

하지만 Random Variable $X$와 $Y$가 Uncorrelated할 때 $X$와 $Y$가 Independent하다는 보장은 없습니다. (Independent할 수도 있고 하지 않을 수도 있습니다.) 다음과 같이 $X$와 $Y$가 Uncorrelated면서 Indepepdent하지 않은 상황이 존재할 수 있습니다.

Random Variable $A$와 $B$가 $A \sim ~ Bernoulli(\frac{1}{2})$, $B \sim ~ Bernoulli(\frac{1}{2})$와 같이 [Bernoulli Distribution](/techblog/Derivation-of-the-Probability-Distribution-Functions#Bernoulli)을 따르고 Independent하다고 할 때 $X$와 $Y$를 다음과 같이 정의합니다.

$$
X=A+B \\
Y=\left | A-B \right |
$$

이때 $X$와 $Y$의 분포는 아래와 같이 정리할 수 있습니다. 각각의 상황이 발생할 확률은 $\frac{1}{4}$입니다.

| A | B | X | Y |   P |
|---|---|---|---|-----|
| 0 | 0 | 0 | 0 | 1/4 |
|---|---|---|---|-----|
| 0 | 1 | 1 | 1 | 1/4 |
|---|---|---|---|-----|
| 1 | 0 | 1 | 1 | 1/4 |
|---|---|---|---|-----|
| 1 | 1 | 2 | 0 | 1/4 |
|---|---|---|---|-----|

$X$와 $Y$가 Uncorrelated하다는 것은 다음과 같이 확인할 수 있습니다.

$$
E(X)=0\times\frac{1}{4}+1\times\frac{1}{4}+1\times\frac{1}{4}+2\times\frac{1}{4}=1 \\
E(Y)=0\times\frac{1}{4}+1\times\frac{1}{4}+1\times\frac{1}{4}+0\times\frac{1}{4}=\frac{1}{2} \\
E(XY)=0\times0\times\frac{1}{4}+1\times1\times\frac{1}{4}+1\times1\times\frac{1}{4}+2\times0\times\frac{1}{4}=\frac{1}{2} \\
E(XY)=E(X)E(Y)
$$

$X$와 $Y$가 Independent하지 않다는 것은 다음과 같이 확인할 수 있습니다.

$$
P(X=0)=\frac{1}{4} \\
P(Y=0)=\frac{1}{2} \\
P(X=0,Y=0)=\frac{1}{4} \\
P(X=0,Y=0) \neq P(X=0)P(Y=0)
$$

즉, $X$와 $Y$가 Uncorrelated하지만 Independent하지 않은 경우가 존재합니다. 그래서 Random Variable $X$와 $Y$가 Uncorrelated할 때 반드시 $X$와 $Y$가 Independent하다고 말할 수 없습니다. (Independent할 수도 있고 하지 않을 수도 있습니다.)

## Bivariate Normal Distribution {#Bivariate-Normal-Distribution}

Random Variable $X$와 $Y$가 [Bivariate Normal Distribution](/techblog/Derivation-of-the-Multivariate-Normal-Distribution#Bivariate-Normal-Distribution)을 따른다면 $f_X(x)$, $f_Y(y)$, $f_{XY}(x,y)$는 아래와 같습니다.

$$
f_X(x)=\frac{1}{\sigma_X\sqrt{2\pi}}\exp\left (-\frac{(x-\mu_X)^2}{2\sigma_X^2}\right ) \\
f_Y(y)=\frac{1}{\sigma_Y\sqrt{2\pi}}\exp\left (-\frac{(y-\mu_Y)^2}{2\sigma_Y^2}\right ) \\
f_{XY}(x,y)=\frac{1}{2\pi\sigma_X\sigma_Y\sqrt{1-\rho^2}}\exp\left (-\frac{1}{2(1-\rho^2)}( (\frac{x-\mu_X}{\sigma_X})^2 + (\frac{y-\mu_Y}{\sigma_Y})^2 - 2\rho\frac{(x-\mu_X)(y-\mu_Y)}{\sigma_X\sigma_Y})\right )
$$

$X$와 $Y$가 Uncorrelated하다면 $\rho=\frac{Cov(X,Y)}{\sigma_X\sigma_Y}=0$이 되어서 아래와 같이 됩니다.

$$
\begin{aligned}
f_{XY}(x,y)
&=\frac{1}{2\pi\sigma_X\sigma_Y}\exp\left (-\frac{1}{2}( (\frac{x-\mu_X}{\sigma_X})^2 + (\frac{y-\mu_Y}{\sigma_Y})^2)\right ) \\
&=f_X(x)f_Y(y)
\end{aligned}
$$

즉, Random Variable $X$와 $Y$가 Bivariate Normal Distribution을 따르고 $X$와 $Y$가 Uncorrelated하다면 $X$와 $Y$는 Independent합니다.

## Normal Distribution {#Normal-Distribution}

$X \sim N(0,1)$이고 $W$가 [Rademacher Distribution](/techblog/Derivation-of-the-Probability-Distribution-Functions#Rademacher)을 따르고 $Y=WX$이라고 해 봅시다. 이 경우 $Y$도 $Y \sim N(0,1)$이 되어 $X$와 $Y$는 둘 다 [Normal Distribution](/techblog/Derivation-of-the-Probability-Distribution-Functions#Normal)을 따르게 됩니다.

$X$와 $Y$는 Uncorrelated하다는 것을 다음과 같이 증명할 수 있습니다.

$$
E(X)=0 \\
E(Y)=0 \\
\begin{aligned}
Cov(X,Y)
&=E(XY)-E(X)E(Y) \\
&=E(XY)-0 \\
&=E(X^2W) \\
&=E(X^2)E(W) \\
&=E(X^2) \cdot 0 \\
&=0
\end{aligned}
$$

$X$와 $Y$가 Independent하지 않다는 것은 다음과 같이 확인할 수 있습니다.

$$
P(X=\frac{1}{2})=0 \\
P(Y=\frac{1}{2})=0 \\
P(X=\frac{1}{2},Y=\frac{1}{2})=\frac{1}{2} \\
P(X=\frac{1}{2},Y=\frac{1}{2}) \neq P(X=\frac{1}{2})P(X=\frac{1}{2})
$$

즉, Random Variable $X$와 $Y$가 각각이 Normal Distribution을 따를 때 $X$와 $Y$가 Uncorrelated하면서 $X$와 $Y$가 Independent하지 않은 경우가 존재합니다. 그래서 Random Variable $X$와 $Y$가 각각이 Normal Distribution을 따를 때 $X$와 $Y$가 Uncorrelated하다고 해서 반드시 $X$와 $Y$가 Independent하지는 않습니다. (Independent할 수도 있고 하지 않을 수도 있습니다.)

## 맺음말
* Random Variable $X$와 $Y$가 Independent하면 $X$와 $Y$는 Uncorrelated합니다.
* Random Variable $X$와 $Y$가 Uncorrelated하다고 해서 반드시 $X$와 $Y$가 Independent하지는 않습니다. (Independent할 수도 있고 하지 않을 수도 있습니다.)
* $X$와 $Y$가 Bivariate Normal Distribution을 따르고 $X$와 $Y$가 Uncorrelated하면 $X$와 $Y$는 Independent합니다.
* $X$와 $Y$가 각각 Normal Distribution을 따르고 $X$와 $Y$가 Uncorrelated하다고 해서 반드시 $X$와 $Y$가 Independent하지는 않습니다. (Independent할 수도 있고 하지 않을 수도 있습니다.)
