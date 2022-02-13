---
layout: post
title:  "Proof of the Chi Squared Test"
date:   2022-02-12 23:00:00 +0900
author: Taeho Oh
tags: [ 오태호, 수학, 통계학 ]
---

안녕하세요. 오태호입니다.

이 글에서는 Chi Squared Test의 수식을 증명해 보도록 하겠습니다. 교과서에 식만 나와 있고 증명이 생략되어 있는 경우가 많아서 정리해 보았습니다.

이 글을 이해하기 위해서는 Linear Algebra, Statistics에 대한 기초지식이 필요합니다.

Matrix나 Vector는 굵은 글꼴로 표현하도록 하겠습니다. 그리고 Vector는 특별히 언급이 없으면 Column Vector를 의미합니다.

## Chi Squared Test {#Chi-Squared-Test}

$$k$$개의 상자에 $$n$$개의 공을 던져서 넣는 상황을 생각해 봅니다.

공 하나가 각각의 상자에 들어갈 확률은 $$p_1, p_2, \cdots, p_k$$입니다. 공은 어딘가의 한 상자에 들어가야 하기 때문에 $$\sum_{j=1}^kp_j=1$$이 됩니다.

$$\mathbf{X}_1, \mathbf{X}_2, \cdots, \mathbf{X}_n$$는 각각의 공이 어느 상자에 들어있는지를 One Hot Vector 형태로 가집니다. 공은 어딘가의 한 상장에 들어가야 하기 때문에 $$\mathbf{X}_i$$는 $$k$$ Dimension으로 되어 있는 Vector이고 $$1$$개의 $$1$$과 $$k-1$$개의 $$0$$으로 이루어져 있습니다. 즉, $$i$$번 째 공이 $$j$$번째 상자에 공이 들어갔다면 $$\mathbf{X}_i$$ Vector에서 $$j$$번 째 Element만 $$1$$이고 나머지 Element는 $$0$$이 됩니다. $$X_{ij}$$는 $$\mathbf{X}_i$$ Vector에서 $$j$$번 째 Element를 의미합니다. 각 공은 다른 공에게 영향을 주지 않으며 모든 공은 동일한 형태로 동작합니다. 즉, $$\mathbf{X}_1, \mathbf{X}_2, \cdots, \mathbf{X}_n$$은 iid입니다. $$i$$번 째 공은 던질 때마다 다른 상자에 들어갈 수 있기 때문에 $$X_{ij}$$는 Random Variable입니다.

$$\bar{\mathbf{X}}$$는 다음과 같이 정의합니다.

$$
\bar{\mathbf{X}}=\frac{1}{n}\sum_{i=1}^n\mathbf{X}_i
$$

$$\bar{X}_j$$는 $$\bar{\mathbf{X}}$$ Vector에서 $$j$$번 째 Element를 의미합니다. $$X_{ij}$$가 Random Variable이기 때문에 $$\bar{X}_j$$도 Random Variable입니다.

이 상황에는 $$n$$이 충분히 크면 다음과 같은 식이 성립합니다. 참고로 이 글에서는 다음 식이 성립하는 이유를 뒤에서 증명할 예정입니다.

$$
\sum_{j=1}^k\frac{(n\bar{X}_j-np_j)^2}{np_j} \sim \chi_{k-1}^2
$$

이 식은, $$O_j=n\bar{X}_j$$로 정의하고 $$E_j=np_j$$로 정의해서 다음과 같이 표현하기도 합니다.

$$
\sum_{j=1}^k\frac{(O_j-E_j)^2}{E_j} \sim \chi_{k-1}^2
$$

즉, $$O_j$$는 각 상자에 들어 있는 공의 갯수이며 $$E_j$$는 각 상자에 들어 있을 것으로 예상되는 공의 갯수입니다. 여기에서 $$O_j$$는 공을 던질 때마다 다른 상자에 들어갈 것이므로 Random Variable이 되고 이 식은 Degree of Freedom이 $$k-1$$인 [Chi Squared Distribution](Derivation-of-the-Probability-Distribution-Functions#Chi-squared)을 따릅니다.

Chi Squared Test에서는 공이 각 상자에 들어갈 확률을 추측해서 이를 기반으로 Null Hypothesis를 세우고, Null Hypothesis가 맞다는 가정하에 현재 관측한 각 상자에 들어 있는 공의 갯수가 나올 확률이(혹은 그보다 더 극단적인 상황이 발생할 확률이) 얼마나 되는지 위의 식으로 계산(이것을 P Value라고 함)합니다. P Value가 Significance Level(이것을 $$\alpha$$라고 함)보다 작으면 Null Hypothesis를 기각합니다.

## Proof of Chi Squared Test {#Proof-of-Chi-Squared-Test}

$$
P(X_{ij}=1)=p_j \\
E(X_{ij})=p_j \\
E(\mathbf{X}_i)=
\begin{bmatrix}
p_1 \\
p_2 \\
\vdots \\
p_k
\end{bmatrix}
=\mathbf{p}
$$

$$j = l$$인 경우 $$Cov(X_{ij},X_{il})$$을 계산합니다.

$$
\begin{aligned}
Cov(X_{ij},X_{il})
&=Var(X_{ij}) \\
&=E((X_{ij}-E(X_{ij}))^2) \\
&=P(X_{ij}=0)(0-E(X_{ij}))^2+P(X_{ij}=1)(1-E(X_{ij}))^2 \\
&=(1-p_j)(0-p_j)^2+p_j(1-p_j)^2 \\
&=p_j^2-p_j^3+p_j-2p_j^2+p_j^3 \\
&=p_j(1-p_j)
\end{aligned}
$$

$$j \ne l$$인 경우 $$Cov(X_{ij},X_{il})$$을 계산합니다. 공 하나가 여러 상자에 들어갈 수 없기 때문에 $$X_{ij}X_{il}$$은 항상 $$0$$이 되는 점을 이용합니다.

$$
\begin{aligned}
Cov(X_{ij},X_{il})
&=E((X_{ij}-E(X_{ij}))(X_{il}-E(X_{il}))) \\
&=E(X_{ij}X_{il}-X_{ij}E(X_{il})-E(X_{ij})X_{il}+E(X_{ij})E(X_{il})) \\
&=E(X_{ij}X_{il})-E(X_{ij})E(X_{il})-E(X_{ij})E(X_{il})+E(X_{ij})E(X_{il}) \\
&=E(X_{ij}X_{il})-E(X_{ij})E(X_{il}) \\
&=-E(X_{ij})E(X_{il}) \\
&=-p_jp_l
\end{aligned}
$$

정리하면 $$\mathbf{X}_i$$의 Covariance Matrix $$\mathbf{\Sigma}$$은 다음과 같습니다.

$$
\mathbf{\Sigma}=
\begin{bmatrix}
p_1(1-p_1) && -p_1p_2 && \cdots && -p_1p_k \\
-p_1p_2 && p_2(1-p_2) && \cdots && -p_2p_k \\
\vdots && \vdots && \ddots && \vdots \\
-p_1p_k && -p_2p_k && \cdots && p_k(1-p_k)
\end{bmatrix}
$$

$$\mathbf{\Sigma}$$을 잘 살펴보면 $$\sum_{j=1}^kp_j=1$$이기 때문에 모든 Column Vector를 더해 보면 $$\mathbf{0}$$이 된다는 것을 알 수 있습니다. 즉, $$\mathbf{\Sigma}$$는 Full Rank가 아니고 Invertible하지 않습니다. $$\mathbf{p}$$에서 $$k$$번 째 Element를 제거한 Vector를 $$\mathbf{p}^*$$라고 정의하고, $$\mathbf{X}_i$$에서 $$k$$번째 Element를 제거한 Vector를 $$\mathbf{X}_i^*$$라고 정의하며, $$\mathbf{X}_i^*$$의 Covariance Matrix를 $$\mathbf{\Sigma}^*$$라고 정의합니다. $$\mathbf{\Sigma}^*$$는 Full Rank이며 Invertible합니다.

$$
\mathbf{\Sigma}^*=
\begin{bmatrix}
p_1(1-p_1) && -p_1p_2 && \cdots && -p_1p_{k-1} \\
-p_1p_2 && p_2(1-p_2) && \cdots && -p_2p_{k-1} \\
\vdots && \vdots && \ddots && \vdots \\
-p_1p_{k-1} && -p_2p_{k-1} && \cdots && p_{k-1}(1-p_{k-1})
\end{bmatrix}
$$

$$(\mathbf{\Sigma}^*)^{-1}$$을 계산하기 위해 [Sherman Morrison Woodbury Formula](Derivation-of-LBFGS-Part-2#Sherman-Morrison-Woodbury-Formula)을 이용합니다. Sherman Morrison Woodbury Formula는 다음과 같습니다.

$$ 
(\mathbf{A}+\mathbf{UCV})^{-1}=\mathbf{A}^{-1}-\mathbf{A}^{-1}\mathbf{U}(\mathbf{C}^{-1}+\mathbf{V}\mathbf{A}^{-1}\mathbf{U})^{-1}\mathbf{V}\mathbf{A}^{-1}
$$

$$\mathbf{\Sigma}^*=\mathbf{A}+\mathbf{UCV}$$라고 하면 $$\mathbf{A}, \mathbf{U}, \mathbf{C}, \mathbf{V}$$는 다음과 같이 정할 수 있습니다.

$$
\mathbf{A}=
\begin{bmatrix}
p_1 && 0 && \cdots && 0 \\
0 && p_2 && \cdots && 0 \\
\vdots && \vdots && \ddots && \vdots \\
0 && 0 && \cdots && p_{k-1}
\end{bmatrix} \\
\mathbf{U}=
\begin{bmatrix}
p_1 \\
p_2 \\
\vdots \\
p_{k-1}
\end{bmatrix} \\
\mathbf{C}=-1 \\
\mathbf{V}=
\begin{bmatrix}
p_1 && p_2 && \cdots && p_{k-1}
\end{bmatrix} \\
$$

$$\mathbf{A}^{-1}-\mathbf{A}^{-1}\mathbf{U}(\mathbf{C}^{-1}+\mathbf{V}\mathbf{A}^{-1}\mathbf{U})^{-1}\mathbf{V}\mathbf{A}^{-1}$$을 계산하기 위해 필요한 각 부분을 계산합니다.

$$
\mathbf{A}^{-1}=
\begin{bmatrix}
\frac{1}{p_1} && 0 && \cdots && 0 \\
0 && \frac{1}{p_2} && \cdots && 0 \\
\vdots && \vdots && \ddots && \vdots \\
0 && 0 && \cdots && \frac{1}{p_{k-1}}
\end{bmatrix} \\
\mathbf{A}^{-1}\mathbf{U}=
\begin{bmatrix}
1 \\
1 \\
\vdots \\
1
\end{bmatrix} \\
\mathbf{V}\mathbf{A}^{-1}=
\begin{bmatrix}
1 && 1 && \cdots && 1
\end{bmatrix} \\
\mathbf{V}\mathbf{A}^{-1}\mathbf{U}=\sum_{j=1}^{k-1}p_j \\
\mathbf{C}^{-1}=-1 \\
\mathbf{C}^{-1}+\mathbf{V}\mathbf{A}^{-1}\mathbf{U}=-1+\sum_{j=1}^{k-1}p_j=-p_k \\
(\mathbf{C}^{-1}+\mathbf{V}\mathbf{A}^{-1}\mathbf{U})^{-1}=-\frac{1}{p_k}
$$

이렇게 계산한 결과를 이용해서 $$\mathbf{A}^{-1}-\mathbf{A}^{-1}\mathbf{U}(\mathbf{C}^{-1}+\mathbf{V}\mathbf{A}^{-1}\mathbf{U})^{-1}\mathbf{V}\mathbf{A}^{-1}$$을 계산합니다.

$$
\begin{aligned}
&\mathbf{A}^{-1}-\mathbf{A}^{-1}\mathbf{U}(\mathbf{C}^{-1}+\mathbf{V}\mathbf{A}^{-1}\mathbf{U})^{-1}\mathbf{V}\mathbf{A}^{-1} \\
&=\begin{bmatrix}
\frac{1}{p_1} && 0 && \cdots && 0 \\
0 && \frac{1}{p_2} && \cdots && 0 \\
\vdots && \vdots && \ddots && \vdots \\
0 && 0 && \cdots && \frac{1}{p_{k-1}}
\end{bmatrix}
-
\begin{bmatrix}
1 \\
1 \\
\vdots \\
1
\end{bmatrix}
\left (-\frac{1}{p_k} \right )
\begin{bmatrix}
1 && 1 && \cdots && 1
\end{bmatrix} \\
&=\begin{bmatrix}
\frac{1}{p_1} && 0 && \cdots && 0 \\
0 && \frac{1}{p_2} && \cdots && 0 \\
\vdots && \vdots && \ddots && \vdots \\
0 && 0 && \cdots && \frac{1}{p_{k-1}}
\end{bmatrix}
+
\frac{1}{p_k}
\begin{bmatrix}
1 && 1 && \cdots && 1 \\
1 && 1 && \cdots && 1 \\
\vdots && \vdots && \ddots && \vdots \\
1 && 1 && \cdots && 1
\end{bmatrix}
\end{aligned}
$$

정리하면 $$(\mathbf{\Sigma}^*)^{-1}$$은 다음과 같습니다.

$$
(\mathbf{\Sigma}^*)^{-1}=
\begin{bmatrix}
\frac{1}{p_1} && 0 && \cdots && 0 \\
0 && \frac{1}{p_2} && \cdots && 0 \\
\vdots && \vdots && \ddots && \vdots \\
0 && 0 && \cdots && \frac{1}{p_{k-1}}
\end{bmatrix}
+
\frac{1}{p_k}
\begin{bmatrix}
1 && 1 && \cdots && 1 \\
1 && 1 && \cdots && 1 \\
\vdots && \vdots && \ddots && \vdots \\
1 && 1 && \cdots && 1
\end{bmatrix}
$$

$$\bar{\mathbf{X}}^*$$를 다음과 같이 정의합니다.

$$
\bar{\mathbf{X}}^*=\frac{1}{n}\sum_{i=1}^n\mathbf{X}_i^*
$$

$$\bar{\mathbf{X}}^*$$와 관련된 값을 계산합니다.

$$
E(\bar{\mathbf{X}}^*)=\mathbf{p}^* \\
Var(\bar{\mathbf{X}}^*)=\frac{Var(\mathbf{X}_i^*)}{n}=\frac{\mathbf{\Sigma}^*}{n} \\
$$

Central Limit Theorem에 따르면 $$n$$이 충분히 클 때 다음 식이 성립합니다.

$$
\sqrt{n}(\mathbf{\Sigma}^*)^{-\frac{1}{2}}(\bar{\mathbf{X}}^*-\mathbf{p}^*) \sim N(\mathbf{0}, \mathbf{I}_{k-1})
$$

Chi Squared Distribution의 정의에 따르면 다음 식은 Degree of Freedom이 $$k-1$$인 Chi Squared Distribution을 따릅니다.

$$
\begin{aligned}
&(\sqrt{n}(\mathbf{\Sigma}^*)^{-\frac{1}{2}}(\bar{\mathbf{X}}^*-\mathbf{p}^*))^{T}(\sqrt{n}(\mathbf{\Sigma}^*)^{-\frac{1}{2}}(\bar{\mathbf{X}}^*-\mathbf{p}^*)) \\
&=n(\bar{\mathbf{X}}^*-\mathbf{p}^*)^T(\mathbf{\Sigma}^*)^{-1}(\bar{\mathbf{X}}^*-\mathbf{p}^*) \\
&\sim \chi_{k-1}^2
\end{aligned}
$$

$$n(\bar{\mathbf{X}}^*-\mathbf{p}^*)^T(\mathbf{\Sigma}^*)^{-1}(\bar{\mathbf{X}}^*-\mathbf{p}^*)$$을 자세히 계산해 보도록 하겠습니다.

$$
\begin{aligned}
&n(\bar{\mathbf{X}}^*-\mathbf{p}^*)^T(\mathbf{\Sigma}^*)^{-1}(\bar{\mathbf{X}}^*-\mathbf{p}^*) \\
&=n
\begin{bmatrix}
\bar{X}_1-p_1 \\
\bar{X}_2-p_2 \\
\vdots \\
\bar{X}_{k-1}-p_{k-1}
\end{bmatrix}^T
\left (
\begin{bmatrix}
\frac{1}{p_1} && 0 && \cdots && 0 \\
0 && \frac{1}{p_2} && \cdots && 0 \\
\vdots && \vdots && \ddots && \vdots \\
0 && 0 && \cdots && \frac{1}{p_{k-1}}
\end{bmatrix}
+
\frac{1}{p_k}
\begin{bmatrix}
1 && 1 && \cdots && 1 \\
1 && 1 && \cdots && 1 \\
\vdots && \vdots && \ddots && \vdots \\
1 && 1 && \cdots && 1
\end{bmatrix}
\right )
\begin{bmatrix}
\bar{X}_1-p_1 \\
\bar{X}_2-p_2 \\
\vdots \\
\bar{X}_{k-1}-p_{k-1}
\end{bmatrix} \\
&=n
\begin{bmatrix}
\bar{X}_1-p_1 \\
\bar{X}_2-p_2 \\
\vdots \\
\bar{X}_{k-1}-p_{k-1}
\end{bmatrix}^T
\begin{bmatrix}
\frac{1}{p_1} && 0 && \cdots && 0 \\
0 && \frac{1}{p_2} && \cdots && 0 \\
\vdots && \vdots && \ddots && \vdots \\
0 && 0 && \cdots && \frac{1}{p_{k-1}}
\end{bmatrix}
\begin{bmatrix}
\bar{X}_1-p_1 \\
\bar{X}_2-p_2 \\
\vdots \\
\bar{X}_{k-1}-p_{k-1}
\end{bmatrix}
\\
&+n
\begin{bmatrix}
\bar{X}_1-p_1 \\
\bar{X}_2-p_2 \\
\vdots \\
\bar{X}_{k-1}-p_{k-1}
\end{bmatrix}^T
\frac{1}{p_k}
\begin{bmatrix}
1 && 1 && \cdots && 1 \\
1 && 1 && \cdots && 1 \\
\vdots && \vdots && \ddots && \vdots \\
1 && 1 && \cdots && 1
\end{bmatrix}
\begin{bmatrix}
\bar{X}_1-p_1 \\
\bar{X}_2-p_2 \\
\vdots \\
\bar{X}_{k-1}-p_{k-1}
\end{bmatrix} \\
&=n\sum_{j=1}^{k-1}\frac{(\bar{X}_j-p_j)^2}{p_j}+n\frac{1}{p_k}\left (\sum_{j=1}^{k-1}(\bar{X}_j-p_j)\right )^2 \\
&=\sum_{j=1}^{k-1}\frac{n(\bar{X}_j-p_j)^2}{p_j}+\frac{n(\sum_{j=1}^{k-1}\bar{X}_j-\sum_{j=1}^{k-1}p_j)^2}{p_k} \\
&=\sum_{j=1}^{k-1}\frac{n(\bar{X}_j-p_j)^2}{p_j}+\frac{n((1-\bar{X}_k)-(1-p_k))^2}{p_k} \\
&=\sum_{j=1}^{k-1}\frac{n(\bar{X}_j-p_j)^2}{p_j}+\frac{n(\bar{X}_k-p_k)^2}{p_k} \\
&=\sum_{j=1}^k\frac{n(\bar{X}_j-p_j)^2}{p_j} \\
&=\sum_{j=1}^k\frac{n^2(\bar{X}_j-p_j)^2}{np_j} \\
&=\sum_{j=1}^k\frac{(n\bar{X}_j-np_j)^2}{np_j}
\end{aligned}
$$

다시 정리하면 다음과 같이 $$\sum_{j=1}^k\frac{(n\bar{X}_j-np_j)^2}{np_j}$$이 Degree of Freedom이 $$k-1$$인 Chi Squared Distribution을 따르는 것을 확인할 수 있습니다.

$$
\sqrt{n}(\mathbf{\Sigma}^*)^{-\frac{1}{2}}(\bar{\mathbf{X}}^*-\mathbf{p}^*) \sim N(\mathbf{0}, \mathbf{I}_{k-1}) \\
n(\bar{\mathbf{X}}^*-\mathbf{p}^*)^T(\mathbf{\Sigma}^*)^{-1}(\bar{\mathbf{X}}^*-\mathbf{p}^*) \sim \chi_{k-1}^2 \\
n(\bar{\mathbf{X}}^*-\mathbf{p}^*)^T(\mathbf{\Sigma}^*)^{-1}(\bar{\mathbf{X}}^*-\mathbf{p}^*)=\sum_{j=1}^k\frac{(n\bar{X}_j-np_j)^2}{np_j} \\
\sum_{j=1}^k\frac{(n\bar{X}_j-np_j)^2}{np_j} \sim \chi_{k-1}^2
$$

## Conclusion {#Conclusion}

이 글에서는 Chi Squared Test의 수식을 증명해 보았습니다. 교과서에 식만 나와 있고 증명이 생략되어 있는 경우가 많아서 교과서만 가지고는 이해가 쉽지 않습니다만 이 글을 통해 조금이라도 이해하는데 도움이 되었으면 좋겠습니다.
