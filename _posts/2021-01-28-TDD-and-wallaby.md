---
layout: post
title: "TDD로 개발 진행히보기. (feat. wallaby.js)"
date: 2021-01-27 15:00:00 +0900
author: changhyun lim
tags: [ 임창현, TDD, wallabyjs ]
---

## TDD?

TDD는 Test Driven Development 즉, 테스트 주도 개발을 뜻합니다.

매우 짧은 개발 사이클을 반복하는 소프트웨어 개발 방법론입니다.

테스트를 먼저 작성하고 그다음 실제 코드를 구현하는 형태로 개발이 진행하는 형식입니다.

**테스트 코드 작성 → 구현 코드 작성 → 리팩토링** 이 3가지를 짧은 주기를 반복하며 점증적으로 개발합니다.

## 일반적인 개발 프로세스

![일반적인 프로세스](/techblog/assets/images/TDD-and-Wallaby/process.png)

TDD를 시작하기 전에 저는 일반적으로 위와 같은 단계로 개발을 진행하였습니다.

**요구사항 분석 → 대략적인 설계 → 코드 작성 → 수동 테스트 OR 테스트 코드 작성** 이후 문제가 발생하면 발생한 부분의 코드를 확인하고 다시 코드를 수정하는 형태입니다.

위와 같이 작업을 하다 보니 다음과 같은 문제가 발생했습니다.

1. 이미 작성한 코드에 테스트를 추가하는 게 귀찮아서 **그냥 테스트 코드를 작성을 안하고 넘어갔다.**
2. 중요한 코드라 테스트 코드를 넣긴 해야 하는데... **코드(=함수)가 너무 비대해서 테스트를 넣는 게 어렵다.**
3. 몇 번의 수정을 거치고 나니 내가 처음에 **설계한 코드가 이미 너무 변질하여 있고, 불명확한 코드가 돼버렸다.** 이러다 보니 하나의 함수가 여러 가지 일을 하는 경우 발생함

## 테스트 주도 개발 프로세스

TDD도 크게 다르진 않습니다. 다만 테스트 작성이 코드 작성보다 먼저 이루어 진다는 것입니다.

**요구사항 분석 → 자세한 설계 → 테스트 작성 → 코드 작성 → 리팩토링** 이런 형태로 이루어집니다.

다만 **코드 작성 이전에 테스트를 먼저 작성한다는 게 가장 큰 차이점**입니다.

![tdd](/techblog/assets/images/TDD-and-Wallaby/tdd.png)

테스트 주도 개발 글이나 블로그를 보시다 보면 위와 같은 그림을 많이 볼 수 있는데요, 각각의 의미는 다음과 같습니다.

- RED: 실패하는 테스트 코드 작성하기
- GREEN: 테스트에 통과할 만한 작은 코드 작성하기
- REFACTOR: 코드를 조금 더 효율적으로 리팩토링하기
- 즉 **테스트 코드를 먼저 작성하고, 그다음 동작하는 코드를 작성한뒤 이 코드를 리팩토링하는 형태를 반복하는 것입니다.**

### 테스트 주도 개발을 하면 좋은 점

- 어떤 기능을 구현해야 하는지 쉽게 정리할 수 있다.
- 개발 사이클이 짧아진다.
- 리팩토링 및 유지보수가 편해진다.
- 디버깅 시간이 단축된다.
- 테스트 케이스가 문서를 대신 할 수 있다.
- 버그가 줄어든다.  (= 코드에 대한 자신감 상승)

## 테스트 주도 개발에 앞서서

일단 테스트 주도 개발을 하기 위해서는 **어떤 기능을 만들 것인지 확실하게 정의**해야 합니다. 해당 기능에 너무 많은 기능이 들어가 있으면 테스트 작성도 힘들어지며, 코드 작성도 까다로워 집니다. [SOLID 원칙](https://ko.wikipedia.org/wiki/SOLID_(%EA%B0%9D%EC%B2%B4_%EC%A7%80%ED%96%A5_%EC%84%A4%EA%B3%84))중 [단일책임원칙(Single Responsibility Principle)](https://ko.wikipedia.org/wiki/%EB%8B%A8%EC%9D%BC_%EC%B1%85%EC%9E%84_%EC%9B%90%EC%B9%99)을 마음에 새겨두고 작업하시는 것을 추천드립니다.

또한 **테스트 수행이 간편해야 합니다.** TDD는 코드를 작성하고 테스트를 돌리고, 다시 리팩토링을 한뒤 다시 실패하는 케이스를 넣고 코드를 넣는 등 짧은 호흡에 여러 번의 테스트를 수행합니다. 이러다보니 테스트를 돌리는 데 힘이 들면 TDD를 금방 포기해버리게 됩니다.

## 일단 테스트 주도 개발을 어떻게 하는지 알아봅시다. (feat. 저는 이렇게 했어요.)

**인터넷에 검색하면 수많은 예제가 나오지만, 대부분 간단한 계산기, API, 팩토리얼 구하는 간단한 기능이고, 저는 제가 어떻게 하였는지 경험담을 공유하고 싶어서 실제 개발한 내용으로 설명해 드립니다. 이러다 보니 보시는 분들이 아시는 실제 TDD와 다를 수 있습니다. 또한 작업하면서 작성한 문서가 아니라 작업한 내용을 되짚어가며 작성한 내용이라 실제 코드와는 약간의 차이가 있을 수 있습니다.**

어느 날 멘션이 왔는데... 다음과 같은 문제가 발생했다고 합니다.

![client가 정산 정보 삭제 메일을 받지 못했어요!](/techblog/assets/images/TDD-and-Wallaby/message1.jpg)

요약하자면 **Client 정산정보 삭제 버튼** 사용시 **Client**에게 메일이 발송되는데 사용자는 아직 삭제 메일을 못 받았다는 것입니다.

문제가 무엇인지 확인을 해보니.... **Client의 관리자가 등록되지 않은 상태**라서 메일을 받지 못한 상황이었습니다. 그래서 아무개님과 커뮤니케이션을 합니다.

![문제의 원인은 관리자가 등록이 안된것.](/techblog/assets/images/TDD-and-Wallaby/slack.jpg)

수정해야 할 부분이 정해졌습니다.

**정산 관리자가 없으면 등록된 지 가장 오래된 admin의 email로 발송하기.**

코드를 살펴보니 다음처럼 되어 있네요.

![기존 코드](/techblog/assets/images/TDD-and-Wallaby/code.png)
a
코드가 매우 단순합니다. **정산 담당자**를 조회한 뒤 이 **관리자의 email을 list**로 만들고 있습니다.

코드를 보아하니 이 **receiver** 변수에 메일만 잘 추가해주면 다른 곳은 수정할 필요가 없습니다.

이제부터 본격적인 TDD의 시작입니다. 목표는 **receiver list를 만들어 주는 함수**를 만들면 됩니다.

그러면 기본적인 빈 함수와 껍데기를 작성합니다.

### 1. 첫 실패 테스트 작성

```jsx
// test file
describe("Test getClientInfoModifyMailReceiver(), Client 변경 메일을 받을 email을 리턴한다.", () => {
  const topic = rewire('../../services/incomeServices');
  const getClientInfoModifyMailReceiver = topic.__get__('getClientInfoModifyMailReceiver');

  it("리스트를 리턴한다.", async() => {
    const result = getClientInfoModifyMailReceiver();
    result.should.eql([]);
    })
});
```

일단 테스트를 먼저 작성했습니다. 위 테스트는 틀림없이 `실패`합니다. 왜냐하면 테스트에 작성한 함수가 아직 안 만들어진 상태라서 그렇습니다.

이제 이 테스트에 성공하는 코드를 작성합니다.

### 2. 처음 테스트를 만족하는 코드 작성

```jsx
// code file
const getClientInfoModifyMailReceiver = () => {
  return [];
};
```

이렇게 작성하고 test를 돌리면 **성공**하게 됩니다. 다만 현재 함수는 빈 리스트만 돌려보내는 기능이 있을 뿐 아무런 기능이 없습니다.

### 3. 기존 기능 모듈화 하기 (실패하는 테스트 작성)

이제 원래 기능을 넣어줘야 합니다. 원래 기능이라 하면 **manager를 조회한 뒤 해당 manager의 email로 리스트를 만들어 돌려보내는 것입니다.**

여기서도 테스트를 먼저 작성합니다.

```jsx
// test.file
describe("Test getClientInfoModifyMailReceiver(), Client 변경 메일을 받을 email을 리턴한다.", () => {
  // describe를 중첩한 이유는 rewire로 함수를 mocking할때 __set__을 하면 다른 it 케이스서도
  // 함수가 overwrite되서 describe를 한번 더 해준 다음 테스트를 진행합니다.
  describe('manager가 있는 경우, manager의 email을 리턴한다.', () => {
    const topic = rewire('../../services/incomeServices');
    const getClientInfoModifyMailReceiver = topic.__get__('getClientInfoModifyMailReceiver');
    before(() => {
      // manager를 가져오는 함수를 DB에서 직접 가져오지 않고 mocking 합니다.
      // fetch_client_manager 함수는 이제 아래 데이터를 리턴합니다.
      topic.__set__({
        income_lib: {
          fetch_client_manager: () => Promise.resolve([
            { email: 'test@dable.io' },
            { email: 'test2@dable.io'}
          ])
        }
      });
    });

    it('manager가 있는 경우 manager의 email 리스트를 리턴한다.', async () => {
      const receiver = await getClientInfoModifyMailReceiver(1);

      receiver.should.eql(['test@dable.io', 'test2@dable.io']);
    });
  });
});
```

테스트 케이스를 작성했습니다. 하지만 테스트를 수행하면 이 테스트는 당연히 **실패**합니다.

왜냐하면 `getClientInfoModifyMailReceiver()` 함수는 여전히 `[]`만 돌려보내도록 되어 있거든요.

이제 이 코드를 만족할 수 있는 코드를 작성합니다.

### 4. 기존 모듈 테스트를 만족 하는 코드 작성

```jsx
// code file
const getClientInfoModifyMailReceiver = async(client_id) => {
  const managers = await income_lib.fetch_client_manager(client_id)
  const receiver = _.map(managers, (item) -> item.email)

  return receiver; 
};
```

이러면 기존 코드와 똑같이 동작하는 코드가 되었습니다. 다만 함수로 적출해서 앞으로는 **receiver**를 이 함수를 통해서 얻어 올 수 있게 되었습니다. 이제부터 다른 코드에서도 이 함수를 사용함으로써 **코드의 중복**을 방지할 수 있게 되었습니다.

테스트를 수행하면 어떻게 될까요.? 테스트에서 `income_lib.fetch_client_manager()` 함수가 특정 결괏값만을 돌려보내도록 **mocking**하였고, 이 **managers**를 통해서 **receiver**를 만듭니다. 실제로 데이터를 만드는 로직은 테스트가 완료되었습니다.

그런데 코드에서 조금 냄새가 납니다. 만약 **client_id**가 주어지지 않았다면 `fetch_client_manager()`에서 에러가 발생할 여지가 있습니다. 이 부분을 보완해주고 싶습니다.

다시 테스트를 작성해봅니다.

### 5. 에러 처리를 위한 테스트 작성

```jsx
// test file
describe("Test getClientInfoModifyMailReceiver(), Client 변경 메일을 받을 email을 리턴한다.", () => {
  describe('client_id에 null, undefined가 들어올 경우', () => {
    const topic = rewire('../../services/incomeServices');
    const getClientInfoModifyMailReceiver = topic.__get__('getClientInfoModifyMailReceiver');
    it('Case1. client_id에 undefined가 들어올 경우', async () => {
      const receiver = await getClientInfoModifyMailReceiver({ client_id: undefined });
      receiver.should.eql([]);
    });

    it('Case2. client_id에 null이 들어올 경우', async () => {
      const receiver = await getClientInfoModifyMailReceiver({ client_id: null });
      receiver.should.eql([]);
    });
  });

  describe('manager가 있는 경우, manager의 email을 리턴한다.', () => {
    // 생략
  });
});
```

만약 **client_id**에 **null**이나 **undefined** 같은 **nil값**이 들어올 경우 **throw**를 던져서 에러를 돌려보낼 수 도 있습니다.

하지만 이렇게 작성할 경우 기존 코드를 수정해야 합니다. (**try ~ catch로 감싸주는 등..**) 에러를 돌려보내는 것 대신 **빈 list**를 돌려보내도록 테스트를 작성했습니다.

이제 다시 코드를 작성합니다.

### 6. 에러처리 테스트를 만족하는 코드 작성

```jsx
// code file
const getClientInfoModifyMailReceiver = async(client_id) => {
  if (common_util.isNil(client_id)) // client_id가 0이 들어올수도 있어서 isNil로 체크한다.
    return [];

  const managers = await income_lib.fetch_client_manager(client_id);
  const receiver = _.map(managers, (item) -> item.email);

  return receiver; 
};
```

코드를 수정했습니다. **client_id**에 **nil**값이 들어와도 에러를 뱉지 않고 **[]**를 돌려보냅니다. 테스트도 **통과**하고 기존 코드를 수정할 필요도 없습니다.

여기까지가 **기존 코드를 함수로 빼면서 테스트도 추가한 작업**이 됩니다. 이제 기능 개발의 본격적인 시작이라는 의미입니다. -_-

여기까지 수정하는 데 오래 걸렸을까요.? 아니요. 얼마 안 걸렸어요. 기존 코드도 **재사용성을 높일 수 있도록 모듈화**되었고 **테스트도 추가되어 안전성이 높아졌습니다.** ( 제 기준!)

**TDD**를 한다고 시간이 되게 많이 소요된다는 것은 아니라고 말씀드리고 싶었습니다. 이제 기능을 추가해 봅시다.

### 7. 새로운 기능추가 테스트

```jsx
// test.js
describe("Test getClientInfoModifyMailReceiver(), Client 변경 메일을 받을 email을 리턴한다.", () => {
  describe('client_id에 null, undefined가 들어올 경우', () => {
    // 생략
  });

  describe('manager가 있는 경우, manager의 email을 리턴한다.', () => {
    // 생략
  });

  describe('manager가 없는 경우, 등록된지 가장 오래된 admin을 리턴한다.', () => {
    const topic = rewire('../../services/incomeServices');
    const getClientInfoModifyMailReceiver = topic.__get__('getClientInfoModifyMailReceiver');
    before(() => {
      topic.__set__({
        income_lib: {
          // manager가 없는 경우를 만들기 위해서 fetch_client_manager함수는
          // 무조건 []를 리턴하도록 mocking합니다.
          fetch_client_manager: () => Promise.resolve([])
        },
        client_lib: {
          // 관리자를 조회하는 경우도 DB에서 직접 가져오지는 않고 mocking한 데이터를 사용합니다. 
          fetch_email_list: () => Promise.resolve([
            { client_id: 1, email: 'test@dable.io', admin_name: 'test', reg_date: new Date('2020-10-01')},
            { client_id: 1, email: 'test2@dable.io', admin_name: 'test2', reg_date: new Date('2020-11-01')},
            { client_id: 1, email: 'test3@dable.io', admin_name: 'test3', reg_date: new Date('2020-01-01')},
          ])
        }
      });
    });

    it('manager가 없는 경우, 등록된지 가장 오래된 admin을 리턴한다.', async () => {
      const receiver = await getClientInfoModifyMailReceiver(1);

      receiver.should.eql(['test3@dable.io']);
    });
  });
});
```

요구사항에 맞게 테스트를 작성하였습니다.

manager가 없는 경우를 만들기 위해서 `fetch_client_manager()` 함수는 무조건 `[]`를 리턴하도록 **mocking** 하였습니다.

관리자 데이터를 가져오는 경우도 마찬가지로 DB에서 가져오지 않고 **mocking**하여 간편하게 테스트가 가능하도록 수정하였습니다.

이제 이제 저 테스트가 통과 할 수 있도록 코드를 작성하면 됩니다.

### 8. 새로운 기능 코드 작성

```jsx
// code file

const getClientInfoModifyMailReceiver = async(client_id) => {
  if (common_util.isNil(client_id)) // client_id가 0이 들어올수도 있어서 isNil로 체크한다.
    return [];

  const managers = await income_lib.fetch_client_manager(client_id)
  let receiver = [];
  if (managers.length) {
    receiver = [..._.map(managers, (item) => item.email)];
  } else {
    const admins = await client_lib.fetch_email_list([client_id]);
    receiver = [..._.chain(admins)
    .sortBy((admin) => admin.reg_date)
    .take(1)
    .map((admin) => admin.email)
    .value()];
  }

  return receiver; 
};
```

코드를 작성해 보았습니다. **managers**가 있는 경우에는 **receiver**에 **manager**의 이메일을 넣어서 돌려보내고, **managers**가 없는 경우에는 관리자를 조회한 뒤 가장 가장 오래된 관리자르 찾아서 이를 넣어 줍니다.

이제 테스트를 구동해서 통과하면 끝입니다.

### 9. 최종 결과

```jsx
// code file

const getClientInfoModifyMailReceiver = async(client_id) => {
  if (common_util.isNil(client_id)) // client_id가 0이 들어올수도 있어서 isNil로 체크한다.
    return [];

  const managers = await income_lib.fetch_client_manager(client_id)
  let receiver = [];
  if (managers.length) {
    receiver = [..._.map(managers, (item) => item.email)];
  } else {
    const admins = await client_lib.fetch_email_list([client_id]);
    receiver = [..._.chain(admins)
    .sortBy((admin) => admin.reg_date)
    .take(1)
    .map((admin) => admin.email)
    .value()];
  }

  return receiver; 
};
```

```jsx
// test file

describe("Test getClientInfoModifyMailReceiver(), Client 변경 메일을 받을 email을 리턴한다.", () => {
  describe('client_id에 null, undefined가 들어올 경우', () => {
    const topic = rewire('../../services/incomeServices');
    const getClientInfoModifyMailReceiver = topic.__get__('getClientInfoModifyMailReceiver');
    it('Case1. client_id에 undefined가 들어올 경우', async () => {
      const receiver = await getClientInfoModifyMailReceiver({ client_id: undefined });
      receiver.should.eql([]);
    });

    it('Case2. client_id에 null이 들어올 경우', async () => {
      const receiver = await getClientInfoModifyMailReceiver({ client_id: null });
      receiver.should.eql([]);
    });
  });

  describe('manager가 있는 경우, manager의 email을 리턴한다.', () => {
    const topic = rewire('../../services/incomeServices');
    const getClientInfoModifyMailReceiver = topic.__get__('getClientInfoModifyMailReceiver');
    before(() => {
      // manager를 가져오는 함수를 DB에서 직접 가져오지 않고 mocking 합니다.
      // fetch_client_manager 함수는 이제 아래 데이터를 리턴합니다.
      topic.__set__({
        income_lib: {
          // 강제로 null을 리턴하도록 수정.
          fetch_client_manager: () => Promise.resolve([
            { email: 'test@dable.io' },
            { email: 'test2@dable.io'}
          ])
        }
      });
    });

    it('manager가 있는 경우 manager의 email 리스트를 리턴한다.', async () => {
      const receiver = await getClientInfoModifyMailReceiver(1);

      receiver.should.eql(['test@dable.io', 'test2@dable.io']);
    });
  });

  describe('manager가 없는 경우, 등록된지 가장 오래된 admin을 리턴한다.', () => {
    const topic = rewire('../../services/incomeServices');
    const getClientInfoModifyMailReceiver = topic.__get__('getClientInfoModifyMailReceiver');
    before(() => {
      topic.__set__({
        income_lib: {
          // manager가 없는 경우를 만들기 위해서 fetch_client_manager함수는
          // 무조건 []를 리턴하도록 mocking합니다.
          fetch_client_manager: () => Promise.resolve([])
        },
        client_lib: {
          // admin을 조회하는 경우도 DB에서 직접 가져오지는 않고 mocking한 데이터를
          // 사용합니다. 
          fetch_email_list: () => Promise.resolve([
            { client_id: 1, email: 'test@dable.io', admin_name: 'test', reg_date: new Date('2020-10-01')},
            { client_id: 1, email: 'test2@dable.io', admin_name: 'test2', reg_date: new Date('2020-11-01')},
            { client_id: 1, email: 'test3@dable.io', admin_name: 'test3', reg_date: new Date('2020-01-01')},
          ])
        }
      });
    });

    it('manager가 없는 경우, 등록된지 가장 오래된 admin을 리턴한다.', async () => {
      const receiver = await getClientInfoModifyMailReceiver(1);

      receiver.should.eql(['test3@dable.io']);
    });
  });
});
```

이러면 처음에 요청한 요구사항을 만족하는 기능을 **TDD**를 통해서 만들어 보았습니다.

사실 중간 과정이 많이 생략된 부분도 있고, 제가 한 방식이 TDD에서 추천이나 요구하는 방식이 아닐 수 있습니다. 다만 저는 이런 식으로 TDD를 진행하였다는 것을 공유하고 싶었습니다.

## Wallaby.js

wallaby.js 페이지에 가면 wallaby.js는 다음과 같은 툴이라고 설명이 되어 있습니다.

> Wallaby.js is a developer productivity tool that runs your JavaScript and TypeScript tests immediately as you type, highlighting results in your IDE right next to your code.

**Wallaby.js는 입력하는 즉시 JavaScript 및 TypeScript 테스트를 실행하여 IDE에서 코드 바로 옆에 결과를 강조 표시하는 개발자 생산성 도구**라고 합니다.

일단 기능을 살펴 보면...

### 지원하는 IDE

- **VS Code**
- **JetBrains IDE**
- Visual Studio
- Sublime Text
- Atom

### 지원하는 Application Type

- **React**
- **Angular**
- Vue
- **Node.js(Backend, serverless, JAMStack, etc..)**
- Preact
- Svelte
- Other Frontend(framework or vanilla)

### 지원하는 Testing Tool

- **Jest**
- **Karma with jasmine or Mocha**
- **Mocha**
- Jasmine
- Ava

### Wallaby.js가 지원하는 기능

- 테스트 코드의 실시간 피드백
- 실시간 코드 커버리지 업데이트
- time travel debugger
- value explorer
- 특정 테스트만 구동
- 실패한 테스트/오류 코드에 대한 빠른 탐색
- 컴팩트한 테스트 결과 diff view

### 그래서 뭐가 좋은건데요..?

- 간편한 테스트 실행
  - 위에도 적었지만, TDD를 위해서는 테스트 수행이 간편해야 합니다.
  - **wallaby.js**는 이렇게 테스트를 수행하는 데 걸리는 시간을 단축해 주며, 일부 파일, 테스트만 구동 시킬 수 있습니다.
  - **repository root**에 **wallaby.js** 파일 하나만 추가해주면 **vs code**, **IntelliJ** 등에서 간편하게 사용할 수 있습니다.
  - 심지어 **coffee** 파일도 지원합니다.
- 테스트를 **작성/수정/관리**하는데 걸리는 시간을 단축해 줍니다.
  - TDD는 테스트 코드를 작성하고 코드를 작성한 뒤 테스트를 구동시켜줘야 합니다. **wallaby.js를 사용하면 테스트 코드나 코드를 작성하는 즉시 결과를 알 수 있게 해줍니다.** 별도로 스크립트를 수행할 필요도 없어집니다.
    - 파일의 테스트 커버리지도 표시해주며, 어떤 코드가 테스트에서 제외되었는지 알려주는 기능도 있습니다.
- 테스트 대시보드를 제공해서 어떤 테스트가 있으며 해당 테스트를 개별적으로 수행할 수 있습니다.
- 설정 한 번이면 간편하게 이용할 수 있습니다.
- 또한 제가 자주 사용하는 기능은 **Test Story** 기능입니다. 이 기능은 테스트하는 코드가 여러 파일에 걸쳐 있는 경우 이 파일들 사이를 이동할 필요 없이 테스트가 어떤 프로세스로 진행되었는지 확인 할 수 있습니다.

[wallabyjs](https://wallabyjs.com/)에 접속해보시면 동영상으로 사용 예제를 보실 수 있습니다.

예제 동영상을 보시고 일단 커뮤니티 버전으로 일주일이라도 써보시는 것을 추천드립니다.

## 마지막으로

여기까지가 해당 포스트 내용의 끝입니다.

제가 TDD 신봉자는 아니지만, TDD로 개발을 진행하면서 제가 작성한 코드의 자신감을 가지게 되었고, 버그를 줄이는 데 많은 도움을 받았습니다.

저처럼 버그 및 실수에 고통받으시는 개발자분들은 TDD를 이용하여 개발을 진행하시는 것을 추천해 드립니다.

감사합니다.
