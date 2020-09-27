---
layout: post
title:  "Derivation of LBFGS - Part 1"
date:   2020-09-23 23:00:00 +0900
author: Taeho Oh
tags: [ 오태호, 머신러닝 ]
---

안녕하세요. 오태호입니다.

이 글에서는 Optimization 기법중에 하나인 LBFGS Method(Limited Memory Broyden–Fletcher–Goldfarb–Shanno Method)의 수식을 여러 Part에 걸쳐서 차근차근 유도하여 LBFGS Method의 구조를 조금 깊게 살펴보도록 하겠습니다.

pytorch.optim 패키지에 보면 SGD, Adadelta, Adagrad, RMSprop, Adam와 같은 Optimizer는 여러 곳에서 자세한 설명을 찾아볼 수 있습니다. 하지만 LBFGS Method의 경우에는 여러 곳에서 설명을 찾아 봐도 자세한 설명을 찾아보기가 쉽지 않아서 정리해 보았습니다.

이 글을 이해하기 위해서는 Calculus, Linear Algebra, Machine Learning에 대한 기초지식이 필요합니다.

이 글에서 굵은 글자체 대문자는 Matrix를 의미하고, 굵은 소문자는 Vector를 의미하며, 일반 소문자는 Scalar를 의미합니다. Vector는 특별히 언급이 없으면 Column Vector를 의미합니다.

## Taylor Series {#Taylor-Series}

Taylor Series를 이용하여 $x$가 $x_0$의 근처의 값을 가질 때 $f(x)$를 근사해서 표현하면 다음과 같습니다.

$$
f(x) \approx f(x_0)+(x-x_0)\frac{\partial}{\partial x}f(x_0)+\frac{(x-x_0)^2}{2}\frac{\partial^2}{\partial x^2}f(x_0)
$$

마찬가지로 Taylor Series를 이용하여 3차원 공간에서 $x$가 $x_0$의 근처의 값을 가지고 $y$가 $y_0$의 근처의 값을 가질 때, $f(x, y)$를 근사해서 표현하면 다음과 같습니다.

$$
\begin{aligned}
f(x,y)\approx&f(x_0,y_0)+(x-x_0)\frac{\partial}{\partial x}f(x_0,y_0)+(y-y_0)\frac{\partial}{\partial y}f(x_0,y_0)+ \\
&\frac{(x-x_0)^2}{2}\frac{\partial^2}{\partial x^2}f(x_0,y_0)+\frac{(x-x_0)(y-y_0)}{2}\frac{\partial^2}{\partial x \partial y}f(x_0,y_0)+ \\
&\frac{(y-y_0)(x-x_0)}{2}\frac{\partial^2}{\partial y \partial x}f(x_0,y_0)+\frac{(y-y_0)^2}{2}\frac{\partial^2}{\partial y^2}f(x_0,y_0) \\
=&f(x_0,y_0)+
(
\begin{bmatrix}
x & y
\end{bmatrix}
-
\begin{bmatrix}
x_0 & y_0
\end{bmatrix}
)
\begin{bmatrix}
\frac{\partial}{\partial x}f(x_0,y_0) \\
\frac{\partial}{\partial y}f(x_0,y_0)
\end{bmatrix}
+ \\
&\frac{1}{2}(
\begin{bmatrix}
x & y
\end{bmatrix}
-
\begin{bmatrix}
x_0 & y_0
\end{bmatrix}
)
\begin{bmatrix}
\frac{\partial^2}{\partial x^2}f(x_0,y_0) & \frac{\partial^2}{\partial x \partial y}f(x_0,y_0) \\
\frac{\partial^2}{\partial y \partial x}f(x_0,y_0) & \frac{\partial^2}{\partial y^2}f(x_0,y_0)
\end{bmatrix}
(
\begin{bmatrix}
x \\
y
\end{bmatrix}
-
\begin{bmatrix}
x_0 \\
y_0
\end{bmatrix}
)
\end{aligned}
$$

$\mathbf{x}$, $\mathbf{x}_0$, $f(\mathbf{x})$, Gradient $\nabla f(\mathbf{x}_0)$, Hessian $\nabla^2 f(\mathbf{x}_0)$을 다음과 같이 정의합니다.

$$
\mathbf{x}=
\begin{bmatrix}
x \\
y
\end{bmatrix} \\
\mathbf{x}_0=
\begin{bmatrix}
x_0 \\
y_0
\end{bmatrix} \\
f(\mathbf{x}_0)=f(x_0,y_0) \\
\nabla f(\mathbf{x}_0)=
\begin{bmatrix}
\frac{\partial}{\partial x}f(x_0,y_0) \\
\frac{\partial}{\partial y}f(x_0,y_0)
\end{bmatrix} \\
\nabla^2 f(\mathbf{x}_0)=
\begin{bmatrix}
\frac{\partial^2}{\partial x^2}f(x_0,y_0) & \frac{\partial^2}{\partial x \partial y}f(x_0,y_0) \\
\frac{\partial^2}{\partial y \partial x}f(x_0,y_0) & \frac{\partial^2}{\partial y^2}f(x_0,y_0)
\end{bmatrix}
$$

위의 $f(x,y)$를 Vector를 사용하여 간결하게 다시 정리하면 다음과 같습니다.

$$
f(\mathbf{x})\approx f(\mathbf{x}_0)+(\mathbf{x}-\mathbf{x}_0)^T\nabla f(\mathbf{x}_0)+\frac{1}{2}(\mathbf{x}-\mathbf{x}_0)^T\nabla^2 f(\mathbf{x}_0)(\mathbf{x}-\mathbf{x}_0)
$$

참고로 이 식은 $\mathbf{x}$가 여기에서 다룬 2차원 Vector가 아니라 더 높은 고차원의 Vector인 경우에도 성립합니다.

## Vector Differentiation {#Vector-Differentiation}

Vector $\mathbf{x}$를 다음과 같이 정의합니다.

$$
\mathbf{x}=
\begin{bmatrix}
x_1 \\
x_2 \\
\vdots \\
x_n
\end{bmatrix}
$$

Scalar $f(\mathbf{x})$를 Vector $\mathbf{x}$로 미분하는 경우 두 가지 방법으로 할 수 있습니다.

첫 번째 방법은 다음과 같은 Numerator Layout입니다.

$$
\frac{\partial f(\mathbf{x})}{\partial \mathbf{x}}=
\begin{bmatrix}
\frac{\partial f(\mathbf{x})}{\partial x_1} & \frac{\partial f(\mathbf{x})}{\partial x_2} \cdots \frac{\partial f(\mathbf{x})}{\partial x_n}
\end{bmatrix}
$$

두 번째 방법은 다음과 같은 Denominator Layout입니다.

$$
\frac{\partial f(\mathbf{x})}{\partial \mathbf{x}}=
\begin{bmatrix}
\frac{\partial f(\mathbf{x})}{\partial x_1} \\
\frac{\partial f(\mathbf{x})}{\partial x_2} \\
\vdots \\
\frac{\partial f(\mathbf{x})}{\partial x_n}
\end{bmatrix}
$$

학계에서 사용되는 것을 살펴보면 표준화된 방법 없이 두 가지 방법 모두가 많이 사용되는 것을 볼 수 있습니다. 어떤 경우에는 두 방법을 섞어가며 사용하는 경우도 있습니다. Machine Learning 분야에서는 Denominator Layout을 사용하는 경우가 더 많은 편입니다. 이 글에서는 특별히 언급이 없으면 Denominator Layout을 사용하도록 하겠습니다.

다음은 몇 가지 유용한 Vector 미분에 관한 정리입니다.

$$
\frac{\partial}{\partial \mathbf{x}}(\mathbf{x}^T\mathbf{a})
=
\begin{bmatrix}
\frac{\partial}{\partial x_1}(a_1 x_1 + a_2 x_2 + \cdots + a_n x_n) \\
\frac{\partial}{\partial x_2}(a_1 x_1 + a_2 x_2 + \cdots + a_n x_n) \\
\vdots \\
\frac{\partial}{\partial x_n}(a_1 x_1 + a_2 x_2 + \cdots + a_n x_n)
\end{bmatrix}
=
\begin{bmatrix}
a_1 \\
a_2 \\
\vdots \\
a_n
\end{bmatrix}
=
\mathbf{a} \\

\begin{align}
\frac{\partial}{\partial \mathbf{x}}(\mathbf{x}^TA\mathbf{x})
&=\left [ \frac{\partial}{\partial x_k}\left (\sum_i\sum_j a_{ij} x_i x_j \right ) \right ]_k \\
&=\left [ \frac{\partial}{\partial x_k}\left (a_{kk}x_k^2 + \sum_{j \neq k} a_{kj} x_k x_j + \sum_{i \neq k} a_{ik} x_i x_k\right ) \right ]_k \\
&=\left [ 2a_{kk}x_k + \sum_{j \neq k} a_{kj} x_j + \sum_{i \neq k} a_{ik} x_i \right ]_k \\
&=\left [ \sum_{j} a_{kj} x_j + \sum_{i} a_{ik} x_i \right ]_k \\
&=\left [ [ \mathbf{Ax} ]_k + [ \mathbf{A}^T\mathbf{x} ]_k \right ]_k \\
&=(\mathbf{A}+\mathbf{A}^T)\mathbf{x}
\end{align}
$$

간략하게 다시 정리하면 다음과 같습니다.

$$
\frac{\partial}{\partial \mathbf{x}}(\mathbf{x}^T\mathbf{a})=\mathbf{a} \\
\frac{\partial}{\partial \mathbf{x}}(\mathbf{x}^TA\mathbf{x})=(\mathbf{A}+\mathbf{A}^T)\mathbf{x}
$$

## Newton's Method {#Newtons-Method}

$f(\mathbf{x})$를 최소로 하는 $\mathbf{x}$를 찾으려고 합니다. 그런 $\mathbf{x}$를 찾기 위해 $\nabla f(\mathbf{x})=\mathbf{0}$을 만족하는 $\mathbf{x}$를 찾는 것을 시도합니다. 처음에는 $\nabla f(\mathbf{x})=\mathbf{0}$으로 하는 $\mathbf{x}$를 $\mathbf{x}_0$로 추정하고, $\mathbf{x}_0$보다 더 개선된 $\mathbf{x}$를 찾습니다. $f(\mathbf{x})$의 형태는 [Tayler Series](#Tayler-Series)를 사용하여 다음과 같이 근사한 형태를 사용합니다.

$$
f(\mathbf{x})\approx f(\mathbf{x}_0)+(\mathbf{x}-\mathbf{x}_0)^T\nabla f(\mathbf{x}_0)+\frac{1}{2}(\mathbf{x}-\mathbf{x}_0)^T\nabla^2 f(\mathbf{x}_0)(\mathbf{x}-\mathbf{x}_0)
$$

$\nabla f(\mathbf{x})=\mathbf{0}$을 만족하는 $\mathbf{x}$는 [Vector Differentiation](#Vector-Differentiation)을 참고하여 다음과 같이 구합니다. $f(\mathbf{x})$가 Continuous하다면 $\nabla^2 f(\mathbf{x})$는 Symmetric한 성질도 이용합니다. (여기서 $f(\mathbf{x})$는 Continuous하다고 가정합니다.)

$$
\begin{align}
\nabla f(\mathbf{x})
&=\frac{\partial}{\partial \mathbf{x}}f(\mathbf{x}) \\
&\approx \frac{\partial}{\partial \mathbf{x}}\left (f(\mathbf{x}_0)+(\mathbf{x}-\mathbf{x}_0)^T\nabla f(\mathbf{x}_0)+\frac{1}{2}(\mathbf{x}-\mathbf{x}_0)^T\nabla^2 f(\mathbf{x}_0)(\mathbf{x}-\mathbf{x}_0) \right ) \\
&=\mathbf{0}+\nabla f(\mathbf{x}_0) + \frac{1}{2}(\nabla^2 f(\mathbf{x}_0) + [\nabla^2 f(\mathbf{x}_0)]^T)(\mathbf{x}-\mathbf{x}_0) \\
&=\nabla f(\mathbf{x}_0)+\nabla^2 f(\mathbf{x}_0)(\mathbf{x}-\mathbf{x}_0) \\
&=\mathbf{0} \\
\end{align} \\

\nabla f(\mathbf{x}_0)+\nabla^2 f(\mathbf{x}_0)(\mathbf{x}-\mathbf{x}_0) = \mathbf{0} \\
\mathbf{x}=\mathbf{x}_0-[\nabla^2 f(\mathbf{x}_0)]^{-1}\nabla f(\mathbf{x}_0)
$$

이렇게 찾은 $\mathbf{x}$를 $\mathbf{x}_1$라고 하고 위의 방법을 다시 수행하여 $\mathbf{x}_1$보다 더 개선된 $\mathbf{x}$를 찾아서 이것을 $\mathbf{x}_2$라고 합니다. 이런 식으로 반복하여 $f(\mathbf{x})$를 최소로 하는 $\mathbf{x}$를 찾습니다. 이렇게 $f(\mathbf{x})$를 최소로 하는 $\mathbf{x}$를 찾는 방법을 Newton's Method라고 합니다.

정리하면 다음과 같이 조금씩 개선된 $\mathbf{x}$를 하나씩 구합니다. 여기서 $-[\nabla^2 f(\mathbf{x}_k)]^{-1}\nabla f(\mathbf{x}_k)$는 Newton Direction이라고 합니다. $\mathbf{x}$가 Newton Direction 방향으로 움직이면서 $f(\mathbf{x})$를 최소로 하는 $\mathbf{x}$ 값을 찾습니다.

$$
\mathbf{x}_{k+1}=\mathbf{x}_k-[\nabla^2 f(\mathbf{x}_k)]^{-1}\nabla f(\mathbf{x}_k)
$$

이 Newton's Method를 그대로 사용하면 $\mathbf{x}$가 Diverge하면서 제대로 $\mathbf{x}$를 구하지 못할 수도 있기 때문에 다음과 같이 Newton's Method를 살짝 수정한 Relaxed Newton's Method를 사용하는 경우가 많이 있습니다. 여기서 $t_k$는 Step Size라고 합니다. $t_k$가 작은 값을 가지면 $\mathbf{x}$가 Diverge하지 않도록 돕는 역할을 합니다.

$$
\mathbf{x}_{k+1}=\mathbf{x}_k-t_k[\nabla^2 f(\mathbf{x}_k)]^{-1}\nabla f(\mathbf{x}_k)
$$

Gradient Descent와 비교해 보도록 하겠습니다. Gradient Descent는 다음과 같이 $\mathbf{x}$를 구합니다.

$$
\mathbf{x}_{k+1}=\mathbf{x}_k-t_k\nabla f(\mathbf{x}_k)
$$

Gradient Descent는 $\mathbf{x}$의 이동방향을 결정할 때 Gradient $\nabla f(\mathbf{x}_k)$만을 활용하지만 Newton's Method에서는 $\mathbf{x}$의 이동방향을 결정할 때 Hessian $\nabla^2 f(\mathbf{x}_k)$도 함께 활용하여 좀 더 정확한 방향으로 $\mathbf{x}$를 이동시키는 것을 확인할 수 있습니다.

## Wolfe Conditions {#Wolfe-Conditions}

Newton's Method에서 Step Size $t_k$를 정할 때 뭔가 기준을 가지고 정해야 하는데 이때 많이 사용하는 기준이 Wolfe Conditions입니다. Wolfe Conditions는 Armijo Rule과 Curvature Condition로 구성되어 있습니다.

Armijo Rule은 다음과 같습니다.

$$
f(\mathbf{x}_k+t_k\mathbf{p}_k) \le f(\mathbf{x}_k)+c_1 t_k \mathbf{p}_k^T \nabla f(\mathbf{x}_k) \\
\mathbf{p}_k=-[\nabla^2 f(\mathbf{x}_k)]^{-1}\nabla f(\mathbf{x}_k) \\
c_1=10^{-4}
$$

여기서 $\mathbf{p}_k$는 Newton Direction입니다. $c_1$은 Hyperparameter로 $0 \lt c_1 \lt 1$의 범위의 값에서 적당히 설정하는데 보통 $0$에 가까운 값으로 설정합니다. 직관적으로 설명하면, $\mathbf{x}$를 Newton Direction으로 $t_k$만큼 이동시켰을 때 실제 $f(\mathbf{x})$의 값이 Newton's Method로 계산한 $f(\mathbf{x})$의 근사치 보다 충분히 작게 되도록 $t_k$를 정해야 된다는 뜻입니다. 얼마나 충분히 작아야 하는지는 설정한 $c_1$의 값에 의해 결정됩니다. $c_1$의 값이 작아지면 허용되는 $t_k$의 범위가 넓어지면서 $t_k$가 더 큰 값을 가질 수 있게 됩니다. $c_1$은 $t_k$가 가질 수 있는 최대값을 결정합니다.

Curvature Condition은 다음과 같습니다.

$$
\mathbf{p}_k^T \nabla f(\mathbf{x}_k+t_k\mathbf{p}_k) \ge c_2 \mathbf{p}_k^T \nabla f(\mathbf{x}_k) \\
\mathbf{p}_k=-[\nabla^2 f(\mathbf{x}_k)]^{-1}\nabla f(\mathbf{x}_k) \\
c_2=0.9
$$

여기서 $\mathbf{p}_k$는 Newton Direction입니다. $c_2$은 Hyperparameter로 $0 \lt c_2 \lt 1$의 범위의 값에서 적당히 설정하는데 보통 $1$에 가까운 값으로 설정합니다. 직관적으로 설명하면, $f(\mathbf{x})$의 Gradient보다 $\mathbf{x}$를 Newton Direction으로 $t_k$만큼 이동시켰을 때의 $f(\mathbf{x})$의 Gradient가 충분히 크도록(Negative이던 것이 $0$에 가까워 지도록) $t_k$를 정해야 된다는 뜻입니다. 얼마나 충분히 커야 하는지는 설정한 $c_2$의 값에 의해 결정됩니다. $c_2$의 값이 커지면 $t_k$의 범위가 넓어지면서 $t_k$가 더 작은 값을 가질 수 있게 됩니다. $c_2$은 $t_k$가 가질 수 있는 최소값을 결정합니다.

Wolfe Conditions에서 위에서 언급한 Curvature Condition대신에 다음과 같은 Curvature Condition을 사용하는 경우도 있습니다.

$$
| \mathbf{p}_k^T \nabla f(\mathbf{x}_k+t_k\mathbf{p}_k) | \le c_2 | \mathbf{p}_k^T \nabla f(\mathbf{x}_k) | \\
\mathbf{p}_k=-[\nabla^2 f(\mathbf{x}_k)]^{-1}\nabla f(\mathbf{x}_k) \\
c_2=0.9
$$

이와 같은 Curvature Condition을 사용하는 경우에는 Strong Wolfe Conditions라고 합니다.

## Conclusion {#Conclusion}

이 글에서는 LBFGS Method를 살펴보기 위한 첫단계로 Newton's Method에 대해 살펴보았습니다.

Newton's Method는 Gradient Descent에 비해서 방향을 잘 결정한다는 장점이 있지만 큰 단점이 하나 있습니다. Newton Direction을 계산하기 위해서는 Inverse Hessian $[\nabla^2 f(\mathbf{x}_k)]^{-1}$을 계산해야 하는데 이것은 $\mathbf{x}$의 차원이 높아지면 계산이 매우 힘들어집니다.

[Derivation of LBFGS - Part 2](Derivation-of-LBFGS-Part-2)에서는 $\mathbf{x}$가 고차원일 경우에 어떻게 Inverse Hessian $[\nabla^2 f(\mathbf{x}_k)]^{-1}$를 계산해서 Newton's Method를 사용할 수 있는지 알아보도록 하겠습니다.
