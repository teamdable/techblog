---
layout: post
title:  "Sample Mean and Sample Variance"
date:   2019-07-12 23:00:00 +0900
author: Taeho Oh
tags: [ 오태호, 수학, 통계학 ]
---
안녕하세요. 오태호입니다.

이번 글에서는 Sample Mean과 Sample Variance에 대해서 설명드리도록 하겠습니다. 쉬운 내용인 것 같으면서도 Sample Variance를 구할 때 $n$이 아니라 $n-1$로 나누는 이유에 대해서 잘 이해하고 있지 못하는 사람도 많이 있어서 조금 자세히 설명해 보도록 하겠습니다. 그리고 추가로 Normal Distribution인 경우에 Sample Mean과 Sample Variance가 가지고 있는 특징도 몇가지 살펴보도록 하겠습니다.

## Sample Mean {#Sample-Mean}
Random Variable $X$의 Mean인 $\mu$를 구하려고 합니다. 하지만 현실적으로 정확히 $\mu$를 구하는 것이 불가능하여 $n$개의 $X$의 Sample을 가지고 $X$의 Mean인 $\mu$를 추정하려고 합니다. 이와 같이 $n$개의 $X$의 Sample을 이용하여 $X$의 Mean인 $\mu$를 추정한 것을 Sample Mean이라고 합니다.

$X$에서 $n$개의 Sample을 뽑은 것을 $X_1$, $X_2$, $\cdots$, $X_n$이라고 해 봅시다. $n$개의 Sample을 뽑는 행동 자체를 여러번 반복해 보면 뽑을 때마다 $X_1$, $X_2$, $\cdots$, $X_n$는 각각의 값이 일정하지 않고 계속 바뀔 것이라는 것을 예상할 수 있습니다. 그래서, $X_1$, $X_2$, $\cdots$, $X_n$는 각각이 Constant가 아니라 iid인 Random Variable이 됩니다.

$X$에서 $n$개의 Sample을 뽑아서 계산한 $X$의 Sample Mean인 $\bar{X}$는 다음과 같이 정의합니다.

$$
\bar{X}=\frac{1}{n}\sum_{i=1}^nX_i
$$

앞에서 언급한 바와 같이 $X_1$, $X_2$, $\cdots$, $X_n$는 각각이 값이 고정되어 있지 않고 계속 바뀌는 Random Variable입니다. 그 Random Variable로부터 $\bar{X}$를 계산했기 때문에 $\bar{X}$도 Random Variable이 됩니다. $\bar{X}$가 Random Variable이므로 $\bar{X}$의 Mean도 계산할 수 있습니다. $\bar{X}$의 Mean을 다음과 같이 계산해 볼 수 있습니다.

$$
\begin{aligned}
E(\bar{X})
&=E\left(\frac{1}{n}\sum_{i=1}^nX_i\right) \\
&=E\left(\frac{1}{n}(X_1+X_2+\cdots+X_n)\right) \\
&=\frac{1}{n}(E(X_1)+E(X_2)+\cdots+E(X_n)) \\
&=\frac{1}{n}(\mu+\mu+\cdots+\mu) \\
&=\frac{1}{n}(n\mu) \\
&=\mu
\end{aligned}
$$

$\bar{X}$를 여러번 계속 구해서($n$개의 Sample을 뽑는 행동을 여러번 계속 해서) $\bar{X}$의 Mean을 구해 보면 $\mu$가 된다는 사실에 비추어볼 때 $X$의 Mean인 $\mu$를 $\bar{X}$로 추정하는 것은 합리적이라는 것을 알 수 있습니다.

## Variance {#Variance}
Sample Variance를 살펴보기에 앞서 알고 있으면 편한 Variance의 몇가지 성질에 대해 살펴보도록 하겠습니다.

Random Variable $X$의 Variance인 $\sigma^2$는 다음과 같이 정의합니다.

$$
\begin{aligned}
Var(X)
&=\sigma^2 \\
&=E((X-E(X))^2) \\
&=E(X^2-2XE(X)+(E(X))^2) \\
&=E(X^2)-2E(X)E(X)+(E(X))^2 \\
&=E(X^2)-(E(X))^2
\end{aligned}
$$

$a$와 $b$가 Constant일 때 Random Variable $aX+b$의 Variance는 다음과 같이 구할 수 있습니다.

$$
\begin{aligned}
Var(aX+b)
&=E((aX+b-E(aX+b))^2) \\
&=E((aX-aE(X))^2) \\
&=E(a^2(X-E(X))^2) \\
&=a^2E((X-E(X))^2) \\
&=a^2Var(X) \\
&=a^2\sigma^2
\end{aligned}
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

Random Variable $X+Y$와 $Z$의 Covariance는 다음과 같이 구할 수 있습니다.

$$
\begin{aligned}
Cov(X+Y,Z)
&=E((X+Y)Z)-E(X+Y)E(Z) \\
&=E(XZ)+E(YZ)-E(X)E(Z)-E(Y)E(Z) \\
&=(E(XZ)-E(X)E(Z))+(E(YZ)-E(Y)E(Z)) \\
&=Cov(X,Z)+Cov(Y,Z)
\end{aligned}
$$

$a$와 $b$가 Constant일 때 Random Variable $aX+b$와 $Y$의 Covariance는 다음과 같이 구할 수 있습니다.

$$
\begin{aligned}
Cov(aX+b,Y)
&=E((aX+b)Y)-E(aX+b)E(Y) \\
&=aE(XY)+bE(Y)-aE(X)E(Y)-bE(Y) \\
&=a(E(XY)-E(X)E(Y)) \\
&=aCov(X,Y)
\end{aligned}
$$

Random Variable $X+Y$의 Variance는 다음과 같이 구할 수 있습니다.

$$
\begin{aligned}
Var(X+Y)
&=Cov(X+Y,X+Y) \\
&=Cov(X,X+Y)+Cov(Y,X+Y) \\
&=(Cov(X,X)+Cov(X,Y))+(Cov(Y,X)+Cov(Y,Y)) \\
&=(Var(X)+Cov(X,Y))+(Cov(X,Y)+Var(Y)) \\
&=Var(X)+Var(Y)+2Cov(X,Y)
\end{aligned}
$$

Random Variable $X$의 Sample Mean인 $\bar{X}$도 Random Variable이므로 Sample Mean의 Variance도 계산할 수 있습니다. $\bar{X}$의 Variance를 다음과 같이 계산해 볼 수 있습니다.

$$
\begin{aligned}
Var(\bar{X})
&=Var\left(\frac{1}{n}\sum_{i=1}^nX_i\right) \\
&=Var\left(\frac{1}{n}(X_1+X_2+\cdots+X_n)\right) \\
&=\frac{1}{n^2}(Var(X_1)+Var(X_2)+\cdots+Var(X_n)) \\
&=\frac{1}{n^2}(\sigma^2+\sigma^2+\cdots+\sigma^2) \\
&=\frac{1}{n^2}(n\sigma^2) \\
&=\frac{\sigma^2}{n}
\end{aligned}
$$

Random Variable $X_1$, $X_2$, $\cdots$, $X_n$는 각각이 iid이기 때문에 서로간의 Covariance가 모두 $0$이 되어서 $Var(X_1+X_2+\cdots+X_n)=Var(X_1)+Var(X_2)+\cdots+Var(X_n)$이 되어서 간단하게 정리되는 것을 살펴볼 수 있습니다. Independent일 때 Uncorrelated하고 Covariance가 $0$이 되는 것에 대한 자세한 내용은 [Independent and Uncorrelated](/techblog/Independent-and-Uncorrelated#Uncorrelated)을 살펴보시기 바랍니다.

좀 더 직관적으로 설명해 보겠습니다. $n$개의 $X$의 Sample을 뽑아서 $X$의 Sample Mean인 $\bar{X}$를 구하는 행동을 반복해서 여러번 해 보면 $\bar{X}$가 일정하지 않고 계속 바뀌게 되는데 $\bar{X}$의 변화가 심하면 $Var(\bar{X})$가 커지고, $\bar{X}$의 변화가 심하지 않으면 $Var(\bar{X})$가 작아집니다. Sample의 갯수인 $n$을 많이 늘리면 $\bar{X}$를 구하는 행동을 반복해도 $\bar{X}$의 변화가 심하지 않을 것을 예상할 수 있는데, 위의 식을 살펴봐도 $n$이 늘면 $Var(\bar{X})$가 작아져서 $\bar{X}$의 변화가 심하지 않게 될 것을 예상할 수 있습니다.

## Sample Variance {#Sample-Variance}
Random Variable $X$의 Variance인 $\sigma^2$를 구하려고 합니다. 하지만 현실적으로 정확히 $\sigma^2$를 구하는 것이 불가능하여 $n$개의 $X$의 Sample을 가지고 $X$의 Variance인 $\sigma^2$를 추정하려고 합니다. 이와 같이 $n$개의 $X$의 Sample을 이용하여 $X$의 Variance인 $\sigma^2$를 추정한 것을 Sample Variance이라고 합니다.

$X$에서 $n$개의 Sample을 뽑아서 계산한 $X$의 Sample Variance인 $s^2$은 다음과 같이 정의합니다.

$$
s^2=\frac{1}{n-1}\sum_{i=1}^n(X_i-\bar{X})^2
$$

하지만 여기서는 계산과정에서 $n-1$로 나눈 이유를 이해해 보기 위해 $n$으로 나누면 어떻게 되는지 $\bar{s}^2$를 다음과 같이 정의해서 $\bar{s}^2$의 특징을 살펴보도록 하겠습니다.

$$
\bar{s}^2=\frac{1}{n}\sum_{i=1}^n(X_i-\bar{X})^2
$$

Sample Mean을 살펴봤을 때와 마찬가지로 $X_1$, $X_2$, $\cdots$, $X_n$는 각각이 iid인 Random Variable이고 거기에서 파생된 $\bar{X}$와 $\bar{s}^2$도 Random Variable입니다. $\bar{s}^2$가 Random Variable이므로 $\bar{s}^2$의 Mean을 다음과 같이 계산해 볼 수 있습니다.

$$
\begin{aligned}
E(\bar{s}^2)
&=E\left(\frac{1}{n}\sum_{i=1}^n(X_i-\bar{X})^2\right) \\
&=E\left(\frac{1}{n}\sum_{i=1}^n(X_i^2-2\bar{X}X_i+\bar{X}^2)\right) \\
&=E\left(\frac{1}{n}\sum_{i=1}^nX_i^2-2\bar{X}\frac{1}{n}\sum_{i=1}^nX_i+\frac{1}{n}\sum_{i=1}^n\bar{X}^2)\right) \\
&=E\left(\frac{1}{n}\sum_{i=1}^nX_i^2-2\bar{X}^2+\frac{1}{n}(n\bar{X}^2)\right) \\

&=\frac{1}{n}\sum_{i=1}^nE(X_i^2)-2E(\bar{X}^2)+E(\bar{X}^2) \\
&=\frac{1}{n}\sum_{i=1}^nE(X_i^2)-E(\bar{X}^2)
\end{aligned}
$$

$E(\bar{s}^2)$을 좀 더 간단하게 정리하기 위해 다음 성질을 이용합니다.

$$
Var(X)=E(X^2)-(E(X))^2 \\
\begin{aligned}
E(X^2)
&=Var(X)+(E(X))^2 \\
&=\sigma^2+\mu^2 \\
\end{aligned} \\
Var(\bar{X})=E(\bar{X}^2)-(E(\bar{X}))^2 \\
\begin{aligned}
E(\bar{X}^2)
&=Var(\bar{X})+(E(\bar{X}))^2 \\
&=\frac{\sigma^2}{n}+\mu^2 \\
\end{aligned}
$$

위의 성질을 이용해 다음과 같이 $E(\bar{s}^2)$ 를 더 간단하게 정리합니다.

$$
\begin{aligned}
E(\bar{s}^2)
&=\frac{1}{n}\sum_{i=1}^nE(X_i^2)-E(\bar{X}^2) \\
&=\frac{1}{n}(E(X_1^2)+E(X_2^2)+\cdots+E(X_n^2))-E(\bar{X}^2) \\
&=\frac{1}{n}((\sigma^2+\mu^2)+(\sigma^2+\mu^2)+\cdots+(\sigma^2+\mu^2))-E(\bar{X}^2) \\
&=\frac{1}{n}(n(\sigma^2+\mu^2))-E(\bar{X}^2) \\
&=\sigma^2+\mu^2-E(\bar{X}^2) \\
&=\sigma^2+\mu^2-\left(\frac{\sigma^2}{n}+\mu^2\right) \\
&=\frac{n-1}{n}\sigma^2
\end{aligned}
$$

$\bar{s}^2$을 여러번 계속 구해서($n$개의 Sample을 뽑는 행동을 여러번 계속 해서) $\bar{s}^2$의 Mean을 구해 보면 $\sigma^2$가 아니라 $\sigma^2$보다 약간 작은 $\frac{n-1}{n}\sigma^2$가 된다는 사실을 알 수 있습니다. $n$개의 Sample을 뽑는 행동을 여러번 계속 해서 $\bar{s}^2$의 Mean을 구했을 때 결과가 $\frac{n-1}{n}\sigma^2$대신에 $\sigma^2$으로 나오게 하기 위해서는 $\bar{s}^2$대신에 $\frac{n}{n-1}\bar{s}^2$을 여러번 계속 구해서 $\frac{n}{n-1}\bar{s}^2$의 Mean을 구해야 합니다. 그런데 살펴보면 $\frac{n}{n-1}\bar{s}^2$은 위에서 정의한 Sample Variance인 $s^2$과 일치합니다. 즉, $s^2$을 여러번 계속 구해서 ($n$개의 Sample을 뽑는 행동을 여러번 계속 해서) $s^2$의 Mean을 구해 보면 $\sigma^2$이 된다는 사실에 비추어볼 때 $X$의 Variance인 $\sigma^2$을 $s^2$로 추정하는 것은 합리적이라는 것을 알 수 있습니다.

즉, Sample Variance를 구할 때 $n$으로 나누면 우리가 추정하고자 하는 실제 Variance보다 작은 값을 추정하게 되고 $n-1$로 나누게 되면 우리가 추정하고자 하는 실제 Variance를 추정하게 되기 때문에 Sample Variance를 구할 때 $n-1$로 나누어서 구합니다.

## Sample Mean and Normal Distribution {#Sample-Mean-and-Normal-Distribution}

Random Variable $X_1$, $X_2$, $\cdots$, $X_n$이 Normal Distribution을 따르고 iid일 때, Sample Mean인 $\bar{X}$와 $X_i-\bar{X}$는 Independent하다는 것을 다음과 같이 증명할 수 있습니다.

우선 $\bar{X}$와 $X_i-\bar{X}$가 Uncorrelated하다는 것을 다음과 같이 증명합니다.

$$
\begin{aligned}
Cov(\bar{X}, X_i-\bar{X})
&=Cov(\bar{X},X_i)-Cov(\bar{X},\bar{X}) \\
&=Cov\left(\frac{1}{n}(X_1+X_2+\cdots+X_n),X_i\right)-Var(\bar{X}) \\
&=Cov\left(\frac{1}{n}X_i,X_i\right)-Var\left(\frac{1}{n}(X_1+X_2+\cdots+X_n)\right) \\
&=\frac{1}{n}Cov(X_i,X_i)-\frac{1}{n^2}(Var(X_1)+Var(X_2)+\cdots+Var(X_n)) \\
&=\frac{1}{n}Var(X_i)-\frac{1}{n^2}(nVar(X_i)) \\
&=0
\end{aligned}
$$

$\bar{X}$와 $X_i-\bar{X}$가 Bivariate Normal Distribution을 따르는 것은 다음과 같이 확인할 수 있습니다.

$$
\begin{bmatrix}
\bar{X} \\
X_i-\bar{X}
\end{bmatrix}
=
\begin{bmatrix}
\frac{1}{n} & \frac{1}{n} \\
1-\frac{1}{n} & -\frac{1}{n}
\end{bmatrix}
\begin{bmatrix}
X_i \\
\sum_{k \neq i}X_k
\end{bmatrix}
$$

$\bar{X}$와 $X_i-\bar{X}$는 Normal Distribution을 따르는 Independent한 Random Variable인 $X_i$와 $\sum_{k \neq i}X_k$의 Linear Transformation으로 표현이 가능하기 때문에 $\bar{X}$와 $X_i-\bar{X}$는 Bivariate Normal Distribution을 따릅니다.

$\bar{X}$와 $X_i-\bar{X}$가 Bivariate Normal Distribution을 따르고 Uncorrelated하기 때문에 $\bar{X}$와 $X_i-\bar{X}$는 Independent합니다. Bivariate Normal Distribution을 따르고 Uncorrelated할 때 Independent한 것에 대한 자세한 내용은 [Independent and Uncorrelated](/techblog/Independent-and-Uncorrelated#Bivariate-Normal-Distribution)을 살펴보시기 바랍니다.

## Sample Variance and Normal Distribution {#Sample-Variance-and-Normal-Distribution}

Random Variable $X_1$, $X_2$, $\cdots$, $X_n$이 $X_i \sim N(\mu, \sigma^2)$이고 iid일 때 Sample Variance를 $s^2$이라 하면 $(n-1)\frac{s^2}{\sigma^2} \sim \chi_{n-1}^2$이 성립함을 다음과 같이 증명할 수 있습니다.

우선 Random Variable $Z_1$, $Z_2$, $\cdots$, $Z_n$이 $Z_i \sim N(0,1)$이고 iid일 때 Sample Mean을 $\bar{Z}$라고 하면 $\sum_{i=1}^n(Z_i-\bar{Z})^2 \sim \chi_{n-1}^2$이 성립함을 다음과 증명합니다.

$$
\begin{aligned}
\sum_{i=1}^n(Z_i-\bar{Z})^2+n\bar{Z}^2
&=\sum_{i=1}^n(Z_i^2-2Z_i\bar{Z}+\bar{Z}^2)+n\bar{Z}^2 \\
&=\sum_{i=1}^nZ_i^2-2\sum_{i=1}^nZ_i\bar{Z}+\sum_{i=1}^n\bar{Z}^2+n\bar{Z}^2 \\
&=\sum_{i=1}^nZ_i^2-2(Z_1+Z_2+\cdots+Z_n)\bar{Z}+n\bar{Z}^2+n\bar{Z}^2 \\
&=\sum_{i=1}^nZ_i^2-2(n\bar{Z})\bar{Z}+n\bar{Z}^2+n\bar{Z}^2 \\
&=\sum_{i=1}^nZ_i^2 \sim \chi_n^2
\end{aligned} \\
Var(\bar{Z})=\frac{1}{n} \\
\sqrt{n}\bar{Z} \sim N(0,1) \\
n\bar{Z}^2 \sim \chi_1^2
$$

앞의 [Sample Mean and Normal Distribution](#Sample-Mean-and-Normal-Distribution)에서 언급된 바에 따르면 $\bar{Z}$와 $Z_i-\bar{Z}$는 Independent합니다. 그래서 MGF를 다음과 같이 계산할 수 있습니다.

$$
\sum_{i=1}^n(Z_i-\bar{Z})^2+n\bar{Z}^2=\sum_{i=1}^nZ_i^2 \\
MGF\left(\sum_{i=1}^n(Z_i-\bar{Z})^2+n\bar{Z}^2\right)=MGF\left(\sum_{i=1}^nZ_i^2\right) \\
MGF\left(\sum_{i=1}^n(Z_i-\bar{Z})^2\right)MGF\left(n\bar{Z}^2\right)=MGF\left(\sum_{i=1}^nZ_i^2\right) \\
MGF\left(\sum_{i=1}^n(Z_i-\bar{Z})^2\right)=\frac{MGF\left(\sum_{i=1}^nZ_i^2\right)}{MGF\left(n\bar{Z}^2\right)} \\
MGF\left(\sum_{i=1}^n(Z_i-\bar{Z})^2\right)=\frac{\left(\frac{1}{1-2t}\right)^{\frac{n}{2}}}{\left(\frac{1}{1-2t}\right)^{\frac{1}{2}}}=\left(\frac{1}{1-2t}\right)^{\frac{n-1}{2}} \\
\sum_{i=1}^n(Z_i-\bar{Z})^2 \sim \chi_{n-1}^2
$$

$X_i \sim N(\mu,\sigma^2)$이고 $Z_i \sim N(0,1)$이므로 $X_i=\mu+\sigma Z_i$, $\bar{X}=\mu+\sigma\bar{Z}$으로 표현할 수 있습니다. 이를 이용해서 $(n-1)\frac{s^2}{\sigma^2} \sim \chi_{n-1}^2$을 다음과 같이 증명합니다.

$$
\begin{aligned}
(n-1)\frac{s^2}{\sigma^2}
&=(n-1)\frac{1}{\sigma^2}\frac{1}{n-1}\sum_{i=1}^n(X_i-\bar{X})^2 \\
&=\frac{1}{\sigma^2}\sum_{i=1}^n(X_i-\bar{X})^2 \\
&=\frac{1}{\sigma^2}\sum_{i=1}^n(\mu+\sigma Z_i-(\mu+\sigma\bar{Z}))^2 \\
&=\frac{1}{\sigma^2}\sum_{i=1}^n\sigma^2(Z_i-\bar{Z})^2 \\
&=\sum_{i=1}^n(Z_i-\bar{Z})^2 \sim \chi_{n-1}^2 \\
\end{aligned}
$$

## Summary {#Summary}

* $n$개의 $X$의 Sample을 가지고 $X$의 Mean인 $\mu$를 추정한 것을 Sample Mean이라고 하며, Sample Mean $\bar{X}$는 $\bar{X}=\frac{1}{n}\sum_{i=1}^nX_i$와 같이 정의합니다.
* $n$개의 $X$의 Sample을 가지고 $X$의 Variance인 $\sigma^2$을 추정한 것을 Sample Variance라고 하며, Sample Variance $s^2$은 $s^2=\frac{1}{n-1}\sum_{i=1}^n(X_i-\bar{X})^2$와 같이 정의합니다.
* Random Variable $X_i$가 Normal Distribution을 따르고 iid이면 $\bar{X}$와 $X_i-\bar{X}$는 Independent합니다.
* Random Variable $X_i$가 Normal Distribution을 따르고 iid이면 $(n-1)\frac{s^2}{\sigma^2} \sim \chi_{n-1}^2$이 성립합니다.
