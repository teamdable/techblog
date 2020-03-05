---
layout: post
title:  "PyTorch Autograd"
date:   2020-03-01 23:00:00 +0900
author: Taeho Oh
tags: [ 오태호, PyTorch, Autograd ]
---

안녕하세요. 오태호입니다.

PyTorch의 Autograd는 수식에서 미분을 자동으로 해 주는 매우 편리하면서 강력한 기능입니다. 하지만 PyTorch 공식 Tutorial이나 Document를 봐도 이해가 쉽지 않습니다. 이 글에서는 PyTorch의 Autograd에 대해 약간 더 깊게 설명을 해서 Autograd에 관심이 있는 분이 Autograd를 조금 더 깊게 이해할 수 있도록 도와드립니다.

이 글은 PyTorch 1.4를 기준으로 작성하였습니다. 이 글을 이해하기 위해서는 미분에 대한 수학지식과 PyTorch에 대한 기초지식이 필요합니다.

## Differentiation {#Differentiation}

함수 $f(x)$를 $x$에 대해 미분(Differentiation)은 다음과 같이 계산합니다.

$$
\frac{df(x)}{dx}=\lim_{h \rightarrow 0}\frac{f(x+h)-f(x)}{h}
$$

$x$가 살짝 증가할 때 $f(x)$도 살짝 증가(혹은 감소)할텐데, $x$가 살짝 증가할 때 $f(x)$가 얼마나 증가하는지에 대한 비율은, $f(x)$의 미분인 $\frac{df(x)}{dx}$을 이용하여 계산할 수 있으며, 이것은 $x$ 지점에서 $f(x)$의 접선의 기울기(Gradient)입니다.

## Partial Differentiation {#Partial-Differentiation}

함수 $f(x,y)$에서 $x$와 $y$가 서로 Dependency가 없는 경우에, 즉 $x$의 변화가 $y$의 변화에 영향을 주지 않고 $y$의 변화가 $x$에 영향을 주지 않을 때, 편미분(Partial Differentiation)은 다음과 같이 계산합니다.

$$
\frac{\partial f(x,y)}{\partial x}=\lim_{h \rightarrow 0}\frac{f(x+h,y)-f(x,y)}{h} \\
\frac{\partial f(x,y)}{\partial y}=\lim_{h \rightarrow 0}\frac{f(x,y+h)-f(x,y)}{h}
$$

$x$ 이외의 변수가 가만히 있고 $x$만 살짝 증가할 때 $f(x,y)$도 살짝 증가(혹은 감소)할텐데, 이때 $x$가 살짝 증가할 때 $f(x,y)$가 얼마나 증가하는지에 대한 비율은, $f(x,y)$의 편미분인 $\frac{\partial f(x,y)}{\partial x}$을 이용하여 계산할 수 있으며, 이것은 $f(x,y)$에서 $x$, $y$ 지점에서 $x$ 방향으로의 접선의 기울기(Gradient)입니다. $x$에 대해서 편미분할 때는 $x$ 외의 변수를 상수로 취급합니다.

$y$ 이외의 변수가 가만히 있고 $y$만 살짝 증가할 때 $f(x,y)$도 살짝 증가(혹은 감소)할텐데, 이때 $y$가 살짝 증가할 때 $f(x,y)$가 얼마나 증가하는지에 대한 비율은, $f(x,y)$의 편미분인 $\frac{\partial f(x,y)}{\partial y}$을 이용하여 계산할 수 있으며, 이것은 $f(x,y)$에서 $x$, $y$ 지점에서 $y$ 방향으로의 접선의 기울기(Gradient)입니다. $y$에 대해서 편미분할 때는 $y$ 외의 변수를 상수로 취급합니다.

## Chain Rule {#Chain-Rule}

함수 $y=f(x)$와 $z=g(y)$가 있을 때, 즉 $x$의 변화가 $y$의 변화에 영향을 주어 $x$와 $y$가 Dependency가 있고 $y$의 변화가 $z$에 영향을 주어 $y$와 $z$가 Dependency가 있을 때, Chain Rule(연쇄법칙)을 사용하여 $\frac{dz}{dx}$을 다음과 같이 계산합니다.

$$
\frac{dz}{dx}=\frac{dy}{dx}\frac{dz}{dy}=\frac{df(x)}{dx}\frac{dg(y)}{dy}
$$

$x$가 변할 때 $z$가 얼마나 변하는지는($\frac{dz}{dx}$), $x$가 변할 때 $y$가 알마나 변하는지와($\frac{dy}{dx}$), $y$가 변할 때 $z$가 얼마나 변하는지를($\frac{dz}{dy}$) 알면 Chain Rule을 사용하여 계산할 수 있습니다.

## PyTorch Autograd {#PyTorch-Autograd}

PyTorch의 Autograd를 간단한 PyTorch를 사용한 Python Code에 조금씩 살을 붙여 가면서 설명하도록 하겠습니다.

### Code 1 {#Code-1}

```python
import torch

x = torch.tensor(5.0)
y = x ** 3
z = torch.log(y)

print('x', x)
print('y', y)
print('z', z)
```

PyTorch를 사용하여 위와 같은 간단한 계산을 해 보면 다음과 같은 결과가 나옵니다.

```
x tensor(5.)
y tensor(125.)
z tensor(4.8283)
```

### Code 2 {#Code-2}

```python
import torch

x = torch.tensor(5.0)
y = x ** 3
z = torch.log(y)

x2 = torch.tensor(5.001)
y2 = x2 ** 3
z2 = torch.log(y2)

print('x', x)
print('y', y)
print('z', z)

print('x2', x2)
print('y2', y2)
print('z2', z2)

print('dz/dx', (z2 - z) / (x2 - x))
```

$x=5$일 때 $\frac{\partial z}{\partial x}$를 미분의 정의를 이용해서($x$를 $0.001$만큼 증가시켜서) 근사값을 계산해 보면 다음과 같이 $0.5999$라는 것을 알 수 있습니다.

```
x tensor(5.)
y tensor(125.)
z tensor(4.8283)
x2 tensor(5.0010)
y2 tensor(125.0750)
z2 tensor(4.8289)
dz/dx tensor(0.5999)
```

### Code 3 {#Code-3}

```python
import torch

def get_tensor_info(tensor):
  info = []
  for name in ['requires_grad', 'is_leaf', 'grad_fn', 'grad']:
    info.append(f'{name}({getattr(tensor, name)})')
  info.append(f'tensor({str(tensor)})')
  return ' '.join(info)

x = torch.tensor(5.0)
y = x ** 3
z = torch.log(y)

print('x', get_tensor_info(x))
print('y', get_tensor_info(y))
print('z', get_tensor_info(z))
```

PyTorch의 Tensor에 있는 requires_grad, is_leaf, grad_fn, grad의 내용을 살펴봅니다. 하나하나의 자세한 내용은 천천히 설명할 예정입니다.

```
x requires_grad(False) is_leaf(True) grad_fn(None) grad(None) tensor(tensor(5.))
y requires_grad(False) is_leaf(True) grad_fn(None) grad(None) tensor(tensor(125.))
z requires_grad(False) is_leaf(True) grad_fn(None) grad(None) tensor(tensor(4.8283))
```

### Code 4 {#Code-4}

```python
import torch

def get_tensor_info(tensor):
  info = []
  for name in ['requires_grad', 'is_leaf', 'retains_grad', 'grad_fn', 'grad']:
    info.append(f'{name}({getattr(tensor, name, None)})')
  info.append(f'tensor({str(tensor)})')
  return ' '.join(info)

x = torch.tensor(5.0, requires_grad=True)
y = x ** 3
z = torch.log(y)

print('x', get_tensor_info(x))
print('y', get_tensor_info(y))
print('z', get_tensor_info(z))

z.backward()

print('x_after_backward', get_tensor_info(x))
print('y_after_backward', get_tensor_info(y))
print('z_after_backward', get_tensor_info(z))
```

[Code 3](#Code-3)에서 x Tensor를 생성할 때 requires_grad를 True로 설정해 주고, z.backward()를 호출합니다.

```
x requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor(5., requires_grad=True))
y requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<PowBackward0 object at 0x7f7822fe19e8>) grad(None) tensor(tensor(125., grad_fn=<PowBackward0>))
z requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<LogBackward object at 0x7f7822fe19e8>) grad(None) tensor(tensor(4.8283, grad_fn=<LogBackward>))
x_after_backward requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(0.6000000238418579) tensor(tensor(5., requires_grad=True))
y_after_backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<PowBackward0 object at 0x7f7822fe19e8>) grad(None) tensor(tensor(125., grad_fn=<PowBackward0>))
z_after_backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<LogBackward object at 0x7f7822fe19e8>) grad(None) tensor(tensor(4.8283, grad_fn=<LogBackward>))
```

계산식을 살펴보면 x로부터 y를 계산하고 y로부터 z를 계산합니다. z.backward()를 호출하면 계산식을 거꾸로 거슬러 올라가며 z를 편미분하여 Gradient를 계산합니다. $\frac{\partial z}{\partial z}$가 z.grad에 저장되고 $\frac{\partial z}{\partial y}$가 y.grad에 저장되고 $\frac{\partial z}{\partial x}$가 x.grad에 저장됩니다. Gradient는 다음과 같이 계산합니다.

$$
\frac{\partial z}{\partial z}=1 \\
\frac{\partial z}{\partial y}=\frac{1}{y}=\frac{1}{x^3}=\frac{1}{125}=0.008 \\
\frac{\partial y}{\partial x}=3x^2=75
$$

$\frac{\partial z}{\partial x}$는 Chain Rule을 사용하여 다음과 같이 계산합니다. 이 값은 [Code 2](#Code-2)에서 근사로 계산한 값과 유사합니다.

$$
\frac{\partial z}{\partial x}=\frac{\partial y}{\partial x}\frac{\partial z}{\partial y}=75 \times 0.008=0.6
$$

requires_grad가 True로 설정되어 있는 Tensor는 계산할 때 Gradient의 계산이 필요하다는 것을 의미합니다. x.requires_grad를 Tensor를 생성할 때 True로 설정해 줬기 때문에 z.backward()를 부른 후에 x.grad에는 $\frac{\partial z}{\partial x}=0.6$이 저장됩니다. x.requires_grad를 True로 설정하면 x로부터 파생되는 Tensor에는 requires_grad가 True로 자동으로 설정됩니다. 그래서 x로부터 파생된 y와 z도 requires_grad가 True로 설정됩니다. 하지만 Gradient를 계산하더라도 그 Gradient를 항상 저장하지는 않습니다. Tensor의 is_leaf가 True이고 requires_grad가 True인 경우에만 Gradient를 계산하고 grad에 Gradient를 저장합니다. Tensor의 requires_grad가 사용자에 의해 True로 설정된 경우에 is_leaf가 True로 설정되고, requires_grad가 True로 설정된 Tensor로부터 파생된 Tensor의 경우에는 is_leaf가 False로 설정됩니다. 그래서 x는 is_leaf가 True이고 y와 z는 is_leaf가 False입니다. y와 z의 is_leaf가 False라서, y와 z는 requires_grad가 True라도, y.grad와 z.grad가 z.backward()를 호출한 뒤에도 Gradient가 저장되지 않고 None이 됩니다. x.grad를 계산하기 위해서는 y.grad와 z.grad를 계산해서 Chain Rule을 사용해야 되기 때문에 x.grad를 계산하기 위해서는 y.grad와 z.grad가 저장이 되지 않더라도 계산은 필요합니다. 그래서 x.grad를 계산하기 위해서 y.grad와 z.grad에 Gradient가 저장이 되지 않더라도 y.requires_grad와 z.requires_grad는 True로 설정합니다.

그림으로 다음과 같이 정리할 수 있습니다.

![code-4](/techblog/assets/images/PyTorch-Autograd/code-4.svg)

### Code 5 {#Code-5}

```python
import torch

def get_tensor_info(tensor):
  info = []
  for name in ['requires_grad', 'is_leaf', 'retains_grad', 'grad_fn', 'grad']:
    info.append(f'{name}({getattr(tensor, name, None)})')
  info.append(f'tensor({str(tensor)})')
  return ' '.join(info)

x = torch.tensor(5.0, requires_grad=True)
y = x ** 3
z = torch.log(y)

print('x', get_tensor_info(x))
print('y', get_tensor_info(y))
print('z', get_tensor_info(z))

y.retain_grad()
z.retain_grad()
z.backward()

print('x_after_backward', get_tensor_info(x))
print('y_after_backward', get_tensor_info(y))
print('z_after_backward', get_tensor_info(z))
```

[Code 4](#Code-4)에서 z.backward()를 호출하기 전에 y.retain_grad()와 z.retain_grad()를 호출합니다.

```
x requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor(5., requires_grad=True))
y requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<PowBackward0 object at 0x7ff0783929e8>) grad(None) tensor(tensor(125., grad_fn=<PowBackward0>))
z requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<LogBackward object at 0x7ff0783929e8>) grad(None) tensor(tensor(4.8283, grad_fn=<LogBackward>))
x_after_backward requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(0.6000000238418579) tensor(tensor(5., requires_grad=True))
y_after_backward requires_grad(True) is_leaf(False) retains_grad(True) grad_fn(<PowBackward0 object at 0x7ff0783929e8>) grad(0.00800000037997961) tensor(tensor(125., grad_fn=<PowBackward0>))
z_after_backward requires_grad(True) is_leaf(False) retains_grad(True) grad_fn(<LogBackward object at 0x7ff0783929e8>) grad(1.0) tensor(tensor(4.8283, grad_fn=<LogBackward>))
```

y와 z는 is_leaf가 False라서 y.grad와 z.grad에 Gradient가 저장되지 않습니다. 만약에 is_leaf가 아닌 Tensor에 Gradient가 grad에 저장되게 하고 싶으면, 해당 Tensor의 retain_grad()를 호출해서 retains_grad를 True로 설정하고, backward()를 호출하면 grad에 저장됩니다. y.retains_grad와 z.retains_grad를 True로 설정한 뒤에는, y.is_leaf와 z.is_leaf가 False로 설정되어 있어도, y.grad($\frac{\partial z}{\partial y}=0.008$)와 z.grad($\frac{\partial z}{\partial z}=1$)이 저장됩니다.

### Code 6 {#Code-6}

```python
import torch

def get_tensor_info(tensor):
  info = []
  for name in ['requires_grad', 'is_leaf', 'retains_grad', 'grad_fn', 'grad']:
    info.append(f'{name}({getattr(tensor, name, None)})')
  info.append(f'tensor({str(tensor)})')
  return ' '.join(info)

x = torch.tensor(5.0, requires_grad=True)
y = x ** 3
z = torch.log(y)

print('x', get_tensor_info(x))
print('y', get_tensor_info(y))
print('z', get_tensor_info(z))

z.backward()

print('x_after_backward', get_tensor_info(x))
print('y_after_backward', get_tensor_info(y))
print('z_after_backward', get_tensor_info(z))

z.backward()
```

[Code 4](#Code-4)에서 z.backward()를 2번 연속으로 호출합니다.

```
x requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor(5., requires_grad=True))
y requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<PowBackward0 object at 0x7fee9c0d29e8>) grad(None) tensor(tensor(125., grad_fn=<PowBackward0>))
z requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<LogBackward object at 0x7fee9c0d29e8>) grad(None) tensor(tensor(4.8283, grad_fn=<LogBackward>))
x_after_backward requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(0.6000000238418579) tensor(tensor(5., requires_grad=True))
y_after_backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<PowBackward0 object at 0x7fee9c0d29e8>) grad(None) tensor(tensor(125., grad_fn=<PowBackward0>))
z_after_backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<LogBackward object at 0x7fee9c0d29e8>) grad(None) tensor(tensor(4.8283, grad_fn=<LogBackward>))
Traceback (most recent call last):
  File "c6.py", line 25, in <module>
    z.backward()
  File "/home/ohhara/pytorch/lib/python3.6/site-packages/torch/tensor.py", line 195, in backward
    torch.autograd.backward(self, gradient, retain_graph, create_graph)
  File "/home/ohhara/pytorch/lib/python3.6/site-packages/torch/autograd/__init__.py", line 99, in backward
    allow_unreachable=True)  # allow_unreachable flag
RuntimeError: Trying to backward through the graph a second time, but the buffers have already been freed. Specify retain_graph=True when calling backward the first time.
```

backward() 함수는 Graph를 만든 후에 한 번만 호출하는 것을 가정하고 있습니다. 그래서 backward() 함수를 호출하면 backward()의 실행 후에 backward()의 실행에 필요한 각종 자원을 해제합니다. 그런 이유로 backward()를 연속해서 호출하면 Exception이 발생합니다.

### Code 7 {#Code-7}

```python
import torch

def get_tensor_info(tensor):
  info = []
  for name in ['requires_grad', 'is_leaf', 'retains_grad', 'grad_fn', 'grad']:
    info.append(f'{name}({getattr(tensor, name, None)})')
  info.append(f'tensor({str(tensor)})')
  return ' '.join(info)

x = torch.tensor(5.0, requires_grad=True)
y = x ** 3
z = torch.log(y)

print('x', get_tensor_info(x))
print('y', get_tensor_info(y))
print('z', get_tensor_info(z))

z.backward(retain_graph=True)

print('x_after_backward', get_tensor_info(x))
print('y_after_backward', get_tensor_info(y))
print('z_after_backward', get_tensor_info(z))

z.backward()

print('x_after_2backward', get_tensor_info(x))
print('y_after_2backward', get_tensor_info(y))
print('z_after_2backward', get_tensor_info(z))
```

[Code 6](#Code-6)에서 z.backward(retain_graph=True)를 호출하고 z.backward()를 호출합니다.

```
x requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor(5., requires_grad=True))
y requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<PowBackward0 object at 0x7f2f5bf589e8>) grad(None) tensor(tensor(125., grad_fn=<PowBackward0>))
z requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<LogBackward object at 0x7f2f5bf589e8>) grad(None) tensor(tensor(4.8283, grad_fn=<LogBackward>))
x_after_backward requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(0.6000000238418579) tensor(tensor(5., requires_grad=True))
y_after_backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<PowBackward0 object at 0x7f2f5bf589e8>) grad(None) tensor(tensor(125., grad_fn=<PowBackward0>))
z_after_backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<LogBackward object at 0x7f2f5bf589e8>) grad(None) tensor(tensor(4.8283, grad_fn=<LogBackward>))
x_after_2backward requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(1.2000000476837158) tensor(tensor(5., requires_grad=True))
y_after_2backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<PowBackward0 object at 0x7f2f5bf589e8>) grad(None) tensor(tensor(125., grad_fn=<PowBackward0>))
z_after_2backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<LogBackward object at 0x7f2f5bf589e8>) grad(None) tensor(tensor(4.8283, grad_fn=<LogBackward>))
```

z.backward(retain_graph=True)와 같이 retain_graph를 True로 설정해서 호출하면 backward() 호출에 필요한 자원을 backward() 내부에서 해제하지 않습니다. 이렇게 backward()를 호출한 경우에는 backward()를 한 번 더 호출할 수 있습니다. 마지막 backward()에서는 retain_graph를 True로 설정하지 않고 backward() 호출해서 backward() 호출에 필요한 자원을 해제합니다. 첫 번째 backward()를 호출한 뒤의 x.grad의 값과 두 번째 backward()를 호출한 뒤의 x.grad의 값을 비교해 보면 값이 다릅니다. 이것은 backward()에서 Gradient를 x.grad에 저장할 때 Gradient를 덮어쓰는 것이 아니라 기존 저장되어 있는 x.grad값에 Gradient를 더하기 때문입니다.

### Code 8 {#Code-8}

```python
import torch

def get_tensor_info(tensor):
  info = []
  for name in ['requires_grad', 'is_leaf', 'retains_grad', 'grad_fn', 'grad']:
    info.append(f'{name}({getattr(tensor, name, None)})')
  info.append(f'tensor({str(tensor)})')
  return ' '.join(info)

x = torch.tensor(5.0, requires_grad=True)
y = x ** 3
z = torch.log(y)

print('x', get_tensor_info(x))
print('y', get_tensor_info(y))
print('z', get_tensor_info(z))

z.backward(retain_graph=True)

print('x_after_backward', get_tensor_info(x))
print('y_after_backward', get_tensor_info(y))
print('z_after_backward', get_tensor_info(z))

x.grad.zero_()
z.backward()

print('x_after_2backward', get_tensor_info(x))
print('y_after_2backward', get_tensor_info(y))
print('z_after_2backward', get_tensor_info(z))
```

[Code 7](#Code-7)에서 z.backward(retain_graph=True)를 호출하고 z.backward()를 호출하는 사이에 x.grad를 In-place Operation을 사용해서 0으로 초기화합니다.

```
x requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor(5., requires_grad=True))
y requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<PowBackward0 object at 0x7fb9d9b24a58>) grad(None) tensor(tensor(125., grad_fn=<PowBackward0>))
z requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<LogBackward object at 0x7fb9d9b24a58>) grad(None) tensor(tensor(4.8283, grad_fn=<LogBackward>))
x_after_backward requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(0.6000000238418579) tensor(tensor(5., requires_grad=True))
y_after_backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<PowBackward0 object at 0x7fb9d9b24a58>) grad(None) tensor(tensor(125., grad_fn=<PowBackward0>))
z_after_backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<LogBackward object at 0x7fb9d9b24a58>) grad(None) tensor(tensor(4.8283, grad_fn=<LogBackward>))
x_after_2backward requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(0.6000000238418579) tensor(tensor(5., requires_grad=True))
y_after_2backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<PowBackward0 object at 0x7fb9d9b24a58>) grad(None) tensor(tensor(125., grad_fn=<PowBackward0>))
z_after_2backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<LogBackward object at 0x7fb9d9b24a58>) grad(None) tensor(tensor(4.8283, grad_fn=<LogBackward>))
```

x.grad를 backward()를 호출하기 전에 초기화를 해 주었기 때문에 첫 번째 backward()를 호출한 후의 x.grad의 값과 두 번째 backward()를 호출한 후의 x.grad의 값이 동일합니다.

### Code 9 {#Code-9}

```python
import torch

def get_tensor_info(tensor):
  info = []
  for name in ['requires_grad', 'is_leaf', 'retains_grad', 'grad_fn', 'grad']:
    info.append(f'{name}({getattr(tensor, name, None)})')
  info.append(f'tensor({str(tensor)})')
  return ' '.join(info)

x = torch.tensor(5.0, requires_grad=True)
y = x ** 3
w = x ** 2
z = torch.log(y) + torch.sqrt(w)

print('x', get_tensor_info(x))
print('y', get_tensor_info(y))
print('w', get_tensor_info(w))
print('z', get_tensor_info(z))

z.backward()

print('x_after_backward', get_tensor_info(x))
print('y_after_backward', get_tensor_info(y))
print('w_after_backward', get_tensor_info(w))
print('z_after_backward', get_tensor_info(z))
```

[Code 4](#Code-4)에서 z를 계산하는 계산식에 w를 추가합니다. w는 x로 계산합니다.

```
x requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor(5., requires_grad=True))
y requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<PowBackward0 object at 0x7f2ed092ca20>) grad(None) tensor(tensor(125., grad_fn=<PowBackward0>))
w requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<PowBackward0 object at 0x7f2ed092ca20>) grad(None) tensor(tensor(25., grad_fn=<PowBackward0>))
z requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<AddBackward0 object at 0x7f2ed092ca20>) grad(None) tensor(tensor(9.8283, grad_fn=<AddBackward0>))
x_after_backward requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(1.600000023841858) tensor(tensor(5., requires_grad=True))
y_after_backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<PowBackward0 object at 0x7f2ed092ca20>) grad(None) tensor(tensor(125., grad_fn=<PowBackward0>))
w_after_backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<PowBackward0 object at 0x7f2ed092ca20>) grad(None) tensor(tensor(25., grad_fn=<PowBackward0>))
z_after_backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<AddBackward0 object at 0x7f2ed092ca20>) grad(None) tensor(tensor(9.8283, grad_fn=<AddBackward0>))
```

각각의 Gradient는 다음과 같이 계산합니다.

$$
\frac{\partial z}{\partial z}=1 \\
\frac{\partial z}{\partial y}=\frac{1}{y}=\frac{1}{x^3}=\frac{1}{125}=0.008 \\
\frac{\partial y}{\partial x}=3x^2=75 \\
\frac{\partial w}{\partial x}=2x=10 \\
\frac{\partial z}{\partial w}=\frac{1}{2\sqrt{w}}=\frac{1}{2\sqrt{x^2}}=\frac{1}{2 \times 5}=0.1
$$

살펴보면 x가 y에 영향을 주고 y가 z에 영향을 줍니다. 그리고 x가 w에 영향을 주고 w가 z에 영향을 줍니다. 이런 경우에 x가 변할 때 z에 주는 영향을 구할 때는, x가 y를 통해 z에 준 영향과 x가 w를 통해 z에 준 영향을 더해서 다음과 같이 계산합니다. 그래서 x.grad에는 $1.6$이 저장됩니다.

$$
\frac{\partial z}{\partial x}=\frac{\partial y}{\partial x}\frac{\partial z}{\partial y}+\frac{\partial w}{\partial x}\frac{\partial z}{\partial w}=75 \times 0.008 + 10 \times 0.1=1.6
$$

backward()에서 grad에 Gradient를 저장할 때 기존의 grad에 Gradient를 더하기 때문에 이런 계산이 자연스럽게 이루어집니다. Convolutional Neural Network의 Convolution Filter처럼 한 Weight가 여러 계산에 Share되면서 계산되는 경우에, 이런 식으로 Gradient가 합산되면서 grad에 저장됩니다.

### Code 10 {#Code-10}

```python
import torch

def get_tensor_info(tensor):
  info = []
  for name in ['requires_grad', 'is_leaf', 'retains_grad', 'grad_fn', 'grad']:
    info.append(f'{name}({getattr(tensor, name, None)})')
  info.append(f'tensor({str(tensor)})')
  return ' '.join(info)

q = torch.tensor(3.0, requires_grad=True)
x = torch.tensor(5.0, requires_grad=True)
y = x ** q
z = torch.log(y)

print('q', get_tensor_info(q))
print('x', get_tensor_info(x))
print('y', get_tensor_info(y))
print('z', get_tensor_info(z))

z.backward()

print('q_after_backward', get_tensor_info(q))
print('x_after_backward', get_tensor_info(x))
print('y_after_backward', get_tensor_info(y))
print('z_after_backward', get_tensor_info(z))
```

[Code 4](#Code-4)에서 y를 계산할 때 자승하는 부분을 $3$대신에 q로 변경하여 q의 Gradient도 계산합니다.

```
q requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor(3., requires_grad=True))
x requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor(5., requires_grad=True))
y requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<PowBackward1 object at 0x7f000f65c9e8>) grad(None) tensor(tensor(125., grad_fn=<PowBackward1>))
z requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<LogBackward object at 0x7f000f65c9e8>) grad(None) tensor(tensor(4.8283, grad_fn=<LogBackward>))
q_after_backward requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(1.6094379425048828) tensor(tensor(3., requires_grad=True))
x_after_backward requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(0.6000000238418579) tensor(tensor(5., requires_grad=True))
y_after_backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<PowBackward1 object at 0x7f000f65c9e8>) grad(None) tensor(tensor(125., grad_fn=<PowBackward1>))
z_after_backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<LogBackward object at 0x7f000f65c9e8>) grad(None) tensor(tensor(4.8283, grad_fn=<LogBackward>))
```

$$
\frac{\partial z}{\partial z}=1 \\
\frac{\partial z}{\partial y}=\frac{1}{y}=\frac{1}{x^3}=\frac{1}{125}=0.008 \\
\frac{\partial y}{\partial x}=qx^{q-1}=3 \times 5^{3-1}=75 \\
\frac{\partial y}{\partial q}=x^q \ln{x}=5^3 \ln{5} \approx 125 \times 1.61=201.25
$$

$\frac{\partial z}{\partial x}$와 $\frac{\partial z}{\partial q}$는 Chain Rule을 사용하여 다음과 같이 계산합니다.

$$
\frac{\partial z}{\partial x}=\frac{\partial y}{\partial x}\frac{\partial z}{\partial y}=75 \times 0.008=0.6 \\
\frac{\partial z}{\partial q}=\frac{\partial y}{\partial q}\frac{\partial z}{\partial y} \approx 201.25 \times 0.008=1.61
$$

x.grad($\frac{\partial z}{\partial x}$)에 $0.6$이 저장되고 q.grad($\frac{\partial z}{\partial q}$)에 $1.61$이 저장됩니다.

그림으로 다음과 같이 정리할 수 있습니다.

![code-10](/techblog/assets/images/PyTorch-Autograd/code-10.svg)

### Code 11 {#Code-11}

```python
import torch

def get_tensor_info(tensor):
  info = []
  for name in ['requires_grad', 'is_leaf', 'retains_grad', 'grad_fn', 'grad']:
    info.append(f'{name}({getattr(tensor, name, None)})')
  info.append(f'tensor({str(tensor)})')
  return ' '.join(info)

class MyPow(torch.autograd.Function):
  @staticmethod
  def forward(ctx, input_1, input_2):
    ctx.save_for_backward(input_1, input_2)
    result = input_1 ** input_2
    return result

  @staticmethod
  def backward(ctx, grad_output):
    input_1, input_2 = ctx.saved_tensors
    grad_input_1 = grad_output * input_2 * input_1 ** (input_2 - 1)
    grad_input_2 = grad_output * input_1 ** input_2 * torch.log(input_1)
    print('input_1', input_1)
    print('input_2', input_2)
    print('grad_output', grad_output)
    print('grad_input_1', grad_input_1)
    print('grad_input_2', grad_input_2)
    return grad_input_1, grad_input_2

myPow = MyPow.apply

q = torch.tensor(3.0, requires_grad=True)
x = torch.tensor(5.0, requires_grad=True)
y = myPow(x, q)
z = torch.log(y)

print('q', get_tensor_info(q))
print('x', get_tensor_info(x))
print('y', get_tensor_info(y))
print('z', get_tensor_info(z))

z.backward()

print('q_after_backward', get_tensor_info(q))
print('x_after_backward', get_tensor_info(x))
print('y_after_backward', get_tensor_info(y))
print('z_after_backward', get_tensor_info(z))
```

[Code 10](#Code-10)에서 y를 계산할 때 자승하는 연산자를, PyTorch에서 제공해 주는 연산자 대신에, MyPow에 직접 구현하여 사용합니다.

```
q requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor(3., requires_grad=True))
x requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor(5., requires_grad=True))
y requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<torch.autograd.function.MyPowBackward object at 0x7f96e247e4a8>) grad(None) tensor(tensor(125., grad_fn=<MyPowBackward>))
z requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<LogBackward object at 0x7f970c1db780>) grad(None) tensor(tensor(4.8283, grad_fn=<LogBackward>))
input_1 tensor(5., requires_grad=True)
input_2 tensor(3., requires_grad=True)
grad_output tensor(0.0080)
grad_input_1 tensor(0.6000)
grad_input_2 tensor(1.6094)
q_after_backward requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(1.6094379425048828) tensor(tensor(3., requires_grad=True))
x_after_backward requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(0.6000000238418579) tensor(tensor(5., requires_grad=True))
y_after_backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<torch.autograd.function.MyPowBackward object at 0x7f96e247e4a8>) grad(None) tensor(tensor(125., grad_fn=<MyPowBackward>))
z_after_backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<LogBackward object at 0x7f970c1dba58>) grad(None) tensor(tensor(4.8283, grad_fn=<LogBackward>))
```

실행결과는 [Code 10](#Code-10)과 동일합니다. 만약에 사용하고자 하는 연산자를 PyTorch에서 제공하지 않는 경우에는 직접 연산자를 구현해서 사용해야 합니다. 여기서는 연산자를 어떻게 구현할 수 있는지 알아보기 위해 PyTorch에서 제공하는 연산자를 직접 구현해 보았습니다. 연산자의 계산과정을(forward) 구현하는 것은 크게 어렵지 않은데 Gradient계산을 위한 부분은(backward)는 조금 신경을 써 줘야 합니다.

backward()를 호출하면 기존의 계산식을 거꾸로 거슬러 올라가면서 Gradient를 계산합니다. 이때 거슬러 올라가면서 호출해 주는 함수의 정보가 Tensor의 grad_fn에 저장됩니다. 살펴보면 is_leaf가 True라서 거슬러 올라갈 필요가 없는 경우에 grad_fn이 존재하지 않고, is_leaf가 False라서 거슬러 올라갈 필요가 있는 경우에 grad_fn이 존재합니다. [Code 10](#Code-10)에서 y.grad_fn이 PowBackward1로 되어 있는데, 이것이 어떻게 작동하는지 살펴보기 위해 여기서는 MyPow를 직접 구현하였고, 현재 y.grad_fn이 torch.autograd.function.MyPowBackward로 설정되어 있는 것을 확인할 수 있습니다.

PyTorch에서 연산자를 정의할 때 torch.autograd.Function를 상속하여 forward()와 backward()를 구현합니다. forward()에는 ctx와 연산자에 전달되는 argument들이 차례대로 전달되고 이것을 이용해서 연산자가 계산해야 될 계산을 한 후에 계산결과를 return합니다. 여기서 추가로 처리해 줘야 할 것이 있는데, backward()에서 Gradient를 계산하기 위해서는 forward()의 연산 당시의 상태를 알고 있어야 하기 때문에, backward()에서 필요한 상태정보를 forward()에서 ctx.save_for_backward()를 호출하여 저장해 줘야 합니다. 예를 들어 $\frac{\partial y}{\partial x}=qx^{q-1}$라는 사실은 forward()의 연산당시의 상태를 몰라도 backward()에서 계산이 가능한데, Gradient를 구체적인 숫자로 계산하기 위해서는 forward()당시의 구체적인 q와 x의 값을 알아야 $\frac{\partial y}{\partial x}=qx^{q-1}=3 \times 5^{3-1}=75$ 와 같이 계산할 수 있습니다. MyPow.forward()에서는 이것을 위해 input_1로 전달된 x와 input_2로 전달된 q를 ctx.save_for_backward()를 호출하여 저장합니다.

MyPow.backward()에서는 일단 ctx.saved_tensors를 통해서 MyPow.forward() 호출당시의 input_1과 input_2를 읽습니다. MyPow.backward()에 전달되는 grad_output argument는 $\frac{\partial z}{\partial y}=\frac{1}{y}=\frac{1}{x^3}=\frac{1}{125}=0.008$입니다. z.backward()가 호출되면 결국 계산해야 되는 목표는 $\frac{\partial z}{\partial x}$와 $\frac{\partial z}{\partial q}$의 계산입니다. 이것의 계산은 z에서부터 계산을 거꾸로 거슬러 올라가면서 backward()들을 차례차례 호출하면서 하게 되는데, MyPow.backward()의 경우에는 $\frac{\partial z}{\partial y}$를 grad_output argument로 넘겨받고 $\frac{\partial z}{\partial x}$와 $\frac{\partial z}{\partial q}$를 grad_input_1과 grad_input_2로 return합니다. forward()에서 $x$와 $q$를 받아서 $y$를 return하고, backward()에서 $\frac{\partial z}{\partial y}$를 받아서 $\frac{\partial z}{\partial x}$와 $\frac{\partial z}{\partial q}$를 return합니다. MyPow의 내부에서는 $\frac{\partial y}{\partial x}$와 $\frac{\partial y}{\partial q}$를 계산할 수 있기 때문에, $\frac{\partial z}{\partial y}$를 외부에서 전달받으면, $\frac{\partial z}{\partial x}=\frac{\partial y}{\partial x}\frac{\partial z}{\partial y}$과 $\frac{\partial z}{\partial q}=\frac{\partial y}{\partial q}\frac{\partial z}{\partial y}$와 같이 Chain Rule을 이용하여 $\frac{\partial z}{\partial x}$과 $\frac{\partial z}{\partial q}$을 계산해서 return할 수 있습니다.

정리하면, MyPow.backward()에서 `grad_output`은 $\frac{\partial z}{\partial y}$, `input_1`은 $x$, `input_2`는 $q$, `input_2 * input_1 ** (input_2 - 1)`는 $\frac{\partial y}{\partial x}$, `input_1 ** input_2 * torch.log(input_1)`는 $\frac{\partial y}{\partial q}$, `grad_input_1`은 $\frac{\partial z}{\partial x}$, `grad_input_2`는 $\frac{\partial z}{\partial q}$입니다.

### Code 12 {#Code-12}

```python
import torch

def get_tensor_info(tensor):
  info = []
  for name in ['requires_grad', 'is_leaf', 'retains_grad', 'grad_fn', 'grad']:
    info.append(f'{name}({getattr(tensor, name, None)})')
  info.append(f'tensor({str(tensor)})')
  return ' '.join(info)

with torch.no_grad():
  q = torch.tensor(3.0, requires_grad=True)
  x = torch.tensor(5.0, requires_grad=True)
  y = x ** q
  z = torch.log(y)

print('q', get_tensor_info(q))
print('x', get_tensor_info(x))
print('y', get_tensor_info(y))
print('z', get_tensor_info(z))

z.backward()

print('q_after_backward', get_tensor_info(q))
print('x_after_backward', get_tensor_info(x))
print('y_after_backward', get_tensor_info(y))
print('z_after_backward', get_tensor_info(z))
```

[Code 10](#Code-10)에서 torch.no_grad()로 Context를 설정하고 계산을 수행합니다.

```
q requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor(3., requires_grad=True))
x requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor(5., requires_grad=True))
y requires_grad(False) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor(125.))
z requires_grad(False) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor(4.8283))
Traceback (most recent call last):
  File "c12.py", line 21, in <module>
    z.backward()
  File "/home/ohhara/pytorch/lib/python3.6/site-packages/torch/tensor.py", line 195, in backward
    torch.autograd.backward(self, gradient, retain_graph, create_graph)
  File "/home/ohhara/pytorch/lib/python3.6/site-packages/torch/autograd/__init__.py", line 99, in backward
    allow_unreachable=True)  # allow_unreachable flag
RuntimeError: element 0 of tensors does not require grad and does not have a grad_fn
```

계산식에서 도중 계산결과의 Tensor의 requires_grad가 True로 설정되어 있으면, backward() 함수 호출을 위한 준비를 위해(예를 들어 ctx.save_for_backward()의 호출로 인해) 상당한 양의 메모리를 사용하게 됩니다. 만약에 backward()를 호출하지 않는다면(Inference만 한다면), torch.no_grad() Context를 사용하여, 해당 Context내에서 생성된 Tensor들의 requires_grad가 False로 설정되도록 하여, 메모리 사용량을 줄일 수 있습니다.

여기의 실행결과를 살펴보면 [Code 10](#Code-10)와 다르게 y와 z의 requires_grad가 False로 설정되어 있고 grad_fn도 설정되어 있지 않습니다. backward() 호출을 위한 준비작업을 해 두지 않았기 때문에 z.backward() 호출시에는 Exception이 발생합니다.

### Code 13 {#Code-13}

```python
import torch

def get_tensor_info(tensor):
  info = []
  for name in ['requires_grad', 'is_leaf', 'retains_grad', 'grad_fn', 'grad']:
    info.append(f'{name}({getattr(tensor, name, None)})')
  info.append(f'tensor({str(tensor)})')
  return ' '.join(info)

x = torch.tensor(5.0, requires_grad=True)
y = x * torch.tensor([2.0, 3.0, 5.0])
z = y @ torch.tensor([4.0, 7.0, 9.0])

print('x', get_tensor_info(x))
print('y', get_tensor_info(y))
print('z', get_tensor_info(z))

y.retain_grad()
z.retain_grad()
z.backward()

print('x_after_backward', get_tensor_info(x))
print('y_after_backward', get_tensor_info(y))
print('z_after_backward', get_tensor_info(z))
```

x에서 Broadcast를 이용해서 3개 Element를 가지는 y를 계산하고, y에서 Dot Product로 Scalar를 가지는 z를 계산합니다. y.grad와 z.grad의 내용을 확인하기 위해 y.retain_grad()와 z.retain_grad()를 z.backward()를 호출하기 전에 호출합니다.

```
x requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor(5., requires_grad=True))
y requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<MulBackward0 object at 0x7fcb825dc9b0>) grad(None) tensor(tensor([10., 15., 25.], grad_fn=<MulBackward0>))
z requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<DotBackward object at 0x7fcb825dc9e8>) grad(None) tensor(tensor(370., grad_fn=<DotBackward>))
x_after_backward requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(74.0) tensor(tensor(5., requires_grad=True))
y_after_backward requires_grad(True) is_leaf(False) retains_grad(True) grad_fn(<MulBackward0 object at 0x7fcb825dc9e8>) grad(tensor([4., 7., 9.])) tensor(tensor([10., 15., 25.], grad_fn=<MulBackward0>))
z_after_backward requires_grad(True) is_leaf(False) retains_grad(True) grad_fn(<DotBackward object at 0x7fcb825dc9e8>) grad(1.0) tensor(tensor(370., grad_fn=<DotBackward>))
```

$$
\frac{\partial z}{\partial z}=1 \\
\frac{\partial z}{\partial y_1}=4 \\
\frac{\partial z}{\partial y_2}=7 \\
\frac{\partial z}{\partial y_3}=9 \\
\frac{\partial y_1}{\partial x}=2 \\
\frac{\partial y_2}{\partial x}=3 \\
\frac{\partial y_3}{\partial x}=5 \\
\frac{\partial z}{\partial x}=\frac{\partial z}{\partial y_1}\frac{\partial y_1}{\partial x}+\frac{\partial z}{\partial y_2}\frac{\partial y_2}{\partial x}+\frac{\partial z}{\partial y_3}\frac{\partial y_3}{\partial x}=4 \times 2 + 7 \times 3 + 9 \times 5=8+21+45=74
$$

그림으로 다음과 같이 정리할 수 있습니다.

![code-13](/techblog/assets/images/PyTorch-Autograd/code-13.svg)

### Code 14 {#Code-14}

```python
import torch

def get_tensor_info(tensor):
  info = []
  for name in ['requires_grad', 'is_leaf', 'retains_grad', 'grad_fn', 'grad']:
    info.append(f'{name}({getattr(tensor, name, None)})')
  info.append(f'tensor({str(tensor)})')
  return ' '.join(info)

x = torch.tensor(5.0, requires_grad=True)
y = x * torch.tensor([2.0, 3.0, 5.0])
w = y.detach()
z = w @ torch.tensor([4.0, 7.0, 9.0])

print('x', get_tensor_info(x))
print('y', get_tensor_info(y))
print('w', get_tensor_info(w))
print('z', get_tensor_info(z))

z.backward()

print('x_after_backward', get_tensor_info(x))
print('y_after_backward', get_tensor_info(y))
print('w_after_backward', get_tensor_info(w))
print('z_after_backward', get_tensor_info(z))
```

[Code 13](#Code-13)에서 y이용하여 z를 계산할 때 y.detach()를 호출합니다.

```
x requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor(5., requires_grad=True))
y requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<MulBackward0 object at 0x7f8a14f9f9b0>) grad(None) tensor(tensor([10., 15., 25.], grad_fn=<MulBackward0>))
w requires_grad(False) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor([10., 15., 25.]))
z requires_grad(False) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor(370.))
Traceback (most recent call last):
  File "c14.py", line 21, in <module>
    z.backward()
  File "/home/ohhara/pytorch/lib/python3.6/site-packages/torch/tensor.py", line 195, in backward
    torch.autograd.backward(self, gradient, retain_graph, create_graph)
  File "/home/ohhara/pytorch/lib/python3.6/site-packages/torch/autograd/__init__.py", line 99, in backward
    allow_unreachable=True)  # allow_unreachable flag
RuntimeError: element 0 of tensors does not require grad and does not have a grad_fn
```

requires_grad가 True인 Tensor를 이용하여 계산을 한 결과 Tensor는 requires_grad를 가집니다. 만약에 계산 도중에 이것을 의도적으로 끊어버리고 싶다면(해당 계산을 통해 backward()를 부르지 않을 것이라면) detach()를 호출합니다. detach()가 return한 Tensor는 requires_grad가 False로 설정되고 해당 Tensor에서 파생된 Tensor도 requires_grad가 False로 설정됩니다. 여기서는 w.requires_grad와 z.requires_grad가 False로 설정됩니다. 그리고 z.backward()를 호출했을 때 Exception이 발생합니다.

### Code 15 {#Code-15}

```python
import torch

def get_tensor_info(tensor):
  info = []
  for name in ['requires_grad', 'is_leaf', 'retains_grad', 'grad_fn', 'grad']:
    info.append(f'{name}({getattr(tensor, name, None)})')
  info.append(f'tensor({str(tensor)})')
  return ' '.join(info)

x = torch.tensor(5.0, requires_grad=True)
y = x * torch.tensor([2.0, 3.0, 5.0])
w = y.detach()
w.requires_grad_()
z = w @ torch.tensor([4.0, 7.0, 9.0])

print('x', get_tensor_info(x))
print('y', get_tensor_info(y))
print('w', get_tensor_info(w))
print('z', get_tensor_info(z))

z.backward()

print('x_after_backward', get_tensor_info(x))
print('y_after_backward', get_tensor_info(y))
print('w_after_backward', get_tensor_info(w))
print('z_after_backward', get_tensor_info(z))
```

[Code 14](#Code-14)에서 y.detach()를 호출하면 w의 requires_grad가 False로 설정되는데, w.requires_grad_()를 호출해서 w.requires_grad를 다시 True로 설정합니다.

```
x requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor(5., requires_grad=True))
y requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<MulBackward0 object at 0x7f68b8bf49b0>) grad(None) tensor(tensor([10., 15., 25.], grad_fn=<MulBackward0>))
w requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor([10., 15., 25.], requires_grad=True))
z requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<DotBackward object at 0x7f68b8bf4978>) grad(None) tensor(tensor(370., grad_fn=<DotBackward>))
x_after_backward requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor(5., requires_grad=True))
y_after_backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<MulBackward0 object at 0x7f68b8bf4978>) grad(None) tensor(tensor([10., 15., 25.], grad_fn=<MulBackward0>))
w_after_backward requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(tensor([4., 7., 9.])) tensor(tensor([10., 15., 25.], requires_grad=True))
z_after_backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<DotBackward object at 0x7f68b8bf49b0>) grad(None) tensor(tensor(370., grad_fn=<DotBackward>))
```

detach()를 호출한 후에 w.requires_grad를 다시 True로 설정해도 w.is_leaf가 True이고 w.grad_fn도 존재하지 않기 때문에 z.backward()를 호출해도 x.grad는 저장되지 않고 w.grad만 저장됩니다.

### Code 16 {#Code-16}

```python
import torch

def get_tensor_info(tensor):
  info = []
  for name in ['requires_grad', 'is_leaf', 'retains_grad', 'grad_fn', 'grad']:
    info.append(f'{name}({getattr(tensor, name, None)})')
  info.append(f'tensor({str(tensor)})')
  return ' '.join(info)

x = torch.tensor(5.0, requires_grad=True)
y = x * torch.tensor([2.0, 3.0, 5.0])
w = y.detach()
w.requires_grad_()
z = w @ torch.tensor([4.0, 7.0, 9.0])

print('x', get_tensor_info(x))
print('y', get_tensor_info(y))
print('w', get_tensor_info(w))
print('z', get_tensor_info(z))

z.backward()
y.backward(gradient=w.grad)

print('x_after_backward', get_tensor_info(x))
print('y_after_backward', get_tensor_info(y))
print('w_after_backward', get_tensor_info(w))
print('z_after_backward', get_tensor_info(z))
```

[Code 15](#Code-15)에서 z.backward() 호출 후에 y.backward() 도 호출해서 x.grad가 저장되도록 합니다.

```
x requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor(5., requires_grad=True))
y requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<MulBackward0 object at 0x7f517f15b9e8>) grad(None) tensor(tensor([10., 15., 25.], grad_fn=<MulBackward0>))
w requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor([10., 15., 25.], requires_grad=True))
z requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<DotBackward object at 0x7f517f15b9b0>) grad(None) tensor(tensor(370., grad_fn=<DotBackward>))
x_after_backward requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(74.0) tensor(tensor(5., requires_grad=True))
y_after_backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<MulBackward0 object at 0x7f517f15b9b0>) grad(None) tensor(tensor([10., 15., 25.], grad_fn=<MulBackward0>))
w_after_backward requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(tensor([4., 7., 9.])) tensor(tensor([10., 15., 25.], requires_grad=True))
z_after_backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<DotBackward object at 0x7f517f15b9e8>) grad(None) tensor(tensor(370., grad_fn=<DotBackward>))
```

z.backward()를 호출하면 w.grad에 $\begin{bmatrix}\frac{\partial z}{\partial y_1} & \frac{\partial z}{\partial y_2} & \frac{\partial z}{\partial y_3}\end{bmatrix}=\begin{bmatrix}4 & 7 & 9\end{bmatrix}$가 저장됩니다. y.backward()는 grad_output argument로 $\begin{bmatrix}\frac{\partial z}{\partial y_1} & \frac{\partial z}{\partial y_2} & \frac{\partial z}{\partial y_3}\end{bmatrix}$을 외부에서 넘겨받고, $\frac{\partial y_1}{\partial x}$, $\frac{\partial y_2}{\partial x}$, $\frac{\partial y_3}{\partial x}$을 내부에서 계산한 후에, $\frac{\partial z}{\partial x}=\frac{\partial z}{\partial y_1}\frac{\partial y_1}{\partial x}+\frac{\partial z}{\partial y_2}\frac{\partial y_2}{\partial x}+\frac{\partial z}{\partial y_3}\frac{\partial y_3}{\partial x}=4 \times 2 + 7 \times 3 + 9 \times 5=8+21+45=74$을 grad_input으로 return하면서 x.grad에 $74$가 저장됩니다. w.grad에 저장되어 있는 $\begin{bmatrix}\frac{\partial z}{\partial y_1} & \frac{\partial z}{\partial y_2} & \frac{\partial z}{\partial y_3}\end{bmatrix}$을 y.backward()에 전달해 주기 위해 y.backward(gradient=w.grad)와 전달합니다. 참고로 z와 다르게 y는 Scalar가 아니라서 y.backward()를 호출할 때는 gradient를 생략하면 안 되며 명시적으로 지정해 주어야 합니다. z와 같이 Scalar의 경우에는 backward()를 호출할 때 gradient를 특별히 설정하지 않으면 기본값 1($\frac{\partial z}{\partial z}$)로 설정됩니다.

### Code 17 {#Code-17}

```python
import torch

def get_tensor_info(tensor):
  info = []
  for name in ['requires_grad', 'is_leaf', 'retains_grad', 'grad_fn', 'grad']:
    info.append(f'{name}({getattr(tensor, name, None)})')
  info.append(f'tensor({str(tensor)})')
  return ' '.join(info)

x = torch.tensor(5.0, requires_grad=True)
y = x ** 3
z = torch.log(y)

print('x', get_tensor_info(x))
print('y', get_tensor_info(y))
print('z', get_tensor_info(z))

z.backward()

print('x_after_backward', get_tensor_info(x))
print('y_after_backward', get_tensor_info(y))
print('z_after_backward', get_tensor_info(z))

print('x.grad_after_backward', get_tensor_info(x.grad))
print('y.grad_after_backward', get_tensor_info(y.grad))
print('z.grad_after_backward', get_tensor_info(z.grad))

x_2nd_grad = torch.autograd.grad(x.grad, x)

print('x_2nd_grad', x_2nd_grad)
```

[Code 4](#Code-4)에서는 $\frac{\partial z}{\partial x}$를 x.grad에 저장했었는데, 여기서는 그 뒤에 torch.autograd.grad()를 사용하여 x.grad를 x로 미분해서 $\frac{\partial^2 z}{\partial x^2}$의 계산을 시도합니다.

```
x requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor(5., requires_grad=True))
y requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<PowBackward0 object at 0x7fedb0175a20>) grad(None) tensor(tensor(125., grad_fn=<PowBackward0>))
z requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<LogBackward object at 0x7fedb0175a20>) grad(None) tensor(tensor(4.8283, grad_fn=<LogBackward>))
x_after_backward requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(0.6000000238418579) tensor(tensor(5., requires_grad=True))
y_after_backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<PowBackward0 object at 0x7fedb0175a20>) grad(None) tensor(tensor(125., grad_fn=<PowBackward0>))
z_after_backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<LogBackward object at 0x7fedb0175a20>) grad(None) tensor(tensor(4.8283, grad_fn=<LogBackward>))
x.grad_after_backward requires_grad(False) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor(0.6000))
y.grad_after_backward requires_grad(None) is_leaf(None) retains_grad(None) grad_fn(None) grad(None) tensor(None)
z.grad_after_backward requires_grad(None) is_leaf(None) retains_grad(None) grad_fn(None) grad(None) tensor(None)
Traceback (most recent call last):
  File "c17.py", line 29, in <module>
    x_2nd_grad = torch.autograd.grad(x.grad, x)
  File "/home/ohhara/pytorch/lib/python3.6/site-packages/torch/autograd/__init__.py", line 157, in grad
    inputs, allow_unused)
RuntimeError: element 0 of tensors does not require grad and does not have a grad_fn
```

x.grad를 살펴보면 x.grad.requires_grad과 x.grad.grad_fn이 설정되어 있지 않습니다. 즉, x.grad가 기존 Graph에서 detach된 것처럼 Graph안에 포함되어 있지 않아서, x가 변할 때 x.grad가 얼마나 변하는지를($\frac{\partial^2 z}{\partial x^2}$) 계산할 수가 없습니다. 그래서 torch.autograd.grad()를 호출할 때 Exception이 발생합니다.

### Code 18 {#Code-18}

```python
import torch

def get_tensor_info(tensor):
  info = []
  for name in ['requires_grad', 'is_leaf', 'retains_grad', 'grad_fn', 'grad']:
    info.append(f'{name}({getattr(tensor, name, None)})')
  info.append(f'tensor({str(tensor)})')
  return ' '.join(info)

x = torch.tensor(5.0, requires_grad=True)
y = x ** 3
z = torch.log(y)

print('x', get_tensor_info(x))
print('y', get_tensor_info(y))
print('z', get_tensor_info(z))

z.backward(create_graph=True)

print('x_after_backward', get_tensor_info(x))
print('y_after_backward', get_tensor_info(y))
print('z_after_backward', get_tensor_info(z))

print('x.grad_after_backward', get_tensor_info(x.grad))
print('y.grad_after_backward', get_tensor_info(y.grad))
print('z.grad_after_backward', get_tensor_info(z.grad))

x_2nd_grad = torch.autograd.grad(x.grad, x)

print('x_2nd_grad', x_2nd_grad)
```

[Code 17](#Code-17)에서는 z.backward()를 호출했는데, 여기서는 그 대신에 z.backward(create_graph=True)를 호출합니다.

```
x requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor(5., requires_grad=True))
y requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<PowBackward0 object at 0x7ff439c63a20>) grad(None) tensor(tensor(125., grad_fn=<PowBackward0>))
z requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<LogBackward object at 0x7ff439c63a20>) grad(None) tensor(tensor(4.8283, grad_fn=<LogBackward>))
x_after_backward requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(0.6000000238418579) tensor(tensor(5., requires_grad=True))
y_after_backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<PowBackward0 object at 0x7ff439c63a20>) grad(None) tensor(tensor(125., grad_fn=<PowBackward0>))
z_after_backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<LogBackward object at 0x7ff439c63a20>) grad(None) tensor(tensor(4.8283, grad_fn=<LogBackward>))
x.grad_after_backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<CloneBackward object at 0x7ff439c63a20>) grad(None) tensor(tensor(0.6000, grad_fn=<CloneBackward>))
y.grad_after_backward requires_grad(None) is_leaf(None) retains_grad(None) grad_fn(None) grad(None) tensor(None)
z.grad_after_backward requires_grad(None) is_leaf(None) retains_grad(None) grad_fn(None) grad(None) tensor(None)
x_2nd_grad (tensor(-0.1200),)
```

z.backward()를 호출하는 대신에 z.backward(create_graph=True)로 호출하면 저장되는 x.grad도 Graph에 포함되면서, x.grad.requires_grad가 True로 설정되고 x.grad.grad_fn도 설정됩니다. torch.autograd.grad(x.grad, x)를 호출하면 $\frac{\partial^2 z}{\partial x^2}=-0.12$를 계산할 수 있습니다.

계산과정이 다소 복잡하니 차근차근 자세히 살펴보겠습니다.

처음 계산식은 다음과 같습니다.

$$
x=5 \\
y=x^3=125 \\
z=\ln(y) \approx 4.83
$$

z.backward(create_graph=True)를 호출하면 다음과 같이 계산합니다. create_graph를 True로 설정했기 때문에 이때 파생되는 계산결과인 $\frac{\partial z}{\partial y}$, $\frac{\partial y}{\partial x}$, $\frac{\partial z}{\partial x}$도 Graph에 포함됩니다.

$$
\frac{\partial z}{\partial z}=1 \\
\frac{\partial z}{\partial y}=\frac{1}{y}=0.008 \\
\frac{\partial y}{\partial x}=3x^2=75 \\
\frac{\partial z}{\partial x}=\frac{\partial y}{\partial x}\frac{\partial z}{\partial y}=0.6
$$

헷갈리지 않도록 a, b, c를 다음과 같이 정의합니다.

$$
a=\frac{\partial y}{\partial x} \\
b=\frac{\partial z}{\partial y} \\
c=\frac{\partial z}{\partial x}
$$

a, b, c를 포함한 새로운 계산식은 아래와 같습니다. z.backward()를 호출하게 되면 a, b, c가 상수로($a=75$, $b=0.008$, $c=0.6$) 생성되고, z.backward(create_graph=True)를 호출하게 되면 a, b, c가 아래처럼 Graph에 포함되면서 수식으로($a=3x^2$, $b=\frac{1}{y}$, $c=ab$) 생성됩니다.

$$
x=5 \\
y=x^3=125 \\
z=\ln(y) \approx 4.83 \\
a=3x^2=75 \\
b=\frac{1}{y}=0.008 \\
c=ab=0.6
$$

이렇게 계산식을 구성하고 c.backward()를 호출하면 x.grad에 $\frac{\partial c}{\partial x}$가 저장되게 되는데 이 값은 $\frac{\partial^2 z}{\partial x^2}$과 동일합니다. c부터 시작해서 Chain Rule을 사용하여 다음과 같이 차례차례 계산합니다. x는 a를 통해 c에 영향을 주고, x는 y를 거처 b를 통해 c에 영향을 주는 것에 주의합니다.

$$
\frac{\partial c}{\partial c}=1 \\
\frac{\partial c}{\partial a}=b=0.008 \\
\frac{\partial a}{\partial x}=6x=30 \\
\frac{\partial c}{\partial b}=a=75 \\
\frac{\partial b}{\partial y}=-\frac{1}{y^2}=-0.000064 \\
\frac{\partial y}{\partial x}=3x^2=75 \\
\frac{\partial c}{\partial x}=\frac{\partial a}{\partial x}\frac{\partial c}{\partial a}+\frac{\partial y}{\partial x}\frac{\partial b}{\partial y}\frac{\partial c}{\partial b}=30 \times 0.008 + 75 \times (-0.000064) \times 75=0.24-0.36=-0.12 \\
\frac{\partial^2 z}{\partial x^2}=\frac{\partial c}{\partial x}=-0.12
$$

### Code 19 {#Code-19}

```python
import torch

def get_tensor_info(tensor):
  info = []
  for name in ['requires_grad', 'is_leaf', 'retains_grad', 'grad_fn', 'grad']:
    info.append(f'{name}({getattr(tensor, name, None)})')
  info.append(f'tensor({str(tensor)})')
  return ' '.join(info)

x = torch.tensor(5.0, requires_grad=True)
y = x ** 3
z = torch.log(y)

print('x', get_tensor_info(x))
print('y', get_tensor_info(y))
print('z', get_tensor_info(z))

def hook_func(grad):
  print('grad', grad)
  return grad * 2

hook = y.register_hook(hook_func)
z.backward()
hook.remove()

print('x_after_backward', get_tensor_info(x))
print('y_after_backward', get_tensor_info(y))
print('z_after_backward', get_tensor_info(z))
```

[Code 4](#Code-4)에서 z.backward()를 호출하기 전에 y.register_hook()을 호출하여 backward hook을 register합니다.

```
x requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor(5., requires_grad=True))
y requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<PowBackward0 object at 0x7f67199d5ac8>) grad(None) tensor(tensor(125., grad_fn=<PowBackward0>))
z requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<LogBackward object at 0x7f67199d5ac8>) grad(None) tensor(tensor(4.8283, grad_fn=<LogBackward>))
grad tensor(0.0080)
x_after_backward requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(1.2000000476837158) tensor(tensor(5., requires_grad=True))
y_after_backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<PowBackward0 object at 0x7f67199d5ac8>) grad(None) tensor(tensor(125., grad_fn=<PowBackward0>))
z_after_backward requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<LogBackward object at 0x7f67199d5ac8>) grad(None) tensor(tensor(4.8283, grad_fn=<LogBackward>))
```

y.register_hook(hook_func)를 호출하여 hook_func를 backward hook으로 register하면, z.backward()를 호출했을 때, 결국에 y.grad가 계산되고 y.grad에 Gradient 값이 저장되기 전에 hook_func가 불립니다. 참고로 y.is_leaf가 False라서 y.grad에 해당하는 Gradient는 계산되더라도 y.grad에 실제로 Gradient가 저장되지는 않습니다. y.grad에 실제로 Gradient가 저장되지 않더라도 hook_func는 불립니다. hook_func에서 grad를 확인해 보면 $\frac{\partial z}{\partial y}=0.008$입니다. 만약에 hook_func에서 grad를 그대로 return하지 않고 다른 grad를 return하면 저장되는 grad가 return한 grad로 바뀝니다. 여기서는 hook_func에서 grad * 2를 return해서 y.grad를 $\frac{\partial z}{\partial y}=0.016$로 강제로 변경했습니다. 이것은 x.grad의 계산에도 영향을 미쳐, x.grad의 계산이 $\frac{\partial z}{\partial x}=\frac{\partial y}{\partial x}\frac{\partial z}{\partial y}=75 \times 0.016=1.2$로 변경됩니다.

### Code 20 {#Code-20}

```python
import torch

class MyPow(torch.autograd.Function):
  @staticmethod
  def forward(ctx, input_1, input_2):
    ctx.save_for_backward(input_1, input_2)
    result = input_1 ** input_2
    return result

  @staticmethod
  def backward(ctx, grad_output):
    input_1, input_2 = ctx.saved_tensors
    grad_input_1 = grad_output * input_2 * input_1 ** (input_2 - 1)
    grad_input_2 = grad_output * input_1 ** input_2 * torch.log(input_1)
    return grad_input_1, grad_input_2

myPow = MyPow.apply

q = torch.tensor(3.0, dtype=torch.float64, requires_grad=True)
x = torch.tensor(5.0, dtype=torch.float64, requires_grad=True)

print(torch.autograd.gradcheck(myPow, (x, q)))
```

[Code 11](#Code-11)에서 MyPow.backward()를 직접 구현했는데 이것이 정상적으로 작동하는지 torch.autograd.gradcheck()를 호출하여 확인합니다.

```
True
```

torch.autograd.gradcheck(myPow, (x, q))은 x와 q를 살짝 움직여서 myPow.forward()가 return하는 결과값의 변화를 살펴봅니다. 그리고 이것을 myPow.backward()가 계산한 Gradient와 비교해서 차이가 충분히 작으면 True를 return하고, 아니면 Exception을 Throw합니다. 여기서 차이가 충분히 작은지 확인할 때 torch.float32를 사용하면 오차가 커서 확인이 힘든 이유로 torch.float64를 사용합니다. backward()를 직접 구현하고 backward()가 정상적으로 작동하는지 확인할 때 torch.autograd.gradcheck()을 호출하여 확인할 수 있습니다.

### Code 21 {#Code-21}

```python
import torch

class MyPow(torch.autograd.Function):
  @staticmethod
  def forward(ctx, input_1, input_2):
    ctx.save_for_backward(input_1, input_2)
    result = input_1 ** input_2
    return result

  @staticmethod
  def backward(ctx, grad_output):
    input_1, input_2 = ctx.saved_tensors
    grad_input_1 = grad_output * input_2 * input_1 ** (input_2 - 1)
    grad_input_2 = grad_output * input_1 ** input_2 * torch.log(input_1 + 1)
    return grad_input_1, grad_input_2

myPow = MyPow.apply

q = torch.tensor(3.0, dtype=torch.float64, requires_grad=True)
x = torch.tensor(5.0, dtype=torch.float64, requires_grad=True)

print(torch.autograd.gradcheck(myPow, (x, q)))
```

[Code 20](#Code-20)에서 MyPow.backward() 안에 있는 grad_input_2의 값을 기존과 다르게 구현합니다.

```
Traceback (most recent call last):
  File "c21.py", line 22, in <module>
    print(torch.autograd.gradcheck(myPow, (x, q)))
  File "/home/ohhara/pytorch/lib/python3.6/site-packages/torch/autograd/gradcheck.py", line 289, in gradcheck
    'numerical:%s\nanalytical:%s\n' % (i, j, n, a))
  File "/home/ohhara/pytorch/lib/python3.6/site-packages/torch/autograd/gradcheck.py", line 227, in fail_test
    raise RuntimeError(msg)
RuntimeError: Jacobian mismatch for output 0 with respect to input 1,
numerical:tensor([[201.1797]], dtype=torch.float64)
analytical:tensor([[223.9699]], dtype=torch.float64)
```

여기서는 MyPow.backward()가 잘못 구현되어 있습니다. 그래서 torch.autograd.gradcheck()을 호출하면 Exception을 Throw합니다.

### Code 22 {#Code-22}

```python
import torch

def get_tensor_info(tensor):
  info = []
  for name in ['requires_grad', 'is_leaf', 'retains_grad', 'grad_fn', 'grad']:
    info.append(f'{name}({getattr(tensor, name, None)})')
  info.append(f'tensor({str(tensor)})')
  return ' '.join(info)

x = torch.tensor(5.0, requires_grad=True)
y = x ** 3
w = x ** 2
z = torch.log(y) + torch.sqrt(w)

print('x', get_tensor_info(x))
print('y', get_tensor_info(y))
print('w', get_tensor_info(w))
print('z', get_tensor_info(z))

print('z.grad_fn', z.grad_fn)
print('z.grad_fn.next_functions', z.grad_fn.next_functions)
print('y.grad_fn', z.grad_fn.next_functions[0][0].next_functions)
print('x_1.grad_fn', z.grad_fn.next_functions[0][0].next_functions[0][0].next_functions)
print('x_1_is_x', z.grad_fn.next_functions[0][0].next_functions[0][0].next_functions[0][0].variable is x)
print('w.grad_fn', z.grad_fn.next_functions[1][0].next_functions)
print('x_2.grad_fn', z.grad_fn.next_functions[1][0].next_functions[0][0].next_functions)
print('x_2_is_x', z.grad_fn.next_functions[1][0].next_functions[0][0].next_functions[0][0].variable is x)
```

[Code 9](#Code-9)에서 grad_fn안의 내용을 자세하게 따라가며 출력합니다.

```
x requires_grad(True) is_leaf(True) retains_grad(None) grad_fn(None) grad(None) tensor(tensor(5., requires_grad=True))
y requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<PowBackward0 object at 0x7f0a2accea90>) grad(None) tensor(tensor(125., grad_fn=<PowBackward0>))
w requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<PowBackward0 object at 0x7f0a2accea90>) grad(None) tensor(tensor(25., grad_fn=<PowBackward0>))
z requires_grad(True) is_leaf(False) retains_grad(None) grad_fn(<AddBackward0 object at 0x7f0a2accea90>) grad(None) tensor(tensor(9.8283, grad_fn=<AddBackward0>))
z.grad_fn <AddBackward0 object at 0x7f0a2acceac8>
z.grad_fn.next_functions ((<LogBackward object at 0x7f0a2accea90>, 0), (<SqrtBackward object at 0x7f0a2accea58>, 0))
y.grad_fn ((<PowBackward0 object at 0x7f0a2acceac8>, 0),)
x_1.grad_fn ((<AccumulateGrad object at 0x7f0a2accea58>, 0),)
x_1_is_x True
w.grad_fn ((<PowBackward0 object at 0x7f0a2acceac8>, 0),)
x_2.grad_fn ((<AccumulateGrad object at 0x7f0a2accea90>, 0),)
x_2_is_x True
```

z.grad_fn의 내용을 자세히 살펴보면 z.backward()를 호출했을 때 어떻게 backward()가 불리는지 알 수 있습니다. z.grad_fn은 z = torch.log(y) + torch.sqrt(w)의 +로 인해 AddBackward0가 설정됩니다. 다음에 호출될 backward()는 z.grad_fn.next_functions에 설정되어 있는 torch.log(y)의 LogBackward와 torch.sqrt(w)의 SqrtBackward입니다. 같은 방법으로 계속 거꾸로 거슬러 올라가면 결국에 x를 만나게 됩니다. 그런데 x가 y를 통해서도 z에 영향을 주고 w를 통해서도 z에 영향을 주기 때문에 backward()과정에서 x를 두 번 만나게 됩니다. 그래서 x_1_is_x와 x_2_is_x를 통해 확인해 보면 두 x가 동일한 x입니다.

## Conclusion {#Conclusion}

PyTorch의 Autograd를 조금 깊게 살펴보았습니다. PyTorch의 Autograd의 모든 기능을 상세하게 살펴보지는 않았지만, 여기에서 다룬 내용을 숙지하고 PyTorch의 Autograd의 Document를 살펴보면, 이전에 이해가 잘 되지 않았던 내용을 이해하는데 도움이 될 것으로 생각합니다.
