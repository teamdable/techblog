---
layout: post
title:  "PyTorch Module"
date:   2020-03-28 23:00:00 +0900
author: Taeho Oh
tags: [ 오태호, PyTorch, Module ]
---

안녕하세요. 오태호입니다.

PyTorch를 쓰다 보면 Module을 자주 사용하게 됩니다. Module은 별 기능이 없어 보여서 특별히 신경을 쓰지 않고 사용하는 경우가 많이 있지만 눈에 잘 보이지 않는 곳에서 미묘하게 작동하는 경우가 가끔 있습니다. 이 글에서는 PyTorch의 Module에 대해 약간 더 깊게 설명을 해서 Module의 미묘한 작동에 대해 조금 더 깊게 이해할 수 있도록 도와드립니다.

이 글은 PyTorch 1.4를 기준으로 작성하였습니다. 이 글을 이해하기 위해서는 Machine Learning에 대한 기초지식, PyTorch에 대한 기초지식, [PyTorch Autograd](PyTorch-Autograd)에 대한 이해가 필요합니다.

## Module {#Module}

PyTorch에서 Module은 Module자체로는 별다른 기능이 없지만 다른 여러 기능들을 포함해 주고 관리해 주는 Container입니다.

### Module Code 1 {#Module-Code-1}

```python
import torch

class PowLogModel(torch.nn.Module):

  def __init__(self):
    super(PowLogModel, self).__init__()

  def forward(self, x, q):
    y = x ** q
    z = torch.log(y)
    return z

powLogModel = PowLogModel()

x = torch.tensor(5.0, requires_grad=True)
q = torch.tensor(3.0, requires_grad=True)
z = powLogModel(x, q)
z.backward()

print('x', x)
print('x.grad', x.grad)
print('q', q)
print('q.grad', q.grad)
print('z', z)
```

[PyTorch Autograd Code 10](PyTorch-Autograd#Code-10)에서 PyTorch의 Module을 이용해서 하나로 묶습니다.

```
x tensor(5., requires_grad=True)
x.grad tensor(0.6000)
q tensor(3., requires_grad=True)
q.grad tensor(1.6094)
z tensor(4.8283, grad_fn=<LogBackward>)
```

결과를 확인해 보면 [PyTorch Autograd Code 10](PyTorch-Autograd#Code-10)과 동일한 결과인 것을 확인할 수 있습니다. Module을 상속한 class에서 forward() method를 정의하면 Module.\__call__()가 호출될 때, 정의한 forward()가 호출됩니다. Module.\__call__()을 살펴보면 다음과 같이 구현되어 있습니다. (내용 이해에 불필요한 구현 내용은 생략하였습니다.)

```python
def __call__(self, *input, **kwargs):
  return self.forward(*input, **kwargs)
```

### Module Code 2 {#Module-Code-2}

```python
import torch

class PowModel(torch.nn.Module):

  def __init__(self):
    super(PowModel, self).__init__()

  def forward(self, x, q):
    return x ** q

class LogModel(torch.nn.Module):

  def __init__(self):
    super(LogModel, self).__init__()

  def forward(self, x):
    return torch.log(x)

class PowLogModel(torch.nn.Module):

  def __init__(self):
    super(PowLogModel, self).__init__()
    self.powModel = PowModel()
    self.logModel = LogModel()

  def forward(self, x, q):
    y = self.powModel(x, q)
    z = self.logModel(y)
    return z

powLogModel = PowLogModel()

x = torch.tensor(5.0, requires_grad=True)
q = torch.tensor(3.0, requires_grad=True)
z = powLogModel(x, q)
z.backward()

print('x', x)
print('x.grad', x.grad)
print('q', q)
print('q.grad', q.grad)
print('z', z)

print('powLogModel.named_children', list(powLogModel.named_children()))
```

[Module Code 1](#Module-Code-1)에서 Module이 다른 Module을 포함하도록 구성하도록 변경합니다.

```
x tensor(5., requires_grad=True)
x.grad tensor(0.6000)
q tensor(3., requires_grad=True)
q.grad tensor(1.6094)
z tensor(4.8283, grad_fn=<LogBackward>)
powLogModel.named_children [('powModel', PowModel()), ('logModel', LogModel())]
```

Module은 다른 Module을 포함하도록 구성할 수 있습니다. 실행결과는 [Module Code 1](#Module-Code-1)과 동일합니다. powLogModel.named_children()을 호출한 결과를 보면 powLogModel이 powModel과 logModel을 포함하고 있는 것을 확인할 수 있습니다.

그런데, 여기서 잘 살펴보면 powLogModel입장에서는 powModel과 logModel을 포함하고 있다는 사실을 알 수가 없을 것 같은데 powLogModel.named_children()의 호출결과를 보면 powModel과 logModel을 포함하고 있는 것을 잘 인식하고 있습니다. 이것은 다음과 같이 Module.\__setattr__()이 구현되어 있기 때문입니다. (내용 이해에 불필요한 구현 내용은 생략하였습니다.)

```
def __setattr__(self, name, value):
  if isinstance(value, torch.nn.Parameter):
    self.register_parameter(name, value)
  elif isinstance(value, torch.nn.Module):
    self.add_module(name, value)
  else:
    object.__setattr__(self, name, value)
```

Parameter에 대한 내용은 나중에 설명할 예정입니다. Instance의 Attribute를 Set할 때 Value가 Module Type Instance면 add_module()을 호출해 주도록 구현되어 있습니다. 즉, PowLogModel.\__init__()안에서 powModel Attribute과 logModel Attribute를 Set할 때, add_module()이 호출되면서, powLogModel에 powModel과 logModel이 추가되었다는 사실을, powLogModel이 인식하게 됩니다.

### Module Code 3 {#Module-Code-3}

```python
import torch

class PowModel(torch.nn.Module):

  def __init__(self):
    super(PowModel, self).__init__()

  def forward(self, x, q):
    return x ** q

class LogModel(torch.nn.Module):

  def __init__(self):
    super(LogModel, self).__init__()

  def forward(self, x):
    return torch.log(x)

class PowLogModel(torch.nn.Module):

  def __init__(self):
    super(PowLogModel, self).__init__()
    self.modelList = [PowModel(), LogModel()]

  def forward(self, x, q):
    y = self.modelList[0](x, q)
    z = self.modelList[1](y)
    return z

powLogModel = PowLogModel()

x = torch.tensor(5.0, requires_grad=True)
q = torch.tensor(3.0, requires_grad=True)
z = powLogModel(x, q)
z.backward()

print('x', x)
print('x.grad', x.grad)
print('q', q)
print('q.grad', q.grad)
print('z', z)

print('powLogModel.named_children', list(powLogModel.named_children()))
```

[Module Code 2](#Module-Code-2)에서 PowLogModel의 PowModel과 LogModel을 List에 저장해서 사용합니다.

```
x tensor(5., requires_grad=True)
x.grad tensor(0.6000)
q tensor(3., requires_grad=True)
q.grad tensor(1.6094)
z tensor(4.8283, grad_fn=<LogBackward>)
powLogModel.named_children []
```

계산 결과는 [Module Code 2](#Module-Code-2)과 동일한 것을 확인할 수 있지만 powLogModel.named_children()이 powLogModel이 포함하고 있는 PowModel과 LogModel을 인식하지 못하는 것을 확인할 수 있습니다. 이것은 PowLogModel.\__init__()에서 modelList Field를 Set할 때 Module Type이 아니라서 powLogModel이 인식하지 못한 것이 원인입니다.

### Module Code 4 {#Module-Code-4}

```python
import torch

class PowModel(torch.nn.Module):

  def __init__(self):
    super(PowModel, self).__init__()

  def forward(self, x, q):
    return x ** q

class LogModel(torch.nn.Module):

  def __init__(self):
    super(LogModel, self).__init__()

  def forward(self, x):
    return torch.log(x)

class PowLogModel(torch.nn.Module):

  def __init__(self):
    super(PowLogModel, self).__init__()
    self.modelList = [PowModel(), LogModel()]
    self.add_module('powModel', self.modelList[0])
    self.add_module('logModel', self.modelList[1])

  def forward(self, x, q):
    y = self.powModel(x, q)
    z = self.logModel(y)
    return z

powLogModel = PowLogModel()

x = torch.tensor(5.0, requires_grad=True)
q = torch.tensor(3.0, requires_grad=True)
z = powLogModel(x, q)
z.backward()

print('x', x)
print('x.grad', x.grad)
print('q', q)
print('q.grad', q.grad)
print('z', z)

print('powLogModel.named_children', list(powLogModel.named_children()))
```

[Module Code 3](#Module-Code-3)에서 PowLogModel의 PowModel과 LogModel을 List에 저장한 후에 각각 add_module()을 호출합니다.

```
x tensor(5., requires_grad=True)
x.grad tensor(0.6000)
q tensor(3., requires_grad=True)
q.grad tensor(1.6094)
z tensor(4.8283, grad_fn=<LogBackward>)
powLogModel.named_children [('powModel', PowModel()), ('logModel', LogModel())]
```

add_module()을 호출한 후에는 [Module Code 2](#Module-Code-2)처럼 powLogModel.named_children()가 정상적으로 작동하는 것을 확인할 수 있습니다.

### Module Code 5 {#Module-Code-5}

```python
import torch

class PowModel(torch.nn.Module):

  def __init__(self):
    super(PowModel, self).__init__()

  def forward(self, x, q):
    return x ** q

class LogModel(torch.nn.Module):

  def __init__(self):
    super(LogModel, self).__init__()

  def forward(self, x):
    return torch.log(x)

class PowLogModel(torch.nn.Module):

  def __init__(self):
    super(PowLogModel, self).__init__()
    self.modelList = torch.nn.ModuleList([PowModel(), LogModel()])

  def forward(self, x, q):
    y = self.modelList[0](x, q)
    z = self.modelList[1](y)
    return z

powLogModel = PowLogModel()

x = torch.tensor(5.0, requires_grad=True)
q = torch.tensor(3.0, requires_grad=True)
z = powLogModel(x, q)
z.backward()

print('x', x)
print('x.grad', x.grad)
print('q', q)
print('q.grad', q.grad)
print('z', z)

print('powLogModel.named_children', list(powLogModel.named_children()))
```

[Module Code 3](#Module-Code-3)에서 PowLogModel의 PowModel과 LogModel을 List로 저장할 때 ModuleList를 이용해서 List를 만들어서 저장합니다.

```
x tensor(5., requires_grad=True)
x.grad tensor(0.6000)
q tensor(3., requires_grad=True)
q.grad tensor(1.6094)
z tensor(4.8283, grad_fn=<LogBackward>)
powLogModel.named_children [('modelList', ModuleList(
  (0): PowModel()
  (1): LogModel()
))]
```

ModuleList는 Module을 상속한 class로 Module Type입니다. Module Type이라는 점을 빼고는 Python의 List와 거의 동일합니다. 여러 Module을 List로 저장할 때는, logPowModel이 자신에게 포함된 Module들을 인식하기 위해서, Python의 List를 보다는 ModuleList를 사용하는 것이 편합니다.

### Module Code 6 {#Module-Code-6}

```python
import torch

class PowModel(torch.nn.Module):

  def __init__(self):
    super(PowModel, self).__init__()

  def forward(self, x, q):
    return x ** q

class LogModel(torch.nn.Module):

  def __init__(self):
    super(LogModel, self).__init__()

  def forward(self, x):
    return torch.log(x)

class PowLogModel(torch.nn.Module):

  def __init__(self):
    super(PowLogModel, self).__init__()
    self.modelDict = {'powModel': PowModel(), 'logModel': LogModel()}

  def forward(self, x, q):
    y = self.modelDict['powModel'](x, q)
    z = self.modelDict['logModel'](y)
    return z

powLogModel = PowLogModel()

x = torch.tensor(5.0, requires_grad=True)
q = torch.tensor(3.0, requires_grad=True)
z = powLogModel(x, q)
z.backward()

print('x', x)
print('x.grad', x.grad)
print('q', q)
print('q.grad', q.grad)
print('z', z)

print('powLogModel.named_children', list(powLogModel.named_children()))
```

[Module Code 2](#Module-Code-2)에서 PowLogModel의 PowModel과 LogModel을 Dictionary에 저장해서 사용합니다.

```
x tensor(5., requires_grad=True)
x.grad tensor(0.6000)
q tensor(3., requires_grad=True)
q.grad tensor(1.6094)
z tensor(4.8283, grad_fn=<LogBackward>)
powLogModel.named_children []
```

계산 결과는 [Module Code 2](#Module-Code-2)과 동일한 것을 확인할 수 있지만 powLogModel.named_children()이 powLogModel이 포함하고 있는 PowModel과 LogModel을 인식하지 못하는 것을 확인할 수 있습니다. 이것은 PowLogModel.\__init__()에서 modelDict Field를 Set할 때 Module Type이 아니라서 powLogModel이 인식하지 못한 것이 원인입니다.

### Module Code 7 {#Module-Code-7}

```python
import torch

class PowModel(torch.nn.Module):

  def __init__(self):
    super(PowModel, self).__init__()

  def forward(self, x, q):
    return x ** q

class LogModel(torch.nn.Module):

  def __init__(self):
    super(LogModel, self).__init__()

  def forward(self, x):
    return torch.log(x)

class PowLogModel(torch.nn.Module):

  def __init__(self):
    super(PowLogModel, self).__init__()
    self.modelDict = torch.nn.ModuleDict(
        {'powModel': PowModel(), 'logModel': LogModel()})

  def forward(self, x, q):
    y = self.modelDict['powModel'](x, q)
    z = self.modelDict['logModel'](y)
    return z

powLogModel = PowLogModel()

x = torch.tensor(5.0, requires_grad=True)
q = torch.tensor(3.0, requires_grad=True)
z = powLogModel(x, q)
z.backward()

print('x', x)
print('x.grad', x.grad)
print('q', q)
print('q.grad', q.grad)
print('z', z)

print('powLogModel.named_children', list(powLogModel.named_children()))
```

[Module Code 6](#Module-Code-6)에서 PowLogModel의 PowModel과 LogModel을 Dictionary로 저장할 때 ModuleDict를 이용해서 Dictionary를 만들어서 저장합니다.

```
x tensor(5., requires_grad=True)
x.grad tensor(0.6000)
q tensor(3., requires_grad=True)
q.grad tensor(1.6094)
z tensor(4.8283, grad_fn=<LogBackward>)
powLogModel.named_children [('modelDict', ModuleDict(
  (logModel): LogModel()
  (powModel): PowModel()
))]
```

ModuleDict는 Module을 상속한 class로 Module Type입니다. Module Type이라는 점을 빼고는 Python의 Dictionary와 거의 동일합니다. 여러 Module을 Dictionary로 저장할 때는, logPowModel이 자신에게 포함된 Module들을 인식하기 위해서, Python의 Dictionary를 보다는 ModuleDict를 사용하는 것이 편합니다.

## Parameter {#Parameter}

Parameter는 Module에 저장해 놓고 사용하는 Tensor의 일종으로 학습을 통해 계산되는 Tensor입니다.

### Parameter Code 1 {#Parameter-Code-1}

```python
import torch

class PowModel(torch.nn.Module):

  def __init__(self):
    super(PowModel, self).__init__()
    self.powParam = torch.nn.Parameter(torch.tensor(1.0))

  def forward(self, x, q):
    return self.powParam * x ** q

class LogModel(torch.nn.Module):

  def __init__(self):
    super(LogModel, self).__init__()
    self.logParam = torch.nn.Parameter(torch.tensor(1.0))

  def forward(self, x):
    return self.logParam * torch.log(x)

class PowLogModel(torch.nn.Module):

  def __init__(self):
    super(PowLogModel, self).__init__()
    self.powModel = PowModel()
    self.logModel = LogModel()

  def forward(self, x, q):
    y = self.powModel(x, q)
    z = self.logModel(y)
    return z

powLogModel = PowLogModel()

x = torch.tensor(5.0, requires_grad=True)
q = torch.tensor(3.0, requires_grad=True)
z = powLogModel(x, q)
z.backward()

print('x', x)
print('x.grad', x.grad)
print('q', q)
print('q.grad', q.grad)
print('z', z)

for name, parameter in powLogModel.named_parameters():
  print(name, f'data({parameter.data}), grad({parameter.grad})')
```

[Module Code 2](#Module-Code-2)에서 powModel에 powParam을 추가하고 logModel에 logParam을 추가합니다. 둘 다 초기값을 1.0으로 설정하고 forward에서 곱하기를 하도록 하여 결과는 기존과 변함이 없도록 합니다.

```
x tensor(5., requires_grad=True)
x.grad tensor(0.6000)
q tensor(3., requires_grad=True)
q.grad tensor(1.6094)
z tensor(4.8283, grad_fn=<MulBackward0>)
powModel.powParam data(1.0), grad(1.0)
logModel.logParam data(1.0), grad(4.828313827514648)
```

Tensor는 requires_grad의 Default설정이 False지만, Parameter는 학습을 통해 구해지는 Tensor이기 때문에 Default설정이 True입니다. [Module Code 2](#Module-Code-2)에서 언급된 Module.\__setattr__()을 살펴보면 Parameter Type이 Module의 Attribute로 Set이 될 때 self.register_parameter()를 호출하도록 구현되어 있습니다. 그래서 powLogModel.named_parameters()를 호출해 보면 powLogModel이 자신이 가지고 있는 Parameter들을 잘 인식하고 있는 것을 확인할 수 있습니다.

### Parameter Code 2 {#Parameter-Code-2}

```python
import torch

class PowModel(torch.nn.Module):

  def __init__(self):
    super(PowModel, self).__init__()
    self.powParamDict = {'powParam': torch.nn.Parameter(torch.tensor(1.0))}

  def forward(self, x, q):
    return self.powParamDict['powParam'] * x ** q

class LogModel(torch.nn.Module):

  def __init__(self):
    super(LogModel, self).__init__()
    self.logParam = torch.nn.Parameter(torch.tensor(1.0))

  def forward(self, x):
    return self.logParam * torch.log(x)

class PowLogModel(torch.nn.Module):

  def __init__(self):
    super(PowLogModel, self).__init__()
    self.powModel = PowModel()
    self.logModel = LogModel()

  def forward(self, x, q):
    y = self.powModel(x, q)
    z = self.logModel(y)
    return z

powLogModel = PowLogModel()

x = torch.tensor(5.0, requires_grad=True)
q = torch.tensor(3.0, requires_grad=True)
z = powLogModel(x, q)
z.backward()

print('x', x)
print('x.grad', x.grad)
print('q', q)
print('q.grad', q.grad)
print('z', z)

for name, parameter in powLogModel.named_parameters():
  print(name, f'data({parameter.data}), grad({parameter.grad})')
```

[Parameter Code 1](#Parameter-Code-1)에서 powModel에 powParam을 추가할 때 Dictionary를 이용해서 추가합니다.

```
x tensor(5., requires_grad=True)
x.grad tensor(0.6000)
q tensor(3., requires_grad=True)
q.grad tensor(1.6094)
z tensor(4.8283, grad_fn=<MulBackward0>)
logModel.logParam data(1.0), grad(4.828313827514648)
```

Module은 Parameter Type을 Attribute로 Set할 때만 Parameter로 인식합니다. Dictionary를 이용하게 되면 Parameter Type이 아니기 때문에 Parameter로 인식이 되지 않아서 register_parameter()를 자동으로 호출해 주지 않습니다. 그래서 여기서 powLogModel.named_parameters()의 내용을 보면 powModel.powParam가 인식되지 않은 것을 확인할 수 있습니다.

Module에 Parameter를 추가하는 것은 [Module](#Module)에서 언급된 Module에 Module을 추가하는 것과 방식이 동일합니다. 그래서 Module에 Parameter를 추가하는 방법으로는, Parameter Type을 Attribute로 Set하는 방법 외에도, 직접 register_parameter()를 직접 호출해 줘서 추가할 수도 있고, ParameterDict를 Python Dictionary대신에 사용해서 Parameter가 자동으로 추가되게 할 수도 있으며, ParameterList를 Python List대신에 사용해서 Parameter가 자동으로 등록되게 할 수도 있습니다.

### Parameter Code 3 {#Parameter-Code-3}

```python
import torch

class PowModel(torch.nn.Module):

  def __init__(self):
    super(PowModel, self).__init__()
    self.powParam = torch.nn.Parameter(torch.tensor(1.0))

  def forward(self, x, q):
    return self.powParam * x ** q

class LogModel(torch.nn.Module):

  def __init__(self):
    super(LogModel, self).__init__()
    self.logParam = torch.nn.Parameter(torch.tensor(1.0))

  def forward(self, x):
    return self.logParam * torch.log(x)

class PowLogModel(torch.nn.Module):

  def __init__(self):
    super(PowLogModel, self).__init__()
    self.powModel = PowModel()
    self.logModel = LogModel()

  def forward(self, x, q):
    y = self.powModel(x, q)
    z = self.logModel(y)
    return z

powLogModel = PowLogModel()

z = powLogModel(5.0, 3.0)
print('z', z)

learning_rate = 0.01
for i in range(10):
  powLogModel.zero_grad()
  x = torch.tensor(5.0)
  q = torch.tensor(3.0)
  z = powLogModel(5.0, 3.0)
  target = 10.0
  loss = (z - target) ** 2
  loss.backward()
  with torch.no_grad():
    for name, parameter in powLogModel.named_parameters():
      parameter -= parameter.grad * learning_rate
      print(i, name, parameter.data)

z = powLogModel(5.0, 3.0)
print('z', z)
```

[Parameter Code 1](#Parameter-Code-1)에서 powParam과 logParam을 학습을 통해 적절한 값을 찾습니다.

```
z tensor(4.8283, grad_fn=<MulBackward0>)
0 powModel.powParam tensor(1.1034)
0 logModel.logParam tensor(1.4994)
1 powModel.powParam tensor(1.1744)
1 logModel.logParam tensor(1.7569)
2 powModel.powParam tensor(1.2114)
2 logModel.logParam tensor(1.8801)
3 powModel.powParam tensor(1.2288)
3 logModel.logParam tensor(1.9365)
4 powModel.powParam tensor(1.2367)
4 logModel.logParam tensor(1.9618)
5 powModel.powParam tensor(1.2403)
5 logModel.logParam tensor(1.9730)
6 powModel.powParam tensor(1.2418)
6 logModel.logParam tensor(1.9779)
7 powModel.powParam tensor(1.2425)
7 logModel.logParam tensor(1.9801)
8 powModel.powParam tensor(1.2428)
8 logModel.logParam tensor(1.9811)
9 powModel.powParam tensor(1.2430)
9 logModel.logParam tensor(1.9815)
z tensor(9.9982, grad_fn=<MulBackward0>)
```

일반적으로 학습을 통해 Parameter의 값을 계산할 때는 torch.optim을 이용하는 것이 일반적이지만 여기서는 이해를 돕기 위해 torch.optim을 사용하지 않고 직접 Gradient Descent를 이용하여 학습을 진행합니다. z의 초기값이 4.8283이고, 이것을 10.0으로 만들어 주는 적절한 powParam과 logParam을 학습을 통해 구합니다. Loss는 Mean Squared Error(MSE)로 설정하고 Learning Rate는 0.01로 설정하고 Iteration은 10으로 설정합니다. powLogModel.named_parameters()가 return해 주는 Parameter들의 값을 Gradient Descent를 이용하여 학습을 통해 찾습니다. 10번의 Iteration후에 powParam가 1.2430이 되고 logParam이 1.9815가 되며 z는 9.9982가 되어 z가 목표값인 10.0에 근접한 값을 가지게 됩니다.

### Parameter Code 4 {#Parameter-Code-4}

```python
import torch

class PowModel(torch.nn.Module):

  def __init__(self):
    super(PowModel, self).__init__()
    self.powParam = torch.nn.Parameter(torch.tensor(1.0))

  def forward(self, x, q):
    return self.powParam * x ** q

class LogModel(torch.nn.Module):

  def __init__(self):
    super(LogModel, self).__init__()
    self.logParam = torch.nn.Parameter(torch.tensor(1.0))

  def forward(self, x):
    return self.logParam * torch.log(x)

class PowLogModel(torch.nn.Module):

  def __init__(self):
    super(PowLogModel, self).__init__()
    self.powModel = PowModel()
    self.logModel = LogModel()

  def forward(self, x, q):
    y1 = self.powModel(x, q)
    z1 = self.logModel(y1)
    y2 = self.powModel(x, q)
    z2 = self.logModel(y2)
    return (z1 + z2) / 2

powLogModel = PowLogModel()

z = powLogModel(5.0, 3.0)
print('z', z)

learning_rate = 0.01
for i in range(10):
  powLogModel.zero_grad()
  x = torch.tensor(5.0)
  q = torch.tensor(3.0)
  z = powLogModel(5.0, 3.0)
  target = 10.0
  loss = (z - target) ** 2
  loss.backward()
  with torch.no_grad():
    for name, parameter in powLogModel.named_parameters():
      parameter -= parameter.grad * learning_rate
      print(i, name, parameter.data)

z = powLogModel(5.0, 3.0)
print('z', z)
```

[Parameter Code 3](#Parameter-Code-3)에서 powModel과 logModel을 여러 곳에서 중복해서 사용합니다.

```
z tensor(4.8283, grad_fn=<DivBackward0>)
0 powModel.powParam tensor(1.1034)
0 logModel.logParam tensor(1.4994)
1 powModel.powParam tensor(1.1744)
1 logModel.logParam tensor(1.7569)
2 powModel.powParam tensor(1.2114)
2 logModel.logParam tensor(1.8801)
3 powModel.powParam tensor(1.2288)
3 logModel.logParam tensor(1.9365)
4 powModel.powParam tensor(1.2367)
4 logModel.logParam tensor(1.9618)
5 powModel.powParam tensor(1.2403)
5 logModel.logParam tensor(1.9730)
6 powModel.powParam tensor(1.2418)
6 logModel.logParam tensor(1.9779)
7 powModel.powParam tensor(1.2425)
7 logModel.logParam tensor(1.9801)
8 powModel.powParam tensor(1.2428)
8 logModel.logParam tensor(1.9811)
9 powModel.powParam tensor(1.2430)
9 logModel.logParam tensor(1.9815)
z tensor(9.9982, grad_fn=<DivBackward0>)
```

한 Module Instance를 여러 곳에서 중복해서 사용하게 되면 [PyTorch Autograd Code 9](PyTorch-Autograd#Code-9)에서 볼 수 있는 것처럼 Parameter(Weight)가 Share되면서 Gradient가 여러번 중복해서 더해집니다. 여기서는 두 번 중복해서 사용해서 Gradient가 두 배가 되었는데, 결과를 (z1 + z2) / 2와 같이 2로 나누어 줘서 결국 Parameter에 전달되는 Gradient가 [Parameter Code 3](#Parameter-Code-3)과 같아집니다.

### Parameter Code 5 {#Parameter-Code-5}

```python
import torch

class PowModel(torch.nn.Module):

  def __init__(self):
    super(PowModel, self).__init__()
    self.powParam = torch.nn.Parameter(torch.tensor(1.0))

  def forward(self, x, q):
    return self.powParam * x ** q

class LogModel(torch.nn.Module):

  def __init__(self):
    super(LogModel, self).__init__()
    self.logParam = torch.nn.Parameter(torch.tensor(1.0))

  def forward(self, x):
    return self.logParam * torch.log(x)

class PowLogModel(torch.nn.Module):

  def __init__(self):
    super(PowLogModel, self).__init__()
    self.powModel1 = PowModel()
    self.logModel1 = LogModel()
    self.powModel2 = PowModel()
    self.logModel2 = LogModel()

  def forward(self, x, q):
    y1 = self.powModel1(x, q)
    z1 = self.logModel1(y1)
    y2 = self.powModel2(x, q)
    z2 = self.logModel2(y2)
    return (z1 + z2) / 2

powLogModel = PowLogModel()

z = powLogModel(5.0, 3.0)
print('z', z)

learning_rate = 0.01
for i in range(10):
  powLogModel.zero_grad()
  x = torch.tensor(5.0)
  q = torch.tensor(3.0)
  z = powLogModel(5.0, 3.0)
  target = 10.0
  loss = (z - target) ** 2
  loss.backward()
  with torch.no_grad():
    for name, parameter in powLogModel.named_parameters():
      parameter -= parameter.grad * learning_rate
      print(i, name, parameter.data)

z = powLogModel(5.0, 3.0)
print('z', z)
```

[Parameter Code 4](#Parameter-Code-4)에서 PowModel과 LogModel을 2개씩 생성하고 중복해서 사용하지 않습니다.

```
z tensor(4.8283, grad_fn=<DivBackward0>)
0 powModel1.powParam tensor(1.0517)
0 logModel1.logParam tensor(1.2497)
0 powModel2.powParam tensor(1.0517)
0 logModel2.logParam tensor(1.2497)
1 powModel1.powParam tensor(1.0981)
1 logModel1.logParam tensor(1.4401)
1 powModel2.powParam tensor(1.0981)
1 logModel2.logParam tensor(1.4401)
2 powModel1.powParam tensor(1.1363)
2 logModel1.logParam tensor(1.5834)
2 powModel2.powParam tensor(1.1363)
2 logModel2.logParam tensor(1.5834)
3 powModel1.powParam tensor(1.1663)
3 logModel1.logParam tensor(1.6901)
3 powModel2.powParam tensor(1.1663)
3 logModel2.logParam tensor(1.6901)
4 powModel1.powParam tensor(1.1892)
4 logModel1.logParam tensor(1.7688)
4 powModel2.powParam tensor(1.1892)
4 logModel2.logParam tensor(1.7688)
5 powModel1.powParam tensor(1.2063)
5 logModel1.logParam tensor(1.8265)
5 powModel2.powParam tensor(1.2063)
5 logModel2.logParam tensor(1.8265)
6 powModel1.powParam tensor(1.2190)
6 logModel1.logParam tensor(1.8685)
6 powModel2.powParam tensor(1.2190)
6 logModel2.logParam tensor(1.8685)
7 powModel1.powParam tensor(1.2283)
7 logModel1.logParam tensor(1.8991)
7 powModel2.powParam tensor(1.2283)
7 logModel2.logParam tensor(1.8991)
8 powModel1.powParam tensor(1.2351)
8 logModel1.logParam tensor(1.9213)
8 powModel2.powParam tensor(1.2351)
8 logModel2.logParam tensor(1.9213)
9 powModel1.powParam tensor(1.2401)
9 logModel1.logParam tensor(1.9373)
9 powModel2.powParam tensor(1.2401)
9 logModel2.logParam tensor(1.9373)
z tensor(9.7706, grad_fn=<DivBackward0>)
```

중복해서 사용하지 않았기 때문에 [Parameter Code 4](#Parameter-Code-4)에 비해서 Parameter 수가 2배가 되었습니다. 얼핏 보기에 [Parameter Code 4](#Parameter-Code-4)와 동일한 결과를 보일 것 같지만 Gradient가 중복으로 더해지지 않고 따로따로 분산되어서 Parameter에게 전달되기 때문에 [Parameter Code 4](#Parameter-Code-4)에 비해서 Parameter가 느리게 변합니다.

## Buffer {#Buffer}

Buffer는 Module에 저장해 놓고 사용하는 Tensor의 일종으로 학습을 통해 계산되지 않는 Tensor입니다.

### Buffer Code 1 {#Buffer-Code-1}

```python
import torch

class PowModel(torch.nn.Module):

  def __init__(self):
    super(PowModel, self).__init__()
    self.powParam = torch.nn.Parameter(torch.tensor(1.0))
    self.powBuff = torch.tensor(0.0)

  def forward(self, x, q):
    self.powBuff = self.powBuff * 0.6 + x * 0.4
    return self.powParam * self.powBuff ** q

class LogModel(torch.nn.Module):

  def __init__(self):
    super(LogModel, self).__init__()
    self.logParam = torch.nn.Parameter(torch.tensor(1.0))
    self.logBuff = torch.tensor(0.0)

  def forward(self, x):
    self.logBuff = self.logBuff * 0.6 + x * 0.4
    return self.logParam * torch.log(self.logBuff)

class PowLogModel(torch.nn.Module):

  def __init__(self):
    super(PowLogModel, self).__init__()
    self.powModel = PowModel()
    self.logModel = LogModel()

  def forward(self, x, q):
    y = self.powModel(x, q)
    z = self.logModel(y)
    return z

powLogModel = PowLogModel()

for i in range(10):
  z = powLogModel(5.0, 3.0)
  print(i, 'z', z)
  print(i, 'powBuff', powLogModel.powModel.powBuff)
  print(i, 'logBuff', powLogModel.logModel.logBuff)

print('state', powLogModel.state_dict())
```

[Parameter Code 1](#Parameter-Code-1)에서 powModel.forward(), logModel.forward()에서 x를 직접 사용하지 않고 지금까지의 x값을 Exponential Average한 값을 사용합니다.

```
0 z tensor(1.1632, grad_fn=<MulBackward0>)
0 powBuff tensor(2.)
0 logBuff tensor(3.2000, grad_fn=<AddBackward0>)
1 z tensor(2.7099, grad_fn=<MulBackward0>)
1 powBuff tensor(3.2000)
1 logBuff tensor(15.0272, grad_fn=<AddBackward0>)
2 z tensor(3.4999, grad_fn=<MulBackward0>)
2 powBuff tensor(3.9200)
2 logBuff tensor(33.1108, grad_fn=<AddBackward0>)
3 z tensor(3.9672, grad_fn=<MulBackward0>)
3 powBuff tensor(4.3520)
3 logBuff tensor(52.8371, grad_fn=<AddBackward0>)
4 z tensor(4.2616, grad_fn=<MulBackward0>)
4 powBuff tensor(4.6112)
4 logBuff tensor(70.9218, grad_fn=<AddBackward0>)
5 z tensor(4.4529, grad_fn=<MulBackward0>)
5 powBuff tensor(4.7667)
5 logBuff tensor(85.8761, grad_fn=<AddBackward0>)
6 z tensor(4.5793, grad_fn=<MulBackward0>)
6 powBuff tensor(4.8600)
6 logBuff tensor(97.4431, grad_fn=<AddBackward0>)
7 z tensor(4.6633, grad_fn=<MulBackward0>)
7 powBuff tensor(4.9160)
7 logBuff tensor(105.9885, grad_fn=<AddBackward0>)
8 z tensor(4.7194, grad_fn=<MulBackward0>)
8 powBuff tensor(4.9496)
8 logBuff tensor(112.0966, grad_fn=<AddBackward0>)
9 z tensor(4.7567, grad_fn=<MulBackward0>)
9 powBuff tensor(4.9698)
9 logBuff tensor(116.3565, grad_fn=<AddBackward0>)
state OrderedDict([('powModel.powParam', tensor(1.)), ('logModel.logParam', tensor(1.))])
```

powModel.forward(), logModel.forward()에서 x를 Exponential Average한 값을 Tensor로 powModel.powBuff와 logModel.logBuff에 저장합니다. 이것은 학습을 통해서 계산하지 않기 때문에 Module의 Parameter로 추가하지 않습니다. 그래서 Parameter가 아닌 Tensor로 저장합니다. Tensor는 Default로 requires_grad가 False이기 때문에 Gradient도 계산되지 않습니다.

powLogModel에 같은 값을 10번을 넣어주면서 확인해 보면 powModel.powBuff와 logModel.logBuff가 각각 조금씩 변하고 출력값인 z값도 조금씩 변하는 것을 확인할 수 있습니다.

Module이 가지고 있는 State값들을 저장해 두었다가 나중에 다시 사용하고 싶은 경우가 있습니다. 이런 경우에는 일반적으로 Module.state_dict()를 호출해서 Module의 State Dictionary를 얻어서 이것을 저장해 뒀다가 나중에 다시 읽어와서 사용합니다. 그런데 여기서는 powLogModel을 구성하고 있는 State중에 Parameter인 powModel.powParam와 logModel.logParam는 정상적으로 얻어지지만, powLogModel을 구성하고 있는 State중에 Buffer인 powModel.powBuff와 logModel.logBuff는 powLogModel.state_dict()를 호출해도 얻어지지 않는 것을 확인할 수 있습니다.

Module의 State를 저장해 두었다가 나중에 다시 사용하기 위해서는 Module내부의 Module, Parameter, Buffer와 같은 State를 구성하는 요소들을 빠뜨리지 말고 모두 적절하게 등록해 주어야 합니다.

### Buffer Code 2 {#Buffer-Code-2}

```python
import torch

class PowModel(torch.nn.Module):

  def __init__(self):
    super(PowModel, self).__init__()
    self.powParam = torch.nn.Parameter(torch.tensor(1.0))
    self.register_buffer('powBuff', torch.tensor(0.0))

  def forward(self, x, q):
    self.powBuff = self.powBuff * 0.6 + x * 0.4
    return self.powParam * self.powBuff ** q

class LogModel(torch.nn.Module):

  def __init__(self):
    super(LogModel, self).__init__()
    self.logParam = torch.nn.Parameter(torch.tensor(1.0))
    self.register_buffer('logBuff', torch.tensor(0.0))

  def forward(self, x):
    self.logBuff = self.logBuff * 0.6 + x * 0.4
    return self.logParam * torch.log(self.logBuff)

class PowLogModel(torch.nn.Module):

  def __init__(self):
    super(PowLogModel, self).__init__()
    self.powModel = PowModel()
    self.logModel = LogModel()

  def forward(self, x, q):
    y = self.powModel(x, q)
    z = self.logModel(y)
    return z

powLogModel = PowLogModel()

for i in range(10):
  z = powLogModel(5.0, 3.0)
  print(i, 'z', z)
  print(i, 'powBuff', powLogModel.powModel.powBuff)
  print(i, 'logBuff', powLogModel.logModel.logBuff)

print('state', powLogModel.state_dict())
print('parameters', list(powLogModel.named_parameters()))
print('buffers', list(powLogModel.named_buffers()))
```

[Buffer Code 1](#Buffer-Code-1)에서 Buffer를 만들고 만든 Buffer를 register_buffer()를 호출해서 Module에 등록합니다.

```
0 z tensor(1.1632, grad_fn=<MulBackward0>)
0 powBuff tensor(2.)
0 logBuff tensor(3.2000, grad_fn=<AddBackward0>)
1 z tensor(2.7099, grad_fn=<MulBackward0>)
1 powBuff tensor(3.2000)
1 logBuff tensor(15.0272, grad_fn=<AddBackward0>)
2 z tensor(3.4999, grad_fn=<MulBackward0>)
2 powBuff tensor(3.9200)
2 logBuff tensor(33.1108, grad_fn=<AddBackward0>)
3 z tensor(3.9672, grad_fn=<MulBackward0>)
3 powBuff tensor(4.3520)
3 logBuff tensor(52.8371, grad_fn=<AddBackward0>)
4 z tensor(4.2616, grad_fn=<MulBackward0>)
4 powBuff tensor(4.6112)
4 logBuff tensor(70.9218, grad_fn=<AddBackward0>)
5 z tensor(4.4529, grad_fn=<MulBackward0>)
5 powBuff tensor(4.7667)
5 logBuff tensor(85.8761, grad_fn=<AddBackward0>)
6 z tensor(4.5793, grad_fn=<MulBackward0>)
6 powBuff tensor(4.8600)
6 logBuff tensor(97.4431, grad_fn=<AddBackward0>)
7 z tensor(4.6633, grad_fn=<MulBackward0>)
7 powBuff tensor(4.9160)
7 logBuff tensor(105.9885, grad_fn=<AddBackward0>)
8 z tensor(4.7194, grad_fn=<MulBackward0>)
8 powBuff tensor(4.9496)
8 logBuff tensor(112.0966, grad_fn=<AddBackward0>)
9 z tensor(4.7567, grad_fn=<MulBackward0>)
9 powBuff tensor(4.9698)
9 logBuff tensor(116.3565, grad_fn=<AddBackward0>)
state OrderedDict([('powModel.powParam', tensor(1.)), ('powModel.powBuff', tensor(4.9698)), ('logModel.logParam', tensor(1.)), ('logModel.logBuff', tensor(116.3565))])
parameters [('powModel.powParam', Parameter containing:
tensor(1., requires_grad=True)), ('logModel.logParam', Parameter containing:
tensor(1., requires_grad=True))]
buffers [('powModel.powBuff', tensor(4.9698)), ('logModel.logBuff', tensor(116.3565, grad_fn=<AddBackward0>))]
```

[Buffer Code 1](#Buffer-Code-1)에서는 register_buffer()를 호출하지 않아서 powLogModel.state_dict()를 호출했을 때 powModel.powBuff과 logModel.logBuff가 보이지 않았지만, 여기에서는 register_buffer()를 호출했기 때문에 powLogModel.state_dict()를 호출했을 때 powModel.powBuff과 logModel.logBuff을 볼 수 있습니다. 이 State Dictionary를 저장해 두면 나중에 powLogModel을 복원할 때 사용할 수 있습니다.

Parameter와 Buffer를 따로따로 분리해서 보고 싶으면, powLogModel.named_parameters()와 powLogModel.named_buffers()를 호출하여 살펴봅니다. 여기서는 Parameter는 powModel.powParam와 logModel.logParam이 있고, Buffer는 powModel.powBuff와 logModel.logBuff가 있는 것을 확인할 수 있습니다.

### Buffer Code 3 {#Buffer-Code-3}

```python
import torch

class PowModel(torch.nn.Module):

  def __init__(self):
    super(PowModel, self).__init__()
    self.powParam = torch.nn.Parameter(torch.tensor(1.0))
    self.register_buffer('powBuff', torch.tensor(0.0))

  def forward(self, x, q):
    if self.training:
      self.powBuff = self.powBuff * 0.6 + x * 0.4
    return self.powParam * self.powBuff ** q

class LogModel(torch.nn.Module):

  def __init__(self):
    super(LogModel, self).__init__()
    self.logParam = torch.nn.Parameter(torch.tensor(1.0))
    self.register_buffer('logBuff', torch.tensor(0.0))

  def forward(self, x):
    if self.training:
      self.logBuff = self.logBuff * 0.6 + x * 0.4
    return self.logParam * torch.log(self.logBuff)

class PowLogModel(torch.nn.Module):

  def __init__(self):
    super(PowLogModel, self).__init__()
    self.powModel = PowModel()
    self.logModel = LogModel()

  def forward(self, x, q):
    y = self.powModel(x, q)
    z = self.logModel(y)
    return z

powLogModel = PowLogModel()

powLogModel.train()
for i in range(10):
  z = powLogModel(5.0, 3.0)
  print(i, 'z', z)
  print(i, 'powBuff', powLogModel.powModel.powBuff)
  print(i, 'logBuff', powLogModel.logModel.logBuff)

powLogModel.eval()
for i in range(10):
  z = powLogModel(5.0, 3.0)
  print(i, 'z', z)
  print(i, 'powBuff', powLogModel.powModel.powBuff)
  print(i, 'logBuff', powLogModel.logModel.logBuff)

print('state', powLogModel.state_dict())
print('parameters', list(powLogModel.named_parameters()))
print('buffers', list(powLogModel.named_buffers()))
```

[Buffer Code 2](#Buffer-Code-2)에서 Train Mode와 Evaluation Mode를 따로 구현합니다.

```
0 z tensor(1.1632, grad_fn=<MulBackward0>)
0 powBuff tensor(2.)
0 logBuff tensor(3.2000, grad_fn=<AddBackward0>)
1 z tensor(2.7099, grad_fn=<MulBackward0>)
1 powBuff tensor(3.2000)
1 logBuff tensor(15.0272, grad_fn=<AddBackward0>)
2 z tensor(3.4999, grad_fn=<MulBackward0>)
2 powBuff tensor(3.9200)
2 logBuff tensor(33.1108, grad_fn=<AddBackward0>)
3 z tensor(3.9672, grad_fn=<MulBackward0>)
3 powBuff tensor(4.3520)
3 logBuff tensor(52.8371, grad_fn=<AddBackward0>)
4 z tensor(4.2616, grad_fn=<MulBackward0>)
4 powBuff tensor(4.6112)
4 logBuff tensor(70.9218, grad_fn=<AddBackward0>)
5 z tensor(4.4529, grad_fn=<MulBackward0>)
5 powBuff tensor(4.7667)
5 logBuff tensor(85.8761, grad_fn=<AddBackward0>)
6 z tensor(4.5793, grad_fn=<MulBackward0>)
6 powBuff tensor(4.8600)
6 logBuff tensor(97.4431, grad_fn=<AddBackward0>)
7 z tensor(4.6633, grad_fn=<MulBackward0>)
7 powBuff tensor(4.9160)
7 logBuff tensor(105.9885, grad_fn=<AddBackward0>)
8 z tensor(4.7194, grad_fn=<MulBackward0>)
8 powBuff tensor(4.9496)
8 logBuff tensor(112.0966, grad_fn=<AddBackward0>)
9 z tensor(4.7567, grad_fn=<MulBackward0>)
9 powBuff tensor(4.9698)
9 logBuff tensor(116.3565, grad_fn=<AddBackward0>)
0 z tensor(4.7567, grad_fn=<MulBackward0>)
0 powBuff tensor(4.9698)
0 logBuff tensor(116.3565, grad_fn=<AddBackward0>)
1 z tensor(4.7567, grad_fn=<MulBackward0>)
1 powBuff tensor(4.9698)
1 logBuff tensor(116.3565, grad_fn=<AddBackward0>)
2 z tensor(4.7567, grad_fn=<MulBackward0>)
2 powBuff tensor(4.9698)
2 logBuff tensor(116.3565, grad_fn=<AddBackward0>)
3 z tensor(4.7567, grad_fn=<MulBackward0>)
3 powBuff tensor(4.9698)
3 logBuff tensor(116.3565, grad_fn=<AddBackward0>)
4 z tensor(4.7567, grad_fn=<MulBackward0>)
4 powBuff tensor(4.9698)
4 logBuff tensor(116.3565, grad_fn=<AddBackward0>)
5 z tensor(4.7567, grad_fn=<MulBackward0>)
5 powBuff tensor(4.9698)
5 logBuff tensor(116.3565, grad_fn=<AddBackward0>)
6 z tensor(4.7567, grad_fn=<MulBackward0>)
6 powBuff tensor(4.9698)
6 logBuff tensor(116.3565, grad_fn=<AddBackward0>)
7 z tensor(4.7567, grad_fn=<MulBackward0>)
7 powBuff tensor(4.9698)
7 logBuff tensor(116.3565, grad_fn=<AddBackward0>)
8 z tensor(4.7567, grad_fn=<MulBackward0>)
8 powBuff tensor(4.9698)
8 logBuff tensor(116.3565, grad_fn=<AddBackward0>)
9 z tensor(4.7567, grad_fn=<MulBackward0>)
9 powBuff tensor(4.9698)
9 logBuff tensor(116.3565, grad_fn=<AddBackward0>)
state OrderedDict([('powModel.powParam', tensor(1.)), ('powModel.powBuff', tensor(4.9698)), ('logModel.logParam', tensor(1.)), ('logModel.logBuff', tensor(116.3565))])
parameters [('powModel.powParam', Parameter containing:
tensor(1., requires_grad=True)), ('logModel.logParam', Parameter containing:
tensor(1., requires_grad=True))]
buffers [('powModel.powBuff', tensor(4.9698)), ('logModel.logBuff', tensor(116.3565, grad_fn=<AddBackward0>))]
```

Buffer의 값을 Train Mode에서만 갱신하고 Evaluation Mode에서는 변경하지 않고 고정해서 사용하고 싶은 경우가 있습니다. 이런 경우에는 powLogModel.train()을 호출하면(혹은 powLogModel.train(True)를 호출하면) Train Mode로 설정되고, powLogModel.eval()을 호출하면(혹은 powLogModel.train(False)를 호출하면) Evaluation Mode로 설정됩니다. Train Mode가 설정되면 Module의 training이 True로 설정되고, Evaluation Mode가 설정되면 Module의 training이 False로 설정됩니다. Module의 forward()에서는 training이 True일 때만 Buffer를 갱신하도록 하고 training이 False일 때는 Buffer를 갱신하지 않고 저장되어 있는 Buffer를 사용하도록 합니다.

Train Mode에서는 powLogModel에 동일한 입력값을 주어도 Buffer가 변하면서 출력값이 변하는 것을 볼 수 있으며, Evaluation Mode에서는 동일한 입력값을 주었을 때 Buffer와 출력값이 변하지 않는 것을 볼 수 있습니다.

Module은 생성했을 때 Default Mode는 Train Mode입니다.

참고로 PyTorch의 BatchNorm이 이와 유사한 방식으로 구현되어 있습니다.

## Hook {#Hook}

Module을 사용할 때 Module내부를 건드리지 않고 Module내부에서 forward나 backward에서 오가는 값을 관찰하거나 수정하고 싶을 때 Hook을 사용합니다.

### Hook Code 1 {#Hook-Code-1}

```python
import torch

class PowModel(torch.nn.Module):

  def __init__(self):
    super(PowModel, self).__init__()
    self.powParam = torch.nn.Parameter(torch.tensor(1.0))

  def forward(self, x, q):
    return self.powParam * x ** q

class LogModel(torch.nn.Module):

  def __init__(self):
    super(LogModel, self).__init__()
    self.logParam = torch.nn.Parameter(torch.tensor(1.0))

  def forward(self, x):
    return self.logParam * torch.log(x)

class PowLogModel(torch.nn.Module):

  def __init__(self):
    super(PowLogModel, self).__init__()
    self.powModel = PowModel()
    self.logModel = LogModel()

  def forward(self, x, q):
    y = self.powModel(x, q)
    z = self.logModel(y)
    return z

powLogModel = PowLogModel()

def forward_pre_hook(module, input):
  print('input', input)
  first_input, *rest_input = input
  return (first_input * 2, *rest_input)

hook = powLogModel.logModel.register_forward_pre_hook(forward_pre_hook)

x = torch.tensor(5.0, requires_grad=True)
q = torch.tensor(3.0, requires_grad=True)
z = powLogModel(x, q)
z.backward()

hook.remove()

print('x', x)
print('x.grad', x.grad)
print('q', q)
print('q.grad', q.grad)
print('z', z)

for name, parameter in powLogModel.named_parameters():
  print(name, f'data({parameter.data}), grad({parameter.grad})')
```

[Parameter Code 1](#Parameter-Code-1)에서 logModel에 register_forward_pre_hook()을 호출해서 logModel에 forward연산이 이루어지기 직전에 input을 확인하고 해당 input에 2를 곱해서 input을 수정합니다. forward에 input으로 여러개가 전달될 수도 있기 때문에 input은 Tuple형태로 전달되는 것에 주의합니다.

```
input (tensor(125., grad_fn=<MulBackward0>),)
x tensor(5., requires_grad=True)
x.grad tensor(0.6000)
q tensor(3., requires_grad=True)
q.grad tensor(1.6094)
z tensor(5.5215, grad_fn=<MulBackward0>)
powModel.powParam data(1.0), grad(1.0)
logModel.logParam data(1.0), grad(5.521461009979248)
```

[Parameter Code 1](#Parameter-Code-1)에서는 $z = \ln(125) \approx 4.83$이었지만, 여기서는 register_forward_pre_hook()을 호출하여 logModel의 forward의 input에 2를 곱해줘서 $z = \ln(125 * 2) \approx 5.52$로 변경되었습니다.

### Hook Code 2 {#Hook-Code-2}

```python
import torch

class PowModel(torch.nn.Module):

  def __init__(self):
    super(PowModel, self).__init__()
    self.powParam = torch.nn.Parameter(torch.tensor(1.0))

  def forward(self, x, q):
    return self.powParam * x ** q

class LogModel(torch.nn.Module):

  def __init__(self):
    super(LogModel, self).__init__()
    self.logParam = torch.nn.Parameter(torch.tensor(1.0))

  def forward(self, x):
    return self.logParam * torch.log(x)

class PowLogModel(torch.nn.Module):

  def __init__(self):
    super(PowLogModel, self).__init__()
    self.powModel = PowModel()
    self.logModel = LogModel()

  def forward(self, x, q):
    y = self.powModel(x, q)
    z = self.logModel(y)
    return z

powLogModel = PowLogModel()

def forward_hook(module, input, output):
  print('input', input)
  print('output', output)
  return output * 2

hook = powLogModel.logModel.register_forward_hook(forward_hook)

x = torch.tensor(5.0, requires_grad=True)
q = torch.tensor(3.0, requires_grad=True)
z = powLogModel(x, q)
z.backward()

hook.remove()

print('x', x)
print('x.grad', x.grad)
print('q', q)
print('q.grad', q.grad)
print('z', z)

for name, parameter in powLogModel.named_parameters():
  print(name, f'data({parameter.data}), grad({parameter.grad})')
```

[Hook Code 1](#Hook-Code-1)에서 register_forward_pre_hook()대신에 register_forward_hook()을 호출해서 logModel에 forward연산이 이루어진 직후의 input과 output을 확인하고 해당 output에 2를 곱해서 output을 수정합니다.

```
input (tensor(125., grad_fn=<MulBackward0>),)
output tensor(4.8283, grad_fn=<MulBackward0>)
x tensor(5., requires_grad=True)
x.grad tensor(1.2000)
q tensor(3., requires_grad=True)
q.grad tensor(3.2189)
z tensor(9.6566, grad_fn=<MulBackward0>)
powModel.powParam data(1.0), grad(2.0)
logModel.logParam data(1.0), grad(9.656627655029297)
```

[Hook Code 1](#Hook-Code-1)에서는 $z = \ln(125) \approx 4.83$이었지만, 여기서는 register_forward_hook()을 호출하여 logModel의 forward의 output에 2를 곱해줘서 $z = 2\ln(125) \approx 9.66$으로 변경되었습니다.

### Hook Code 3 {#Hook-Code-3}

```python
import torch

class PowModel(torch.nn.Module):

  def __init__(self):
    super(PowModel, self).__init__()
    self.powParam = torch.nn.Parameter(torch.tensor(1.0))

  def forward(self, x, q):
    return self.powParam * x ** q

class LogModel(torch.nn.Module):

  def __init__(self):
    super(LogModel, self).__init__()
    self.logParam = torch.nn.Parameter(torch.tensor(1.0))

  def forward(self, x):
    return self.logParam * torch.log(x)

class PowLogModel(torch.nn.Module):

  def __init__(self):
    super(PowLogModel, self).__init__()
    self.powModel = PowModel()
    self.logModel = LogModel()

  def forward(self, x, q):
    y = self.powModel(x, q)
    z = self.logModel(y)
    return z

powLogModel = PowLogModel()

def backward_hook(module, grad_input, grad_output):
  print('grad_input', grad_input)
  print('grad_output', grad_output)
  return grad_input

hook = powLogModel.powModel.register_backward_hook(backward_hook)

x = torch.tensor(5.0, requires_grad=True)
q = torch.tensor(3.0, requires_grad=True)
z = powLogModel(x, q)
z.backward()

hook.remove()

print('x', x)
print('x.grad', x.grad)
print('q', q)
print('q.grad', q.grad)
print('z', z)

for name, parameter in powLogModel.named_parameters():
  print(name, f'data({parameter.data}), grad({parameter.grad})')
```

[Parameter Code 1](#Parameter-Code-1)에서 powModel에 register_backward_hook()을 호출해서 powModel에 backward연산이 이루어진 직후에 grad_input과 grad_output을 확인합니다.

```
grad_input (tensor(1.), tensor(0.0080))
grad_output (tensor(0.0080),)
x tensor(5., requires_grad=True)
x.grad tensor(0.6000)
q tensor(3., requires_grad=True)
q.grad tensor(1.6094)
z tensor(4.8283, grad_fn=<MulBackward0>)
powModel.powParam data(1.0), grad(1.0)
logModel.logParam data(1.0), grad(4.828313827514648)
```

grad_input과 grad_output에 대한 내용은 [PyTorch Autograd Code 11](PyTorch-Autograd#Code-11)을 참조합니다. register_backward_hook()을 이용해서 새 grad_input을 return해 주면 grad_input을 변경하는 것이 가능합니다. 하지만 grad_input의 의미를 파악하는 것이 쉽지가 않기 때문에 Debug용도 외에는 실용성이 떨어집니다. 상식적으로 생각해 보았을 때 [PyTorch Autograd Code 11](PyTorch-Autograd#Code-11)과 마찬가지로 grad_input의 값은 $\frac{\partial z}{\partial x}=0.6$, $\frac{\partial z}{\partial q} \approx 1.61$이 되어야 할 것으로 보입니다. 하지만 실제 grad_input의 값이 $1.0$, $0.008$입니다. 이것은 forward연산 내부의 최종 연산의 input들의 Gradient입니다. 즉, grad_input은 self.powParam * x ** q에서 self.powParam.grad = 1.0, (x ** q).grad = 0.008이 됩니다. 이렇게 register_backward_hook()의 grad_input이 작동하기 때문에, register_backward_hook()을 사용해서 grad_input값을 수정하는 Code를 작성하게 되면, forward연산이 약간이라도 수정되었을 때 해당 Code가 정상적으로 작동하지 않게 됩니다. 예를 들어 PowModel.forward()의 구현을 self.powParam * x ** q에서 x ** q * self.powParam로 변경하게 되면 grad_input의 값이 $1.0$, $0.008$에서 $0.008$, $1.0$으로 변경됩니다. 이런 이유로 register_backward_hook()을 이용해서 grad_input은 값을 Debug용도로 확인하거나 수정하는 것은 적절하지만, 그 외의 용도로 사용할 때는 상당한 주의가 필요합니다.

## Functional {#Functional}

torch.nn.functional에서 찾을 수 있는 각종 Function들은 torch.nn에서 찾을 수 있는 각종 Module들을 구현할 때 사용됩니다.

### Functional Code 1 {#Functional-Code-1}

```python
import torch

class LinearModel(torch.nn.Module):

  def __init__(self):
    super(LinearModel, self).__init__()
    self.linearModel = torch.nn.Linear(
        in_features=1, out_features=1, bias=False)
    self.linearModel.weight.data.fill_(2.0)

  def forward(self, x):
    return self.linearModel(x.expand(1, 1, 1)).squeeze()

linearModel = LinearModel()
z = linearModel(torch.tensor(3.0))
print('z', z)
```

torch.nn.Linear Module을 사용해서 간단하게 곱하기 연산을 구현합니다. linearModel의 weight(Parameter)는 2.0으로 초기화합니다. Dimension을 맞춰주기 위해 적절하게 expand()와 squeeze()를 호출합니다.

```
z tensor(6., grad_fn=<SqueezeBackward0>)
```

LinearModel.linearModel 내부에는 Parameter를 한 개 가지고 있으며 이 Parameter는 2.0의 값을 가집니다. 그래서 linearModel에 3.0을 입력해 주었을 때 실행 결과는 2.0 * 3.0 = 6.0이 됩니다.

### Functional Code 2 {#Functional-Code-2}

```python
import torch

class LinearModel(torch.nn.Module):

  def __init__(self):
    super(LinearModel, self).__init__()
    self.linearParams = torch.nn.Parameter(torch.tensor([[2.0]]))

  def forward(self, x):
    return torch.nn.functional.linear(
        x.expand(1, 1, 1), self.linearParams).squeeze()

linearModel = LinearModel()
z = linearModel(torch.tensor(3.0))
print('z', z)
```

[Functional Code 1](#Functional-Code-1)에서 torch.nn.Linear대신에 torch.nn.functional.linear를 사용해서 동일한 기능을 구현합니다.

```
z tensor(6., grad_fn=<SqueezeBackward0>)
```

torch.nn.Linear Module대신에 torch.nn.functional.linear Function을 사용하기 위해서는 torch.nn.Linear Module이 가지고 있는 Parameter를 직접 제공해 주어야 합니다. 그래서 torch.nn.Parameter을 사용해서 linearModel.linearParams을 설정해 주고 이것을 torch.nn.functional.linear에 넘겨줍니다. 실제로 torch.nn.Linear의 내부 구현을 보면 torch.nn.functional.linear을 사용해서 구현되어 있습니다.

torch.nn.Linear Module과 같이 내부에 State를 가지는 경우에는, torch.nn.functional.linear Function을 사용해서 동일한 기능을 구현하기 위해서는, torch.nn.Parameter등을 사용해서 State를 직접 제공해 주어야 되기 때문에, Function을 사용하게 되면 사용이 다소 번거로워집니다.

### Functional Code 3 {#Functional-Code-3}

```python
import torch

class ReLUModel(torch.nn.Module):

  def __init__(self):
    super(ReLUModel, self).__init__()
    self.reLUModel = torch.nn.ReLU()

  def forward(self, x):
    return self.reLUModel(x)

reLUModel = ReLUModel()

z = reLUModel(torch.tensor(3.0))
print('z', z)

z = reLUModel(torch.tensor(-1.0))
print('z', z)
```

torch.nn.ReLU Module을 사용해서 ReLU연산을 구현합니다.

```
z tensor(3.)
z tensor(0.)
```

ReLU연산이 정상적으로 작동합니다.

### Functional Code 4 {#Functional-Code-4}

```python
import torch

class ReLUModel(torch.nn.Module):

  def __init__(self):
    super(ReLUModel, self).__init__()

  def forward(self, x):
    return torch.nn.functional.relu(x)

reLUModel = ReLUModel()

z = reLUModel(torch.tensor(3.0))
print('z', z)

z = reLUModel(torch.tensor(-1.0))
print('z', z)
```

[Functional Code 3](#Functional-Code-3)에서 torch.nn.ReLU대신에 torch.nn.functional.relu를 사용해서 동일한 기능을 구현합니다.

```
z tensor(3.)
z tensor(0.)
```

torch.nn.ReLU Module은 State를 가지고 있지 않은 Module입니다. 이런 경우에는 torch.nn.functional.relu Function을 사용하더라도 State를 따로 제공해 주지 않아도 됩니다. 오히려 torch.nn.ReLU Module을 사용하게 되면 reLUModel.reLUModel에 torch.nn.ReLU Module의 Instance를 저장해 두고 사용해야 하지만, torch.nn.functional.relu Function을 사용하게 되면 그런 번거로운 작업이 필요가 없습니다. 그래서 State를 가지고 있지 않은 torch.nn.ReLU Module과 같은 경우에는 torch.nn.functional.relu Function을 사용하는 것이 더 편합니다.

### Functional Code 5 {#Functional-Code-5}

```python
import torch

class DropoutModel(torch.nn.Module):

  def __init__(self):
    super(DropoutModel, self).__init__()
    self.dropoutModel = torch.nn.Dropout(0.5)

  def forward(self, x):
    return self.dropoutModel(x)

dropoutModel = DropoutModel()

print('train mode')
dropoutModel.train(True)
for i in range(5):
  print(i, dropoutModel(torch.tensor(1.0)))

print('eval mode')
dropoutModel.train(False)
for i in range(5):
  print(i, dropoutModel(torch.tensor(1.0)))
```

torch.nn.Dropout Module을 사용해서 Dropout을 구현합니다. Dropout은 50%의 확률로(0.5) 발생합니다.

```
train mode
0 tensor(2.)
1 tensor(0.)
2 tensor(2.)
3 tensor(0.)
4 tensor(2.)
eval mode
0 tensor(1.)
1 tensor(1.)
2 tensor(1.)
3 tensor(1.)
4 tensor(1.)
```

Dropout Module은 Train Mode에서는 Random하게 Dropout이 발생하지만 Evaluation Mode에서는 Dropout이 발생하지 않습니다.

### Functional Code 6 {#Functional-Code-6}

```python
import torch

class DropoutModel(torch.nn.Module):

  def __init__(self):
    super(DropoutModel, self).__init__()

  def forward(self, x):
    return torch.nn.functional.dropout(x, p=0.5, training=self.training)

dropoutModel = DropoutModel()

print('train mode')
dropoutModel.train(True)
for i in range(5):
  print(i, dropoutModel(torch.tensor(1.0)))

print('eval mode')
dropoutModel.train(False)
for i in range(5):
  print(i, dropoutModel(torch.tensor(1.0)))
```

[Functional Code 5](#Functional-Code-5)에서 torch.nn.Dropout대신에 torch.nn.functional.dropout를 사용해서 동일한 기능을 구현합니다.

```
train mode
0 tensor(2.)
1 tensor(0.)
2 tensor(2.)
3 tensor(0.)
4 tensor(0.)
eval mode
0 tensor(1.)
1 tensor(1.)
2 tensor(1.)
3 tensor(1.)
4 tensor(1.)
```

torch.nn.Dropout Module의 경우에는 내부에 Parameter도 없고 Buffer도 없기 때문에 torch.nn.functional.dropout을 사용하는 것이 간편하다고 생각할 수 있습니다. 하지만 torch.nn.functional.dropout을 살펴보면 주의가 필요하다는 것을 알 수 있습니다. p와 training을 넘겨줘야 되고 이것을 잘못 넘겨주거나 빠뜨리게 되면 의도치 않은 결과가 발생할 수 있습니다.

Module의 경우에 State가 없는 경우에 Function을 쓰는 것이 더 간편하지만, Module의 State는 Parameter와 Buffer만 있는 것이 아니기 때문에 주의가 필요합니다.

## Conclusion {#Conclusion}

PyTorch의 Module을 조금 깊게 살펴보았습니다. 지금까지 살펴본 내용을 요약하면 다음과 같습니다.

* Module은 Container로 다른 Module, Parameter, Buffer를 포함(등록)할 수 있습니다. 포함하는 것의 많은 부분이 자동으로 이루어져서 있어서 아무런 신경을 쓰지 않고 자유롭게 사용하는 경향이 있는데, 그러다 보면 포함을 하도록 구성했다고 생각했는데 실제로는 포함되지 않게 구성되기도 합니다. 의도한 대로 Module이 제대로 구성되지 않게 되면 Module.parameters()가 필요한 Parameter를 return하지 않아서 학습이 제대로 이루어지지 않거나, Module.state_dict()가 필요한 State를 return하지 않아서 Module이 제대로 저장이 되지 않기도 합니다. 그래서 Module은 편하게 사용하더라도 의도한 대로 Module, Parameter, Buffer가 잘 포함되도록 주의를 해서 사용해야 합니다.

* 학습에 사용되는 Tensor는 Parameter로 Module에 등록해 주고, 학습에 사용하지 않지만 Module을 저장할 때 State로 함께 저장해야 될 필요가 있는 Tensor는 Buffer로 Module에 등록해 줍니다.

* Module을 사용할 때 Module내부를 건드리지 않고 Module내부에서 forward나 backward에서 오가는 값을 관찰하거나 수정하고 싶을 때 Hook을 사용하면 편합니다. forward가 실행되기 직전, forward가 실행된 직후, backward가 실행된 직후의 값들을 Hook을 사용하여 관찰하거나 수정할 수 있습니다.

* torch.nn에 있는 각종 기능을 하는 Module들은 torch.nn.functional에 그와 유사한 Function들이 있습니다. 일반적으로는 State를 가지고 있는 경우에는 Module을 사용하는 것이 간편하고 State를 가지고 있지 않은 경우에는 Function을 사용하는 것이 간편합니다. 하지만 Module에서 State는 Parameter나 Buffer만을 의미하는 것은 아니기 때문에 주의가 필요합니다.

PyTorch의 Module은 단순해 보이는 듯 하면서도 눈에 잘 보이지 않는 미묘한 기능들을 가지고 있습니다. 이 글을 통해 PyTorch의 Module에 대해 조금이라도 더 깊게 이해하는데 도움이 되었기를 바랍니다.
