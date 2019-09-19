---
layout: post
title:  "TypeScript in the real world - 02"
date:   2019-09-22 11:00:00 +0900
author: MinJeong Kim
tags: [ minjeongkim, typescript, programming ]
---

이번 편에서는 함수에서 받는 인자의 타입이 다양한 경우를 `Union`, `Generic`을 활용하여 처리하는 방법에 대해 설명하겠습니다.

# Union

Union은 TypeScript에서 지원하는 타입입니다. 데이터에 대한 타입을 정의할 때 한 개 이상의 타입으로 선언할 수 있게 합니다.

Union은 아래와 같은 문법으로 정의합니다.

```typescript
(type1 | type2 | type3 | .. | typeN)
```

예시를 하나 들어보겠습니다.

```typescript
function isNull(value: string | null): boolean {
  return !value;
}
```

`isNull` 함수에서 value 인자가 string 또는 null 타입으로 들어는 경우에 `string | null` 으로 Union 타입의 인자를 선언해 전달받습니다.

# Generic

Generic은 모듈이 다양한 타입을 지원하도록 재사용하게 만들어주는 고급 타입입니다. Java, C# 에서는 native로 지원하고 있습니다.

TypeScript 공식 문서에서 가져온 예시를 하나 들어보겠습니다.

```typescript
function identity<T>(arg: T): T {
    return arg;
}
```

`identity` 함수명 옆에 `<T>` 라고 표기가 되어있는데 이를 `타입 변수(type variable)`라고 합니다. 타입 변수로 받은 `T`가 `arg` 의 타입과 반환하는 값의 타입으로 전달됩니다.

Generic 함수의 호출 예시는 다음과 같습니다.

```typescript
let output = identity<string>("myString");  // type of output will be 'string'
```

타입 변수를 `string`으로 전달하여 반환 타입을 `string`으로 정의합니다.

# Union, Generic in the real world

Union 변수의 특정 타입에만 적용되는 로직을 작성해야할 때 컴파일 에러가 나는 예제를 Generic으로 해결해보겠습니다.

```typescript
function getUser(userData: EmailUser | FacebookUser): EmailUser | FacebookUser {
  ...

  return user;
}

function facebookUserLogic(userData: FacebookUser) {
  const user = getUser(userData);

  const email = getEmail(user.facebook_id); // Property 'facebook_id' does not exist on type 'EmailUser'.ts(2339)
  
  ...
}
```

`facebookUserLogic` 함수에서 `getUser` 함수를 호출하여 `user`를 받아와서 `facebook_id` property에 접근하니 `facebook_id`가 `EmailUser`에는 존재하지 않는다는 에러가 뜹니다. 이 경우에 [type guard](https://www.typescriptlang.org/docs/handbook/advanced-types.html#user-defined-type-guards)를 이용해서 타입을 좁혀줄 수도 있지만 다음과 같이 Generic으로 깔끔하게 해결할 수 있습니다.

```typescript
function getUser<T>(user: T): T {
  ...

  return user;
}

function facebookUserLogic(user: FacebookUser) {
  const user = getUser<FacebookUser>(user);

  const email = getEmail(user.facebook_id);
  
  ...
}
```

`getUser` 함수를 Generic 타입 변수를 받을 수 있게 하여 `FacebookUser` 로 타입을 넘기니 타입이 `FacebookUser`로 좁혀졌습니다. 이와 같이 Union과 Generic을 쓰면 깔끔하게 다양한 타입에 대해 처리할 수 있습니다.

TypeScript에서 타입을 정의할 때는 불편하더라도 `any` 타입을 쓰지말고 위와 같이 TypeScript의 고급 타입들과 유틸을 이용하여 최대한 명확하게 정의해놓으면 유지보수하기 편해지고 컴파일 타임에 버그를 방지할 수 있게 됩니다. 다음 편에서는 새로운 내용으로 또 찾아뵙겠습니다.

### 참고 문서
- [https://www.typescriptlang.org/docs/handbook/generics.html](https://www.typescriptlang.org/docs/handbook/generics.html)
- [https://www.typescriptlang.org/docs/handbook/advanced-types.html#union-types](https://www.typescriptlang.org/docs/handbook/advanced-types.html#union-types)
- [https://www.tutorialsteacher.com/typescript/typescript-union](https://www.tutorialsteacher.com/typescript/typescript-union)