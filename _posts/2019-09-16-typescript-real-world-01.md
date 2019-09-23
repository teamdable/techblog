---
layout: post
title:  "TypeScript in the real world - 01"
date:   2019-09-20 11:00:00 +0900
author: MinJeong Kim
tags: [ minjeongkim, typescript, programming ]
---

안녕하세요, 데이터 플랫폼 소프트웨어 엔지니어 김민정입니다. 데이블에서는 주로 `Node.js`로 서버를 개발하고 있는데 이번 연도부터 `TypeScript`를 적극적으로 도입하고 있습니다. 이 시리즈 글에서는 개발하면서 유용했던 타입스크립트 기능들을 소개해드리려고 합니다.

# Decorator

오늘 소개해 드릴 것은 TypeScript의 `데코레이터(decorator)`입니다. 원래 데코레이터는 디자인 패턴 중의 하나인데, 타깃 오브젝트를 감싸서 타깃 오브젝트에 새로운 기능을 추가하는 패턴입니다. Java, Python 등 고급 프로그래밍 언어 단에서 보편적으로 지원하는 구문입니다. 현재 JavaScript 에는 [stage 2 제안](https://github.com/tc39/proposal-decorators)으로 올라와 있고 TypeScript 에서는 `experimentalDecorators` 라는 컴파일러 옵션을 키면 사용 가능합니다. 좀 더 상세한 방법은 [공식 문서](https://www.typescriptlang.org/docs/handbook/decorators.html)에 올라와 있습니다.


실사용 예제를 들어보겠습니다.

```javascript
function doSomething() {
    if (condition1) {
        someFunctionMustCallBeforeReturn();
        return;
    }
    
    ....
    
    if (condition2) {
        someFunctionMustCallBeforeReturn();
        return;
    }
    
    someFunctionMustCallBeforeReturn();
    return;
}
```


`doSomething` 함수가 return 하기 전에 반드시 불러야 하는 함수(`someFunctionMustCallBeforeReturn`)가 있습니다. 테스트 코드를 완벽하게 짜놓거나 호출해야 하는 것을 잊어먹지 않는다면 버그를 막을 수 있겠지만, 알다시피 human error는 항상 발생합니다.

이때 데코레이터로 함수에 대한 후처리를 달 수 있습니다.


```javascript
function postTask(target: object, propertyKey: string, descriptor: PropertyDescriptor): PropertyDescriptor {
    const method = descriptor.value; // doSomething 함수

    // doSomething 함수 실행 후 someFunctionMustCallBeforeReturn 호출하는 함수를 override
    descriptor.value = function (...args: any[]) {
        method.apply(this, args);
        
        someFunctionMustCallBeforeReturn();

        return;
    };
    return descriptor;
}

@postTask
function doSomething() {
    if (condition1) {
        return;
    }
    
    ....
    
    if (condition2) {
        return;
    }
    
    return;
}
```

훨씬 간결하고 명확해 보입니다. `target`, `propertyKey`, `descriptor`는 TypeScript 에서 넘겨주는 인자입니다. `descriptor.value`로 데코레이터가 달린 함수에 접근할 수 있습니다.

TypeScript를 사용하면서 자연스럽게 객체 지향적으로 개발을 하고 있는데 상속으로는 불편한 것들을 데코레이터로 처리하고 있습니다. 다음 편에서는 다른 내용으로 찾아뵙겠습니다.