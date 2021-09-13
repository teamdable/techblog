---
layout: post
title: 'Node.js express와 error handling'
date: 2021-09-15 08:00:00 +0900
author: Goonoo Kim
tags: [node.js, express]
---

안녕하세요, 데이블의 김군우 입니다.

Node.js 개발자라면 [express framework](https://www.npmjs.com/package/express)을 모르시는 분들은 없으리라 생각합니다. 다만, 마지막 release인 [v4.17.1](https://www.npmjs.com/package/express/v/4.17.1)의 출시가 벌써 2년 이상 훌쩍 지났다거나 다음 버전인 [v5의 첫 알파 버전](https://www.npmjs.com/package/express/v/5.0.0-alpha.1)의 등장은 벌써 7년이 넘게 지났으나 아직 정식 출시가 되지 않았다는 사실은 모르시는 분들도 꽤 계실 것 같아요.

물론 이 글은 express에 대한 푸념이나 비판을 하기 위한 글은 아니고, 반대로 express framework를 쓰시는 분들에게 error handling에 대한 팁을 드리는 목적으로 작성한 글입니다. 다만, 아직 서버 개발을 위한 프레임워크를 결정할 여력이 있으신 분들은 [Fastify](https://www.fastify.io/) 같은 대안을 추천드립니다. :)

## 들어가며

이 단락을 읽기 시작하시는 분들은 아마도 express framework를 이미 사용중이시거나 익숙하신 분들이 아닐까 싶습니다. 이 글은 이런 분들께 초점을 맞추고 있습니다.

callback, Promise, async/await 등 다양한 코드 형태별 최적의 에러 핸들링 방안을 소개해 드립니다.

## 에러 발생시키기 - 기본

아래는 express 공식 가이드인 [에러 핸들링](https://expressjs.com/en/guide/error-handling.html)에 있는 코드인데요.

```
app.get('/', (req, res) => {
  throw new Error('BROKEN'); // express가 알아서 오류를 처리합니다.
});
```

코드가 동기인 경우 단순히 이렇게 오류를 발생시키면 express는 알아서 사용자에게 HTTP 500 응답과 실행 환경에 맞는 HTML 코드를 응답합니다.

![코드 실행 결과 브라우저 스크린샷: 500 응답과 기본 HTML 코드](/techblog/assets/images/2021-09-15-express-error-handling/1.png)

## 에러 응답 포맷 다듬기 - 기본

우리가 개발하는 서버는 JSON 응답을 하는 API 서버라고 가정해봅시다. 그래서 express가 기본적으로 응답하는 HTML 코드를 사용하는 대신 JSON 포맷으로 된 오류 메시지를 제공하려고 합니다.

```
app.get('/api', (req, res) => {
  try {
    // try 구문 내의 코드에서 무언가 오류가 발생한다고 가정합시다!
    // 아래 줄은 오류가 발생하는 경우를 단순화 한 예제 정도로 봐주세요.
    throw new Error('BROKEN');
  } catch (err) {
    res.status(500);
    res.json({message: err.message});
  }
});
```

일단 이렇게 작성해볼 수 있습니다. 음... 어떤가요? 오류가 발생했을 때 원하는 응답을 해 줄 수는 있는데 코드가 좀 복잡해졌습니다. 컨트롤러를 추가하고 같은 에러 응답 포맷을 제공하려면 에러 처리 부분을 공통으로 처리하도록 코드를 분리하는 게 좋을 것 같습니다.

```
app.get('/api', (req, res) => {
  throw new Error('BROKEN1');
});

app.get('/api2', (req, res) => {
  throw new Error('BROKEN2');
});

app.use((err, req, res, next) => {
  res.status(500);
  res.json({message: err.message});
});
```

맨 아래 `app.use`는 각 컨트롤러에서 발생한 에러를 일괄 처리하기 위한 [에러 핸들러 작성](https://expressjs.com/en/guide/error-handling.html#writing-error-handlers)을 위한 선언입니다. 이제 각 컨트롤러는 요청을 처리 하기 위한 로직만 남겨둘 수 있고 공통적인 에러 핸들링을 위한 선언을 분리해서 코드가 잘 정리된 것 같습니다! 👏

## 에러 발생시키기 - callback

Node.js로 코드를 작성하다 보면 비동기 처리는 흔합니다. callback, Promise, async/await 등 여러가지 방법이 있죠. 비동기 함수의 에러 발생은 앞서 설명한 기본적인 동기 함수의 에러 발생과는 다소 차이가 있습니다.

일단, 요새는 점점 역사의 뒤안길로 사라지고 있긴 하지만 일단 callback 패턴을 살펴보죠.

```
app.get('/api', (req, res) => {
  setTimeout(() => {
    throw new Error('BROKEN1');
  }, 10);
});
```

비동기 상황을 연출하기 위해 `setTimeout`을 사용했습니다. `setTimeout` 함수 내에서 오류가 발생한 상황입니다. 이 컨트롤러는 어떻게 동작할까요?

![코드 실행 결과 브라우저 스크린샷: 서버를 찾을 수 없음](/techblog/assets/images/2021-09-15-express-error-handling/2.png)

서버를 찾을 수 없다는 오류가 표시됩니다. 아래는 전체 서버 코드와 서버 실행 CLI 응답 전체입니다.

```
// server.js
const express = require('express');
const app = express();

app.get('/', (req, res, next) => {
  setTimeout(() => {
    throw new Error('BROKEN');
  }, 10);
});

app.listen(3000, () => {
  console.info('test server is running!');
});

---

$ node server.js
test server is running!

/Users/tenshi/test/server.js:8
    throw new Error('BROKEN');
    ^

Error: BROKEN
    at Timeout._onTimeout (/Users/tenshi/test/server.js:8:11)
    at listOnTimeout (internal/timers.js:531:17)
    at processTimers (internal/timers.js:475:7)
```

네. 아마 짐작하신 분도 계시겠지만, 비동기로 발생한 오류는 express가 처리해주지 못합니다. express는 이 경우를 위해 next 함수를 사용할 수 있습니다. next 함수의 첫번째 인자에 Error 객체나 String 등을 선언하는 경우 express는 이를 동기에서의 오류 발생과 같은 형태로 취급합니다.

```
app.get('/', (req, res, next) => {
  setTimeout(() => {
    next(new Error('BROKEN'));
  }, 10);
});
```

지정한 파일을 여는 콜백 패턴의 함수인 `fs.open`을 이용한 실제와 유사한 예제를 준비해봤습니다.

```
app.get('/', (req, res, next) => {
  fs.open('/file/path', (err, fd) => {
    if (err) {
      next(new Error('cannot open file'));
      return;
    }
    // 연 파일 다루는 로직...
  });
});
```

... 코드가 복잡하고 지저분해집니다. 이래서 콜백 패턴은 역사의 뒤안길로...... (매우 주관적인 감상 죄송합니다.)

콜백 패턴은 그만 알아보죠.

## 에러 발생시키기 - async/await

이제 async/await와 Promise의 에러 발생을 살펴보겠습니다.

```
app.get('/api', async (req, res) => {
  throw new Error('BROKEN1');
});
```

컨트롤러 함수에 async 키워드를 붙여서 함수를 선언했습니다. 어떻게 동작할까요?

![코드 실행 결과 브라우저 스크린샷: 서버가 응답하지 않음](/techblog/assets/images/2021-09-15-express-error-handling/3.png)

서버가 응답하지 않습니다. 서버를 실행한 콘솔에는 다음과 같은 오류가 기록됩니다.

```
$ node server.js
test server is running!
(node:57055) UnhandledPromiseRejectionWarning: Error: BROKEN
    at /Users/tenshi/test/server.js:5:9
    at Layer.handle [as handle_request] (/Users/tenshi/test/node_modules/express/lib/router/layer.js:95:5)
    at next (/Users/tenshi/test/node_modules/express/lib/router/route.js:137:13)
    at Route.dispatch (/Users/tenshi/test/node_modules/express/lib/router/route.js:112:3)
    at Layer.handle [as handle_request] (/Users/tenshi/test/node_modules/express/lib/router/layer.js:95:5)
    at /Users/tenshi/test/node_modules/express/lib/router/index.js:281:22
    at Function.process_params (/Users/tenshi/test/node_modules/express/lib/router/index.js:335:12)
    at next (/Users/tenshi/test/node_modules/express/lib/router/index.js:275:10)
    at expressInit (/Users/tenshi/test/node_modules/express/lib/middleware/init.js:40:5)
    at Layer.handle [as handle_request] (/Users/tenshi/test/node_modules/express/lib/router/layer.js:95:5)
(node:57055) UnhandledPromiseRejectionWarning: Unhandled promise rejection. This error originated either by throwing inside of an async function without a catch block, or by rejecting a promise which was not handled with .catch(). (rejection id: 1)
(node:57055) [DEP0018] DeprecationWarning: Unhandled promise rejections are deprecated. In the future, promise rejections that are not handled will terminate the Node.js process with a non-zero exit code.
```

`UnhandledPromiseRejectionWarning` 입니다. Promise rejection이 핸들링되지 않았다는 오류입니다. async 함수에서 발생한 오류는 `.catch(err)` 혹은 async 함수 내의 try/catch 로 다루어져야 하지만 express는 이를 지원하지 않습니다. 네. express가 Promise나 async/await를 지원하기에는 너무 오래되었죠? 물론 그 과거에도 수많은 논의가 있었지만 결국 다음 버전인 v5에서 지원을 하기로 결정했고, v5는 아직 릴리즈가 되지 않았고 우리가 사용하는 v4는 여전히 지원하지 않는 상황입니다.

express 공식 가이드의 [에러 핸들링](https://expressjs.com/en/guide/error-handling.html)은 이런 방법을 제안합니다.

```
// promise version
app.get('/', function (req, res, next) {
  Promise.resolve().then(function () {
    throw new Error('BROKEN');
  }).catch(next); // Errors will be passed to Express.
});

// async/await version
app.get('/', async function (req, res, next) {
  try {
    throw new Error('BROKEN');
  } catch (err) {
    next(err);
  }
});
```

동작은 잘 되지만 의미없는 코드 조각들 때문에 콜백 패턴처럼 깔끔해보이지는 않습니다.

### express-async-errors

[express-async-errors](https://www.npmjs.com/package/express-async-errors) 패키지는 async/await의 에러를 깔끔하게 다룰 수 있게 해줍니다. express와 async/await를 함께 활용하신다면 꼭 쓰세요. 두 번 쓰세요.

```
// server.js
const express = require('express');
require('express-async-errors');
const app = express();

app.get('/', async (req, res, next) => {
  throw new Error('BROKEN');
});

app.listen(3000, () => {
  console.info('test server is running!');
});
```

이렇게 express include 다음 라인에 express-async-errors 패키지를 include 해주면, async block에서도 오류를 따로 처리해서 next 함수를 호출해줄 필요가 없어집니다.

[express-async-errors](https://www.npmjs.com/package/express-async-errors) 패키지는 express의 내부 동작에 컨트롤러 함수가 Promise reject를 한 경우 동기 함수의 에러와 동일하게 처리하도록 하는 로직이 전부인 간단한 패키지입니다. 이 패키지와 함께 async/await의 에러 핸들링도 깔끔해집니다!

## 에러 응답 포맷 다듬기 - 심화

지금까지 동기 함수와 callback, async/await 등 비동기 함수에서 express가 다룰 수 있게 에러를 발생시키는 방법을 알아보았습니다. 앞서, `app.use`를 이용하여 공통으로 에러 응답 포맷을 다듬는 방법도 살펴보았는데요. 실전에서 사용할 수 있을 정도로 조금 더 알아보겠습니다.

게시판의 ID를 파라미터로 받아 게시물의 수를 응답하는 API를 만든다고 가정해봅시다.

```
const {getArticleCount} = require('./board_model');

app.get('/board_article_count', async (req, res) => {
  const board_id = req.query.board_id;
  const count = await getArticleCount(board_id);
  res.json({result: {count}});
});

app.use((err, req, res, next) => {
  res.status(500);
  res.json({message: err.message});
});
```

이 코드는 express-async-errors 패키지를 쓴다는 가정 하에 해석해보면,
 * `getArticleCount` 함수에서 오류가 발생할 경우 express의 공통 에러 핸들링에 의해 HTTP 500 + message를 포함한 JSON 응답
 * 그 밖의 경우 `getArticleCount` 함수에서 얻은 숫자로 HTTP 200 JSON 응답

이렇게 동작합니다.

여 컨트롤러에 `board_id` 파라미터에 대한 유효성 검사를 추가하고자 한다고 합시다.

```
app.get('/board_article_count', async (req, res) => {
  const board_id = req.query.board_id;
  if (!board_id) {
    res.status(400);
    res.json({message: 'board_id is required');
    return;
  }
  const count = await getArticleCount(board_id);
  res.json({result: {count}});
});
```

이렇게 구현할 수 있겠죠.

하지만 비슷한 컨트롤러가 여러개 생긴다면, HTTP 500 오류 응답 처리와 동일하게 비슷한 유효성 검사 로직의 공통화 등을 고민하게 될 것입니다.

```
class BadRequestError extends Error {}

app.get('/board_article_count', async (req, res) => {
  const board_id = req.query.board_id;
  if (!board_id)
    throw new BadRequestError('board_id is required');
  }
  const count = await getArticleCount(board_id);
  res.json({result: {count}});
});

app.use((err, req, res, next) => {
  if (err instanceof BadRequestError) {
    res.status(400);
    res.json({message: err.message});
  } else {
    res.status(500);
    res.json({message: err.message});
  }
});
```

이렇게 유효성 검사를 위한 400 응답을 위한 `BadRequestError` 클래스를 정의하고 유효성 검사 오류 시 단순히 이 클래스의 인스턴스를 에러로 발생시키도록 바꿔보았습니다.

이를 응용하면 다양한 종류의 오류를 공통적으로 다루면서 컨트롤러의 로직은 최대한 단순하게 유지할 수 있으리라 생각합니다. 어떠신가요?

## 마치며

이 글이 express를 사용할 수 밖에 없는 개발 현장에서 분투하시는 개발자분들의 코드 라인을 줄이고 코드의 가독성을 올리는 데 도움이 되길 바랍니다!

